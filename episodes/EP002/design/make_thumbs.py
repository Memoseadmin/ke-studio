#!/usr/bin/env python3
"""EP002 thumbnail layout mockups. Pillow only, no image-generation API.

These are LAYOUT MOCKUPS (colour, type, composition), not final art.
Final plates come from the prompts in thumbnails.md; type is added in post.
Structure follows episodes/EP001/design/make_thumbs.py (EP001 file untouched).

Usage:
    python3 episodes/EP002/design/make_thumbs.py              # writes PNGs next to this file
    python3 episodes/EP002/design/make_thumbs.py --guides DIR # also writes guide overlays + feed-size previews to DIR
    python3 episodes/EP002/design/make_thumbs.py --compare-only  # rebuild thumbs-compare.png from existing thumb-1..3.png

Outputs: thumb-1.png, thumb-2.png, thumb-3.png (1280x720), thumbs-compare.png (1920 wide)
Tokens and rules: /episodes/EP001/design/design-system.md v1.0 (channel-wide, referenced, not copied).

Hangul: all jamo are drawn with the installed KR font (WenQuanYi Zen Hei, mockup only).
The four obsolete letters (U+3181 yesieung, U+317F pansios, U+3186 yeorinhieuh, U+318D araea)
render in that font, so no shape substitutes were needed. If a font lacks them, the
`jamo_glyph()` helper falls back to simple geometric shapes.
"""
import argparse
import functools
import os
import random
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1280, 720
S = 2  # supersampling factor, downsampled with LANCZOS at the end

# --- colour tokens (design-system.md) ---------------------------------------
RED = "#C8102E"
YELLOW = "#FFD23F"
INK = "#111111"
PAPER = "#F7F3EA"
NIGHT = "#1B1F2A"
WHITE = "#FFFFFF"
STEEL = "#C9CDD2"
KRAFT = "#C9A877"
# shades derived for illustration volume (not brand tokens, each < 15% of frame)
NIGHT_L = "#2A3040"
STONE_A = "#262B39"
STONE_B = "#303648"
STONE_C = "#222736"
PAPER_D = "#E9E2D3"
GREY = "#7C838F"      # "no longer used" jamo (grey per script S04)
INK_SOFT = "#4A4F5A"  # blurred, unreadable jamo on paper

SAFE = 64                          # outer safe margin (px at 1280x720)
BR_ZONE = (1040, 620, 1280, 720)   # bottom-right duration badge zone, keep empty

# 28 letters of 1446: 17 consonants + 11 vowels. Grey = no longer used.
JAMO_28 = [
    "ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ",
    "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ",
    "ㆁ", "ㅿ", "ㆆ", "ㅏ", "ㅑ", "ㅓ", "ㅕ",
    "ㅗ", "ㅛ", "ㅜ", "ㅠ", "ㅡ", "ㅣ", "ㆍ",
]
OBSOLETE = {"ㆁ", "ㅿ", "ㆆ", "ㆍ"}
MODERN_24 = [j for j in JAMO_28 if j not in OBSOLETE]


# --- fonts --------------------------------------------------------------------
def find_font(families, fallbacks):
    """Prefer brand fonts if installed (fc-list), else fall back to system fonts."""
    listing = ""
    try:
        listing = subprocess.run(["fc-list", ":", "family", "file"], capture_output=True,
                                 text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        pass
    for fam in families:
        for line in listing.splitlines():
            path, _, names = line.partition(": ")
            if fam in [n.strip() for n in names.split(",")]:
                return path.strip()
    for path in fallbacks:
        if os.path.exists(path):
            return path
    raise SystemExit("No usable font for %s" % (families,))


EN_HEAD = find_font(["Anton"], [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
])
KR_FONT = find_font(["Black Han Sans", "Pretendard", "Noto Sans CJK KR", "Noto Sans KR"], [
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/opentype/unifont/unifont.otf",
])


@functools.lru_cache(maxsize=None)
def font(path, size):
    return ImageFont.truetype(path, size, index=0)


def has_glyph(path, ch, size=64):
    """True if the font draws `ch` differently from an unassigned PUA codepoint (.notdef)."""
    f = font(path, size)
    a = Image.new("L", (size * 2, size * 2), 0)
    b = Image.new("L", (size * 2, size * 2), 0)
    ImageDraw.Draw(a).text((size // 2, size // 2), ch, font=f, fill=255)
    ImageDraw.Draw(b).text((size // 2, size // 2), "", font=f, fill=255)
    return a.tobytes() != b.tobytes() and a.getbbox() is not None


# --- helpers ------------------------------------------------------------------
def p(v):
    return int(round(v * S))


def P(seq):
    """Scale a box [x0,y0,x1,y1] or a list of (x,y) points to supersampled px."""
    if seq and isinstance(seq[0], (tuple, list)):
        return [(p(x), p(y)) for x, y in seq]
    return [p(v) for v in seq]


def rgba(hex_colour, a=255):
    h = hex_colour.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


class Art:
    def __init__(self, bg, size=(W, H)):
        self.img = Image.new("RGBA", (p(size[0]), p(size[1])), rgba(bg))
        self.d = ImageDraw.Draw(self.img)

    def layer(self):
        lay = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        return lay, ImageDraw.Draw(lay)

    def merge(self, lay):
        self.img = Image.alpha_composite(self.img, lay)
        self.d = ImageDraw.Draw(self.img)

    def final(self):
        w, h = self.img.size
        return self.img.resize((w // S, h // S), Image.LANCZOS).convert("RGB")


def jamo_glyph(d, cx, cy, ch, size, fill):
    """Draw one jamo centred at (cx, cy) in 1280x720 coordinates.
    Falls back to a simple shape if the KR font lacks the glyph (obsolete letters)."""
    if has_glyph(KR_FONT, ch):
        d.text((p(cx), p(cy)), ch, font=font(KR_FONT, p(size)), fill=fill, anchor="mm")
        return
    r = size * 0.32
    lw = p(max(4, size * 0.09))
    if ch == "ㆁ":    # yesieung: circle with a short stem
        d.ellipse(P([cx - r, cy - r + 6, cx + r, cy + r + 6]), outline=fill, width=lw)
        d.line(P([(cx, cy - r - 6), (cx, cy - r + 8)]), fill=fill, width=lw)
    elif ch == "ㅿ":  # pansios: triangle
        d.polygon(P([(cx, cy - r), (cx - r, cy + r), (cx + r, cy + r)]), outline=fill, width=lw)
    elif ch == "ㆆ":  # yeorinhieuh: bar over a circle
        d.line(P([(cx - r, cy - r), (cx + r, cy - r)]), fill=fill, width=lw)
        d.ellipse(P([cx - r * 0.8, cy - r * 0.5, cx + r * 0.8, cy + r]), outline=fill, width=lw)
    else:                 # araea: dot
        d.ellipse(P([cx - size * 0.1, cy - size * 0.1, cx + size * 0.1, cy + size * 0.1]), fill=fill)


# --- generic objects (no readable text, no brands) ----------------------------
def stone_wall(art, x0, y0, x1, y1, rows=6, seed=2):
    rnd = random.Random(seed)
    rh = (y1 - y0) / rows
    d = art.d
    for r in range(rows):
        y = y0 + r * rh
        x = x0 - rnd.uniform(0, 120)
        while x < x1:
            w = rnd.uniform(130, 230)
            fill = rnd.choice([STONE_A, STONE_B, STONE_C])
            d.rounded_rectangle(P([x + 4, y + 4, x + w - 4, y + rh - 4]), radius=p(14),
                                fill=fill, outline=INK, width=p(3))
            x += w
    # lower ground line
    d.rectangle(P([x0, y1 - 10, x1, y1]), fill=INK)


def blurred_jamo_sheet(w, h, cols, rows, seed, tilt, size=30):
    """A paper sheet with unreadable columns of jamo (blurred so no sentence can be read)."""
    rnd = random.Random(seed)
    pad = 60
    sheet = Image.new("RGBA", (p(w + pad * 2), p(h + pad * 2)), (0, 0, 0, 0))
    d = ImageDraw.Draw(sheet)
    d.rectangle(P([pad, pad, pad + w, pad + h]), fill=PAPER, outline=INK, width=p(5))
    txt = Image.new("RGBA", sheet.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(txt)
    cw, ch = (w - 40) / cols, (h - 40) / rows
    for c in range(cols):
        for r in range(rows):
            if rnd.random() < 0.12:
                continue
            jamo_glyph(td, pad + 20 + cw * (c + 0.5), pad + 20 + ch * (r + 0.5),
                       rnd.choice(MODERN_24), size, rgba(INK_SOFT, 200))
    txt = txt.filter(ImageFilter.GaussianBlur(p(3.2)))
    sheet = Image.alpha_composite(sheet, txt)
    # a folded corner (plain paper, no text)
    cd = ImageDraw.Draw(sheet)
    cx, cy = pad + w, pad + h
    cd.polygon(P([(cx - 46, cy), (cx, cy - 46), (cx, cy)]), fill=NIGHT_L)
    cd.polygon(P([(cx - 46, cy), (cx, cy - 46), (cx - 46, cy - 46)]), fill=PAPER_D, outline=INK, width=p(3))
    return sheet.rotate(tilt, resample=Image.BICUBIC, expand=True)


def glow(art, cx, cy, rx, ry, colour, alpha=70, blur=60):
    lay, ld = art.layer()
    ld.ellipse(P([cx - rx, cy - ry, cx + rx, cy + ry]), fill=rgba(colour, alpha))
    lay = lay.filter(ImageFilter.GaussianBlur(p(blur)))
    art.merge(lay)


def open_book(art, cx, base, w, h):
    """Open old book, kraft cover, cream pages, blurred unreadable jamo lines."""
    d = art.d
    x0, x1 = cx - w / 2, cx + w / 2
    top = base - h
    d.rounded_rectangle(P([x0 - 12, top - 6, x1 + 12, base + 10]), radius=p(10), fill=KRAFT, outline=INK, width=p(5))
    d.polygon(P([(x0, top + 10), (cx, top + 22), (cx, base), (x0, base - 8)]), fill=PAPER, outline=INK)
    d.polygon(P([(cx, top + 22), (x1, top + 10), (x1, base - 8), (cx, base)]), fill=PAPER, outline=INK)
    d.line(P([(cx, top + 22), (cx, base)]), fill=INK, width=p(4))
    lay, ld = art.layer()
    rnd = random.Random(7)
    for page_x0, page_x1 in ((x0 + 22, cx - 18), (cx + 18, x1 - 22)):
        cols = 4
        cw = (page_x1 - page_x0) / cols
        for c in range(cols):
            for r in range(5):
                if rnd.random() < 0.15:
                    continue
                jamo_glyph(ld, page_x0 + cw * (c + 0.5), top + 46 + r * ((h - 70) / 5),
                           rnd.choice(MODERN_24), 20, rgba(INK_SOFT, 210))
    lay = lay.filter(ImageFilter.GaussianBlur(p(2.2)))
    art.merge(lay)


def calendar_page(art, x0, y0, x1, y1, mark_col, mark_row, numeral="9"):
    """Plain calendar page: red header band, 7x5 empty grid, one large numeral with a red ring."""
    d = art.d
    d.rounded_rectangle(P([x0, y0, x1, y1]), radius=p(18), fill=WHITE, outline=INK, width=p(5))
    head_h = 86
    d.rounded_rectangle(P([x0, y0, x1, y0 + head_h + 18]), radius=p(18), fill=RED, outline=INK, width=p(5))
    d.rectangle(P([x0 + 3, y0 + head_h, x1 - 3, y0 + head_h + 18]), fill=RED)
    d.line(P([(x0, y0 + head_h + 18), (x1, y0 + head_h + 18)]), fill=INK, width=p(5))
    for hx in (x0 + (x1 - x0) * 0.3, x0 + (x1 - x0) * 0.7):
        d.ellipse(P([hx - 16, y0 + 22, hx + 16, y0 + 54]), fill=NIGHT, outline=INK, width=p(3))
        d.rounded_rectangle(P([hx - 7, y0 - 34, hx + 7, y0 + 38]), radius=p(7), fill=STEEL, outline=INK, width=p(3))
    gy0 = y0 + head_h + 18
    cols, rows = 7, 5
    cw, ch = (x1 - x0) / cols, (y1 - gy0) / rows
    for c in range(1, cols):
        d.line(P([(x0 + c * cw, gy0), (x0 + c * cw, y1)]), fill=PAPER_D, width=p(2))
    for r in range(1, rows):
        d.line(P([(x0, gy0 + r * ch), (x1, gy0 + r * ch)]), fill=PAPER_D, width=p(2))
    # small grey dots stand in for the other dates (no readable numbers)
    for c in range(cols):
        for r in range(rows):
            if (c, r) == (mark_col, mark_row):
                continue
            cx, cy = x0 + cw * (c + 0.5), gy0 + ch * (r + 0.5)
            d.ellipse(P([cx - 5, cy - 5, cx + 5, cy + 5]), fill=STEEL)
    # the marked day: large numeral plus one hand-drawn red ring
    cx, cy = x0 + cw * (mark_col + 0.5), gy0 + ch * (mark_row + 0.5)
    f = font(EN_HEAD, p(118))
    d.text((p(cx), p(cy + 4)), numeral, font=f, fill=INK, anchor="mm")
    for k in range(3):
        d.ellipse(P([cx - 72 - k * 2, cy - 68 + k * 3, cx + 74 + k * 2, cy + 70 - k * 2]), outline=RED, width=p(7))


# --- type -----------------------------------------------------------------------
def fit_size(text, max_w, max_size, min_size=40):
    size = max_size
    while size > min_size:
        if font(EN_HEAD, p(size)).getlength(text) <= p(max_w):
            break
        size -= 2
    return size


def headline(art, x, top, lines, col_w, gap=14, stroke=0, bar=True):
    """lines: list of (text, colour, max_size, block_colour or None). Returns (bottom, max_width)."""
    d = art.d
    y = top
    widest = 0
    for text, colour, max_size, block in lines:
        size = fit_size(text, col_w - (36 if block else 0), max_size)
        f = font(EN_HEAD, p(size))
        cap = -f.getbbox("H", anchor="ls")[1] / S
        tw = f.getlength(text) / S
        tx = x + (18 if block else 0)
        if block:
            d.rounded_rectangle(P([x, y - 14, x + tw + 36, y + cap + 14]), radius=p(10), fill=block)
            widest = max(widest, tw + 36)
        else:
            widest = max(widest, tw)
        d.text((p(tx), p(y + cap)), text, font=f, fill=colour, anchor="ls",
               stroke_width=p(stroke), stroke_fill=INK)
        y += cap + gap + (28 if block else 0)
    if bar:
        d.rectangle(P([x, y + 4, x + widest, y + 18]), fill=YELLOW, outline=INK, width=p(2))
        y += 18
    return y, widest


def mockup_tag(art):
    f = font(EN_HEAD, p(17))
    text = "MOCKUP"
    tw = f.getlength(text) / S
    x1, y1 = W - 14, H - 12
    x0, y0 = x1 - tw - 16, y1 - 26
    lay, ld = art.layer()
    ld.rounded_rectangle(P([x0, y0, x1, y1]), radius=p(6), fill=rgba(INK, 150))
    ld.text((p(x0 + 8), p(y1 - 7)), text, font=f, fill=rgba(WHITE, 230), anchor="ls")
    art.merge(lay)


# --- thumbnails -------------------------------------------------------------
def thumb1():
    """1안: 벽 위의 세 장. Night stone wall, three sheets with blurred jamo. Text: WHO WROTE THESE?"""
    art = Art(NIGHT)
    stone_wall(art, 0, 0, W, H)
    # dim the left 45% so white headline sits on a calm field (per design-system §3)
    lay, ld = art.layer()
    ld.rectangle(P([0, 0, 640, H]), fill=rgba(NIGHT, 165))
    lay = lay.filter(ImageFilter.GaussianBlur(p(40)))
    art.merge(lay)
    # lantern light from upper right, warm but low
    glow(art, 1010, 90, 380, 220, YELLOW, alpha=55, blur=70)
    # three sheets, the focal object (right 55%, about 35% of the frame)
    # paste positions include the 60px transparent pad of each sheet image
    sheets = [
        (blurred_jamo_sheet(280, 360, 4, 9, 11, 5), 586, 48),
        (blurred_jamo_sheet(280, 360, 4, 9, 12, -4), 852, 36),
        (blurred_jamo_sheet(240, 300, 3, 8, 13, 7), 696, 262),
    ]
    for sh, x, y in sheets:
        shadow = Image.new("RGBA", sh.size, (0, 0, 0, 0))
        shadow.paste(rgba(INK, 140), (0, 0), sh.split()[3])
        shadow = shadow.filter(ImageFilter.GaussianBlur(p(8)))
        lay, _ = art.layer()
        lay.paste(shadow, (p(x) + p(10), p(y) + p(14)), shadow)
        art.merge(lay)
        lay, _ = art.layer()
        lay.paste(sh, (p(x), p(y)), sh)
        art.merge(lay)
    headline(art, SAFE, 150, [
        ("WHO", WHITE, 150, None),
        ("WROTE", WHITE, 150, None),
        ("THESE?", WHITE, 130, RED),
    ], col_w=540, stroke=6)
    mockup_tag(art)
    return art.final()


def thumb2():
    """2안: 사라진 네 글자. 28-letter grid, 24 white and 4 grey with red rings. Text: 4 LETTERS VANISHED"""
    art = Art(NIGHT)
    # faint jamo texture in the far background
    lay, ld = art.layer()
    rnd = random.Random(5)
    for i in range(40):
        jamo_glyph(ld, rnd.uniform(0, W), rnd.uniform(0, H), rnd.choice(MODERN_24), 90, rgba(NIGHT_L, 255))
    lay = lay.filter(ImageFilter.GaussianBlur(p(1.5)))
    art.merge(lay)
    # grid, right 55%
    cols, rows, cell = 7, 4, 92
    gx0, gy0 = 572, 160   # 572 + 7*92 = 1216 = right safe line
    d = art.d
    for i, ch in enumerate(JAMO_28):
        c, r = i % cols, i // cols
        x0, y0 = gx0 + c * cell, gy0 + r * cell
        cx, cy = x0 + cell / 2, y0 + cell / 2
        obsolete = ch in OBSOLETE
        d.rounded_rectangle(P([x0 + 4, y0 + 4, x0 + cell - 4, y0 + cell - 4]), radius=p(10),
                            fill=STONE_A if not obsolete else NIGHT, outline=INK, width=p(2))
        if obsolete:
            d.rounded_rectangle(P([x0 + 4, y0 + 4, x0 + cell - 4, y0 + cell - 4]), radius=p(10),
                                outline=RED, width=p(6))
        jamo_glyph(d, cx, cy, ch, 60 if ch != "ㆍ" else 150, GREY if obsolete else WHITE)
    headline(art, SAFE, 120, [
        ("4", YELLOW, 230, None),
        ("LETTERS", WHITE, 120, None),
        ("VANISHED", WHITE, 110, RED),
    ], col_w=500)
    mockup_tag(art)
    return art.final()


def thumb3():
    """3안: 10월 9일. Paper background, calendar page with one marked day, open old book. Text: WHY OCTOBER 9?"""
    art = Art(PAPER)
    # soft paper grain: faint jamo at very low contrast
    lay, ld = art.layer()
    rnd = random.Random(9)
    for i in range(30):
        jamo_glyph(ld, rnd.uniform(0, W), rnd.uniform(0, H), rnd.choice(MODERN_24), 110, rgba(PAPER_D, 255))
    lay = lay.filter(ImageFilter.GaussianBlur(p(1.5)))
    art.merge(lay)
    # calendar page, right 55%, ends above the bottom-right badge zone
    calendar_page(art, 690, 100, 1200, 600, mark_col=4, mark_row=1, numeral="9")  # ring tops at y 66, bottom above badge zone
    # open book, lower left under the headline
    open_book(art, 330, 640, 420, 150)
    headline(art, SAFE, 110, [
        ("WHY", INK, 150, None),
        ("OCTOBER 9?", WHITE, 120, RED),
    ], col_w=600)
    mockup_tag(art)
    return art.final()


LABELS = ["벽 위의 세 장", "사라진 네 글자", "10월 9일"]


def compare(thumbs, out):
    gap, tw = 12, 624
    th = round(tw * 9 / 16)
    band = 74
    cw = gap * 4 + tw * 3
    ch = gap + th + band + gap // 2
    sheet = Image.new("RGB", (cw, ch), "#E6E1D6")
    d = ImageDraw.Draw(sheet)
    fnum = ImageFont.truetype(EN_HEAD, 40)
    flab = ImageFont.truetype(KR_FONT, 36, index=0)
    for i, im in enumerate(thumbs):
        x = gap + i * (tw + gap)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, gap))
        d.rectangle([x - 1, gap - 1, x + tw, gap + th], outline=INK, width=2)
        cy = gap + th + band // 2
        d.ellipse([x, cy - 28, x + 56, cy + 28], fill=RED, outline=INK, width=2)
        d.text((x + 28, cy + 2), str(i + 1), font=fnum, fill=WHITE, anchor="mm")
        d.text((x + 72, cy + 2), LABELS[i], font=flab, fill=INK, anchor="lm")
    sheet = sheet.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    sheet.save(out, optimize=True)
    return cw, ch


def save_png(im, path):
    im.save(path, optimize=True)
    if os.path.getsize(path) > 500 * 1024:
        im.quantize(colors=256, method=Image.Quantize.MEDIANCUT,
                    dither=Image.Dither.FLOYDSTEINBERG).save(path, optimize=True)


def guides(im, n, outdir):
    g = im.copy()
    d = ImageDraw.Draw(g)
    d.rectangle([SAFE, SAFE, W - SAFE, H - SAFE], outline="#00C2FF", width=2)
    d.rectangle(list(BR_ZONE), outline="#FF3B3B", width=3)
    g.save(os.path.join(outdir, "thumb-%d-guides.png" % n))
    for wpx in (320, 168):
        im.resize((wpx, round(wpx * 9 / 16)), Image.LANCZOS).save(
            os.path.join(outdir, "thumb-%d-%dpx.png" % (n, wpx)))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--guides", metavar="DIR", help="write guide overlays and feed-size previews here")
    ap.add_argument("--compare-only", action="store_true",
                    help="rebuild thumbs-compare.png from existing thumb-1..3.png (e.g. final art)")
    args = ap.parse_args()
    if args.compare_only:
        thumbs = [Image.open(os.path.join(HERE, "thumb-%d.png" % i)).convert("RGB").resize((W, H), Image.LANCZOS)
                  for i in (1, 2, 3)]
    else:
        thumbs = [thumb1(), thumb2(), thumb3()]
    for i, im in enumerate([] if args.compare_only else thumbs, 1):
        path = os.path.join(HERE, "thumb-%d.png" % i)
        save_png(im, path)
        print("%s %dx%d %.0fKB" % (path, im.width, im.height, os.path.getsize(path) / 1024))
        if args.guides:
            os.makedirs(args.guides, exist_ok=True)
            guides(im, i, args.guides)
    out = os.path.join(HERE, "thumbs-compare.png")
    cw, ch = compare(thumbs, out)
    print("%s %dx%d %.0fKB" % (out, cw, ch, os.path.getsize(out) / 1024))
    print("fonts: headline=%s kr=%s" % (EN_HEAD, KR_FONT))
    print("obsolete jamo glyphs in kr font: %s" % {ch: has_glyph(KR_FONT, ch) for ch in sorted(OBSOLETE)})


if __name__ == "__main__":
    main()
