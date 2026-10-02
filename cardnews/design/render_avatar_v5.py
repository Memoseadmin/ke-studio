#!/usr/bin/env python3
"""책가도 노트 프로필 사진 v5: 대표 피드백(2026-10-02) 반영 3안. 코드 렌더만(AI 생성 0).

피드백: "낙관 '책'은 좀 별로다. 뒤의 책가도 바탕이 너무 희미하다(선명하지 않다)."
  v5-A 낙관 없음 + 바탕 가시성 3단계(45/60/75%) 중 110px 판독 유지 최대값 채택
  v5-B 붉은 '책' 낙관 -> 먹색 백문 소인 '노트'(세로 2자, 서체 글자를 그림으로)
  v5-C 바탕 주인공(가시성 85%) + 한지색 띠 위 가로 "책가도"

사용:
  bash scripts/setup.sh                                    # 서체(~/.fonts/ke/, 커밋 안 함)
  python3 cardnews/design/render_avatar_v5.py --download   # 원화 -> render/avatar-v3/src/ (커밋 제외)
  python3 cardnews/design/render_avatar_v5.py

산출물(cardnews/profile/, v4 이전 파일은 건드리지 않음):
  avatar-v5-A/B/C.png, -320.png, -110.png   정사각(업로드용, 원형 크롭은 플랫폼이 함)
  contact-profile-v5.png                     v4 A(현재) + v5 3안, 원형 320/110 + 가시성 %, 아래 A 단계 3개
  avatar-v5-RENDER.json                      설정·가시성 단계·판독 수치·채택값

가시성 % = 원화 크롭(채도 -20% + lut-v1)을 한지 바탕 위에 섞는 불투명도. v4 = 15%.
판독 = 110px 원형 축소본에서 글자 획(마스크>0.6) 평균 휘도 vs 획 바깥 2~4px 고리 평균 휘도의 WCAG 대비비.
  채택 기준 4.5:1 이상(WCAG AA 본문 기준을 빌린 추정 문턱) + 축소본 육안 확인.
"""
import argparse
import hashlib
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_cards as rc  # noqa: E402  (수정하지 않음)
import render_profile as rp  # noqa: E402  (circle_crop·max_radius, 수정하지 않음)
import render_avatar_v3 as v3  # noqa: E402  (hanji_texture·common_lut·download, 수정하지 않음)
import render_avatar_v4 as v4  # noqa: E402  (paper_bg·ink_layer·FONTS, 수정하지 않음)

OUT_DIR = os.path.join(os.path.dirname(HERE), "profile")
AV, SAFE_R = v3.AV, v3.SAFE_R
PAPER = (0xF7, 0xF3, 0xEA)
INK = v4.INK
BG_SRC = v3.SOURCES[0]  # 클리블랜드미술관 〈책가도〉 2011.37 CC0
SAT = 0.80  # 채도 -20% (§8-3, 추정치)
STEPS_A = [0.45, 0.60, 0.75]
CR_MIN = 4.5
HALO = {"dilate": 31, "blur": 16, "alpha": 0.82}  # 글자 뒤 한지색 여백(먹 번짐 바깥), 진한 남색·밤색 칸 위 판독용

# v4 A와 같은 글자 배치(세로 3자). 크롭: A·B = v4와 같은 부위, C = 아래 칸 기물이 더 크게 보이게 조금 당김.
VERT = [("책", "nanum_brush", 300, 290), ("가", "nanum_brush", 300, 520), ("도", "nanum_brush", 300, 750)]
CROP_AB = [1372, 182, 2028, 838]
CROP_C = [1388, 262, 1948, 822]
CROP_NOTE = {
    "AB": "10폭 중 5~6폭 위 2단(v3 A·v4 A와 같음): 왼쪽 위 책갑 5권, 오른쪽 위 쌓인 책, 왼쪽 아래 찬합·붉은 항아리·빙렬 병, 오른쪽 아래 책갑",
    "C": "같은 원화 5~6폭, 위·왼쪽을 조금 잘라 아래 칸 기물(찬합·붉은 항아리·빙렬 병)과 책갑 붉은 책끈을 크게",
}


def sha(p):
    with open(p, "rb") as fp:
        return hashlib.sha256(fp.read()).hexdigest()


def art(crop):
    src = os.path.join(v3.SRC_DIR, BG_SRC["file"])
    if not os.path.exists(src):
        sys.exit(f"원본 없음: {src}  (먼저 --download)")
    im = Image.open(src).convert("RGB").crop(tuple(crop)).resize((AV, AV), Image.LANCZOS)
    return v3.common_lut(ImageEnhance.Color(im).enhance(SAT)), sha(src)


def text_mask(lines, x):
    """v4.ink_layer와 같은 글자 마스크(번짐·그레인 전), 여백·판독 계산용."""
    SS = 2
    m = Image.new("L", (AV * SS, AV * SS), 0)
    d = ImageDraw.Draw(m)
    for txt, fk, size, cy in lines:
        d.text((x * SS, cy * SS), txt, font=ImageFont.truetype(v4.font_path(fk), size * SS), fill=255, anchor="mm")
    return m.resize((AV, AV), Image.LANCZOS).filter(ImageFilter.MaxFilter(9))


def halo(img, mask, alpha):
    """글자 둘레만 한지색으로 살짝 덮는다(원화 내용 변형 아님, 위에 얹는 반투명 층)."""
    h = mask.filter(ImageFilter.MaxFilter(HALO["dilate"])).filter(ImageFilter.GaussianBlur(HALO["blur"]))
    a = np.asarray(h).astype(np.float32)[..., None] / 255 * alpha
    out = np.asarray(img).astype(np.float32) * (1 - a) + np.array(PAPER, np.float32) * a
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def band(img, y0, y1, alpha=0.92, feather=10):
    """한지색 가로 띠(바탕 위, 가장자리만 살짝 풀어짐) + 한지 결."""
    m = Image.new("L", (AV, AV), 0)
    ImageDraw.Draw(m).rectangle([0, y0, AV, y1], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(feather))
    tex = v3.hanji_texture((AV, AV), seed=77)[..., None]
    paper = np.array(PAPER, np.float32) * (0.85 + 0.15 * tex) * np.array(v3.SEPIA, np.float32)
    a = np.asarray(m).astype(np.float32)[..., None] / 255 * alpha
    out = np.asarray(img).astype(np.float32) * (1 - a) + paper * a
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def mono_seal(center, size, seed):
    """먹색 백문 소인: 정사각 먹면 + 종이색 세로 '노트'(Nanum Brush 글자를 그림으로). 붉은색·'책' 없음."""
    cx, cy = center
    h = size / 2
    SS = 3
    m = Image.new("L", (AV * SS, AV * SS), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([(cx - h) * SS, (cy - h * 1.35) * SS, (cx + h) * SS, (cy + h * 1.35) * SS], radius=6 * SS, fill=255)
    f = ImageFont.truetype(v4.font_path("nanum_brush"), int(size * 0.92) * SS)
    for ch, dy in (("노", -0.62), ("트", 0.58)):
        d.text((cx * SS, (cy + dy * h) * SS), ch, font=f, fill=0, anchor="mm")
    m = m.resize((AV, AV), Image.LANCZOS)
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (AV // 6, AV // 6)).astype(np.float32)
    n = np.array(Image.fromarray(n).resize((AV, AV), Image.BILINEAR))
    n = (n - n.min()) / max(1e-6, n.max() - n.min())
    a = np.asarray(m).astype(np.float32) * (0.80 + 0.15 * n)
    layer = Image.new("RGBA", (AV, AV), (34, 30, 28, 0))
    layer.putalpha(Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0)))
    return layer


def _lin(v):
    v = v / 255
    return np.where(v <= 0.03928, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def legibility_110(img, mask):
    """110px 원형 축소본에서 획 vs 획 바깥 고리 WCAG 대비비."""
    s = 110
    im = np.asarray(img.resize((s, s), Image.LANCZOS)).astype(np.float32)
    mk = mask.resize((s, s), Image.LANCZOS)
    core = np.asarray(mk).astype(np.float32) / 255 > 0.6
    ring = np.asarray(mk.filter(ImageFilter.MaxFilter(7))).astype(np.float32) / 255 > 0.3
    ring &= ~(np.asarray(mk.filter(ImageFilter.MaxFilter(3))).astype(np.float32) / 255 > 0.1)
    L = 0.2126 * _lin(im[..., 0]) + 0.7152 * _lin(im[..., 1]) + 0.0722 * _lin(im[..., 2])
    li, lo = float(L[core].mean()), float(L[ring].mean())
    return round((max(li, lo) + 0.05) / (min(li, lo) + 0.05), 2)


def detail_score(img, mask):
    """바탕 디테일 선명도(추정 지표): 글자·여백 밖 원 안 영역 휘도 표준편차(0~255)."""
    g = np.asarray(img.convert("L")).astype(np.float32)
    yy, xx = np.mgrid[0:AV, 0:AV]
    inside = (xx - AV / 2) ** 2 + (yy - AV / 2) ** 2 < SAFE_R ** 2
    away = np.asarray(mask.filter(ImageFilter.MaxFilter(61))) < 10
    return round(float(g[inside & away].std()), 1)


def compose(vis, crop, seed, lines, x, halo_alpha, extra=None):
    bg = v4.paper_bg(seed)
    a_img, a_sha = art(crop)
    bg = Image.blend(bg, a_img, vis)
    mask = text_mask(lines, x)
    if extra:
        bg = extra(bg)
    if halo_alpha:
        bg = halo(bg, mask, halo_alpha)
    ink = v4.ink_layer({"lines": lines, "x": x, "weight": 9}, seed)
    out = bg.convert("RGBA")
    out.alpha_composite(ink)
    return out, ink, mask, a_sha


def art_rec(crop, note, vis, a_sha):
    return ({k: BG_SRC[k] for k in ("title", "title_ko", "institution", "accession", "object_url", "url",
                                    "license", "license_url", "credit_short")}
            | {"crop": crop, "crop_note": note, "src_sha256": a_sha, "visibility": vis, "saturation": -0.20,
               "lut": "render_avatar_v3.common_lut (lut-v1)"})


def font_rec():
    f = v4.FONTS["nanum_brush"]
    return [{**{k: f[k] for k in ("family", "license", "source_url", "license_url")},
             "sha256": sha(v4.font_path("nanum_brush"))}]


BASE_STEPS = ["paper #F7F3EA", "hanji multiply 15% (procedural)", "sepia warm R x1.035 G x1.005 B x0.94 (estimate)"]
INK_STEP = "ink: render_avatar_v4.ink_layer (Nanum Brush, dilate 9px, bleed 22%, dry-brush grain)"


def render_A():
    seed = 2026 + ord("A")
    steps = []
    for vis in STEPS_A:
        out, ink, mask, a_sha = compose(vis, CROP_AB, seed, VERT, 470, HALO["alpha"])
        out = out.convert("RGB")
        steps.append({"visibility": vis, "img": out, "cr110": legibility_110(out, mask),
                      "detail_std": detail_score(out, mask), "ink": ink, "mask": mask, "sha": a_sha})
    ok = [s for s in steps if s["cr110"] >= CR_MIN]
    pick = (ok or steps[:1])[-1]
    rec = {
        "key": "A", "name": "낙관 없음(세로 책가도)", "text": "책가도", "method": "code_render",
        "fonts": font_rec(), "background_art": art_rec(CROP_AB, CROP_NOTE["AB"], pick["visibility"], pick["sha"]),
        "visibility_steps": [{"visibility": s["visibility"], "contrast_110": s["cr110"], "detail_std": s["detail_std"],
                              "pass": s["cr110"] >= CR_MIN} for s in steps],
        "adopted_visibility": pick["visibility"],
        "steps": BASE_STEPS + [f"art crop saturation -20% + lut-v1, opacity {int(pick['visibility']*100)}%",
                               f"halo: paper color under text, mask max{HALO['dilate']}+blur{HALO['blur']}, alpha {HALO['alpha']}",
                               INK_STEP, "seal: none"],
        "max_radius": {"ink": rp.max_radius(pick["ink"], (AV / 2, AV / 2), thr=60), "limit": SAFE_R},
        "legibility_110": {"contrast": pick["cr110"], "threshold": CR_MIN},
        "ai_generated": False, "content_changed": False,
    }
    return pick["img"], rec, steps


def render_B(vis):
    seed = 2026 + ord("B")
    out, ink, mask, a_sha = compose(vis, CROP_AB, seed, VERT, 470, HALO["alpha"])
    seal_c, seal_s = (660, 800), 84
    # 소인 둘레도 같은 한지색 여백
    sm = Image.new("L", (AV, AV), 0)
    ImageDraw.Draw(sm).rectangle([seal_c[0] - 50, seal_c[1] - 64, seal_c[0] + 50, seal_c[1] + 64], fill=255)
    rgb = halo(out.convert("RGB"), sm, HALO["alpha"]).convert("RGBA")
    rgb.alpha_composite(ink)
    seal = mono_seal(seal_c, seal_s, seed=ord("B"))
    rgb.alpha_composite(seal)
    out = rgb.convert("RGB")
    cr = legibility_110(out, mask)
    rec = {
        "key": "B", "name": "먹색 소인 '노트'", "text": "책가도 + 소인 노트", "method": "code_render",
        "fonts": font_rec(), "background_art": art_rec(CROP_AB, CROP_NOTE["AB"], vis, a_sha),
        "seal": {"type": "먹색 백문 소인(세로 2자 '노트')", "color": "#221E1C, 알파 0.80~0.95 얼룩", "center": seal_c,
                 "size_px": [seal_s, int(seal_s * 1.35)], "red": False},
        "steps": BASE_STEPS + [f"art crop saturation -20% + lut-v1, opacity {int(vis*100)}% (= v5-A 채택값)",
                               f"halo alpha {HALO['alpha']} (글자 + 소인 둘레)", INK_STEP,
                               "seal: mono_seal 노트 (Nanum Brush 글자를 백문으로 뚫음)"],
        "max_radius": {"ink": rp.max_radius(ink, (AV / 2, AV / 2), thr=60),
                       "seal": rp.max_radius(seal, (AV / 2, AV / 2)), "limit": SAFE_R},
        "legibility_110": {"contrast": cr, "threshold": CR_MIN, "seal_note": "소인 '노트'는 110px에서 장식(판독 대상 아님), 320px에서 판독"},
        "ai_generated": False, "content_changed": False,
    }
    return out, rec


def render_C():
    seed = 2026 + ord("C")
    vis = 0.85
    y0, y1 = 425, 655
    lines = [("책가도", "nanum_brush", 280, 548)]
    out, ink, mask, a_sha = compose(vis, CROP_C, seed, lines, 540, 0, extra=lambda im: band(im, y0, y1))
    out = out.convert("RGB")
    cr = legibility_110(out, mask)
    rec = {
        "key": "C", "name": "바탕 주인공(한지 띠 가로)", "text": "책가도", "method": "code_render",
        "fonts": font_rec(), "background_art": art_rec(CROP_C, CROP_NOTE["C"], vis, a_sha),
        "band": {"y": [y0, y1], "color": "paper #F7F3EA x hanji 15% x sepia", "alpha": 0.92, "feather_px": 10},
        "steps": BASE_STEPS + [f"art crop saturation -20% + lut-v1, opacity {int(vis*100)}%",
                               f"hanji band y{y0}-{y1} alpha 0.92", INK_STEP, "seal: none"],
        "max_radius": {"ink": rp.max_radius(ink, (AV / 2, AV / 2), thr=60), "limit": SAFE_R},
        "legibility_110": {"contrast": cr, "threshold": CR_MIN},
        "detail_std": detail_score(out, mask),
        "ai_generated": False, "content_changed": False,
    }
    return out, rec


def contact(cols, a_steps, fonts):
    big, small, gap, pad, head = 300, 110, 48, 48, 74
    n = len(cols)
    W = pad * 2 + big * n + gap * (n - 1)
    row1 = head + big + 28 + small + 120
    sub_big = 220
    H = row1 + 60 + sub_big + 24 + small + 90
    sheet = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(sheet)
    body = lambda s: rc.font(fonts["body"], s)  # noqa: E731
    d.text((pad, 24), "프로필 사진 v5 — 대표 피드백 반영(낙관 '책' 빼기·바탕 선명하게) / 원형 300px · 110px",
           font=body(26), fill=rp.APP_TEXT)

    def put(img, x, y, b, s, lab, sub):
        c = rp.circle_crop(img, (AV / 2, AV / 2), AV, b)
        sheet.paste(c, (x, y), c)
        sm = rp.circle_crop(img, (AV / 2, AV / 2), AV, s)
        sy = y + b + 24
        sheet.paste(sm, (x + (b - s) // 2, sy), sm)
        ly = sy + s + 20
        d.text((x + b // 2, ly), lab, font=body(26), fill=rp.APP_TEXT, anchor="ma", stroke_width=1, stroke_fill=rp.APP_TEXT)
        d.text((x + b // 2, ly + 38), sub, font=body(20), fill="#6B6B6B", anchor="ma")

    for i, (img, lab, sub) in enumerate(cols):
        put(img, pad + i * (big + gap), head, big, small, lab, sub)
    y = row1 + 10
    d.line([(pad, y), (W - pad, y)], fill="#E0E0E0", width=2)
    d.text((pad, y + 14), f"v5-A 바탕 가시성 3단계 (110px 대비비 {CR_MIN}:1 이상 중 최대 채택)", font=body(22), fill=rp.APP_TEXT)
    for i, s in enumerate(a_steps):
        x = pad + i * (sub_big + gap * 2) + 40
        mark = "채택" if s.get("adopted") else ("통과" if s["cr110"] >= CR_MIN else "미달")
        put(s["img"], x, y + 56, sub_big, small, f"가시성 {int(s['visibility']*100)}%",
            f"110px 대비 {s['cr110']}:1 · {mark}")
    return sheet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", action="store_true")
    a = ap.parse_args()
    if a.download:
        v3.download()
    fonts = rc.load_fonts()
    names = [f"avatar-v5-{k}{s}.png" for k in "ABC" for s in ("", "-320", "-110")] + ["contact-profile-v5.png", "avatar-v5-RENDER.json"]
    clash = [n for n in names if os.path.exists(os.path.join(OUT_DIR, n))]
    if clash and os.environ.get("KE_V5_REWRITE") != "1":
        sys.exit(f"이미 있음(덮어쓰지 않음): {clash}  (v5 재렌더 의도면 KE_V5_REWRITE=1)")
    imA, recA, stepsA = render_A()
    for s in stepsA:
        s["adopted"] = s["visibility"] == recA["adopted_visibility"]
    imB, recB = render_B(recA["adopted_visibility"])
    imC, recC = render_C()
    for img, rec in ((imA, recA), (imB, recB), (imC, recC)):
        k = rec["key"]
        img.save(os.path.join(OUT_DIR, f"avatar-v5-{k}.png"), optimize=True)
        for s in (320, 110):
            img.resize((s, s), Image.LANCZOS).save(os.path.join(OUT_DIR, f"avatar-v5-{k}-{s}.png"), optimize=True)
        print(k, "vis", rec["background_art"]["visibility"], "cr110", rec["legibility_110"]["contrast"], "r", rec["max_radius"])
    for s in stepsA:
        print("A step", s["visibility"], "cr110", s["cr110"], "detail", s["detail_std"])
    v4a = Image.open(os.path.join(OUT_DIR, "avatar-v4-A.png")).convert("RGB")
    cols = [(v4a, "현재  v4 A", "바탕 15% · 붉은 낙관"),
            (imA, "v5-A  낙관 없음", f"바탕 {int(recA['adopted_visibility']*100)}% · 110px {recA['legibility_110']['contrast']}:1"),
            (imB, "v5-B  먹색 소인", f"바탕 {int(recB['background_art']['visibility']*100)}% · 110px {recB['legibility_110']['contrast']}:1"),
            (imC, "v5-C  바탕 주인공", f"바탕 85% · 110px {recC['legibility_110']['contrast']}:1")]
    contact(cols, stepsA, fonts).save(os.path.join(OUT_DIR, "contact-profile-v5.png"), optimize=True)
    meta = {"feedback": "2026-10-02 대표: 낙관 '책' 별로, 책가도 바탕 너무 희미", "visibility_def": "원화 크롭 블렌드 불투명도(v4 = 0.15)",
            "legibility_def": "110px 축소본 획 vs 획 바깥 고리 WCAG 대비비, 문턱 4.5(추정)", "halo": HALO,
            "variants": [recA, recB, recC]}
    with open(os.path.join(OUT_DIR, "avatar-v5-RENDER.json"), "w", encoding="utf-8") as fp:
        json.dump(meta, fp, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
