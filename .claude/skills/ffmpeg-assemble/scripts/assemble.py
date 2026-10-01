#!/usr/bin/env python3
"""ffmpeg-assemble: scene list JSON -> 16:9 long-form MP4 (H.264/AAC) + .srt + manifest.

Modes (per scene, see SKILL.md):
  mockup  Pillow text slide (scene id, screen text, MOCKUP label), silent audio, burned subtitles
  real    plate image (cover-fit) + TTS audio; screen text drawn as overlay panel
  auto    real where image/audio files exist, mockup/silence where they do not (default)

Usage:
  python3 assemble.py SCENES.json [--out render/EPxxx/long.mp4] [--mode auto|mockup|real]
                      [--contact-sheet episodes/EPxxx/render-preview/long-contact.png]
                      [--dry-run] [--keep-work] [--preset medium] [--crf 20]
Relative paths inside the JSON are resolved from the current working directory (run from repo root).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kemedia as km  # noqa: E402

TOOL = "ffmpeg-assemble"
VERSION = "1.0.0"

DEFAULTS = {
    "size": [1920, 1080], "fps": 30, "wpm": 150, "mode": "auto", "burn_subtitles": "auto",
    "mockup_label": "MOCKUP — final AI plate pending", "cue_max_chars": 84,
    "scene_pad": 0.3, "default_scene_seconds": 3.0,
    "music": None, "music_volume": 0.12, "loudnorm": False,
    "preset": "medium", "crf": 20, "theme": {}, "fonts": {},
}


def load_spec(path):
    spec = json.loads(Path(path).read_text(encoding="utf-8"))
    for k, v in DEFAULTS.items():
        spec.setdefault(k, v)
    if not spec.get("scenes"):
        raise SystemExit("%s: no scenes in %s" % (TOOL, path))
    return spec


def exists(p):
    return bool(p) and Path(p).is_file()


def resolve_scenes(spec, mode, warnings):
    fps, wpm = spec["fps"], spec["wpm"]
    out, cum, missing = [], 0.0, []
    for sc in spec["scenes"]:
        sid = sc.get("id") or "S%02d" % (len(out) + 1)
        img, aud = sc.get("image"), sc.get("audio")
        if mode == "mockup":
            use_img = use_aud = False
        else:
            use_img, use_aud = exists(img), exists(aud)
            if mode == "real" and not (use_img and use_aud):
                missing.append("%s: %s" % (sid, ", ".join(
                    x for x, ok in (("image", use_img), ("audio", use_aud)) if not ok)))
            for kind, val, ok in (("image", img, use_img), ("audio", aud, use_aud)):
                if val and not ok:
                    warnings.append("%s: %s not found (%s), using %s" % (
                        sid, kind, val, "mockup slide" if kind == "image" else "silence"))
        narration = sc.get("narration", "")
        words = km.word_count(narration)
        audio_sec = km.probe_duration(aud) if use_aud else None
        if sc.get("duration"):
            dur, src = float(sc["duration"]), "explicit"
            if audio_sec and audio_sec > dur:
                warnings.append("%s: audio %.2fs longer than explicit duration %.2fs (trimmed)"
                                % (sid, audio_sec, dur))
        elif audio_sec:
            dur, src = audio_sec + float(spec["scene_pad"]), "audio+pad"
        elif words:
            dur, src = words / float(wpm) * 60.0, "words/%gwpm" % wpm
        else:
            dur, src = float(spec["default_scene_seconds"]), "default"
        start_f = round(cum * fps)
        cum += dur
        end_f = round(cum * fps)
        out.append({"src": sc, "id": sid, "title": sc.get("title", ""), "use_img": use_img,
                    "use_aud": use_aud, "words": words, "audio_sec": audio_sec, "duration_source": src,
                    "start_f": start_f, "end_f": end_f})
    if missing:
        raise SystemExit("%s: --mode real but inputs missing -> %s" % (TOOL, "; ".join(missing)))
    return out


def build_cues(spec, fonts, scenes, k, warnings):
    fps = spec["fps"]
    sub_size, sub_min, sub_w = int(46 * k), int(36 * k), int(1500 * k)
    cues = []
    for s in scenes:
        sc = s["src"]
        n = s["end_f"] - s["start_f"]
        if sc.get("subtitles"):
            local = []
            for c in sc["subtitles"]:
                st = s["start_f"] + round(float(c["start"]) * fps)
                en = min(s["end_f"], s["start_f"] + round(float(c["end"]) * fps))
                if en > st:
                    local.append({"text": c["text"], "para": c.get("para"), "sent": c.get("sent"),
                                  "words": km.word_count(c["text"]), "start": st, "end": en})
            timing = "explicit"
        else:
            units = km.narration_units(sc.get("narration", ""))
            local = km.make_cues(units, int(spec["cue_max_chars"]))
            speech = n
            if s["audio_sec"]:
                speech = min(n, max(1, round(s["audio_sec"] * fps)))
            if local:
                km.distribute(local, s["start_f"], speech)
            timing = "estimated" if local else "none"
        for c in local:
            c["scene"] = s["id"]
            c["size"], c["lines"] = km.fit_lines(fonts, c["text"], "body", sub_size, sub_min, sub_w, 2)
            if len(c["lines"]) > 2:
                warnings.append("%s: subtitle cue wraps to %d lines: %r" % (s["id"], len(c["lines"]), c["text"][:40]))
        s["cue_timing"] = timing
        s["cues"] = local
        cues.extend(local)
    return cues


def paint_base_factory(spec, fonts, theme, s, k):
    W, H = spec["size"]
    sc = s["src"]
    screen = sc.get("screen") or {}

    def make():
        img = km.Image.new("RGBA", (W, H), km.hex_rgba(theme["night"]))
        if s["use_img"]:
            plate, scale = km.cover_fit(sc["image"], (W, H))
            img.alpha_composite(plate)
            s["upscale"] = round(scale, 3)
            if any(screen.get(x) for x in ("heading", "lines", "cards", "bars", "note")):
                km.overlay_rect(img, (72 * k, 150 * k, 1000 * k, 860 * k), km.hex_rgba(theme["night"], 205), int(18 * k))
                km.paint_screen(img, fonts, theme, (112 * k, 190 * k, 960 * k, 820 * k), screen,
                                {kk: (tuple(x * k for x in v) if isinstance(v, (list, tuple)) else v * k)
                                 for kk, v in km.SIZES_LONG.items()})
        else:
            d = km.ImageDraw.Draw(img)
            badge = km.paint_tag(img, fonts, s["id"], "body", int(34 * k), 96 * k, 56 * k,
                                 theme["ink"], km.hex_rgba(theme["yellow"]), pad=(int(16 * k), int(10 * k)))
            if s["title"]:
                cap, _ = fonts.vmetrics("body", int(34 * k))
                title = s["title"]
                while fonts.length(title, "body", int(34 * k)) > 1060 * k and len(title) > 8:
                    title = title[:-2]
                fonts.draw(d, badge[2] + 20 * k, 56 * k + 10 * k + cap, title, "body", int(34 * k), theme["white"])
            if spec.get("mockup_label"):
                km.paint_tag(img, fonts, spec["mockup_label"], "body", int(26 * k), 1824 * k, 60 * k,
                             theme["white"], km.hex_rgba(theme["red"]), anchor="right")
            y_box = 200 * k
            plate = sc.get("plate")
            if plate:
                size = int(24 * k)
                lines = km.wrap_greedy(fonts, "Planned plate: " + plate, "body_regular", size, 1728 * k)[:2]
                y_box = km.draw_block(img, fonts, lines, "body_regular", size, 96 * k, 1824 * k, 138 * k,
                                      theme["muted"], align="left") + 36 * k
            km.paint_screen(img, fonts, theme, (160 * k, y_box, 1760 * k, 820 * k), screen,
                            {kk: (tuple(x * k for x in v) if isinstance(v, (list, tuple)) else v * k)
                             for kk, v in km.SIZES_LONG.items()})
        bar = sc.get("bottom_bar")
        if bar:
            size = int(38 * k)
            cap, desc = fonts.vmetrics("body", size)
            w = fonts.length(bar, "body", size) + 64 * k
            h = cap + desc + 28 * k
            x0, y1 = (W - w) / 2, 1046 * k
            km.overlay_rect(img, (x0, y1 - h, x0 + w, y1), km.hex_rgba(theme["yellow"]), int(10 * k))
            fonts.draw(km.ImageDraw.Draw(img), x0 + 32 * k, y1 - h + 14 * k + cap, bar, "body", size, theme["ink"])
        return img

    cache = {}

    def paint(img):
        if "img" not in cache:
            cache["img"] = make()
        img.alpha_composite(cache["img"])
    return paint


def paint_sub_factory(fonts, theme, cue, W, bottom, k):
    def paint(img):
        size, lines = cue["size"], cue["lines"]
        h = km.block_height(fonts, len(lines), "body", size)
        km.draw_block(img, fonts, lines, "body", size, 0, W, bottom - h, theme["white"],
                      stroke=max(2, int(4 * k)), stroke_fill=theme["ink"])
    return paint


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scenes_json")
    ap.add_argument("--out", help="output mp4 (overrides JSON 'output')")
    ap.add_argument("--mode", choices=["auto", "mockup", "real"], help="overrides JSON 'mode'")
    ap.add_argument("--contact-sheet", help="write a review PNG with one frame per scene")
    ap.add_argument("--contact-max-kb", type=int, default=600)
    ap.add_argument("--preset")
    ap.add_argument("--crf", type=int)
    ap.add_argument("--keep-work", action="store_true", help="keep intermediate frames/audio")
    ap.add_argument("--dry-run", action="store_true", help="print timing table only, no rendering")
    args = ap.parse_args(argv)

    t0 = time.time()
    km.require_tools()
    spec = load_spec(args.scenes_json)
    mode = args.mode or spec["mode"]
    out = Path(args.out or spec.get("output") or "long.mp4")
    srt = out.with_suffix(".srt")
    manifest_path = out.with_suffix(".manifest.json")
    fps = int(spec["fps"])
    W, H = spec["size"]
    k = min(W / 1920.0, H / 1080.0)
    theme = dict(km.DEFAULT_THEME, **(spec.get("theme") or {}))
    warnings = []

    scenes = resolve_scenes(spec, mode, warnings)
    total = scenes[-1]["end_f"]
    fonts = km.FontSet(spec.get("fonts"))
    for role in fonts.designated_missing():
        warnings.append("font role '%s': designated font not installed, fallback %s used"
                        % (role, Path(fonts.choice[role][0]).name))
    cues = build_cues(spec, fonts, scenes, k, warnings)
    any_mock = any(not s["use_img"] for s in scenes)
    burn = spec["burn_subtitles"]
    burn = any_mock if burn == "auto" else bool(burn)

    print("%s %s | mode=%s | %dx%d@%d | scenes=%d | cues=%d | total=%.2fs | burn_subtitles=%s"
          % (TOOL, VERSION, mode, W, H, fps, len(scenes), len(cues), total / fps, burn))
    for s in scenes:
        print("  %-4s %7.2fs -> %7.2fs  %6.2fs  words=%-4d %-12s %s/%s" % (
            s["id"], s["start_f"] / fps, s["end_f"] / fps, (s["end_f"] - s["start_f"]) / fps, s["words"],
            s["duration_source"], "image" if s["use_img"] else "mockup", "audio" if s["use_aud"] else "silent"))
    if args.dry_run:
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    work = out.parent / (".work-" + out.stem)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    try:
        tl = km.Timeline((W, H), total, theme["night"])
        for s in scenes:
            tl.add(s["start_f"], s["end_f"], 0, ("base", s["id"]), paint_base_factory(spec, fonts, theme, s, k))
            if burn:
                bottom = (960 if s["src"].get("bottom_bar") else 1012) * k
                for i, c in enumerate(s["cues"]):
                    tl.add(c["start"], c["end"], 10, ("sub", s["id"], i), paint_sub_factory(fonts, theme, c, W, bottom, k))
        t_frames = time.time()
        seq, n_png = tl.render(work)
        concat = work / "video.ffconcat"
        km.write_ffconcat(seq, fps, concat)
        parts = [{"path": s["src"]["audio"] if s["use_aud"] else None,
                  "frames": s["end_f"] - s["start_f"]} for s in scenes]
        audio = km.build_audio(parts, fps, work, music=spec.get("music") if exists(spec.get("music")) else None,
                               music_volume=float(spec["music_volume"]), loudnorm=bool(spec["loudnorm"]))
        if spec.get("music") and not exists(spec.get("music")):
            warnings.append("music not found (%s): no music track" % spec["music"])
        t_enc = time.time()
        km.encode(concat, audio, out, fps, total, preset=args.preset or spec["preset"],
                  crf=args.crf if args.crf is not None else spec["crf"])
        t_done = time.time()
    finally:
        if not args.keep_work:
            shutil.rmtree(work, ignore_errors=True)

    km.write_srt(srt, cues, fps)
    probe = km.probe_media(out)
    checks = {
        "resolution": (probe.get("width"), probe.get("height")) == (W, H),
        "fps": abs(probe.get("fps", 0) - fps) < 0.01,
        "h264": probe.get("vcodec") == "h264",
        "duration_match": abs(probe["duration"] - total / fps) < 0.1,
    }
    for name, ok in checks.items():
        if not ok:
            warnings.append("check failed: %s (%s)" % (name, probe))
    sheet = None
    if args.contact_sheet:
        items = [((s["start_f"] + (s["end_f"] - s["start_f"]) / 2) / fps,
                  "%s  %s" % (s["id"], km.srt_time((s["end_f"] - s["start_f"]), fps)[3:8])) for s in scenes]
        sheet = km.contact_sheet(out, items, args.contact_sheet, fonts, cols=4, tile_w=456,
                                 title="%s  |  %s  |  %d scenes  |  %s" % (
                                     out.name, mode, len(scenes), km.srt_time(total, fps)[:8]),
                                 max_kb=args.contact_max_kb, theme=theme)
    manifest = {
        "tool": TOOL, "version": VERSION, "kemedia": km.KEMEDIA_VERSION, "spec": str(args.scenes_json),
        "output": str(out), "srt": str(srt), "mode_requested": mode, "size": [W, H], "fps": fps,
        "wpm": spec["wpm"], "burn_subtitles": burn, "total_frames": total, "duration": total / fps,
        "fonts": fonts.report(), "tools": km.tool_versions(), "probe": probe, "checks": checks,
        "contact_sheet": {"path": args.contact_sheet, **sheet} if sheet else None,
        "frames_rendered": n_png,
        "timing_sec": {"total": round(time.time() - t0, 2), "frames": round(t_enc - t_frames, 2),
                       "encode": round(t_done - t_enc, 2)},
        "warnings": warnings,
        "scenes": [{
            "id": s["id"], "title": s["title"], "visual": "image" if s["use_img"] else "mockup",
            "audio_used": s["use_aud"], "words": s["words"], "duration_source": s["duration_source"],
            "start": s["start_f"] / fps, "end": s["end_f"] / fps, "start_frame": s["start_f"],
            "end_frame": s["end_f"], "upscale": s.get("upscale"), "cue_timing": s["cue_timing"],
            "narration": s["src"].get("narration", ""), "screen": s["src"].get("screen"),
            "plate": s["src"].get("plate"), "image": s["src"].get("image"),
            "image_vertical": s["src"].get("image_vertical"), "audio": s["src"].get("audio"),
            "bottom_bar": s["src"].get("bottom_bar"),
            "cues": [{"start": (c["start"] - s["start_f"]) / fps, "end": (c["end"] - s["start_f"]) / fps,
                      "text": c["text"], "para": c.get("para"), "sent": c.get("sent")} for c in s["cues"]],
        } for s in scenes],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"output": str(out), "srt": str(srt), "manifest": str(manifest_path),
                      "duration": round(probe["duration"], 3), "size": [probe.get("width"), probe.get("height")],
                      "fps": probe.get("fps"), "vcodec": probe.get("vcodec"), "acodec": probe.get("acodec"),
                      "bytes": probe["size_bytes"], "checks": checks, "warnings": warnings,
                      "contact_sheet": manifest["contact_sheet"], "timing_sec": manifest["timing_sec"]},
                     ensure_ascii=False, indent=1))
    return 0 if all(checks.values()) else 3


if __name__ == "__main__":
    sys.exit(main())
