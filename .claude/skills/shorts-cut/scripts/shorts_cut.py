#!/usr/bin/env python3
"""shorts-cut: shorts plan JSON (+ long-form manifest) -> 9:16 shorts, each <= max_seconds, + .srt.

Each short = ordered segments. A segment either quotes narration from a scene of the long-form
(paragraphs / sentences / exclude_sentences) or carries its own "text" (hook or CTA line).
Visuals come from that scene: vertical plate > 16:9 plate (cover crop) > Pillow mockup panel.
Layers: top hook text, burned subtitles, optional bottom disclosure bar, optional end card,
optional AI label for the last N seconds. Refuses to write a short longer than max_seconds.

Usage:
  python3 shorts_cut.py PLAN.json [--manifest render/EPxxx/long.manifest.json] [--only short-1 ...]
                        [--mode auto|mockup|real] [--contact-sheet PNG] [--dry-run] [--keep-work]
Requires the sibling skill ffmpeg-assemble (scripts/kemedia.py).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

_KM = Path(__file__).resolve().parents[2] / "ffmpeg-assemble" / "scripts"
sys.path.insert(0, str(_KM))
try:
    import kemedia as km  # noqa: E402
except ImportError:
    raise SystemExit("shorts-cut: needs .claude/skills/ffmpeg-assemble/scripts/kemedia.py (looked in %s)" % _KM)

TOOL = "shorts-cut"
VERSION = "1.0.0"

DEFAULTS = {
    "size": [1080, 1920], "fps": 30, "wpm": 150, "max_seconds": 60, "mode": "auto",
    "cue_max_chars": 46, "mockup_label": "MOCKUP — final AI plate pending",
    "ai_label": None, "burn_subtitles": True, "segment_gap": 0.0, "hook_max_px": 120,
    "preset": "medium", "crf": 20, "theme": {}, "fonts": {},
    "music": None, "music_volume": 0.10, "loudnorm": False,
}


def exists(p):
    return bool(p) and Path(p).is_file()


def load_scenes(plan, manifest_arg):
    src = manifest_arg or plan.get("manifest") or plan.get("scenes")
    if not src:
        return {}, None
    data = json.loads(Path(src).read_text(encoding="utf-8"))
    return {s["id"]: s for s in data.get("scenes", [])}, src


def norm_index(i, n):
    return i if i > 0 else n + i + 1


def select_units(seg, scene):
    units = km.narration_units(scene.get("narration", ""))
    if seg.get("paragraphs"):
        keep = set(seg["paragraphs"])
        units = [u for u in units if u["para"] in keep]
    if seg.get("sentences"):
        idx = [norm_index(i, len(units)) for i in seg["sentences"]]
        units = [units[i - 1] for i in idx if 1 <= i <= len(units)]
    if seg.get("exclude_sentences"):
        ex = {norm_index(i, len(units)) for i in seg["exclude_sentences"]}
        units = [u for n, u in enumerate(units, 1) if n not in ex]
    return units


def expand(short, scenes, cfg, mode, warnings):
    """Segments -> contiguous sub-segments with text, words, audio source, visual."""
    subs = []
    for si, seg in enumerate(short["segments"]):
        sc = scenes.get(seg.get("scene")) if seg.get("scene") else None
        if seg.get("scene") and sc is None:
            raise SystemExit("%s: %s segment %d references unknown scene %s (give --manifest)"
                             % (TOOL, short["id"], si + 1, seg["scene"]))
        visual = {
            "scene": seg.get("scene") or "",
            "title": (sc or {}).get("title", ""),
            "screen": seg.get("screen", (sc or {}).get("screen")),
            "plate": seg.get("plate", (sc or {}).get("plate")),
            "image": seg.get("image") or (sc or {}).get("image_vertical") or (sc or {}).get("image"),
        }
        role = seg.get("role", "text" if "text" in seg else "excerpt")
        if "text" in seg:
            runs = [[{"para": None, "sent": None, "idx": None, "text": t} for t in km.split_sentences(seg["text"])]]
        else:
            units = select_units(seg, sc)
            if not units:
                raise SystemExit("%s: %s segment %d selects no sentences" % (TOOL, short["id"], si + 1))
            runs, cur = [], []
            for u in units:
                if cur and u["idx"] != cur[-1]["idx"] + 1 and not seg.get("audio"):
                    runs.append(cur)
                    cur = []
                cur.append(u)
            runs.append(cur)
        for run in runs:
            text = " ".join(u["text"] for u in run)
            audio = None
            if mode != "mockup":
                if seg.get("audio"):
                    if exists(seg["audio"]):
                        audio = {"path": seg["audio"], "start": seg.get("audio_in"), "end": seg.get("audio_out"),
                                 "how": "segment audio"}
                    else:
                        warnings.append("%s: segment audio not found: %s" % (short["id"], seg["audio"]))
                elif sc and sc.get("audio_used") and exists(sc.get("audio")) and run[0]["idx"] is not None:
                    keys = {(u["para"], u["sent"]) for u in run}
                    hits = [c for c in sc.get("cues", []) if (c.get("para"), c.get("sent")) in keys]
                    if hits:
                        audio = {"path": sc["audio"], "start": min(c["start"] for c in hits),
                                 "end": max(c["end"] for c in hits), "how": "cut from scene audio"}
                        if sc.get("cue_timing") != "explicit":
                            warnings.append("%s: %s audio cut points are proportional estimates; give per-line "
                                            "audio or timestamped subtitles for exact cuts" % (short["id"], sc["id"]))
            img_ok = exists(visual["image"]) and mode != "mockup"
            if visual["image"] and not img_ok and mode != "mockup":
                warnings.append("%s: image not found: %s (mockup panel used)" % (short["id"], visual["image"]))
            if mode == "real" and not (audio and img_ok):
                raise SystemExit("%s: --mode real but %s segment %d lacks %s" % (
                    TOOL, short["id"], si + 1, " and ".join(x for x, ok in (("audio", audio), ("image", img_ok)) if not ok)))
            words = km.word_count(text)
            if seg.get("duration") and len(runs) == 1:
                dur, how = float(seg["duration"]), "explicit"
            elif audio:
                a_len = (audio["end"] if audio["end"] is not None else km.probe_duration(audio["path"])) - (audio["start"] or 0)
                dur, how = a_len, "audio"
            else:
                dur, how = words / float(cfg["wpm"]) * 60.0, "words/%gwpm" % cfg["wpm"]
            subs.append({"seg": si + 1, "role": role, "scene": visual["scene"], "text": text, "units": run,
                         "words": words, "seconds": dur, "duration_source": how, "audio": audio,
                         "visual": dict(visual, use_img=img_ok)})
    return subs


def make_base(cfg, fonts, theme, sub, k, hook_bottom, has_bar):
    W, H = cfg["size"]
    v = sub["visual"]
    img = km.Image.new("RGBA", (W, H), km.hex_rgba(theme["night"]))
    sizes = {kk: (tuple(x * k for x in val) if isinstance(val, (list, tuple)) else val * k)
             for kk, val in km.SIZES_SHORT.items()}
    top = max(hook_bottom + 40 * k, 600 * k)
    box_bottom = 1090 * k
    if v["use_img"]:
        plate, scale = km.cover_fit(v["image"], (W, H))
        img.alpha_composite(plate)
        sub["upscale"] = round(scale, 3)
        scr = v.get("screen") or {}
        if any(scr.get(x) for x in ("heading", "lines", "cards", "bars", "note")):
            km.overlay_rect(img, (48 * k, top - 16 * k, 952 * k, box_bottom), km.hex_rgba(theme["night"], 200), int(16 * k))
            km.paint_screen(img, fonts, theme, (72 * k, top, 928 * k, box_bottom - 16 * k), scr, sizes)
        return img
    badge = km.paint_tag(img, fonts, v["scene"] or "TEXT", "body", int(30 * k), 60 * k, top, theme["ink"],
                         km.hex_rgba(theme["yellow"]), pad=(int(14 * k), int(8 * k)))
    if cfg.get("mockup_label"):
        km.paint_tag(img, fonts, cfg["mockup_label"], "body", int(22 * k), 940 * k, top + 4 * k,
                     theme["white"], km.hex_rgba(theme["red"]), anchor="right")
    y = badge[3] + 18 * k
    if v.get("plate"):
        size = int(22 * k)
        lines = km.wrap_greedy(fonts, "Planned plate: " + v["plate"], "body_regular", size, 880 * k)[:3]
        y = km.draw_block(img, fonts, lines, "body_regular", size, 60 * k, 940 * k, y, theme["muted"], align="left")
        y += 26 * k
    km.paint_screen(img, fonts, theme, (60 * k, y, 940 * k, box_bottom), v.get("screen") or {}, sizes)
    return img


def render_short(short, cfg, scenes, mode, fonts, theme, args, warnings):
    fps = int(cfg["fps"])
    W, H = cfg["size"]
    k = W / 1080.0
    subs = expand(short, scenes, cfg, mode, warnings)
    gap = float(cfg["segment_gap"])
    cum = 0.0
    for i, s in enumerate(subs):
        s["start_f"] = round(cum * fps)
        cum += s["seconds"] + (gap if i < len(subs) - 1 else 0.0)
        s["end_f"] = round(cum * fps)
        s["speech_f"] = min(s["end_f"] - s["start_f"], max(1, round(s["seconds"] * fps)))
    total = subs[-1]["end_f"]
    limit = int(round(float(cfg["max_seconds"]) * fps))
    info = {"id": short["id"], "output": short["output"], "frames": total, "seconds": total / fps,
            "words": sum(s["words"] for s in subs), "hook": short.get("hook"),
            "disclosure_bar": short.get("disclosure_bar"), "end_card": short.get("end_card"),
            "ai_label": cfg.get("ai_label"), "notes": short.get("notes"),
            "segments": [{"seg": s["seg"], "role": s["role"], "scene": s["scene"], "words": s["words"],
                          "seconds": round((s["end_f"] - s["start_f"]) / fps, 3),
                          "duration_source": s["duration_source"],
                          "visual": "image" if s["visual"]["use_img"] else "mockup",
                          "audio": (s["audio"] or {}).get("how", "silent"),
                          "sentences": [[u["para"], u["sent"]] for u in s["units"] if u["idx"] is not None]}
                         for s in subs]}
    print("  %-8s %6.2fs  words=%-4d segments=%d  %s" % (short["id"], total / fps, info["words"], len(subs),
                                                        "OK" if total <= limit else "OVER LIMIT"))
    for s in info["segments"]:
        print("           seg%-2d %-8s %-4s %6.2fs words=%-4d %s/%s" % (
            s["seg"], s["role"], s["scene"], s["seconds"], s["words"], s["visual"], s["audio"]))
    if total > limit:
        info["error"] = "duration %.2fs exceeds max_seconds %s" % (total / fps, cfg["max_seconds"])
        return info
    if args.dry_run:
        return info

    # subtitle cues (always written to .srt; burned in only when burn_subtitles is true)
    cues = []
    for s in subs:
        local = km.make_cues(s["units"], int(cfg["cue_max_chars"]))
        km.distribute(local, s["start_f"], s["speech_f"])
        for c in local:
            c["size"], c["lines"] = km.fit_lines(fonts, c["text"], "body", int(64 * k), int(52 * k), 880 * k, 2)
        cues.extend(local)

    out = Path(short["output"])
    out.parent.mkdir(parents=True, exist_ok=True)
    work = out.parent / (".work-" + out.stem)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    t0 = time.time()
    try:
        tl = km.Timeline((W, H), total, theme["night"])
        hook = short.get("hook")
        hook_bottom = 220 * k
        if hook:
            hmax = int(cfg["hook_max_px"] * k)
            hsize, hlines = km.fit_lines(fonts, hook, "headline", hmax, int(hmax * 0.8), 880 * k, 2)
            if len(hlines) > 2 or any(fonts.length(l, "headline", hsize) > 880 * k for l in hlines):
                hsize, hlines = km.fit_lines(fonts, hook, "headline", hmax, int(84 * k), 880 * k, 3)
            hook_bottom = 268 * k + km.block_height(fonts, len(hlines), "headline", hsize, lh=1.08)

            def paint_hook(img, hsize=hsize, hlines=hlines):
                km.draw_block(img, fonts, hlines, "headline", hsize, 60 * k, 940 * k, 268 * k, theme["yellow"],
                              stroke=int(6 * k), stroke_fill=theme["ink"], lh=1.08)
            tl.add(0, total, 5, ("hook",), paint_hook)
        bar = short.get("disclosure_bar")
        sub_bottom = (1336 if bar else 1400) * k
        if bar:
            bsize, blines = km.fit_lines(fonts, bar, "body", int(44 * k), int(40 * k), 840 * k, 2)
            if len(blines) > 2:
                raise SystemExit("%s: %s disclosure bar does not fit in 2 lines at 40px" % (TOOL, short["id"]))

            def paint_bar(img, bsize=bsize, blines=blines):
                h = km.block_height(fonts, len(blines), "body", bsize) + 32 * k
                km.overlay_rect(img, (60 * k, 1440 * k - h, 940 * k, 1440 * k), km.hex_rgba(theme["yellow"]), int(10 * k))
                km.draw_block(img, fonts, blines, "body", bsize, 60 * k, 940 * k, 1440 * k - h + 16 * k, theme["ink"])
            tl.add(0, total, 8, ("bar",), paint_bar)
        bases = {}
        for i, s in enumerate(subs):
            vkey = json.dumps([s["visual"]["scene"], s["visual"].get("screen"), s["visual"].get("image"),
                               s["visual"]["use_img"]], sort_keys=True, ensure_ascii=False)
            if vkey not in bases:
                bases[vkey] = make_base(cfg, fonts, theme, s, k, hook_bottom, bool(bar))
            tl.add(s["start_f"], s["end_f"], 0, ("base", vkey), lambda img, b=bases[vkey]: img.alpha_composite(b))
        if cfg["burn_subtitles"]:
            for i, c in enumerate(cues):
                def paint_sub(img, c=c):
                    h = km.block_height(fonts, len(c["lines"]), "body", c["size"])
                    km.draw_block(img, fonts, c["lines"], "body", c["size"], 60 * k, 940 * k, sub_bottom - h,
                                  theme["white"], stroke=int(5 * k), stroke_fill=theme["ink"])
                tl.add(c["start"], c["end"], 10, ("sub", i), paint_sub)
        ec = short.get("end_card")
        if ec and ec.get("text"):
            n = round(float(ec.get("seconds", 4)) * fps)
            esize, elines = km.fit_lines(fonts, ec["text"], "body", int(42 * k), int(32 * k), 780 * k, 3)

            mid_top = max(hook_bottom + 40 * k, 600 * k)

            def paint_end(img, esize=esize, elines=elines, mid_top=mid_top):
                h = km.block_height(fonts, len(elines), "body", esize)
                km.overlay_rect(img, (60 * k, mid_top, 940 * k, 1090 * k), km.hex_rgba(theme["paper"]), int(16 * k))
                km.draw_block(img, fonts, elines, "body", esize, 80 * k, 920 * k,
                              mid_top + (1090 * k - mid_top - h) / 2, theme["ink"])
            tl.add(total - n, total, 9, ("end",), paint_end)
        ai = cfg.get("ai_label")
        if ai and ai.get("text"):
            n = round(float(ai.get("seconds", 1.0)) * fps)
            tl.add(total - n, total, 11, ("ai",), lambda img: km.paint_tag(
                img, fonts, ai["text"], "body", int(32 * k), 500 * k, 1098 * k, theme["white"],
                km.hex_rgba(theme["ink"], 225), anchor="center"))
        seq, n_png = tl.render(work)
        concat = work / "video.ffconcat"
        km.write_ffconcat(seq, fps, concat)
        parts = []
        for i, s in enumerate(subs):
            a = s["audio"] or {}
            parts.append({"path": a.get("path"), "start": a.get("start"), "end": a.get("end"),
                          "frames": s["end_f"] - s["start_f"]})
        music = cfg.get("music") if exists(cfg.get("music")) else None
        audio = km.build_audio(parts, fps, work, music=music, music_volume=float(cfg["music_volume"]),
                               loudnorm=bool(cfg["loudnorm"]))
        t1 = time.time()
        km.encode(concat, audio, out, fps, total, preset=args.preset or cfg["preset"],
                  crf=args.crf if args.crf is not None else cfg["crf"])
        t2 = time.time()
    finally:
        if not args.keep_work:
            shutil.rmtree(work, ignore_errors=True)
    for s in subs:
        if (s.get("upscale") or 0) > 1.5:
            warnings.append("%s: %s plate upscaled %.2fx to fill 9:16 (generate a native 9:16 plate, "
                            "design-system section 4)" % (short["id"], s["scene"], s["upscale"]))
    srt = out.with_suffix(".srt")
    km.write_srt(srt, cues, fps)
    probe = km.probe_media(out)
    checks = {"resolution": (probe.get("width"), probe.get("height")) == (W, H),
              "fps": abs(probe.get("fps", 0) - fps) < 0.01, "h264": probe.get("vcodec") == "h264",
              "max_seconds": probe["duration"] <= float(cfg["max_seconds"]),
              "duration_match": abs(probe["duration"] - total / fps) < 0.1}
    for name, ok in checks.items():
        if not ok:
            warnings.append("%s check failed: %s (%s)" % (short["id"], name, probe))
    info.update({"srt": str(srt), "probe": probe, "checks": checks, "frames_rendered": n_png,
                 "timing_sec": {"frames": round(t1 - t0, 2), "encode": round(t2 - t1, 2)},
                 "upscale": [s.get("upscale") for s in subs if s.get("upscale")]})
    return info


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan_json")
    ap.add_argument("--manifest", help="long-form manifest from ffmpeg-assemble (overrides plan 'manifest')")
    ap.add_argument("--only", nargs="*", help="short ids to render")
    ap.add_argument("--mode", choices=["auto", "mockup", "real"])
    ap.add_argument("--contact-sheet", help="review PNG with one frame per short")
    ap.add_argument("--contact-max-kb", type=int, default=600)
    ap.add_argument("--manifest-out", help="where to write the shorts manifest JSON")
    ap.add_argument("--preset")
    ap.add_argument("--crf", type=int)
    ap.add_argument("--keep-work", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="timing check only (exit 4 if any short is too long)")
    args = ap.parse_args(argv)

    t0 = time.time()
    km.require_tools()
    plan = json.loads(Path(args.plan_json).read_text(encoding="utf-8"))
    cfg_base = dict(DEFAULTS)
    cfg_base.update({k: v for k, v in plan.items() if k in DEFAULTS})
    mode = args.mode or cfg_base["mode"]
    scenes, scene_src = load_scenes(plan, args.manifest)
    theme = dict(km.DEFAULT_THEME, **(cfg_base.get("theme") or {}))
    fonts = km.FontSet(cfg_base.get("fonts"))
    warnings = ["font role '%s': designated font not installed, fallback %s used"
                % (r, Path(fonts.choice[r][0]).name) for r in fonts.designated_missing()]
    shorts = [s for s in plan["shorts"] if not args.only or s["id"] in args.only]
    print("%s %s | mode=%s | %dx%d@%d | max %ss | scenes from %s" % (
        TOOL, VERSION, mode, cfg_base["size"][0], cfg_base["size"][1], cfg_base["fps"],
        cfg_base["max_seconds"], scene_src))
    results = []
    for short in shorts:
        cfg = dict(cfg_base)
        cfg.update({k: v for k, v in short.items() if k in DEFAULTS})
        results.append(render_short(short, cfg, scenes, mode, fonts, theme, args, warnings))
    failed = [r["id"] for r in results if r.get("error")]
    sheet = None
    if args.contact_sheet and not args.dry_run:
        items = []
        for r, short in zip(results, shorts):
            if r.get("error"):
                continue
            t = float(short.get("preview_at", r["seconds"] * 0.4))
            items.append((r["output"], min(t, r["seconds"] - 0.05), "%s  %.1fs" % (r["id"], r["probe"]["duration"])))
        if items:
            sheet = km.contact_sheet(None, items, args.contact_sheet, fonts, cols=len(items), tile_w=324,
                                     title="shorts 9:16  |  %s  |  %d clips" % (mode, len(items)),
                                     max_kb=args.contact_max_kb, theme=theme)
    if not args.dry_run and results:
        mpath = Path(args.manifest_out) if args.manifest_out else Path(results[0]["output"]).parent / "shorts.manifest.json"
        mpath.write_text(json.dumps({
            "tool": TOOL, "version": VERSION, "kemedia": km.KEMEDIA_VERSION, "plan": args.plan_json,
            "scenes_source": scene_src, "mode_requested": mode, "max_seconds": cfg_base["max_seconds"],
            "fonts": fonts.report(), "tools": km.tool_versions(), "warnings": warnings,
            "contact_sheet": {"path": args.contact_sheet, **sheet} if sheet else None,
            "elapsed_sec": round(time.time() - t0, 2), "shorts": results}, ensure_ascii=False, indent=1),
            encoding="utf-8")
        print("manifest: %s" % mpath)
    summary = [{"id": r["id"], "seconds": round(r.get("probe", {}).get("duration", r["seconds"]), 3),
                "size": [r.get("probe", {}).get("width"), r.get("probe", {}).get("height")],
                "bytes": r.get("probe", {}).get("size_bytes"), "error": r.get("error")} for r in results]
    print(json.dumps({"shorts": summary, "warnings": sorted(set(warnings)), "contact_sheet": sheet,
                      "elapsed_sec": round(time.time() - t0, 2)}, ensure_ascii=False, indent=1))
    if failed:
        print("FAILED (too long): %s" % ", ".join(failed), file=sys.stderr)
        return 4
    bad = [r["id"] for r in results if r.get("checks") and not all(r["checks"].values())]
    return 3 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
