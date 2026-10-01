#!/usr/bin/env python3
"""EP001 thumbnail layout mockups. Pillow only, no image-generation API.

These are LAYOUT MOCKUPS (colour, type, composition), not final art.
Final plates come from the prompts in thumbnails.md; type is added in post.

Usage:
    python3 episodes/EP001/design/make_thumbs.py            # writes PNGs next to this file
    python3 episodes/EP001/design/make_thumbs.py --guides DIR  # also writes guide overlays + feed-size previews to DIR
    python3 episodes/EP001/design/make_thumbs.py --compare-only  # rebuild thumbs-compare.png from existing thumb-1..3.png

Outputs: thumb-1.png, thumb-2.png, thumb-3.png (1280x720), thumbs-compare.png (1920 wide)
Tokens and rules: design-system.md (same folder).
"""
import argparse
import functools
import math
import os
import subprocess

from PIL import Image, ImageChops, ImageDraw, ImageFont

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
# illustration-only support colours
NOODLE = "#F2D49B"
BROTH = "#E0662A"
STEEL = "#C9CDD2"
KRAFT = "#C9A877"
# shades derived for illustration volume (not brand tokens)
YELLOW_D = "#E3B21F"
YELLOW_L = "#FFE68A"
NOODLE_D = "#C99A4E"
NIGHT_L = "#2A3040"
STEAM_ON_LIGHT = "#9AA3B5"  # steam on paper/light frames

SAFE = 64                          # outer safe margin (px at 1280x720)
BR_ZONE = (1040, 620, 1280, 720)   # bottom-right duration badge zone, keep empty


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
KR_LABEL = find_font(["Black Han Sans", "Pretendard"], [
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
])


@functools.lru_cache(maxsize=None)
def font(path, size):
    return ImageFont.truetype(path, size, index=0)


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

    def paste_rgba(self, im, x, y):
        lay = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        lay.paste(im, (p(x), p(y)), im)
        self.merge(lay)

    def final(self):
        w, h = self.img.size
        return self.img.resize((w // S, h // S), Image.LANCZOS).convert("RGB")


# --- generic objects (unbranded, no text) ------------------------------------
def steam(d, x, y0, height, amp=14, width=10, phase=0.0, alpha=120, colour=WHITE):
    n = 36
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append((x + amp * math.sin(phase + t * math.pi * 3) * (0.4 + 0.6 * t), y0 - t * height))
    for i in range(n):
        a = int(alpha * (1 - i / n) ** 1.2)
        d.line(P([pts[i], pts[i + 1]]), fill=rgba(colour, a), width=p(width))
        r = width / 2
        x1, y1 = pts[i + 1]
        d.ellipse(P([x1 - r, y1 - r, x1 + r, y1 + r]), fill=rgba(colour, a))


def steam_plume(art, cx, y0, height, spread, n=3, width=10, alpha=120, colour=WHITE):
    lay, ld = art.layer()
    for k in range(n):
        off = (k - (n - 1) / 2) * spread
        steam(ld, cx + off, y0, height * (0.85 + 0.15 * ((k + 1) % 2)), width=width,
              phase=k * 1.7, alpha=alpha, colour=colour)
    art.merge(lay)


def noodle_waves(art, box, rows=4, width=5):
    """Wavy noodles clipped to an ellipse (the pot or bowl opening)."""
    x0, y0, x1, y1 = box
    lay, ld = art.layer()
    h = y1 - y0
    for r in range(rows + 1):
        y = y0 + (r + 0.3) * h / rows
        pts = [(x, y + 0.18 * h * math.sin((x - x0) / 14.0 + r)) for x in range(int(x0) - 10, int(x1) + 12, 4)]
        ld.line(P(pts), fill=NOODLE_D, width=p(width + 3), joint="curve")
        ld.line(P(pts), fill=NOODLE, width=p(width), joint="curve")
    mask = Image.new("L", art.img.size, 0)
    ImageDraw.Draw(mask).ellipse(P(box), fill=255)
    a = ImageChops.multiply(lay.getchannel("A"), mask)
    lay.putalpha(a)
    art.merge(lay)


def pot(art, cx, rim_y, w, depth, line=5, shadow=True):
    """Plain yellow aluminium ramyeon pot (yangeun-style), no embossing or marks."""
    hw, bw = w / 2, w * 0.42
    base = rim_y + depth
    rh = w * 0.2
    if shadow:
        lay, ld = art.layer()
        ld.ellipse(P([cx - hw * 1.08, base - 12, cx + hw * 1.08, base + 20]), fill=rgba(INK, 110))
        art.merge(lay)
    d = art.d
    for side in (-1, 1):
        hx = cx + side * (hw - 4)
        box = [min(hx, hx + side * w * 0.17), rim_y + 2, max(hx, hx + side * w * 0.17), rim_y + w * 0.065]
        d.rounded_rectangle(P(box), radius=p(6), fill=YELLOW_D, outline=INK, width=p(line - 1))
    d.polygon(P([(cx - hw, rim_y), (cx + hw, rim_y), (cx + bw, base), (cx - bw, base)]), fill=YELLOW)
    d.ellipse(P([cx - bw, base - w * 0.05, cx + bw, base + w * 0.05]), fill=YELLOW)
    d.polygon(P([(cx - hw * 0.74, rim_y + 8), (cx - hw * 0.58, rim_y + 8),
                 (cx - bw * 0.66, base - 4), (cx - bw * 0.8, base - 4)]), fill=YELLOW_L)
    d.line(P([(cx - hw, rim_y), (cx - bw, base)]), fill=INK, width=p(line))
    d.line(P([(cx + hw, rim_y), (cx + bw, base)]), fill=INK, width=p(line))
    d.arc(P([cx - bw, base - w * 0.05, cx + bw, base + w * 0.05]), 0, 180, fill=INK, width=p(line))
    d.ellipse(P([cx - hw - 5, rim_y - rh / 2, cx + hw + 5, rim_y + rh / 2]), fill=YELLOW_D,
              outline=INK, width=p(line))
    inner = [cx - hw + 9, rim_y - rh / 2 + 7, cx + hw - 9, rim_y + rh / 2 - 5]
    art.d.ellipse(P(inner), fill=BROTH)
    noodle_waves(art, inner, rows=4, width=max(3, w / 70))
    art.d.ellipse(P(inner), outline=INK, width=p(max(2, line - 2)))
    return base


def chopstick(d, x1, y1, x2, y2, w1=10, w2=5, fill=STEEL, line=3):
    ang = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(ang), math.cos(ang)
    poly = [(x1 + nx * w1 / 2, y1 + ny * w1 / 2), (x2 + nx * w2 / 2, y2 + ny * w2 / 2),
            (x2 - nx * w2 / 2, y2 - ny * w2 / 2), (x1 - nx * w1 / 2, y1 - ny * w1 / 2)]
    d.polygon(P(poly), fill=fill, outline=INK, width=p(line))


def strand(d, pts, width=7):
    d.line(P(pts), fill=INK, width=p(width + 5), joint="curve")
    d.line(P(pts), fill=NOODLE, width=p(width), joint="curve")


def bowl(d, cx, top, w, h, fill=PAPER, inside="#3B2A1E", line=4):
    d.chord(P([cx - w / 2, top - h, cx + w / 2, top + h]), 0, 180, fill=fill, outline=INK, width=p(line))
    d.ellipse(P([cx - w / 2, top - h * 0.22, cx + w / 2, top + h * 0.22]), fill=inside, outline=INK, width=p(line))


def cup(d, cx, base, w, h, line=4):
    """Plain unprinted cup with a peeled lid."""
    tw, bw = w / 2, w * 0.36
    top = base - h
    d.polygon(P([(cx - tw, top), (cx + tw, top), (cx + bw, base), (cx - bw, base)]), fill=WHITE,
              outline=INK, width=p(line))
    band_t, band_b = top + h * 0.38, top + h * 0.62
    lt, lb = tw - (tw - bw) * 0.38, tw - (tw - bw) * 0.62
    d.polygon(P([(cx - lt, band_t), (cx + lt, band_t), (cx + lb, band_b), (cx - lb, band_b)]), fill=KRAFT,
              outline=INK, width=p(line - 2))
    d.ellipse(P([cx - tw, top - w * 0.12, cx + tw, top + w * 0.12]), fill=PAPER, outline=INK, width=p(line))
    d.polygon(P([(cx - tw * 0.2, top - w * 0.08), (cx + tw * 0.95, top - w * 0.05),
                 (cx + tw * 0.7, top - w * 0.55), (cx - tw * 0.1, top - w * 0.35)]),
              fill="#E9E4D8", outline=INK, width=p(line - 1))


def packet(d, x0, y0, w, h, fill, line=4):
    """Plain pillow pack with crimped ends and no print."""
    d.rounded_rectangle(P([x0, y0 + 8, x0 + w, y0 + h - 8]), radius=p(10), fill=fill, outline=INK, width=p(line))
    for yy, sgn in ((y0, 1), (y0 + h, -1)):
        teeth = []
        n = 9
        for i in range(n + 1):
            teeth.append((x0 + i * w / n, yy + (0 if i % 2 == 0 else sgn * 8)))
        poly = teeth + [(x0 + w, yy + sgn * 16), (x0, yy + sgn * 16)]
        d.polygon(P(poly), fill=fill, outline=INK, width=p(line - 1))


def clapper(w, h, line=5):
    """Generic film slate, blank (no text, no markings)."""
    pad = 12
    im = Image.new("RGBA", (p(w + 2 * pad), p(h + 2 * pad)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    sh = h * 0.22
    d.rounded_rectangle(P([pad, pad + sh + 4, pad + w, pad + h]), radius=p(10), fill="#2E3443",
                        outline=INK, width=p(line))
    for i in (1, 2):
        y = pad + sh + 4 + i * (h - sh) / 3
        d.line(P([(pad + 18, y), (pad + w - 18, y)]), fill="#46506A", width=p(4))
    stick = Image.new("RGBA", (p(w), p(sh)), rgba(WHITE))
    sd = ImageDraw.Draw(stick)
    step = w / 6
    for i in range(-1, 8):
        x = i * step
        sd.polygon(P([(x, sh), (x + step / 2, sh), (x + step / 2 + sh * 0.7, 0), (x + sh * 0.7, 0)]), fill=rgba(INK))
    im.paste(stick, (p(pad), p(pad)))
    d.rectangle(P([pad, pad, pad + w, pad + sh]), outline=INK, width=p(line))
    return im


def gas_stove(d, x0, y0, x1, y1, line=5):
    """Generic portable tabletop burner, no markings."""
    d.rounded_rectangle(P([x0, y0, x1, y1]), radius=p(10), fill="#3A4152", outline=INK, width=p(line))
    d.line(P([(x0 + 14, y0 + 16), (x1 - 14, y0 + 16)]), fill="#4C5468", width=p(4))
    kx, ky = x1 - 40, (y0 + y1) / 2 + 6
    d.ellipse(P([kx - 16, ky - 16, kx + 16, ky + 16]), fill=STEEL, outline=INK, width=p(3))


def flames(d, cx, y, n=5, spread=26):
    for k in range(n):
        x = cx + (k - (n - 1) / 2) * spread
        d.polygon(P([(x - 7, y), (x + 7, y), (x, y - 18)]), fill="#5AA9E6", outline="#2F6FA8", width=p(2))


# --- type -------------------------------------------------------------------
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
    """Concept 1: ramyeon as the star prop, under a spotlight with a blank film slate."""
    art = Art(NIGHT)
    lay, ld = art.layer()
    ld.polygon(P([(760, 0), (960, 0), (1190, 640), (540, 640)]), fill=rgba(WHITE, 20))
    ld.ellipse(P([520, 545, 1210, 700]), fill=rgba(WHITE, 26))
    art.merge(lay)
    art.paste_rgba(clapper(230, 180).rotate(-11, resample=Image.BICUBIC, expand=True), 945, 290)
    pot(art, 840, 410, 360, 170)
    d = art.d
    tip = (875, 270)
    for k in range(5):
        x0 = tip[0] - 16 + k * 8
        pts = [(x0 + 8 * math.sin(t / 9 + k), tip[1] + t) for t in range(0, 141, 6)]
        strand(d, pts, width=6)
    chopstick(d, 1060, 120, tip[0] - 10, tip[1] + 6, w1=13, w2=7)
    chopstick(d, 1085, 140, tip[0] + 14, tip[1] + 10, w1=13, w2=7)
    steam_plume(art, 840, 380, 280, 120, n=3, width=12, alpha=110)
    headline(art, SAFE, 120, [
        ("KOREA'S", WHITE, 110, None),
        ("FAVORITE", YELLOW, 120, None),
        ("PROP", YELLOW, 200, None),
    ], col_w=540, gap=22, stroke=0)
    mockup_tag(art)
    return art.final()


def thumb2():
    """Concept 2: the 2001 invitation line, a night kitchen set for two, no people."""
    art = Art(NIGHT)
    d = art.d
    d.rectangle(P([0, 545, W, H]), fill=NIGHT_L)
    d.line(P([(0, 545), (W, 545)]), fill=INK, width=p(5))
    # door ajar with warm light
    d.rectangle(P([1092, 70, 1250, 545]), fill="#141720", outline=INK, width=p(5))
    d.polygon(P([(1110, 82), (1150, 92), (1150, 545), (1110, 545)]), fill=YELLOW)
    lay, ld = art.layer()
    ld.polygon(P([(1110, 545), (1150, 545), (1060, H), (700, H)]), fill=rgba(YELLOW, 55))
    ld.polygon(P([(1100, 70), (1160, 70), (1160, 545), (1100, 545)]), fill=rgba(YELLOW, 40))
    art.merge(lay)
    d = art.d
    d.polygon(P([(1150, 92), (1238, 78), (1238, 545), (1150, 545)]), fill="#232838", outline=INK, width=p(4))
    # stove + pot + steam
    gas_stove(d, 760, 470, 1060, 548)
    flames(d, 910, 470)
    pot(art, 910, 370, 300, 100, shadow=False)
    steam_plume(art, 910, 345, 250, 95, n=3, width=11, alpha=115)
    d = art.d
    # two bowls, two pairs of chopsticks
    for cx in (520, 668):
        bowl(d, cx, 580, 124, 44, inside="#E9E4D8")
        chopstick(d, cx - 60, 560, cx + 62, 548, w1=7, w2=5)
        chopstick(d, cx - 58, 568, cx + 64, 558, w1=7, w2=5)
    headline(art, SAFE, 92, [
        ("WANT", WHITE, 120, None),
        ("SOME", WHITE, 120, None),
        ("RAMYEON?", WHITE, 120, RED),
    ], col_w=600, gap=18, stroke=0)
    mockup_tag(art)
    return art.final()


def film_strip():
    sw, sh = 1420, 250
    im = Image.new("RGBA", (p(sw), p(sh)), (0, 0, 0, 0))
    a = Art.__new__(Art)
    a.img, a.d = im, ImageDraw.Draw(im)
    d = a.d
    d.rounded_rectangle(P([0, 0, sw, sh]), radius=p(8), fill=INK)
    for x in range(14, sw - 20, 44):
        for y in (12, sh - 32):
            d.rounded_rectangle(P([x, y, x + 24, y + 20]), radius=p(4), fill=PAPER)
    frames = [(110, 480), (510, 880), (910, 1280)]
    for x0, x1 in frames:
        d.rectangle(P([x0, 46, x1, sh - 46]), fill="#FBF8F1")
    # frame 1: pot + two pairs of chopsticks (the invitation)
    pot(a, 255, 120, 150, 58, line=4, shadow=False)
    steam_plume(a, 255, 104, 60, 40, n=2, width=7, alpha=200, colour=STEAM_ON_LIGHT)
    d = a.d
    for k, dx in enumerate((0, 34)):
        chopstick(d, 368 + dx, 70, 398 + dx, 192, w1=10, w2=6, line=2)
        chopstick(d, 384 + dx, 68, 408 + dx, 190, w1=10, w2=6, line=2)
    # frame 2: two plain packets combine (ram-don)
    packet(d, 560, 64, 112, 120, KRAFT)
    packet(d, 718, 64, 112, 120, WHITE)
    # plus sign in yellow + ink (a red cross on white could read as the protected Red Cross emblem)
    d.polygon(P([(687, 104), (703, 104), (703, 120), (719, 120), (719, 136), (703, 136), (703, 152),
                 (687, 152), (687, 136), (671, 136), (671, 120), (687, 120)]), fill=YELLOW, outline=INK, width=p(3))
    # frame 3: three plain cups (animated film)
    for cx in (995, 1095, 1195):
        cup(d, cx, 192, 78, 82)
    lay, ld = a.layer()
    for cx in (995, 1095, 1195):
        steam(ld, cx, 84, 40, amp=6, width=6, phase=cx, alpha=200, colour=STEAM_ON_LIGHT)
    a.merge(lay)
    d = a.d
    # one noodle running through all three frames
    pts = [(x, sh - 24 + 12 * math.sin(x / 38.0)) for x in range(-10, sw + 12, 6)]
    strand(d, pts, width=9)
    return a.img


def thumb3():
    """Concept 3: three films, one noodle. Film strip on paper."""
    art = Art(PAPER)
    strip = film_strip().rotate(7, resample=Image.BICUBIC, expand=True)
    sw, sh = strip.size[0] / S, strip.size[1] / S
    art.paste_rgba(strip, 660 - sw / 2, 528 - sh / 2)
    headline(art, SAFE, 52, [
        ("3 FILMS,", INK, 150, None),
        ("1 NOODLE", RED, 150, None),
    ], col_w=680, gap=34, stroke=0)
    mockup_tag(art)
    return art.final()


# --- compare sheet + checks -------------------------------------------------
LABELS = ["주연 소품", "밤의 초대", "필름 3컷, 면 한 가닥"]


def compare(thumbs, out):
    gap, tw = 12, 624
    th = round(tw * 9 / 16)
    band = 74
    cw = gap * 4 + tw * 3
    ch = gap + th + band + gap // 2
    sheet = Image.new("RGB", (cw, ch), "#E6E1D6")
    d = ImageDraw.Draw(sheet)
    fnum = ImageFont.truetype(EN_HEAD, 40)
    flab = ImageFont.truetype(KR_LABEL, 36, index=0)
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
    print("fonts: headline=%s label=%s" % (EN_HEAD, KR_LABEL))


if __name__ == "__main__":
    main()
