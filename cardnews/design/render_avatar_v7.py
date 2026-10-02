#!/usr/bin/env python3
"""책가도 노트 프로필 사진 v7: "처음으로 돌아가 전혀 다른 방향 3안"(대표 2026-10-02). 코드 렌더만(AI 생성 0).

v4~v6의 틀("붓글씨 글자 + 원화 바탕")을 버린다. 글자 0.
  a 단일 모티프: 클리블랜드미술관 〈책가도〉 2011.37 CC0(full TIFF)에서 청화 화병 + 꽃 한 점만 누끼 → 한지색 원 + 먹남색 테
  b 민화 동물:   메트로폴리탄미술관 〈Golden Rooster and Hen〉 19.103.2 CC0에서 수탉 머리만 크롭(눈·볏) — 호랑이·까치(금지 모티프 #30·#31) 대신
  c 추상 기하:   책가도 칸막이(좌우 칸 높이가 엇갈림)를 기호화한 3색 심볼, 붉은 '한 칸' 1개 — 원화 픽셀 0

누끼(a)는 원화 픽셀을 그대로 쓰고 바탕만 지운다(색·형태 변형 없음, lut-v1·채도 -20%는 v3~v6와 같은 공통 보정).

사용:
  python3 cardnews/design/render_avatar_v7.py --download   # 원화 -> render/avatar-v3/src/ (커밋 제외, full TIFF 237MB)
  python3 cardnews/design/render_avatar_v7.py

산출물(cardnews/profile/, v6 이전 파일은 건드리지 않음):
  avatar-v7-{a,b,c}.png, -320.png, -110.png   정사각(업로드용)
  contact-profile-v7.png                       v6-bx(직전) + 3안, 각 칸: 정사각 → 원형 320 → 원형 110 + 콘셉트 한 줄
  avatar-v7-RENDER.json                        출처·크롭 좌표·색·110px 대비
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_cards as rc  # noqa: E402  (수정하지 않음)
import render_profile as rp  # noqa: E402  (circle_crop, 수정하지 않음)
import render_avatar_v3 as v3  # noqa: E402  (hanji_texture·common_lut·SRC_DIR, 수정하지 않음)
import render_avatar_v5 as v5  # noqa: E402  (legibility_110, 수정하지 않음)

Image.MAX_IMAGE_PIXELS = None
OUT_DIR = v5.OUT_DIR
AV, SAFE_R = v3.AV, v3.SAFE_R
SRC = v3.SRC_DIR
T = rc.TOKENS
hexrgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))  # noqa: E731
SAT = 0.80  # 채도 -20% (v3~v6 공통)

ARTS = {
    "a": {"file": "cleveland-2011.37-full.tif", "url": "https://openaccess-cdn.clevelandart.org/2011.37/2011.37_full.tif",
          "title": "Books and Scholars' Accoutrements", "title_ko": "책가도", "institution": "클리블랜드미술관",
          "accession": "2011.37", "object_url": "https://clevelandart.org/art/2011.37", "license": "CC0",
          "license_url": "https://creativecommons.org/publicdomain/zero/1.0/", "credit_short": "클리블랜드미술관 〈책가도〉 CC0",
          "image_size": [11838, 6670],
          # full TIFF 픽셀 좌표. print JPG(3400px) 기준 [2987,646,3230,991] × 3.4818
          "crop": [10400, 2250, 11250, 3450],
          "part": "10폭 중 10폭 가운데 단 오른쪽 칸: 청화 화병(구름무늬 원문)에 꽂힌 분홍 꽃가지 한 점. 옆 붉은 잔·칸 벽은 지움"},
    "b": {"file": "met-40073.jpg", "url": "https://images.metmuseum.org/CRDImages/as/original/DP289323.jpg",
          "title": "Golden Rooster and Hen", "title_ko": "금계도(수탉과 암탉)", "institution": "메트로폴리탄미술관",
          "accession": "19.103.2", "object_url": "https://www.metmuseum.org/art/collection/search/40073", "license": "CC0",
          "license_url": "https://www.metmuseum.org/policies/image-resources", "credit_short": "메트로폴리탄미술관 〈금계도〉 CC0",
          "image_size": [861, 2000],
          "crop": [396, 790, 656, 1050],
          "part": "가운데 수탉의 머리: 붉은 볏·눈·부리·턱볏, 목 깃털 일부. 오른쪽 위 소나무 잎 끝이 모서리에 걸림(원형 크롭에서 대부분 잘림)"},
}

# a 누끼: 꽃가지 줄기 가이드선(크롭 좌표). 줄기는 어두운 올리브색이라 칸 벽(검정)과 색이 붙어 있어 선 주변 9px 안에서만 줍는다.
STEMS = [
    [(450, 692), (477, 631), (504, 546), (515, 500), (535, 400), (554, 331), (569, 296), (585, 265), (581, 215), (579, 196), (577, 172)],
    [(585, 265), (600, 258), (615, 250)],
    [(588, 254), (598, 230), (604, 212)],
    [(565, 300), (558, 277)],
    [(446, 685), (435, 608), (419, 562), (396, 542), (380, 528)],
]
CUP_BOX = (0, 860, 330, 1200)  # 붉은 잔(지움)
# a 화병 외곽선(펜 툴처럼 손으로 딴 오른쪽 윤곽, 크롭 좌표에서 x=457 축으로 좌우 대칭). 화병 왼쪽은 그늘이 져 색 문턱으로는 잘린다.
VASE_R = [(457, 672), (500, 673), (560, 676), (590, 682), (588, 698), (535, 712), (523, 740), (524, 780), (538, 800),
          (592, 807), (622, 822), (638, 846), (641, 872), (626, 898), (575, 938), (538, 968), (520, 1000), (520, 1040),
          (532, 1078), (546, 1105), (552, 1140)]
VASE_AXIS = 457
FLOWER_MAX_Y = 690  # 이보다 위만 꽃·줄기 색 문턱으로 줍는다(아래는 화병 윤곽)

COLORS = {
    "a": {"ground": "paper", "ring": "night", "accent": None},
    "b": {"ground": None, "ring": "night", "accent": None},
    "c": {"ground": "paper", "ink": "ink", "accent": "red"},
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fp:
        for b in iter(lambda: fp.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def download():
    os.makedirs(SRC, exist_ok=True)
    for a in ARTS.values():
        p = os.path.join(SRC, a["file"])
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            subprocess.run(["curl", "-sSfL", "-A", "ke-studio-cardnews/1.0", "-o", p, a["url"]], check=True)
            print("downloaded", p)


def tone(im):
    return v3.common_lut(ImageEnhance.Color(im).enhance(SAT))


def fill_holes(m):
    """이진 마스크(L)의 구멍 메우기: 바깥에서 flood fill 후 반전."""
    w, h = m.size
    pad = Image.new("L", (w + 2, h + 2), 0)
    pad.paste(m, (1, 1))
    ImageDraw.floodfill(pad, (0, 0), 128)
    a = np.asarray(pad)[1:-1, 1:-1]
    return Image.fromarray(np.where(a == 128, 0, 255).astype(np.uint8))


def keep_largest(m, extra_keep):
    """vase·꽃과 이어진 덩어리만(떠 있는 벽 얼룩 제거). extra_keep = 반드시 남길 시드 좌표."""
    work = m.copy()
    out = Image.new("L", m.size, 0)
    for s in extra_keep:
        if work.getpixel(s) == 255:
            ImageDraw.floodfill(work, s, 100)
    a = np.asarray(work)
    out = Image.fromarray(np.where(a == 100, 255, 0).astype(np.uint8))
    return out


def vase_cutout():
    a = ARTS["a"]
    src = os.path.join(SRC, a["file"])
    reg = Image.open(src).crop(a["crop"]).convert("RGB")
    arr = np.asarray(reg).astype(np.int16)
    R, G, B = arr[..., 0], arr[..., 1], arr[..., 2]
    lum = 0.299 * R + 0.587 * G + 0.114 * B
    body = (lum > 74) & ((R - B) > 28)  # 화병·꽃(따뜻한 밝은색). 칸 바닥(회녹색 R-B≈21)·남색 벽 제외
    w, h = reg.size
    yy, xx = np.mgrid[0:h, 0:w]
    body &= xx < 760  # 오른쪽 붉은 벽
    x0, y0, x1, y1 = CUP_BOX
    body &= ~((xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1))
    guide = Image.new("L", (w, h), 0)
    gd = ImageDraw.Draw(guide)
    for line in STEMS:
        gd.line(line, fill=255, width=18, joint="curve")
    near = np.asarray(guide) > 0
    stem = near & (lum > 22) & (lum < 120) & ((G - B) > 8) & (G >= R - 6)  # 올리브(남색 벽 B↑·검은 칸 무채색·붉은 벽 R↑ 제외)
    core = Image.new("L", (w, h), 0)
    cd = ImageDraw.Draw(core)
    for line in STEMS:
        cd.line(line, fill=255, width=5, joint="curve")
    body &= yy < FLOWER_MAX_Y
    vase = Image.new("L", (w, h), 0)
    poly = VASE_R + [(2 * VASE_AXIS - x, y) for x, y in reversed(VASE_R)]
    ImageDraw.Draw(vase).polygon(poly, fill=255)
    m = Image.fromarray(((body | stem | (np.asarray(core) > 0) | (np.asarray(vase) > 0)) * 255).astype(np.uint8))
    m = m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))  # closing
    m = keep_largest(m, [(470, 900), (300, 520), (690, 260), (560, 130)])
    m = fill_holes(m)
    m = m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    return tone(reg), m, vase, sha(src)


def ring(img, color, width):
    d = ImageDraw.Draw(img)
    r = AV // 2 - 4
    d.ellipse([AV / 2 - r, AV / 2 - r, AV / 2 + r, AV / 2 + r], outline=color, width=width)


def hanji(rgb, seed):
    tex = v3.hanji_texture((AV, AV), seed=seed)[..., None]
    base = np.array(rgb, np.float32)[None, None, :]
    return Image.fromarray(np.clip(base * (0.93 + 0.07 * tex / 1.0), 0, 255).astype(np.uint8))


def render_a():
    reg, m, vase, s = vase_cutout()
    bb = m.getbbox()
    obj, mk, vk = reg.crop(bb), m.crop(bb), vase.crop(bb)
    target_h = 840  # 원형 안전 반경 430 안: 높이 820 → 위아래 ±410
    k = target_h / obj.height
    obj = obj.resize((round(obj.width * k), target_h), Image.LANCZOS)
    mk = mk.resize(obj.size, Image.LANCZOS)
    vk = vk.resize(obj.size, Image.LANCZOS)
    img = hanji(hexrgb(T["paper"]), 2027)
    # 원형 안전 반경(430) 안에 오도록 무게중심을 가운데로
    ox = (AV - obj.width) // 2 + 18
    oy = (AV - target_h) // 2
    img.paste(obj, (ox, oy), mk)
    ring(img, hexrgb(T["night"]), 22)
    full = Image.new("L", (AV, AV), 0)
    full.paste(vk, (ox, oy))  # 판독 기준 = 화병 몸통
    rec = {"source_crop_box": ARTS["a"]["crop"], "object_bbox_in_crop": list(bb), "scale": round(k, 3),
           "paste_xy": [ox, oy], "upsample": "없음(원본 해상도 ≥ 출력)" if k <= 1 else f"×{k:.2f}",
           "mask": "화병 = 손으로 딴 대칭 윤곽(VASE_R) / 꽃 = lum>74 & R-B>28 (y<690) / 줄기 = 가이드선 9px 안 올리브색(G-B>8, G≥R-6) → closing 5 → 연결 덩어리만 → 구멍 메움",
           "source_sha256": s}
    return img, full, rec


def render_b():
    a = ARTS["b"]
    src = os.path.join(SRC, a["file"])
    reg = Image.open(src).convert("RGB").crop(a["crop"])
    k = AV / reg.width
    img = tone(reg.resize((AV, AV), Image.LANCZOS)).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    ring(img, hexrgb(T["night"]), 22)
    arr = np.asarray(img).astype(np.int16)
    comb = (arr[..., 0] > 150) & (arr[..., 1] < 120) & (arr[..., 2] < 110)  # 볏·턱볏(붉은색) = 판독 기준 형태
    mask = Image.fromarray((comb * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5))
    rec = {"source_crop_box": a["crop"], "upsample": f"×{k:.2f} (LANCZOS + unsharp r2/60%, 원본 머리 폭 약 110px)",
           "source_sha256": sha(src)}
    return img, mask, rec


# c: 책가도 칸막이 기호. 좌우 두 단의 칸 높이가 엇갈린다(2011.37 각 폭의 칸 배치에서 가져온 원리, 비율은 추정 단순화)
C_BOX = 560
C_STROKE = 40
C_LEFT = [0.40, 0.74]   # 왼쪽 단 칸막이 높이(위에서 비율)
C_RIGHT = [0.22, 0.58]  # 오른쪽 단
C_RED = ("R", 0.22, 0.58)  # 붉은 '한 칸' = 오른쪽 단 가운데


def render_c():
    img = hanji(hexrgb(T["paper"]), 2028)
    ink, red = hexrgb(T["ink"]), hexrgb(T["red"])
    SS = 4
    big = Image.new("RGBA", (AV * SS, AV * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    x0 = (AV - C_BOX) / 2
    y0 = (AV - C_BOX) / 2
    xm = x0 + C_BOX / 2
    s = C_STROKE
    S = lambda v: v * SS  # noqa: E731
    _, t0, t1 = C_RED
    d.rectangle([S(xm), S(y0 + C_BOX * t0), S(x0 + C_BOX), S(y0 + C_BOX * t1)], fill=red + (255,))
    d.rectangle([S(x0), S(y0), S(x0 + C_BOX), S(y0 + C_BOX)], outline=ink + (255,), width=S(s))
    d.rectangle([S(xm - s / 2), S(y0), S(xm + s / 2), S(y0 + C_BOX)], fill=ink + (255,))
    for t in C_LEFT:
        y = y0 + C_BOX * t
        d.rectangle([S(x0), S(y - s / 2), S(xm), S(y + s / 2)], fill=ink + (255,))
    for t in C_RIGHT:
        y = y0 + C_BOX * t
        d.rectangle([S(xm), S(y - s / 2), S(x0 + C_BOX), S(y + s / 2)], fill=ink + (255,))
    lay = big.resize((AV, AV), Image.LANCZOS)
    img.paste(lay, (0, 0), lay)
    mask = lay.split()[3]
    half_diag = round((C_BOX / 2 + s / 2) * 2 ** 0.5)
    rec = {"box_px": C_BOX, "stroke_px": C_STROKE, "left_dividers": C_LEFT, "right_dividers": C_RIGHT,
           "red_cell": "오른쪽 단 가운데 칸", "half_diagonal_px": half_diag, "fits_safe_r": half_diag <= SAFE_R,
           "art_pixels": 0}
    return img, mask, rec


def _lab(rgb):
    v = v5._lin(rgb.astype(np.float32))
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]], np.float32)
    xyz = v @ M.T / np.array([0.9505, 1.0, 1.089], np.float32)
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def delta_e_110(img, mask):
    """110px 축소본에서 기준 형태 평균색 vs 바깥 고리 평균색 CIE76 ΔE(명도 대비가 낮은 색상 대비를 보완)."""
    s = 110
    im = np.asarray(img.resize((s, s), Image.LANCZOS)).astype(np.float32)
    mk = mask.resize((s, s), Image.LANCZOS)
    core = np.asarray(mk).astype(np.float32) / 255 > 0.6
    ring_ = np.asarray(mk.filter(ImageFilter.MaxFilter(7))).astype(np.float32) / 255 > 0.3
    ring_ &= ~(np.asarray(mk.filter(ImageFilter.MaxFilter(3))).astype(np.float32) / 255 > 0.1)
    a, b = _lab(im[core].mean(0)), _lab(im[ring_].mean(0))
    return round(float(np.linalg.norm(a - b)), 1)


CONCEPT = {
    "a": ("단일 모티프", "책가도 한 칸에서 화병 한 점만 꺼내 왔다"),
    "b": ("민화 동물", "민화 수탉이 눈을 맞춘다"),
    "c": ("추상 기하", "엇갈린 책장 칸 중 오늘 펼친 '한 칸'"),
}


def contact(prev, cells, recs, fonts, pick):
    sq, big, small, gap, pad, head, txt = 320, 320, 110, 40, 40, 132, 120
    cw = sq
    ch = sq + 14 + big + 14 + small + txt
    W = pad * 2 + cw * 4 + gap * 3
    H = head + ch + 40
    sheet = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(sheet)
    body = lambda s: rc.font(fonts["body"], s)  # noqa: E731
    d.text((pad, 22), "프로필 사진 v7 — 틀 교체: '붓글씨 글자 + 원화 바탕'을 버리고 전혀 다른 방향 3안",
           font=body(28), fill=rp.APP_TEXT)
    d.text((pad, 64), "각 칸: 정사각 → 원형 320 → 원형 110(실제 크기) · 글자 0 · AI 생성 0 · 맨 왼쪽 = 직전 v6-bx(반려)",
           font=body(19), fill="#6B6B6B")
    d.text((pad, 90), "110px = 기준 형태(a 화병 / b 볏 / c 칸막이) vs 바깥 고리: WCAG 명도 대비(문턱 3:1) · 색차 ΔE(문턱 20) — 둘 다 추정 문턱",
           font=body(19), fill="#6B6B6B")

    def put(img, x, y, lab, sub, sub2, mark=None, dim=False):
        sheet.paste(img.resize((sq, sq), Image.LANCZOS), (x, y))
        c = rp.circle_crop(img, (AV / 2, AV / 2), AV, big)
        sheet.paste(c, (x, y + sq + 14), c)
        s = rp.circle_crop(img, (AV / 2, AV / 2), AV, small)
        sy = y + sq + 14 + big + 14
        sheet.paste(s, (x + (cw - small) // 2, sy), s)
        ly = sy + small + 12
        d.text((x + cw // 2, ly), lab, font=body(22), fill="#8A8A8A" if dim else rp.APP_TEXT, anchor="ma",
               stroke_width=0 if dim else 1, stroke_fill=rp.APP_TEXT)
        d.text((x + cw // 2, ly + 32), sub, font=body(17), fill="#6B6B6B", anchor="ma")
        d.text((x + cw // 2, ly + 56), sub2, font=body(17), fill="#6B6B6B", anchor="ma")
        if mark:
            d.rectangle([x - 10, y - 10, x + cw + 10, ly + 84], outline=T["red"], width=5)
            d.text((x + cw - 4, y - 8), mark, font=body(20), fill="#FFFFFF", anchor="ra", stroke_width=4, stroke_fill=T["red"])

    put(prev, pad, head, "직전  v6-bx (반려)", "붓글씨 + 원화 바탕 틀", "→ v7에서 틀 자체를 교체", dim=True)
    for i, k in enumerate("abc"):
        x = pad + (i + 1) * (cw + gap)
        kind, line = CONCEPT[k]
        put(cells[k], x, head, f"v7-{k}  {kind}", line, f"110px 대비 {recs[k]['legibility_110']['contrast']}:1 · ΔE {recs[k]['legibility_110']['delta_e']}",
            "추천" if k == pick else None)
    return sheet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", action="store_true")
    ap.add_argument("--pick", default="a")
    a = ap.parse_args()
    if a.download:
        download()
    names = [f"avatar-v7-{k}{s}.png" for k in "abc" for s in ("", "-320", "-110")] + ["contact-profile-v7.png", "avatar-v7-RENDER.json"]
    clash = [n for n in names if os.path.exists(os.path.join(OUT_DIR, n))]
    if clash and os.environ.get("KE_V7_REWRITE") != "1":
        sys.exit(f"이미 있음(덮어쓰지 않음): {clash}  (v7 재렌더 의도면 KE_V7_REWRITE=1)")
    fonts = rc.load_fonts()
    cells, recs = {}, {}
    for k, fn in (("a", render_a), ("b", render_b), ("c", render_c)):
        img, mask, rec = fn()
        rec = {"key": k, "kind": CONCEPT[k][0], "concept": CONCEPT[k][1], "method": "code_render", "ai_generated": False,
               "text_glyphs": 0, "colors": {n: T[v] for n, v in COLORS[k].items() if v},
               "art": ARTS.get(k), **rec,
               "legibility_110": {"contrast": v5.legibility_110(img, mask), "threshold": 3.0,
                                  "delta_e": delta_e_110(img, mask), "delta_e_threshold": 20}}
        if k == "a":
            rec["tone"] = "채도 -20% + lut-v1(render_avatar_v3.common_lut), 형태·색 변형 없음"
        if k == "b":
            rec["tone"] = "채도 -20% + lut-v1, unsharp r2/60%"
        cells[k], recs[k] = img, rec
        img.save(os.path.join(OUT_DIR, f"avatar-v7-{k}.png"), optimize=True)
        for s in (320, 110):
            img.resize((s, s), Image.LANCZOS).save(os.path.join(OUT_DIR, f"avatar-v7-{k}-{s}.png"), optimize=True)
        print(k, "cr110", rec["legibility_110"]["contrast"])
    prev = Image.open(os.path.join(OUT_DIR, "avatar-v6-bx.png")).convert("RGB")
    contact(prev, cells, recs, fonts, a.pick).save(os.path.join(OUT_DIR, "contact-profile-v7.png"), optimize=True)
    meta = {"feedback": "2026-10-02 대표: v4·v5·v6 전부 반려, '처음으로 돌아가서 전혀 다른 방향 3안을 새로'",
            "dropped_frame": "붓글씨 글자 + 원화 바탕 (v4~v6)",
            "legibility_def": "110px 축소본에서 기준 형태 vs 바깥 고리 ① WCAG 대비비(render_avatar_v5.legibility_110), 비글자 그래픽 문턱 3:1(WCAG 1.4.11 차용, 추정) ② CIE76 ΔE, 문턱 20(추정). 둘 중 하나 이상 통과 + 육안",
            "recommended": a.pick, "variants": [recs[k] for k in "abc"]}
    with open(os.path.join(OUT_DIR, "avatar-v7-RENDER.json"), "w", encoding="utf-8") as fp:
        json.dump(meta, fp, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
