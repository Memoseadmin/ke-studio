#!/usr/bin/env python3
"""kemedia: shared render helpers for the KE Studio in-house skills.

Used by
  .claude/skills/ffmpeg-assemble/scripts/assemble.py   (16:9 long-form)
  .claude/skills/shorts-cut/scripts/shorts_cut.py      (9:16 shorts)

Needs Python 3.9+, Pillow, and ffmpeg/ffprobe on PATH (scripts/setup.sh).
No network access, no API keys, no external media: every mockup pixel is
drawn here with Pillow (text, flat colors, simple shapes).
"""
from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

KEMEDIA_VERSION = "1.0.0"

# Korea Explained design-system v1.0 tokens. "muted"/"panel" are mockup-only
# annotation tones (not final-design colors).
DEFAULT_THEME = {
    "night": "#1B1F2A",
    "paper": "#F7F3EA",
    "red": "#C8102E",
    "yellow": "#FFD23F",
    "ink": "#111111",
    "white": "#FFFFFF",
    "chart": "#6FA89B",
    "muted": "#A9AEB8",
    "panel": "#262C3A",
}


def hex_rgba(value, alpha=255):
    value = value.lstrip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), alpha)


# --------------------------------------------------------------------------- #
# Fonts
# --------------------------------------------------------------------------- #
LIB_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
LIB_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
DEJAVU_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
WQY = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

# role -> designated (brand) fonts first, then alternates, then installed fallbacks
FONT_ROLES = {
    "headline": {"designated": ["Anton"], "alt": [], "fallback": [LIB_BOLD, DEJAVU_BOLD]},
    "body": {"designated": ["Pretendard:style=Bold"], "alt": ["Inter:style=Bold"],
             "fallback": [LIB_BOLD, DEJAVU_BOLD]},
    "body_regular": {"designated": ["Pretendard:style=Regular"], "alt": ["Inter:style=Regular"],
                     "fallback": [LIB_REG, DEJAVU]},
    "cjk": {"designated": ["Pretendard:style=Bold", "Black Han Sans"],
            "alt": ["Noto Sans CJK KR:style=Bold", "Noto Sans KR:style=Bold"], "fallback": [WQY]},
    "symbol": {"designated": [], "alt": [], "fallback": [DEJAVU_BOLD, LIB_BOLD]},
}

# Filename substring -> license note (for render logs). Unknown -> must be checked.
KNOWN_LICENSES = [
    ("anton", "SIL OFL 1.1"),
    ("blackhansans", "SIL OFL 1.1"),
    ("pretendard", "SIL OFL 1.1"),
    ("inter", "SIL OFL 1.1"),
    ("liberation", "SIL OFL 1.1 (Liberation Fonts 2.x)"),
    ("dejavu", "Bitstream Vera license + public-domain DejaVu changes"),
    ("wqy-zenhei", "GPL-2 with font embedding exception"),
    ("noto", "SIL OFL 1.1"),
]


def font_license(path):
    name = Path(path).name.lower().replace(" ", "")
    for key, lic in KNOWN_LICENSES:
        if key in name:
            return lic
    return "UNKNOWN - check before commercial use"


def fc_find(pattern):
    """Return (file, index) of the first installed font matching a fontconfig pattern."""
    if not shutil.which("fc-list"):
        return None
    try:
        out = subprocess.run(["fc-list", "-f", "%{file}|%{index}\n", pattern],
                             capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    for line in out.splitlines():
        if "|" not in line:
            continue
        file_, idx = line.rsplit("|", 1)
        if Path(file_).exists():
            try:
                return file_, int(idx or 0)
            except ValueError:
                return file_, 0
    return None


class FontSet:
    """Resolves font roles and draws mixed-script text with per-glyph fallback."""

    def __init__(self, overrides=None):
        overrides = overrides or {}
        self.choice = {}
        for role, spec in FONT_ROLES.items():
            chosen = None
            ov = overrides.get(role)
            if ov:
                file_ = ov["file"] if isinstance(ov, dict) else ov
                idx = int(ov.get("index", 0)) if isinstance(ov, dict) else 0
                if Path(file_).exists():
                    chosen = (file_, idx, "override")
            for tier in ("designated", "alt"):
                if chosen:
                    break
                for pat in spec[tier]:
                    hit = fc_find(pat)
                    if hit:
                        chosen = (hit[0], hit[1], tier if tier == "designated" else "alternate")
                        break
            if not chosen:
                for file_ in spec["fallback"]:
                    if Path(file_).exists():
                        chosen = (file_, 0, "fallback")
                        break
            if not chosen:
                hit = fc_find(":style=Bold") or fc_find(":")
                if hit:
                    chosen = (hit[0], hit[1], "fallback")
            if not chosen:
                raise SystemExit("kemedia: no usable font for role '%s'" % role)
            self.choice[role] = chosen
        self._fonts = {}
        self._glyph = {}
        self._notdef = {}

    def report(self):
        rows = []
        for role, (file_, idx, tier) in self.choice.items():
            rows.append({"role": role, "file": file_, "index": idx, "tier": tier,
                         "license": font_license(file_)})
        return rows

    def designated_missing(self):
        return [r for r, (_, _, tier) in self.choice.items()
                if tier == "fallback" and FONT_ROLES[r]["designated"]]

    def font(self, role, size):
        key = (role, int(size))
        if key not in self._fonts:
            file_, idx, _ = self.choice[role]
            self._fonts[key] = ImageFont.truetype(file_, int(size), index=idx)
        return self._fonts[key]

    @staticmethod
    def _sig(fnt, ch):
        im = Image.new("L", (96, 96), 0)
        ImageDraw.Draw(im).text((16, 16), ch, font=fnt, fill=255)
        return im.tobytes()

    def has_glyph(self, role, ch):
        if ch.isspace():
            return True
        key = (role, ch)
        if key not in self._glyph:
            fnt = self.font(role, 40)
            if role not in self._notdef:
                self._notdef[role] = {self._sig(fnt, c) for c in ("", "\U0010fffd")}
            sig = self._sig(fnt, ch)
            self._glyph[key] = sig not in self._notdef[role]
        return self._glyph[key]

    def runs(self, text, role):
        chain = [role] + [r for r in ("cjk", "symbol") if r != role]
        runs, buf, cur = [], "", None
        for ch in text:
            if ch.isspace() and cur:
                r = cur
            else:
                r = next((c for c in chain if self.has_glyph(c, ch)), role)
            if r != cur and buf:
                runs.append((buf, cur))
                buf = ""
            cur = r
            buf += ch
        if buf:
            runs.append((buf, cur))
        return runs

    def length(self, text, role, size):
        return sum(self.font(r, size).getlength(s) for s, r in self.runs(text, role))

    def vmetrics(self, role, size):
        """(cap/ascender height above baseline, descender below) in px."""
        box = self.font(role, size).getbbox("Hgy", anchor="ls")
        return -box[1], box[3]

    def draw(self, draw, x, baseline, text, role, size, fill, stroke=0, stroke_fill=None):
        for s, r in self.runs(text, role):
            fnt = self.font(r, size)
            draw.text((x, baseline), s, font=fnt, fill=fill, anchor="ls",
                      stroke_width=stroke, stroke_fill=stroke_fill)
            x += fnt.getlength(s)


def wrap_greedy(fonts, text, role, size, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and fonts.length(trial, role, size) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines or [""]


def wrap_balanced(fonts, text, role, size, max_w):
    """One line if it fits, else the 2-line split with the shortest longer line."""
    if fonts.length(text, role, size) <= max_w:
        return [text]
    words = text.split()
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        wa, wb = fonts.length(a, role, size), fonts.length(b, role, size)
        if wa <= max_w and wb <= max_w and (best is None or max(wa, wb) < best[0]):
            best = (max(wa, wb), [a, b])
    return best[1] if best else wrap_greedy(fonts, text, role, size, max_w)


def fit_lines(fonts, text, role, max_size, min_size, max_w, max_lines):
    """Largest size (step 2px) at which text wraps into <= max_lines within max_w."""
    size = int(max_size)
    while size >= int(min_size):
        lines = (wrap_balanced if max_lines == 2 else wrap_greedy)(fonts, text, role, size, max_w)
        if len(lines) <= max_lines and all(fonts.length(l, role, size) <= max_w for l in lines):
            return size, lines
        size -= 2
    return int(min_size), wrap_greedy(fonts, text, role, int(min_size), max_w)


def block_height(fonts, n_lines, role, size, lh=1.22):
    cap, desc = fonts.vmetrics(role, size)
    return cap + desc + (n_lines - 1) * size * lh


def draw_block(img, fonts, lines, role, size, x0, x1, y_top, fill, align="center",
               stroke=0, stroke_fill=None, lh=1.22):
    """Draw pre-wrapped lines inside [x0, x1] from y_top; returns the bottom y."""
    d = ImageDraw.Draw(img)
    cap, desc = fonts.vmetrics(role, size)
    for i, line in enumerate(lines):
        w = fonts.length(line, role, size)
        if align == "center":
            x = x0 + (x1 - x0 - w) / 2
        elif align == "right":
            x = x1 - w
        else:
            x = x0
        fonts.draw(d, x, y_top + cap + i * size * lh, line, role, size, fill, stroke, stroke_fill)
    return y_top + cap + desc + (len(lines) - 1) * size * lh


def overlay_rect(img, box, fill_rgba, radius=0):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(box, radius=radius, fill=fill_rgba)
    img.alpha_composite(layer)


def paint_tag(img, fonts, text, role, size, x, y, fg, bg, pad=(14, 8), anchor="left", radius=8):
    """Small label in a rounded box. Returns (x0, y0, x1, y1)."""
    cap, desc = fonts.vmetrics(role, size)
    w = fonts.length(text, role, size) + 2 * pad[0]
    h = cap + desc + 2 * pad[1]
    x0 = {"left": x, "right": x - w, "center": x - w / 2}[anchor]
    box = (x0, y, x0 + w, y + h)
    overlay_rect(img, box, bg, radius)
    fonts.draw(ImageDraw.Draw(img), x0 + pad[0], y + pad[1] + cap, text, role, size, fg)
    return box


def cover_fit(path, size):
    """Scale-to-cover + center-crop an image file to size (w, h). Returns (RGBA image, upscale factor)."""
    src = Image.open(path).convert("RGBA")
    w, h = size
    scale = max(w / src.width, h / src.height)
    nw, nh = max(w, round(src.width * scale)), max(h, round(src.height * scale))
    src = src.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - w) // 2, (nh - h) // 2
    return src.crop((left, top, left + w, top + h)), scale


# --------------------------------------------------------------------------- #
# Screen text (numbers, quotes, titles drawn as overlays: never inside AI plates)
# --------------------------------------------------------------------------- #
SIZES_LONG = {"heading": (100, 48), "line": (54, 32), "card": (72, 34), "bar": 40, "note": 30, "gap": 40}
SIZES_SHORT = {"heading": (76, 40), "line": (46, 30), "card": (50, 28), "bar": 32, "note": 26, "gap": 30}
SCREEN_ORDER = ("heading", "lines", "cards", "bars", "note")


def _layout_screen(fonts, screen, box_w, sizes, s):
    items = []
    hd = screen.get("heading")
    if hd:
        size, lines = fit_lines(fonts, hd, "headline", sizes["heading"][0] * s, sizes["heading"][1] * s, box_w, 2)
        items.append(("heading", block_height(fonts, len(lines), "headline", size), (size, lines)))
    for text in screen.get("lines", []) or []:
        size, lines = fit_lines(fonts, text, "body", sizes["line"][0] * s, sizes["line"][1] * s, box_w, 2)
        items.append(("line", block_height(fonts, len(lines), "body", size), (size, lines)))
    cards = screen.get("cards") or []
    if cards:
        gap = 24 * s
        cw = (box_w - gap * (len(cards) - 1)) / len(cards)
        size = int(sizes["card"][0] * s)
        while size > sizes["card"][1] * s and any(fonts.length(c, "headline", size) > cw - 64 * s for c in cards):
            size -= 2
        cap, desc = fonts.vmetrics("headline", size)
        items.append(("cards", cap + desc + 44 * s, (size, cw, gap)))
    bars = screen.get("bars") or []
    if bars:
        size = int(sizes["bar"] * s)
        cap, desc = fonts.vmetrics("body", size)
        row = cap + desc + 10 * s + 26 * s
        items.append(("bars", row * len(bars) + 18 * s * (len(bars) - 1), (size, row)))
    note = screen.get("note")
    if note:
        size = int(sizes["note"] * s)
        lines = wrap_greedy(fonts, note, "body_regular", size, box_w)[:2]
        items.append(("note", block_height(fonts, len(lines), "body_regular", size), (size, lines)))
    order = list(screen.get("order") or SCREEN_ORDER)
    rank = {"line": order.index("lines") if "lines" in order else 99}
    rank.update({kind: order.index(kind) for kind in order if kind != "lines"})
    items.sort(key=lambda it: rank.get(it[0], 99))
    total = sum(h for _, h, _ in items) + sizes["gap"] * s * max(0, len(items) - 1)
    return items, total


def paint_screen(img, fonts, theme, box, screen, sizes):
    """Lay out heading / lines / cards / bars / note centered inside box."""
    if not screen:
        return
    x0, y0, x1, y1 = box
    box_w, box_h = x1 - x0, y1 - y0
    for s in (1.0, 0.92, 0.85, 0.78, 0.7, 0.62, 0.55, 0.48):
        items, total = _layout_screen(fonts, screen, box_w, sizes, s)
        if total <= box_h:
            break
    d = ImageDraw.Draw(img)
    y = y0 + max(0, (box_h - total) / 2)
    yellow, white, chart = theme["yellow"], theme["white"], theme["chart"]
    for kind, h, data in items:
        if kind == "heading":
            size, lines = data
            draw_block(img, fonts, lines, "headline", size, x0, x1, y, yellow)
        elif kind == "line":
            size, lines = data
            draw_block(img, fonts, lines, "body", size, x0, x1, y, white)
        elif kind == "note":
            size, lines = data
            draw_block(img, fonts, lines, "body_regular", size, x0, x1, y, theme["muted"])
        elif kind == "cards":
            size, cw, gap = data
            cap, desc = fonts.vmetrics("headline", size)
            for i, text in enumerate(screen["cards"]):
                cx0 = x0 + i * (cw + gap)
                d.rounded_rectangle((cx0, y, cx0 + cw, y + h), radius=14, fill=theme["panel"],
                                    outline=yellow, width=4)
                tw = fonts.length(text, "headline", size)
                baseline = y + (h - (cap + desc)) / 2 + cap
                fonts.draw(d, cx0 + (cw - tw) / 2, baseline, text, "headline", size, yellow)
        elif kind == "bars":
            size, row = data
            cap, desc = fonts.vmetrics("body", size)
            vmax = max(float(b.get("value", 0)) for b in screen["bars"]) or 1.0
            by = y
            for b in screen["bars"]:
                label, disp = b.get("label", ""), b.get("display", "")
                hl = bool(b.get("highlight"))
                fonts.draw(d, x0, by + cap, label, "body", size, white)
                if disp:
                    lx = x0 + fonts.length(label + "  ", "body", size)
                    fonts.draw(d, lx, by + cap, disp, "body", size, yellow if hl else white)
                bar_y = by + cap + desc + 10 * s
                bw = max(8, box_w * float(b.get("value", 0)) / vmax)
                d.rectangle((x0, bar_y, x0 + bw, bar_y + 26 * s), fill=yellow if hl else chart)
                by += row + 18 * s
        y += h + sizes["gap"] * s


# --------------------------------------------------------------------------- #
# Narration -> sentences -> subtitle cues
# --------------------------------------------------------------------------- #
_WORD = re.compile(r"\S+")
_BOUNDARY = re.compile(r"([.!?…][\"”’)\]]*)\s+(?=[\"“‘(\[]?[A-Z0-9$€£가-힣])")


def word_count(text):
    return len(_WORD.findall(text or ""))


def split_paragraphs(narration):
    paras = re.split(r"\n\s*\n", (narration or "").strip())
    return [re.sub(r"\s+", " ", p).strip() for p in paras if p.strip()]


def split_sentences(par):
    out, last = [], 0
    for m in _BOUNDARY.finditer(par):
        out.append(par[last:m.end(1)].strip())
        last = m.end()
    tail = par[last:].strip()
    if tail:
        out.append(tail)
    return out


def narration_units(narration):
    """[{para, sent, idx, text}] with 1-based para/sent and 0-based global idx."""
    units = []
    for pi, par in enumerate(split_paragraphs(narration), 1):
        for si, sent in enumerate(split_sentences(par), 1):
            units.append({"para": pi, "sent": si, "idx": len(units), "text": sent})
    return units


def chunk_sentence(s, max_chars):
    """Split a sentence into ~equal pieces of <= max_chars (+15% tolerance) at word boundaries,
    preferring cuts after , ; : . Always makes progress, so recursion terminates."""
    words = s.split()
    if len(s) <= max_chars or len(words) < 2:
        return [s]
    n = math.ceil(len(s) / max_chars)
    ends, pos = [], 0
    for w in words:
        pos += len(w)
        ends.append(pos)
        pos += 1
    cuts = []
    for j in range(1, n):
        ideal = len(s) * j / n
        best = None
        for i in range(len(words) - 1):
            if cuts and i <= cuts[-1]:
                continue
            score = abs(ends[i] - ideal) - (0.2 * max_chars if words[i][-1] in ",;:" else 0)
            if best is None or score < best[0]:
                best = (score, i)
        if best is None:
            break
        cuts.append(best[1])
    pieces, start = [], 0
    for c in cuts:
        pieces.append(" ".join(words[start:c + 1]))
        start = c + 1
    pieces.append(" ".join(words[start:]))
    out = []
    for piece in pieces:
        if len(piece) > max_chars * 1.15 and len(piece.split()) >= 2:
            out.extend(chunk_sentence(piece, max_chars))
        else:
            out.append(piece)
    return out


def make_cues(units, max_chars):
    cues = []
    for u in units:
        for piece in chunk_sentence(u["text"], max_chars):
            cues.append({"text": piece, "para": u.get("para"), "sent": u.get("sent"),
                         "words": max(1, word_count(piece))})
    return cues


def distribute(cues, start_f, n_frames):
    """Assign start/end frames to cues proportionally to word count, contiguous."""
    total = sum(c["words"] for c in cues) or 1
    acc = 0
    prev = start_f
    for i, c in enumerate(cues):
        acc += c["words"]
        end = start_f + round(n_frames * acc / total)
        end = max(end, prev + 1) if i < len(cues) - 1 else start_f + n_frames
        c["start"], c["end"] = prev, end
        prev = end
    return cues


def srt_time(frame, fps):
    ms = int(round(frame * 1000.0 / fps))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def write_srt(path, cues, fps):
    out = []
    for i, c in enumerate(cues, 1):
        out.append("%d\n%s --> %s\n%s\n" % (i, srt_time(c["start"], fps), srt_time(c["end"], fps),
                                          "\n".join(c["lines"])))
    Path(path).write_text("\n".join(out), encoding="utf-8")


# --------------------------------------------------------------------------- #
# Timeline -> still frames -> ffconcat
# --------------------------------------------------------------------------- #
class Timeline:
    """Layers with [start, end) in frames. Each distinct layer combination becomes one PNG."""

    def __init__(self, size, total_frames, bg):
        self.size, self.total, self.bg = size, total_frames, bg
        self.layers = []

    def add(self, start, end, z, key, paint):
        start, end = max(0, int(start)), min(self.total, int(end))
        if end > start:
            self.layers.append((start, end, z, key, paint))

    def render(self, workdir):
        bounds = sorted({0, self.total} | {l[0] for l in self.layers} | {l[1] for l in self.layers})
        cache, seq = {}, []
        for a, b in zip(bounds, bounds[1:]):
            active = sorted((l for l in self.layers if l[0] <= a and l[1] >= b), key=lambda l: l[2])
            key = tuple(l[3] for l in active)
            if key not in cache:
                img = Image.new("RGBA", self.size, hex_rgba(self.bg))
                for layer in active:
                    layer[4](img)
                p = Path(workdir) / ("frame_%05d.png" % len(cache))
                img.convert("RGB").save(p, compress_level=1)
                cache[key] = p
            if seq and seq[-1][0] == cache[key]:
                seq[-1] = (seq[-1][0], seq[-1][1] + b - a)
            else:
                seq.append((cache[key], b - a))
        return seq, len(cache)


def write_ffconcat(seq, fps, path):
    def q(p):
        return str(Path(p).resolve()).replace("'", "'\\''")
    lines = ["ffconcat version 1.0"]
    for p, n in seq:
        lines += ["file '%s'" % q(p), "duration %.6f" % (n / fps)]
    lines.append("file '%s'" % q(seq[-1][0]))
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# ffmpeg / ffprobe
# --------------------------------------------------------------------------- #
def run(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError("command failed (%d): %s\n%s" % (res.returncode, " ".join(map(str, cmd[:6])),
                                                           res.stderr[-3000:]))
    return res.stdout


def require_tools():
    missing = [t for t in ("ffmpeg", "ffprobe") if not shutil.which(t)]
    if missing:
        raise SystemExit("kemedia: missing %s (install via scripts/setup.sh; do not install ad hoc)"
                         % ", ".join(missing))


def tool_versions():
    v = {}
    for t in ("ffmpeg", "ffprobe"):
        try:
            v[t] = run([t, "-version"]).splitlines()[0]
        except Exception as exc:  # noqa: BLE001
            v[t] = "unavailable (%s)" % exc
    import PIL
    v["Pillow"] = PIL.__version__
    import sys
    v["python"] = sys.version.split()[0]
    return v


def probe_duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)])
    return float(json.loads(out)["format"]["duration"])


def probe_media(path):
    out = run(["ffprobe", "-v", "error", "-show_entries",
               "format=duration,size:stream=codec_type,codec_name,profile,width,height,r_frame_rate,"
               "pix_fmt,nb_frames,sample_rate,channels", "-of", "json", str(path)])
    data = json.loads(out)
    info = {"duration": float(data["format"]["duration"]), "size_bytes": int(data["format"]["size"])}
    for st in data.get("streams", []):
        if st.get("codec_type") == "video":
            num, den = (st.get("r_frame_rate") or "0/1").split("/")
            info.update({"vcodec": st.get("codec_name"), "profile": st.get("profile"),
                         "width": st.get("width"), "height": st.get("height"),
                         "fps": round(float(num) / float(den or 1), 3), "pix_fmt": st.get("pix_fmt"),
                         "nb_frames": int(st.get("nb_frames") or 0)})
        elif st.get("codec_type") == "audio":
            info.update({"acodec": st.get("codec_name"), "sample_rate": int(st.get("sample_rate") or 0),
                         "channels": st.get("channels")})
    return info


def build_audio(parts, fps, workdir, music=None, music_volume=0.12, loudnorm=False):
    """parts: [{path|None, start, end, frames}] -> one 48 kHz stereo WAV of exact length.
    Returns None when every part is silent and there is no music (caller uses anullsrc)."""
    if not any(p.get("path") for p in parts) and not music and not loudnorm:
        return None
    workdir = Path(workdir)
    base = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    files = []
    for i, p in enumerate(parts):
        dur = p["frames"] / fps
        out = workdir / ("aud_%04d.wav" % i)
        if p.get("path"):
            cmd = list(base)
            if p.get("start"):
                cmd += ["-ss", "%.6f" % p["start"]]
            if p.get("end") is not None:
                cmd += ["-t", "%.6f" % max(0.01, p["end"] - (p.get("start") or 0))]
            cmd += ["-i", str(p["path"]), "-af", "aresample=48000,apad,atrim=0:%.6f" % dur]
        else:
            cmd = base + ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "%.6f" % dur]
        run(cmd + ["-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(out)])
        files.append(out)
    lst = workdir / "audio.ffconcat"
    lst.write_text("ffconcat version 1.0\n" + "".join("file '%s'\n" % f.resolve() for f in files))
    full = workdir / "audio_full.wav"
    run(base + ["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(full)])
    if not music and not loudnorm:
        return full
    total = sum(p["frames"] for p in parts) / fps
    final = workdir / "audio_final.wav"
    cmd = base + ["-i", str(full)]
    chain = "[0:a]anull[v]"
    if music:
        cmd += ["-stream_loop", "-1", "-i", str(music)]
        fade = max(0.0, total - 2.0)
        chain = ("[1:a]aresample=48000,volume=%.3f,atrim=0:%.6f,afade=t=out:st=%.3f:d=2[m];"
                 "[0:a][m]amix=inputs=2:duration=first:normalize=0[v]" % (music_volume, total, fade))
    if loudnorm:
        chain += ";[v]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[v2]"
        out_label = "[v2]"
    else:
        out_label = "[v]"
    run(cmd + ["-filter_complex", chain, "-map", out_label, "-t", "%.6f" % total,
               "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(final)])
    return final


def encode(concat, audio, out, fps, total_frames, preset="medium", crf=20, abitrate="192k"):
    total = total_frames / fps
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-f", "concat", "-safe", "0", "-i", str(concat)]
    if audio:
        cmd += ["-i", str(audio)]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
    cmd += ["-map", "0:v:0", "-map", "1:a:0", "-vf", "fps=%s,format=yuv420p" % fps,
            "-c:v", "libx264", "-preset", preset, "-tune", "stillimage", "-crf", str(crf),
            "-profile:v", "high", "-r", str(fps), "-c:a", "aac", "-b:a", abitrate, "-ar", "48000", "-ac", "2",
            "-t", "%.6f" % total, "-movflags", "+faststart", str(out)]
    run(cmd)


# --------------------------------------------------------------------------- #
# Review contact sheet (small PNG for PRs)
# --------------------------------------------------------------------------- #
def save_png_under(img, path, max_kb):
    path = Path(path)
    img.save(path, optimize=True)
    steps = []
    for colors in (256, 128, 64):
        if path.stat().st_size <= max_kb * 1024:
            break
        img.quantize(colors=colors, method=Image.Quantize.MEDIANCUT).save(path, optimize=True)
        steps.append("quantize%d" % colors)
    cur = img
    while path.stat().st_size > max_kb * 1024 and cur.width > 400:
        cur = cur.resize((int(cur.width * 0.85), int(cur.height * 0.85)), Image.LANCZOS)
        cur.quantize(colors=128, method=Image.Quantize.MEDIANCUT).save(path, optimize=True)
        steps.append("scale%d" % cur.width)
    return {"bytes": path.stat().st_size, "size": list(Image.open(path).size), "steps": steps}


def contact_sheet(video, items, out_png, fonts, cols, tile_w, title=None, max_kb=600, theme=None):
    """items: [(time_sec, label)] from `video`, or [(video_path, time_sec, label)] across videos
    -> grid PNG of frames grabbed from the encoded file(s)."""
    theme = theme or DEFAULT_THEME
    items = [it if len(it) == 3 else (video, it[0], it[1]) for it in items]
    tiles = []
    with tempfile.TemporaryDirectory() as td:
        for i, (src, t, _) in enumerate(items):
            p = Path(td) / ("t%03d.png" % i)
            run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "%.3f" % t, "-i", str(src),
                 "-frames:v", "1", "-vf", "scale=%d:-2" % tile_w, str(p)])
            tiles.append(Image.open(p).convert("RGB"))
    items = [(t, label) for _, t, label in items]
    th = tiles[0].height
    pad, label_h, title_h = 14, 36, (58 if title else 0)
    rows = math.ceil(len(tiles) / cols)
    W = cols * tile_w + (cols + 1) * pad
    H = title_h + rows * (th + label_h) + (rows + 1) * pad
    sheet = Image.new("RGBA", (W, H), hex_rgba(theme["night"]))
    d = ImageDraw.Draw(sheet)
    if title:
        fonts.draw(d, pad, pad + 30, title, "body", 26, theme["white"])
    for i, (tile, (_, label)) in enumerate(zip(tiles, items)):
        r, c = divmod(i, cols)
        x = pad + c * (tile_w + pad)
        y = title_h + pad + r * (th + label_h + pad)
        sheet.paste(tile, (x, y))
        fonts.draw(d, x + 2, y + th + 25, label, "body", 20, theme["yellow"])
    Path(out_png).parent.mkdir(parents=True, exist_ok=True)
    return save_png_under(sheet.convert("RGB"), out_png, max_kb)
