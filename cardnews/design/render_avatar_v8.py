#!/usr/bin/env python3
"""책가도 노트 프로필 사진 v8: v4 A 구도 복귀 + 바탕 20% + 낙관 0 + 붓글씨 먹 질감.

대표 지시(2026-10-02, v4 A를 보며): "바탕 20% 정도로, '책' 낙관 제외, 책가도 그 글씨체 붓글씨를 제대로."
v7(틀 교체)은 접는다. 한지색 원 + 클리블랜드 〈책가도〉 2011.37 책갑 칸(가시성 20%) + 세로 3자 "책가도".

붓글씨를 "제대로" = 서체 외형은 그대로 두고(OFL 서체를 그림으로 렌더) 먹 질감만 코드로 입힌다.
  ⓐ 먹 번짐: 마스크 가우시안 + 섬유 노이즈 섞은 부드러운 임계값 -> 종이에 스민 들쭉날쭉한 가장자리 + 옅은 테
  ⓑ 갈필: 획 방향(구조 텐서)으로 늘인 결 노이즈 -> 획 가장자리·얇은 곳 위주로 미세한 흰 결
  ⓒ 농담: 글자마다 붓이 들어간 쪽(위·왼쪽)이 진하고 빠지는 쪽(아래·오른쪽)이 옅은 알파 그라데이션 + 저주파 얼룩
  ⓓ 한지 질감 15%(§8-3, v4와 같은 레시피)
가짜 볼드(마스크 팽창) 없음. AI 생성 0. 낙관 없음. 글자 둘레 한지색 덮개 없음.

사용:
  bash scripts/setup.sh                                    # 서체 1·2(~/.fonts/ke/, 커밋 안 함)
  curl -sSfL -o ~/.fonts/ke/yeonsung_YeonSung-Regular.ttf \
    https://raw.githubusercontent.com/google/fonts/main/ofl/yeonsung/YeonSung-Regular.ttf   # 서체 3(setup.sh 미수정)
  python3 cardnews/design/render_avatar_v8.py --download   # 원화 -> render/avatar-v3/src/ (커밋 제외)
  python3 cardnews/design/render_avatar_v8.py
의존: pillow, numpy, scipy(ndimage).

산출물(cardnews/profile/): avatar-v8-{1,2,3}.png(+ -320, -110), contact-profile-v8.png, avatar-v8-RENDER.json
"""
import argparse
import hashlib
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_cards as rc  # noqa: E402  (수정하지 않음)
import render_profile as rp  # noqa: E402  (circle_crop·max_radius, 수정하지 않음)
import render_avatar_v3 as v3  # noqa: E402  (hanji_texture·common_lut·download, 수정하지 않음)

OUT_DIR = os.path.join(os.path.dirname(HERE), "profile")
FONT_DIR = os.path.expanduser("~/.fonts/ke")
AV = v3.AV
SAFE_R = v3.SAFE_R
INK = (22, 20, 19)  # 먹색 #161413 (순흑 금지, 아주 약간 따뜻하게)
BG_SRC = v3.SOURCES[0]  # 2011.37, v3/v4 A와 같은 크롭

GF = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
FONTS = {
    "1": {"file": "nanumbrushscript_NanumBrushScript-Regular.ttf", "family": "Nanum Brush Script",
          "path": "nanumbrushscript/NanumBrushScript-Regular.ttf", "lic": "nanumbrushscript/OFL.txt"},
    "2": {"file": "eastseadokdo_EastSeaDokdo-Regular.ttf", "family": "East Sea Dokdo",
          "path": "eastseadokdo/EastSeaDokdo-Regular.ttf", "lic": "eastseadokdo/OFL.txt"},
    "3": {"file": "yeonsung_YeonSung-Regular.ttf", "family": "Yeon Sung (BM YEONSUNG)",
          "path": "yeonsung/YeonSung-Regular.ttf", "lic": "yeonsung/OFL.txt"},
}

# 세로쓰기 배치(손 조정): 글자별 잉크 높이(px), 중심 x 흔들림, 기울기(도, 서체 외형 변형이 아닌 배치 회전).
# 위 글자가 가장 크고 아래로 갈수록 살짝 작아진다. 글자 사이 간격 GAP.
LAYOUT = {
    "1": [(270, -6, -1.5), (250, 10, 1.0), (238, -2, -0.5)],
    "2": [(268, -4, -1.0), (250, 8, 1.5), (236, -6, 0.0)],
    "3": [(266, -8, -1.0), (250, 10, 0.8), (236, -4, -0.6)],
}
GAP = 34

# 먹 처리 강도(약/중/강). blur = 번짐 가우시안 sigma, soft = 임계 램프 폭, fib = 가장자리 섬유 노이즈 진폭,
# halo = 스민 테 알파, dry = 갈필 결 깊이, shade = 농담(획 끝 알파 하강폭), mottle = 저주파 얼룩 진폭.
STRENGTH = {
    "약": {"blur": 1.2, "soft": 0.10, "fib": 0.10, "halo": 0.10, "dry": 0.18, "shade": 0.10, "mottle": 0.04},
    "중": {"blur": 1.8, "soft": 0.14, "fib": 0.18, "halo": 0.14, "dry": 0.32, "shade": 0.16, "mottle": 0.06},
    "강": {"blur": 2.6, "soft": 0.18, "fib": 0.28, "halo": 0.18, "dry": 0.50, "shade": 0.24, "mottle": 0.09},
}
BG_PCT = {"18": 0.18, "20": 0.20, "22": 0.22}


def font_path(k):
    p = os.path.join(FONT_DIR, FONTS[k]["file"])
    if not os.path.exists(p):
        sys.exit(f"서체 없음: {p}  (bash scripts/setup.sh 의 서체 블록)")
    return p


def sha(p):
    with open(p, "rb") as fp:
        return hashlib.sha256(fp.read()).hexdigest()


def paper_bg(seed, pct):
    """한지색 바탕(#F7F3EA x 한지 15% x 세피아) 위에 원화 크롭을 pct 불투명도로. 원화 내용 변형 없음."""
    base = np.ones((AV, AV, 3), np.float32) * np.array([0xF7, 0xF3, 0xEA], np.float32)
    tex = v3.hanji_texture((AV, AV), seed=seed)[..., None]
    bg = Image.fromarray(np.clip(base * (0.85 + 0.15 * tex) * np.array(v3.SEPIA, np.float32), 0, 255).astype(np.uint8))
    src = os.path.join(v3.SRC_DIR, BG_SRC["file"])
    if not os.path.exists(src):
        sys.exit(f"원본 없음: {src}  (먼저 --download)")
    im = Image.open(src).convert("RGB").crop(tuple(BG_SRC["crop"])).resize((AV, AV), Image.LANCZOS)
    im = v3.common_lut(ImageEnhance.Color(im).enhance(0.80))
    return Image.blend(bg, im, pct), sha(src)


def glyph_masks(fk):
    """글자별 마스크를 잉크 높이에 맞춰 렌더(2x 슈퍼샘플)해 세로로 배치. 반환: 전체 마스크(0..1), 글자별 bbox."""
    SS = 2
    canvas = np.zeros((AV, AV), np.float32)
    boxes = []
    sizes = LAYOUT[fk]
    total = sum(h for h, _, _ in sizes) + GAP * (len(sizes) - 1)
    y = AV / 2 - total / 2
    for ch, (h, dx, rot) in zip("책가도", sizes):
        f = ImageFont.truetype(font_path(fk), 400 * SS)
        g = Image.new("L", (900 * SS, 900 * SS), 0)
        ImageDraw.Draw(g).text((450 * SS, 450 * SS), ch, font=f, fill=255, anchor="mm")
        g = g.crop(g.getbbox())
        sc = h / (g.height / SS)
        g = g.resize((max(1, round(g.width * sc / SS)), h), Image.LANCZOS)
        if rot:
            g = g.rotate(rot, resample=Image.BICUBIC, expand=True)
        cx, cy = AV / 2 + dx, y + h / 2
        x0, y0 = round(cx - g.width / 2), round(cy - g.height / 2)
        a = np.asarray(g).astype(np.float32) / 255
        canvas[y0:y0 + g.height, x0:x0 + g.width] = np.maximum(canvas[y0:y0 + g.height, x0:x0 + g.width], a)
        boxes.append((x0, y0, x0 + g.width, y0 + g.height))
        y += h + GAP
    return canvas, boxes


def streak_noise(rng, along):
    """한 방향으로 길게 늘인 결 노이즈(0..1). along='v'면 세로 결, 'h'면 가로 결."""
    if along == "v":
        n = rng.normal(0, 1, (AV // 40, AV // 2)).astype(np.float32)
    else:
        n = rng.normal(0, 1, (AV // 2, AV // 40)).astype(np.float32)
    n = np.array(Image.fromarray(n).resize((AV, AV), Image.BICUBIC))
    return (n - n.min()) / max(1e-6, n.max() - n.min())


def ink_alpha(mask, boxes, p, seed):
    """서체 마스크 -> 먹 알파(0..1). 외형 팽창 없음(가짜 볼드 금지), 번짐은 가장자리 몇 px 안에서만."""
    rng = np.random.default_rng(seed)
    # ⓐ 번짐: 가우시안 + 섬유 노이즈로 흔든 임계 램프(0.5 기준) -> 들쭉날쭉 스민 가장자리
    fib = v3.hanji_texture((AV, AV), seed=seed + 7)
    fib = (fib - 0.9) / 0.1  # 대략 -1..1
    b = ndi.gaussian_filter(mask, p["blur"])
    t = 0.5 + p["fib"] * 0.5 * fib
    core = np.clip((b - t) / p["soft"] + 0.5, 0, 1)
    halo = ndi.gaussian_filter(mask, p["blur"] * 3.5)
    halo = np.clip(halo * 1.6, 0, 1) * p["halo"] * (0.7 + 0.3 * np.clip(fib, -1, 1))
    # ⓑ 갈필: 획 방향(구조 텐서) 따라 늘인 결, 획 가장자리·얇은 곳에서 강하게
    gy, gx = np.gradient(ndi.gaussian_filter(mask, 3.0))
    jxx, jyy = ndi.gaussian_filter(gx * gx, 6), ndi.gaussian_filter(gy * gy, 6)
    w_v = jxx / (jxx + jyy + 1e-6)  # 가로 그라디언트가 크면 세로 획 -> 세로 결
    streak = w_v * streak_noise(rng, "v") + (1 - w_v) * streak_noise(rng, "h")
    depth = ndi.distance_transform_edt(mask > 0.5)
    edge_w = np.clip(1.0 - depth / 14.0, 0.25, 1.0)
    dry = np.clip((streak - 0.55) / 0.25, 0, 1) * edge_w * p["dry"]
    # ⓒ 농담: 글자마다 붓이 들어간 위·왼쪽이 진하고 빠지는 아래·오른쪽이 옅게 + 저주파 얼룩
    yy, xx = np.mgrid[0:AV, 0:AV].astype(np.float32)
    shade = np.ones((AV, AV), np.float32)
    for x0, y0, x1, y1 in boxes:
        u = np.clip(((xx - x0) / max(1, x1 - x0) * 0.35 + (yy - y0) / max(1, y1 - y0) * 0.65), 0, 1)
        inside = (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)
        shade = np.where(inside, 1.0 - p["shade"] * u ** 1.5, shade)
    mot = rng.normal(0, 1, (AV // 60, AV // 60)).astype(np.float32)
    mot = np.array(Image.fromarray(mot).resize((AV, AV), Image.BICUBIC))
    mot = mot / max(1e-6, np.abs(mot).max())
    a = core * shade * (1 - p["mottle"] * 0.5 * (1 + mot)) * (1 - dry)
    return np.clip(np.maximum(a, halo), 0, 1)


def compose(fk, sk, bg_key, seed=2026):
    bg, art_sha = paper_bg(seed, BG_PCT[bg_key])
    mask, boxes = glyph_masks(fk)
    a = ink_alpha(mask, boxes, STRENGTH[sk], seed + int(fk))
    layer = Image.new("RGBA", (AV, AV), INK + (0,))
    layer.putalpha(Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8)))
    out = bg.convert("RGBA")
    out.alpha_composite(layer)
    return out.convert("RGB"), layer, boxes, art_sha


def legibility(img, fk):
    """110px 판독 지표: 110px 축소본에서 글자 칸(잉크 마스크) 평균 휘도 vs 바탕 휘도 차, 그리고
    질감 없는 순수 마스크 110px 과의 상관계수(1에 가까울수록 형태 보존)."""
    mask, _ = glyph_masks(fk)
    sm = np.asarray(rp.circle_crop(img, (AV / 2, AV / 2), AV, 110).convert("L")).astype(np.float32)
    mk = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).resize((110, 110), Image.LANCZOS)).astype(np.float32) / 255
    yy, xx = np.mgrid[0:110, 0:110]
    circ = (xx - 54.5) ** 2 + (yy - 54.5) ** 2 < 52 ** 2
    ink = sm[(mk > 0.6) & circ].mean()
    paper = sm[(mk < 0.02) & circ].mean()
    corr = np.corrcoef((255 - sm)[circ], mk[circ])[0, 1]
    return {"ink_L": round(float(ink), 1), "bg_L": round(float(paper), 1),
            "delta_L": round(float(paper - ink), 1), "shape_corr": round(float(corr), 3)}


def save_set(img, name):
    img.save(os.path.join(OUT_DIR, f"{name}.png"), optimize=True)
    img.resize((320, 320), Image.LANCZOS).save(os.path.join(OUT_DIR, f"{name}-320.png"), optimize=True)
    rp.circle_crop(img, (AV / 2, AV / 2), AV, 110).save(os.path.join(OUT_DIR, f"{name}-110.png"), optimize=True)


def cell(sheet, d, fnt, x, y, img, title, sub, hl=False):
    """한 칸: 1080 정사각(320 축소) + 320 원형 + 110 원형(실제 크기) + 라벨."""
    sq = img.resize((320, 320), Image.LANCZOS)
    sheet.paste(sq, (x, y))
    c = rp.circle_crop(img, (AV / 2, AV / 2), AV, 320)
    sheet.paste(c, (x, y + 340), c)
    s = rp.circle_crop(img, (AV / 2, AV / 2), AV, 110)
    sheet.paste(s, (x + 105, y + 680), s)
    d.text((x + 160, y + 806), title, font=rc.font(fnt, 26), fill=rp.APP_TEXT, anchor="ma")
    d.text((x + 160, y + 842), sub, font=rc.font(fnt, 19), fill="#6B6B6B", anchor="ma")
    if hl:
        d.rectangle((x - 10, y - 10, x + 330, y + 876), outline="#C8102E", width=3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", action="store_true")
    ap.add_argument("--strength", default="강", help="1행 채택 강도(110·320px 판독 유지 최대 = 강)")
    ap.add_argument("--rec", default="3", help="추천 서체 키(2행 비교 대상)")
    a = ap.parse_args()
    if a.download:
        v3.download()
    fonts = rc.load_fonts()
    recs = {"fonts": [], "strength_compare": [], "bg_compare": []}
    row1 = []
    for fk in ("1", "2", "3"):
        img, layer, boxes, art_sha = compose(fk, a.strength, "20")
        save_set(img, f"avatar-v8-{fk}")
        leg = legibility(img, fk)
        r = {"key": fk, "family": FONTS[fk]["family"], "license": "SIL OFL 1.1",
             "source_url": GF + FONTS[fk]["path"], "license_url": GF + FONTS[fk]["lic"],
             "sha256": sha(font_path(fk)), "layout_ink_h_dx_rot": LAYOUT[fk], "gap": GAP,
             "glyph_ink_heights_px": [b[3] - b[1] for b in boxes],
             "column_height_px": boxes[-1][3] - boxes[0][1],
             "strength": a.strength, "ink_params": STRENGTH[a.strength], "bg_pct": 20,
             "max_radius": {"ink": rp.max_radius(layer, (AV / 2, AV / 2), thr=60), "limit": SAFE_R},
             "legibility_110": leg}
        recs["fonts"].append(r)
        row1.append((img, r))
        print(fk, FONTS[fk]["family"], r["glyph_ink_heights_px"], r["column_height_px"], r["max_radius"], leg)
    row2 = []
    for sk in ("약", "중", "강"):
        img, _, _, _ = compose(a.rec, sk, "20")
        leg = legibility(img, a.rec)
        recs["strength_compare"].append({"font": a.rec, "strength": sk, "params": STRENGTH[sk], "legibility_110": leg})
        row2.append((img, sk, leg))
        print("strength", sk, leg)
    row3 = []
    for bk in ("18", "20", "22"):
        img, _, _, _ = compose(a.rec, a.strength, bk)
        recs["bg_compare"].append({"font": a.rec, "bg_pct": int(bk), "legibility_110": legibility(img, a.rec)})
        row3.append((img, bk))
    # 컨택트시트
    cw, gap, pad, head = 320, 44, 50, 90
    W = pad * 2 + cw * 4 + gap * 3
    rowh = 900
    H = head + rowh * 2 + 60 + 420
    sheet = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(sheet)
    fnt = fonts["body"]
    d.text((pad, 26), "프로필 사진 v8 — v4 A 구도 · 바탕 20% · 낙관 0 · 붓글씨 먹 질감 (정사각 / 320 원형 / 110 원형)",
           font=rc.font(fnt, 26), fill=rp.APP_TEXT)
    y1 = head
    cur = Image.open(os.path.join(OUT_DIR, "avatar-v4-A.png")).convert("RGB")
    cell(sheet, d, fnt, pad, y1, cur, "현재 v4 A", "Nanum Brush · 바탕15% · 낙관")
    for i, (img, r) in enumerate(row1):
        cell(sheet, d, fnt, pad + (i + 1) * (cw + gap), y1, img, f"v8-{r['key']} {r['family'].split(' (')[0]}",
             f"먹 처리 {a.strength} · 바탕 20%", hl=(r["key"] == a.rec))
    y2 = head + rowh + 30
    d.text((pad, y2 + 300), f"2행: v8-{a.rec}", font=rc.font(fnt, 24), fill=rp.APP_TEXT)
    d.text((pad, y2 + 336), "먹 처리 강도 비교", font=rc.font(fnt, 22), fill="#6B6B6B")
    d.text((pad, y2 + 368), "(번짐·갈필·농담)", font=rc.font(fnt, 20), fill="#6B6B6B")
    for i, (img, sk, leg) in enumerate(row2):
        cell(sheet, d, fnt, pad + (i + 1) * (cw + gap), y2, img, f"먹 처리 {sk}",
             f"110px ΔL {leg['delta_L']} · 형태 {leg['shape_corr']}", hl=(sk == a.strength))
    y3 = y2 + rowh + 30
    d.text((pad, y3 + 10), f"바탕 18/20/22% (v8-{a.rec}, 먹 {a.strength}) — 320 원형", font=rc.font(fnt, 22), fill=rp.APP_TEXT)
    for i, (img, bk) in enumerate(row3):
        c = rp.circle_crop(img, (AV / 2, AV / 2), AV, 320)
        sheet.paste(c, (pad + (i + 1) * (cw + gap), y3 + 50), c)
        d.text((pad + (i + 1) * (cw + gap) + 160, y3 + 50 + 330), f"바탕 {bk}%", font=rc.font(fnt, 22),
               fill=rp.APP_TEXT, anchor="ma")
    sheet.save(os.path.join(OUT_DIR, "contact-profile-v8.png"), optimize=True)
    art = {k: BG_SRC[k] for k in ("title", "title_ko", "institution", "accession", "object_url", "url",
                                  "license", "license_url", "credit_short", "crop")}
    rec = {"version": "v8", "composition": "v4 A (세로 3자 '책가도', 한지색 원 + 원화 바탕)", "seal": None,
           "text": "책가도", "ink_color": "#161413", "fake_bold": False, "ai_generated": False,
           "background_art": art | {"src_sha256": sha(os.path.join(v3.SRC_DIR, BG_SRC["file"])), "opacity": 0.20,
                                    "saturation": -0.20, "hanji_cover_around_text": False},
           "paper": "#F7F3EA x hanji 15% x sepia (v4와 동일)", "adopted_strength": a.strength,
           "recommended_font": a.rec, "strengths": STRENGTH, **recs}
    with open(os.path.join(OUT_DIR, "avatar-v8-RENDER.json"), "w", encoding="utf-8") as fp:
        json.dump(rec, fp, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
