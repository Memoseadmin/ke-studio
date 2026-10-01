#!/usr/bin/env python3
"""script_to_scenes: KE Studio script.<lang>.md (S-numbered) -> draft scenes JSON for assemble.py.

Channel script format (writer output):
  ## S01 — Title | 0:00–0:16 | 39 words
  <narration paragraphs; [F7]-style fact tags are stripped>
  - 화면: <visual note, "quoted" strings optional>
  - 텍스트: <on-screen text as "quoted" strings>      (also: 자막(KR):, Text:, On-screen:)
A "quoted" string on a text line containing "하단 고정" / "bottom bar" becomes the scene's bottom_bar.

Optional --prompts design/scene-prompts.md: the "요약:" (or "Summary:") line under each "## Sxx"
becomes the scene's "plate" note (shown only on mockup slides).

Usage:
  python3 script_to_scenes.py episodes/EPxxx/script.en.md --prompts episodes/EPxxx/design/scene-prompts.md \
      --output-video render/EPxxx/long.mp4 --out render/EPxxx/scenes.json
The draft is meant to be reviewed/edited (cards, bars, note) before rendering.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HEADER = re.compile(r"^##\s+(S\d+)\s*[—–-]\s*(.+?)\s*$")
TAG = re.compile(r"\s*\[[A-Z]{1,3}\d+\]")
QUOTE = re.compile(r"\"([^\"]+)\"|“([^”]+)”")
TEXT_KEYS = ("텍스트", "자막", "text", "on-screen")
VISUAL_KEYS = ("화면", "visual", "screen")
BAR_KEYS = ("하단 고정", "bottom bar")


def quotes(line):
    return [a or b for a, b in QUOTE.findall(line)]


def parse_script(path):
    scenes, cur = [], None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        m = HEADER.match(raw)
        if m:
            if cur is not None:
                cur["paras"].append(" ".join(cur["buf"]))
            parts = [p.strip() for p in m.group(2).split("|")]
            declared = None
            for p in parts[1:]:
                wm = re.search(r"(\d[\d,]*)\s*(words?|단어|어절)", p)
                if wm:
                    declared = int(wm.group(1).replace(",", ""))
            cur = {"id": m.group(1), "title": parts[0], "declared_words": declared,
                   "paras": [], "buf": [], "text_lines": [], "visual_lines": []}
            scenes.append(cur)
            continue
        if cur is None:
            continue
        line = raw.strip()
        if raw.startswith("## ") or line == "---":
            cur["paras"].append(" ".join(cur["buf"]))
            cur = None
            continue
        if line.startswith("- "):
            body = line[2:]
            key = body.split(":", 1)[0].strip().lower()
            if any(key.startswith(k) for k in TEXT_KEYS):
                cur["text_lines"].append(body)
            elif any(key.startswith(k) for k in VISUAL_KEYS):
                cur["visual_lines"].append(body)
            continue
        if not line:
            if cur["buf"]:
                cur["paras"].append(" ".join(cur["buf"]))
                cur["buf"] = []
            continue
        if line.startswith(("|", ">", "```", "#")):
            continue
        cur["buf"].append(TAG.sub("", line).strip())
    if cur is not None:
        cur["paras"].append(" ".join(cur["buf"]))
    return scenes


def parse_prompts(path):
    plates, cur = {}, None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(S\d+)\b", raw)
        if m:
            cur = m.group(1)
            continue
        if cur and cur not in plates:
            sm = re.match(r"^\s*(요약|Summary)\s*:\s*(.+)$", raw)
            if sm:
                plates[cur] = sm.group(2).strip()
    return plates


def to_spec(scenes, plates, output_video):
    out, warnings = [], []
    for s in scenes:
        paras = [p.strip() for p in s["paras"] if p.strip()]
        narration = "\n\n".join(paras)
        words = len(narration.split())
        if s["declared_words"] is not None and s["declared_words"] != words:
            warnings.append("%s: header says %d words, parsed %d" % (s["id"], s["declared_words"], words))
        lines, bar = [], None
        for tl in s["text_lines"]:
            qs = quotes(tl)
            if any(k in tl.lower() for k in BAR_KEYS) and qs:
                bar = qs[0]
                qs = qs[1:]
            lines.extend(qs)
        if not lines:
            for vl in s["visual_lines"]:
                lines.extend(quotes(vl))
        screen = {}
        if lines:
            screen["heading"] = lines[0]
            if lines[1:]:
                screen["lines"] = lines[1:]
        scene = {"id": s["id"], "title": s["title"], "narration": narration, "screen": screen,
                 "image": None, "image_vertical": None, "audio": None}
        if bar:
            scene["bottom_bar"] = bar
        if plates.get(s["id"]):
            scene["plate"] = plates[s["id"]]
        out.append(scene)
    spec = {"output": output_video, "size": [1920, 1080], "fps": 30, "wpm": 150, "mode": "auto",
            "scenes": out}
    return spec, warnings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script")
    ap.add_argument("--prompts")
    ap.add_argument("--output-video", default="long.mp4")
    ap.add_argument("--out", help="write JSON here (default: stdout)")
    args = ap.parse_args(argv)
    scenes = parse_script(args.script)
    if not scenes:
        raise SystemExit("no '## Sxx — Title' scenes found in %s" % args.script)
    plates = parse_prompts(args.prompts) if args.prompts else {}
    spec, warnings = to_spec(scenes, plates, args.output_video)
    text = json.dumps(spec, ensure_ascii=False, indent=1)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    total = sum(len(s["narration"].split()) for s in spec["scenes"])
    print("scenes=%d words=%d est=%.1fs @150wpm" % (len(spec["scenes"]), total, total / 150 * 60), file=sys.stderr)
    for w in warnings:
        print("WARN " + w, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
