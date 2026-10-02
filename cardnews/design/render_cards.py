#!/usr/bin/env python3
"""KE Studio 카드뉴스(인스타 4:5) 목업 렌더러.

사용:
  python3 render_cards.py <post_dir>          # <post_dir>/cards.json -> card-NN.png + contact.png
  python3 render_cards.py --all cardnews/posts  # 날짜 폴더 전부

규격: cardnews/design/template.md. 디자인 토큰은 EP001 design-system.md v1.0 §1~§3·§6을 그대로 쓴다.
목업 전용: 우하단 "MOCKUP" 표기. 모티프는 글자 없는 플랫 도형만 그린다(인물·로고·IP·스틸 없음).
레이어: 배경(paper+한지 결) -> 플레이트(모티프, <post_dir>/plates/card-NN.png 있으면 교체) -> 텍스트 -> MOCKUP.
"""
import argparse
import glob
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------- 토큰 (design-system.md §1, 값 변경 금지) ----------
TOKENS = {
    "red": "#C8102E",
    "yellow": "#FFD23F",
    "ink": "#111111",
    "paper": "#F7F3EA",
    "night": "#1B1F2A",
    "white": "#FFFFFF",
    "kraft": "#C9A877",   # 일러스트 보조(면적 15% 이하)
    "celadon": "#6FA89B",  # 일러스트 보조
    "wheat": "#F2D49B",    # 일러스트 보조
}
W, H = 1080, 1350
MARGIN = 72                      # 안전 영역(사방)
GRID_TOP, GRID_BOTTOM = 135, 1215  # 프로필 1:1 크롭 범위(헤드라인은 이 안에)
HANDLE = "@chaekgado.note"
ACCOUNT = "책가도 노트"
MOCKUP_TAG = "MOCKUP"

# 타이포 크기(px). 헤드라인 >=72, 본문 >=40 (폰 가독)
SIZE = {
    "cover_head": 128, "cover_sub": 44, "cover_handle": 40,
    "body_head": 88, "body_text": 44, "body_num": 40,
    "last_cta": 84, "last_src": 40, "last_handle": 40,
    "label": 34, "mockup": 30,
}


# ---------- 폰트 탐색: Black Han Sans / Pretendard 우선, 없으면 WenQuanYi -> Noto CJK -> DejaVu ----------
def _fc_list():
    try:
        out = subprocess.run(["fc-list", ":", "file", "family", "style"],
                             capture_output=True, text=True, timeout=10).stdout
    except Exception:
        return []
    rows = []
    for line in out.splitlines():
        parts = line.split(":")
        if len(parts) >= 2:
            rows.append((parts[0].strip(), parts[1].strip(), ":".join(parts[2:]).strip()))
    return rows


_FC = None


def find_font(candidates):
    """candidates: [(family_substring, style_substring_or_None), ...] -> (path, index) or None"""
    global _FC
    if _FC is None:
        _FC = _fc_list()
    for fam, style in candidates:
        for path, family, st in _FC:
            st_l = st.lower()
            if fam.lower() in family.lower() and (style is None or (style.lower() in st_l and "italic" not in st_l)):
                return path
        # fc-list가 없을 때 흔한 경로 글롭
        for pat in [f"/usr/share/fonts/**/*{fam.replace(' ', '')}*", f"{os.path.expanduser('~')}/.fonts/**/*{fam.replace(' ', '')}*"]:
            hits = sorted(glob.glob(pat, recursive=True))
            if hits:
                return hits[0]
    return None


def load_fonts():
    head_path = find_font([("Black Han Sans", None), ("Pretendard", "Black"), ("Pretendard", "Bold"),
                           ("WenQuanYi Zen Hei", None), ("Noto Sans CJK KR", "Bold"), ("Noto Sans CJK", None)])
    body_path = find_font([("Pretendard", "Regular"), ("Pretendard", None),
                           ("WenQuanYi Zen Hei", None), ("Noto Sans CJK KR", None), ("Noto Sans CJK", None)])
    latin_path = find_font([("Liberation Sans", "Bold"), ("DejaVu Sans", "Bold")])
    if head_path is None:
        head_path = latin_path or "DejaVuSans.ttf"
    if body_path is None:
        body_path = head_path
    fake_bold = "BlackHanSans" not in head_path.replace(" ", "") and "Pretendard" not in head_path
    return {"head": head_path, "body": body_path, "latin": latin_path or head_path, "fake_bold": fake_bold}


_FONT_CACHE = {}


def font(path, size):
    key = (path, size)
    if key not in _FONT_CACHE:
        try:
            _FONT_CACHE[key] = ImageFont.truetype(path, size)
        except Exception:
            _FONT_CACHE[key] = ImageFont.load_default(size)
    return _FONT_CACHE[key]


# ---------- 텍스트 유틸 ----------
def text_w(draw, s, f):
    l, t, r, b = draw.textbbox((0, 0), s, font=f)
    return r - l


def wrap(draw, text, f, maxw):
    """공백 우선, 길면 글자 단위로 줄바꿈. 명시적 \n 유지."""
    lines = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split(" "):
            cand = word if not cur else cur + " " + word
            if text_w(draw, cand, f) <= maxw:
                cur = cand
                continue
            if cur:
                lines.append(cur)
            cur = ""
            for ch in word:
                if text_w(draw, cur + ch, f) <= maxw:
                    cur += ch
                else:
                    lines.append(cur)
                    cur = ch
        lines.append(cur)
    return lines


def draw_lines(draw, lines, f, x, y, fill, line_gap=1.18, stroke=0, anchor_center=False):
    size = f.size
    for ln in lines:
        if anchor_center:
            draw.text((W // 2, y), ln, font=f, fill=fill, anchor="ma", stroke_width=stroke, stroke_fill=fill)
        else:
            draw.text((x, y), ln, font=f, fill=fill, stroke_width=stroke, stroke_fill=fill)
        y += int(size * line_gap)
    return y


# ---------- 배경: paper + 한지 결 ----------
def hanji_background(seed=7):
    bg = Image.new("RGB", (W, H), TOKENS["paper"])
    # 결을 5단계로 포스터라이즈 -> 색 수가 적어 PNG 용량이 작다(장당 ~250KB)
    noise = Image.effect_noise((W, H), 30).filter(ImageFilter.GaussianBlur(1.8))
    fiber = Image.effect_noise((W // 8, H), 60).resize((W, H), Image.BILINEAR)  # 세로 결
    grain = Image.blend(noise, fiber, 0.35).point(lambda v: (v // 52) * 52).convert("RGB")
    return Image.blend(bg, grain, 0.09)


# ---------- 플랫 모티프(글자 없음) ----------
def motif_bookshelf(layer, box, accent):
    """책가도 책장 격자: 칸 + 책 묶음(단색 직사각형)."""
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    cols, rows = 4, 2
    cw, rh = (x1 - x0) / cols, (y1 - y0) / rows
    d.rectangle(box, outline=TOKENS["ink"], width=6)
    for c in range(1, cols):
        d.line([(x0 + c * cw, y0), (x0 + c * cw, y1)], fill=TOKENS["ink"], width=6)
    for r in range(1, rows):
        d.line([(x0, y0 + r * rh), (x1, y0 + r * rh)], fill=TOKENS["ink"], width=6)
    palette = [TOKENS["kraft"], accent, TOKENS["celadon"], TOKENS["wheat"], TOKENS["night"]]
    k = 0
    for r in range(rows):
        for c in range(cols):
            cx0, cy1 = x0 + c * cw + 18, y0 + (r + 1) * rh - 10
            # 눕힌 책 3~4권 쌓기
            n = 3 + (c + r) % 2
            bh = (rh - 40) / 4
            for i in range(n):
                col = palette[(k + i) % len(palette)]
                bw = cw - 36 - (i * 11 % 40)
                d.rectangle([cx0 + (i * 7 % 20), cy1 - (i + 1) * bh, cx0 + bw, cy1 - i * bh - 6],
                            fill=col, outline=TOKENS["ink"], width=4)
            k += 1


def motif_dancheong(layer, box, accent):
    """단청 띠: 반복 사각 + 반원 패턴."""
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    band_h = min(120, y1 - y0)
    yb = y0 + (y1 - y0 - band_h) // 2
    d.rectangle([x0, yb, x1, yb + band_h], fill=TOKENS["night"], outline=TOKENS["ink"], width=6)
    step = 90
    x = x0 + 20
    i = 0
    while x + step <= x1 - 20:
        col = [accent, TOKENS["celadon"], TOKENS["wheat"]][i % 3]
        d.pieslice([x, yb + 14, x + step - 20, yb + band_h - 14 + (step - 20 - band_h + 28)],
                   180, 360, fill=col, outline=TOKENS["ink"], width=3)
        d.rectangle([x + 20, yb + band_h - 38, x + step - 40, yb + band_h - 14], fill=TOKENS["paper"], outline=TOKENS["ink"], width=3)
        x += step
        i += 1


def motif_moon_mountain(layer, box, accent):
    """십장생풍 달·산 실루엣(동물 없음)."""
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    r = (y1 - y0) // 3
    cx = x1 - r - 40
    d.ellipse([cx - r, y0, cx + r, y0 + 2 * r], fill=accent, outline=TOKENS["ink"], width=6)
    wdt = x1 - x0
    peaks = [(x0, y1), (x0 + wdt * 0.18, y0 + (y1 - y0) * 0.45), (x0 + wdt * 0.36, y1 - 60),
             (x0 + wdt * 0.55, y0 + (y1 - y0) * 0.3), (x0 + wdt * 0.78, y1 - 40), (x1, y0 + (y1 - y0) * 0.6), (x1, y1)]
    d.polygon(peaks, fill=TOKENS["night"], outline=TOKENS["ink"])
    peaks2 = [(x0, y1), (x0 + wdt * 0.3, y0 + (y1 - y0) * 0.65), (x0 + wdt * 0.6, y1 - 20),
              (x0 + wdt * 0.85, y0 + (y1 - y0) * 0.72), (x1, y1)]
    d.polygon(peaks2, fill=TOKENS["celadon"], outline=TOKENS["ink"])


def motif_peony(layer, box, accent):
    """모란(민화 꽃) 단순 도형: 원 겹침 + 잎."""
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    R = min(x1 - x0, y1 - y0) // 2 - 10
    for i in range(6):
        import math
        a = math.pi * 2 * i / 6
        px, py = cx + math.cos(a) * R * 0.45, cy + math.sin(a) * R * 0.45
        d.ellipse([px - R * 0.42, py - R * 0.42, px + R * 0.42, py + R * 0.42], fill=accent, outline=TOKENS["ink"], width=5)
    d.ellipse([cx - R * 0.3, cy - R * 0.3, cx + R * 0.3, cy + R * 0.3], fill=TOKENS["yellow"] if accent != TOKENS["yellow"] else TOKENS["red"], outline=TOKENS["ink"], width=5)
    for sx in (-1, 1):
        d.polygon([(cx + sx * R * 0.6, cy + R * 0.7), (cx + sx * R * 1.0, cy + R * 0.95), (cx + sx * R * 0.5, cy + R * 1.0)],
                  fill=TOKENS["celadon"], outline=TOKENS["ink"])


def motif_hanji(layer, box, accent):
    """한지 결: 가로 결 띠 + 작은 사각 도장(글자 없음)."""
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    for i, y in enumerate(range(y0 + 10, y1 - 10, 34)):
        d.line([(x0, y), (x1, y)], fill=TOKENS["kraft"] if i % 2 else TOKENS["wheat"], width=10)
    s = 110
    d.rectangle([x1 - s - 20, y1 - s - 20, x1 - 20, y1 - 20], fill=accent, outline=TOKENS["ink"], width=6)
    d.rectangle([x1 - s + 10, y1 - s + 10, x1 - 50, y1 - 50], outline=TOKENS["paper"], width=6)


BANNED_MOTIF_WORDS = ["호랑이", "까치", "tiger", "magpie", "캐릭터", "로고", "logo", "얼굴", "배우", "아이돌", "드라마", "still"]


def pick_motif(visual: str):
    """visual 문자열 -> (모티프 함수, 경고). 디자인 시스템 §6-3(호랑이·까치 조수 모티프 금지)에 걸리면 달·산으로 대체."""
    v = (visual or "").lower()
    warn = None
    # "로고 금지", "얼굴 없음"처럼 금지·부정 맥락의 언급은 소재가 아니라 제약이므로 매칭에서 뺀다 (COO 2026-10-02)
    import re as _re
    v_pos = " ".join(c for c in _re.split(r"[.,\n]", v) if not _re.search(r"금지|없음|없는|없이|제외|않음", c))
    if any(w in v_pos for w in BANNED_MOTIF_WORDS):
        warn = f"visual '{visual}' 에 금지 소재(인물/로고/IP 또는 호랑이·까치) 포함 -> 달·산 모티프로 대체"
        return motif_moon_mountain, warn
    if any(w in v for w in ["책가도", "책장", "책", "chaekgado", "bookshelf", "book"]):
        return motif_bookshelf, warn
    if any(w in v for w in ["단청", "dancheong", "띠", "처마"]):
        return motif_dancheong, warn
    if any(w in v for w in ["달", "산", "moon", "mountain", "십장생"]):
        return motif_moon_mountain, warn
    if any(w in v for w in ["꽃", "모란", "peony", "화조"]):
        return motif_peony, warn
    if any(w in v for w in ["한지", "hanji", "결", "도장"]):
        return motif_hanji, warn
    return motif_bookshelf, warn


def plate_layer(post_dir, n, visual, box, accent):
    """플레이트 레이어: <post_dir>/plates/card-NN.png 가 있으면 그걸 box에 맞춰 씀(AI 플레이트 교체 지점)."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    custom = os.path.join(post_dir, "plates", f"card-{n:02d}.png")
    warn = None
    if os.path.exists(custom):
        im = Image.open(custom).convert("RGBA")
        bw, bh = box[2] - box[0], box[3] - box[1]
        im = im.resize((bw, bh), Image.LANCZOS)
        layer.paste(im, (box[0], box[1]), im)
        return layer, "custom plate"
    fn, warn = pick_motif(visual)
    fn(layer, box, accent)
    return layer, warn


# ---------- 공통 요소 ----------
def signature_bar(d, x, y, w):
    """design-system §3 시그니처: yellow 14px 바 + ink 2px 테두리."""
    d.rectangle([x, y, x + w, y + 14], fill=TOKENS["yellow"], outline=TOKENS["ink"], width=2)


def mockup_tag(img, fonts):
    d = ImageDraw.Draw(img)
    f = font(fonts["latin"], SIZE["mockup"])
    tw = text_w(d, MOCKUP_TAG, f)
    x, y = W - MARGIN - tw - 24, H - 52 - 24
    d.rounded_rectangle([x - 14, y - 6, x + tw + 14, y + SIZE["mockup"] + 10], radius=8, outline=TOKENS["red"], width=3)
    d.text((x, y), MOCKUP_TAG, font=f, fill=TOKENS["red"])


def handle_line(d, fonts, y, size, fill=TOKENS["ink"], center=False):
    f = font(fonts["body"], size)
    if center:
        d.text((W // 2, y), HANDLE, font=f, fill=fill, anchor="ma")
    else:
        d.text((MARGIN, y), HANDLE, font=f, fill=fill)


def head_stroke(fonts, size=88):
    """Black Han Sans 부재 시 획 두께 보강(목업). 크기 비례, 48px 미만은 1."""
    if not fonts["fake_bold"]:
        return 0
    return max(1, size // 40)


# ---------- 장 유형 1: 표지 ----------
def render_cover(post, card, fonts, post_dir):
    img = hanji_background()
    n = card.get("n", 1)
    # 플레이트: 상단 책가도 격자(배경 장식, 텍스트 뒤)
    box = (MARGIN, 150, W - MARGIN, 560)
    plate, warn = plate_layer(post_dir, n, card.get("visual", "책가도 책장"), box, TOKENS["red"])
    img.paste(plate, (0, 0), plate)
    d = ImageDraw.Draw(img)
    # 상단 라벨: 계정명 + 유형
    f_lab = font(fonts["body"], SIZE["label"])
    d.rounded_rectangle([MARGIN, MARGIN, MARGIN + text_w(d, ACCOUNT, f_lab) + 40, MARGIN + 52], radius=10, fill=TOKENS["ink"])
    d.text((MARGIN + 20, MARGIN + 8), ACCOUNT, font=f_lab, fill=TOKENS["paper"])
    ptype = post.get("type", "")
    if ptype:
        tw = text_w(d, ptype, f_lab)
        d.rounded_rectangle([W - MARGIN - tw - 40, MARGIN, W - MARGIN, MARGIN + 52], radius=10, fill=TOKENS["red"])
        d.text((W - MARGIN - tw - 20, MARGIN + 8), ptype, font=f_lab, fill=TOKENS["white"])
    # 헤드라인 블록(paper 단색 블록 위, 그리드 크롭 안)
    f_h = font(fonts["head"], SIZE["cover_head"])
    lines = wrap(d, card.get("headline", post.get("title", "")), f_h, W - 2 * MARGIN - 80)[:2]  # 표지 헤드라인 2줄 상한
    lh = int(SIZE["cover_head"] * 1.15)
    block_h = lh * len(lines) + 70
    y0 = 600
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + block_h], fill=TOKENS["paper"], outline=TOKENS["ink"], width=6)
    y = y0 + 36
    for ln in lines:
        d.text((MARGIN + 40, y), ln, font=f_h, fill=TOKENS["ink"], stroke_width=head_stroke(fonts, SIZE["cover_head"]), stroke_fill=TOKENS["ink"])
        y += lh
    signature_bar(d, MARGIN + 40, y0 + block_h + 24, 320)
    # 부제
    f_s = font(fonts["body"], SIZE["cover_sub"])
    sub = card.get("body", "")
    ys = y0 + block_h + 70
    for ln in wrap(d, sub, f_s, W - 2 * MARGIN - 40)[:2]:
        d.text((MARGIN + 40, ys), ln, font=f_s, fill=TOKENS["ink"])
        ys += int(SIZE["cover_sub"] * 1.3)
    # 핸들 + 넘김 힌트(화살표 대신 점 3개)
    handle_line(d, fonts, H - MARGIN - 50, SIZE["cover_handle"])
    for i in range(3):
        d.ellipse([W // 2 - 40 + i * 32, H - MARGIN - 36, W // 2 - 40 + i * 32 + 16, H - MARGIN - 20], fill=TOKENS["ink"])
    return img, warn


# ---------- 장 유형 2: 본문 (기본 / 체크리스트 / 비교표) ----------
def _body_header(d, fonts, card, total):
    n = card.get("n", 0)
    f_n = font(fonts["latin"], SIZE["body_num"])
    s = f"{n}/{total}"
    tw = text_w(d, s, f_n)
    d.rounded_rectangle([MARGIN, MARGIN, MARGIN + tw + 44, MARGIN + 60], radius=30, fill=TOKENS["yellow"], outline=TOKENS["ink"], width=3)
    d.text((MARGIN + 22, MARGIN + 9), s, font=f_n, fill=TOKENS["ink"])
    f_lab = font(fonts["body"], SIZE["label"])
    d.text((W - MARGIN, MARGIN + 12), ACCOUNT, font=f_lab, fill=TOKENS["ink"], anchor="ra")
    # 헤드라인
    f_h = font(fonts["head"], SIZE["body_head"])
    lines = wrap(d, card.get("headline", ""), f_h, W - 2 * MARGIN)
    y = 200
    for ln in lines[:2]:
        d.text((MARGIN, y), ln, font=f_h, fill=TOKENS["ink"], stroke_width=head_stroke(fonts, SIZE["body_head"]), stroke_fill=TOKENS["ink"])
        y += int(SIZE["body_head"] * 1.15)
    signature_bar(d, MARGIN, y + 10, 200)
    return y + 60


def render_body(post, card, fonts, post_dir, total):
    img = hanji_background()
    d = ImageDraw.Draw(img)
    y = _body_header(d, fonts, card, total)
    layout = card.get("layout") or ("checklist" if post.get("type") == "체크리스트" and ("\n" in card.get("body", "") or "·" in card.get("body", "")) else "body")
    if card.get("table"):
        layout = "table"
    f_b = font(fonts["body"], SIZE["body_text"])
    if layout == "checklist":
        items = [s.strip() for s in card.get("body", "").replace("·", "\n").split("\n") if s.strip()][:4]
        for it in items:
            d.rectangle([MARGIN, y + 6, MARGIN + 40, y + 46], fill=TOKENS["yellow"], outline=TOKENS["ink"], width=3)
            d.line([(MARGIN + 9, y + 26), (MARGIN + 18, y + 36), (MARGIN + 33, y + 14)], fill=TOKENS["ink"], width=5)
            lines = wrap(d, it, f_b, W - 2 * MARGIN - 64)[:2]
            yy = y
            for ln in lines:
                d.text((MARGIN + 64, yy), ln, font=f_b, fill=TOKENS["ink"])
                yy += int(SIZE["body_text"] * 1.3)
            y = yy + 18
    elif layout == "table":
        rows = card["table"][:4]
        colw = (W - 2 * MARGIN) // 2
        rh = 92
        for i, row in enumerate(rows):
            for j in range(2):
                x0 = MARGIN + j * colw
                fill = TOKENS["red"] if i == 0 and j == 0 else TOKENS["night"] if i == 0 else TOKENS["paper"]
                d.rectangle([x0, y, x0 + colw, y + rh], fill=fill, outline=TOKENS["ink"], width=4)
                txt = str(row[j]) if j < len(row) else ""
                col = TOKENS["white"] if i == 0 else TOKENS["ink"]
                ln = wrap(d, txt, f_b, colw - 32)[0]
                d.text((x0 + colw // 2, y + rh // 2), ln, font=f_b, fill=col, anchor="mm")
            y += rh
        y += 24
    else:
        lines = wrap(d, card.get("body", ""), f_b, W - 2 * MARGIN)[:3]
        for ln in lines:
            d.text((MARGIN, y), ln, font=f_b, fill=TOKENS["ink"])
            y += int(SIZE["body_text"] * 1.4)
    # 모티프 영역(아래쪽, 플레이트 교체 지점)
    top = max(y + 40, 760)
    box = (MARGIN, top, W - MARGIN, H - MARGIN - 110)
    plate, warn = plate_layer(post_dir, card.get("n", 0), card.get("visual", ""), box, TOKENS["red"])
    img.paste(plate, (0, 0), plate)
    d = ImageDraw.Draw(img)
    handle_line(d, fonts, H - MARGIN - 50, SIZE["label"])
    return img, warn


# ---------- 장 유형 3: 출처·CTA ----------
def render_last(post, card, fonts, post_dir, total):
    img = hanji_background()
    d = ImageDraw.Draw(img)
    # 상단 단청 띠(플레이트 교체 지점)
    box = (MARGIN, MARGIN, W - MARGIN, MARGIN + 160)
    plate, warn = plate_layer(post_dir, card.get("n", total), card.get("visual", "단청 띠"), box, TOKENS["red"])
    img.paste(plate, (0, 0), plate)
    d = ImageDraw.Draw(img)
    # CTA (red 블록 위 white, 대비 5.9)
    cta = card.get("headline") or "저장해 두고 다시 보기"
    f_c = font(fonts["head"], SIZE["last_cta"])
    lines = wrap(d, cta, f_c, W - 2 * MARGIN - 80)[:2]
    lh = int(SIZE["last_cta"] * 1.15)
    y0 = 320
    bh = lh * len(lines) + 70
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + bh], fill=TOKENS["red"], outline=TOKENS["ink"], width=6)
    y = y0 + 36
    for ln in lines:
        d.text((W // 2, y), ln, font=f_c, fill=TOKENS["white"], anchor="ma", stroke_width=head_stroke(fonts, SIZE["last_cta"]), stroke_fill=TOKENS["white"])
        y += lh
    signature_bar(d, W // 2 - 160, y0 + bh + 24, 320)
    # 출처 1~2줄
    f_s = font(fonts["body"], SIZE["last_src"])
    ys = y0 + bh + 90
    d.text((MARGIN, ys), "출처", font=font(fonts["head"], 48), fill=TOKENS["ink"], stroke_width=head_stroke(fonts, 48), stroke_fill=TOKENS["ink"])
    ys += 70
    # 공개 카드에는 원본 URL을 찍지 않는다(캡션·sources.txt가 담당). 마지막 장 body = 출처 이름 줄 (COO 2026-10-02)
    sources = [card["body"]] if card.get("body") else [s for s in post.get("sources", [])[:2] if not str(s).startswith("http")]
    for src in sources[:2]:
        for ln in wrap(d, str(src), f_s, W - 2 * MARGIN)[:2]:
            d.text((MARGIN, ys), ln, font=f_s, fill=TOKENS["ink"])
            ys += int(SIZE["last_src"] * 1.35)
        ys += 10
    # 협찬 슬롯(있을 때만, 상단 광고 표기는 캡션 첫 줄이 담당)
    sponsor = post.get("sponsor_slot") if post.get("render_sponsor_slot") else None  # 내부 기획 정보, 기본 비표시 (COO 2026-10-02)
    if sponsor and sponsor not in ("", "none", "없음"):
        d.rectangle([MARGIN, ys + 20, W - MARGIN, ys + 110], fill=TOKENS["wheat"], outline=TOKENS["ink"], width=4)
        d.text((MARGIN + 24, ys + 44), wrap(d, f"협찬 슬롯: {sponsor}", f_s, W - 2 * MARGIN - 48)[0], font=f_s, fill=TOKENS["ink"])
        ys += 130
    # AI 생성물 표시 + 핸들
    f_ai = font(fonts["body"], SIZE["label"])
    d.text((W // 2, H - MARGIN - 120), "이미지·초안은 AI로 생성, 사실 확인은 사람이 했습니다", font=f_ai, fill=TOKENS["ink"], anchor="ma")
    handle_line(d, fonts, H - MARGIN - 56, SIZE["last_handle"], center=True)
    return img, warn


# ---------- 저장 ----------
SAVE_RGB = False


def save_png(img, path):
    """기본 PNG-8(적응 팔레트 256색, 플랫 디자인이라 손실 거의 없음) -> 장당 ~300KB 이하. --rgb 면 24비트."""
    if SAVE_RGB:
        img.save(path, optimize=True)
    else:
        img.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(path, optimize=True)


# ---------- 조립 ----------
def render_post(post_dir, fonts, verbose=True):
    path = os.path.join(post_dir, "cards.json")
    with open(path, encoding="utf-8") as fp:
        post = json.load(fp)
    cards = sorted(post.get("cards", []), key=lambda c: c.get("n", 0))
    total = len(cards)
    outputs, warns = [], []
    for i, card in enumerate(cards):
        n = card.get("n", i + 1)
        if i == 0:
            img, warn = render_cover(post, card, fonts, post_dir)
        elif i == total - 1:
            img, warn = render_last(post, card, fonts, post_dir, total)
        else:
            img, warn = render_body(post, card, fonts, post_dir, total)
        mockup_tag(img, fonts)
        out = os.path.join(post_dir, f"card-{n:02d}.png")
        save_png(img, out)
        outputs.append(out)
        if warn and warn != "custom plate":
            warns.append(f"card-{n:02d}: {warn}")
        # 글자수 규칙 점검(경고만)
        if len(card.get("headline", "")) > 14:
            warns.append(f"card-{n:02d}: headline {len(card['headline'])}자 (>14)")
        if len(card.get("body", "")) > 60:
            warns.append(f"card-{n:02d}: body {len(card['body'])}자 (>60)")
    contact = contact_sheet(outputs, post.get("post_id", os.path.basename(post_dir)), fonts)
    cpath = os.path.join(post_dir, "contact.png")
    contact.save(cpath, optimize=True)
    if verbose:
        print(f"[{post_dir}] {len(outputs)} cards -> card-01..{total:02d}.png, contact.png")
        for w in warns:
            print("  warn:", w)
    return outputs, cpath, warns


def contact_sheet(paths, title, fonts, tile=(320, 400), per_row=4):
    """장 전체 나열 1장. 타일 = 320x400(폰 피드 축소 검수 겸용)."""
    pad, head = 24, 70
    rows = (len(paths) + per_row - 1) // per_row
    cols = min(per_row, len(paths))
    cw = pad + cols * (tile[0] + pad)
    ch = head + rows * (tile[1] + pad + 30) + pad
    sheet = Image.new("RGB", (cw, ch), TOKENS["night"])
    d = ImageDraw.Draw(sheet)
    d.text((pad, 20), f"{title}  contact ({tile[0]}x{tile[1]} tiles)  MOCKUP", font=font(fonts["latin"], 28), fill=TOKENS["yellow"])
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB").resize(tile, Image.LANCZOS)
        x = pad + (i % per_row) * (tile[0] + pad)
        y = head + (i // per_row) * (tile[1] + pad + 30)
        sheet.paste(im, (x, y))
        d.text((x, y + tile[1] + 6), os.path.basename(p), font=font(fonts["latin"], 22), fill=TOKENS["white"])
    return sheet


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("post_dir", nargs="?", help="cards.json 이 있는 게시물 폴더")
    ap.add_argument("--all", metavar="POSTS_DIR", help="하위 폴더 중 cards.json 이 있는 것 전부 렌더")
    ap.add_argument("--rgb", action="store_true", help="PNG-24로 저장(기본은 PNG-8 적응 팔레트)")
    args = ap.parse_args()
    global SAVE_RGB
    SAVE_RGB = args.rgb
    fonts = load_fonts()
    print("fonts:", {k: v for k, v in fonts.items()})
    targets = []
    if args.all:
        for d in sorted(glob.glob(os.path.join(args.all, "*"))):
            if os.path.isfile(os.path.join(d, "cards.json")):
                targets.append(d)
    elif args.post_dir:
        targets.append(args.post_dir)
    else:
        ap.error("post_dir 또는 --all 을 지정하세요")
    if not targets:
        print("cards.json 을 가진 폴더가 없습니다"); return 1
    total_warn = 0
    for t in targets:
        _, _, warns = render_post(t, fonts)
        total_warn += len(warns)
    return 0


if __name__ == "__main__":
    sys.exit(main())
