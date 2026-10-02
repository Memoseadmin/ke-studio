#!/usr/bin/env python3
"""책가도 노트 프로필 사진 v4 폴백: 코드 렌더 붓글씨 + 한지 바탕 + 붉은 낙관 하나.

대표 결정(2026-10-02): v3(원화 크롭+낙관) 보류 -> v4 = AI 생성 또는 붓글씨.
이 스크립트는 생성 키가 없을 때의 폴백(AI 생성 0). AI 안은 profile/AVATAR-v4-PROMPTS.md.

사용:
  bash scripts/setup.sh                              # 서체 다운로드(~/.fonts/ke/, 커밋 안 함)
  python3 cardnews/design/render_avatar_v4.py --download   # 원화 1점 -> render/avatar-v3/src/ (커밋 제외)
  python3 cardnews/design/render_avatar_v4.py

산출물(cardnews/profile/):
  avatar-v4-A/B/C.png       1080x1080 (글자·낙관 = 중앙 지름 860 원 안, 원형 크롭 안전 영역 80%)
  avatar-v4-A/B/C-320.png   320x320
  contact-profile-v4.png    3안 원형 미리보기(320px + 110px) 나란히, 라벨 "코드 렌더"
  avatar-v4-RENDER.json     서체·원화·단계 기록

원칙: 서체는 OFL만(글자를 그림으로 렌더 = 서체 수정·재배포 아님). 원화는 바탕 디테일로만(채도 -20%, 15% 불투명),
내용 변형 없음. 낙관 = render_avatar_v3.seal_layer 재사용(글꼴 미사용 '책'). 실존 인물·로고·호랑이·까치 0.
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
import render_cards as rc  # noqa: E402  (토큰·폰트, 수정하지 않음)
import render_profile as rp  # noqa: E402  (circle_crop·max_radius, 수정하지 않음)
import render_avatar_v3 as v3  # noqa: E402  (hanji_texture·common_lut·seal_layer·download, 수정하지 않음)

T = rc.TOKENS
OUT_DIR = os.path.join(os.path.dirname(HERE), "profile")
FONT_DIR = os.path.expanduser("~/.fonts/ke")
AV = v3.AV
SAFE_R = v3.SAFE_R
INK = (17, 17, 17)

FONTS = {
    "nanum_brush": {
        "file": "nanumbrushscript_NanumBrushScript-Regular.ttf",
        "family": "Nanum Brush Script",
        "license": "SIL OFL 1.1",
        "source_url": "https://raw.githubusercontent.com/google/fonts/main/ofl/nanumbrushscript/NanumBrushScript-Regular.ttf",
        "license_url": "https://raw.githubusercontent.com/google/fonts/main/ofl/nanumbrushscript/OFL.txt",
    },
    "east_sea_dokdo": {
        "file": "eastseadokdo_EastSeaDokdo-Regular.ttf",
        "family": "East Sea Dokdo",
        "license": "SIL OFL 1.1",
        "source_url": "https://raw.githubusercontent.com/google/fonts/main/ofl/eastseadokdo/EastSeaDokdo-Regular.ttf",
        "license_url": "https://raw.githubusercontent.com/google/fonts/main/ofl/eastseadokdo/OFL.txt",
    },
}

BG_SRC = v3.SOURCES[0]  # 클리블랜드미술관 〈책가도〉 2011.37 CC0 (v3 A와 같은 원본·크롭)

# lines: (글자, 서체 키, 크기px, 중심 y). seal: 낙관 중심.
VARIANTS = [
    {"key": "A", "name": "책가도(세로)", "text": "책가도", "bg_art": True,
     "lines": [("책", "nanum_brush", 300, 290), ("가", "nanum_brush", 300, 520), ("도", "nanum_brush", 300, 750)],
     "x": 470, "seal": (680, 770), "weight": 9},
    {"key": "B", "name": "책가도 노트", "text": "책가도 노트", "bg_art": False,
     "lines": [("책가도", "nanum_brush", 340, 440), ("노트", "nanum_brush", 240, 680)],
     "x": 520, "seal": (770, 690), "weight": 9},
    {"key": "C", "name": "노트", "text": "노트", "bg_art": False,
     "lines": [("노트", "east_sea_dokdo", 580, 500)],
     "x": 510, "seal": (790, 740), "weight": 3},
]


def font_path(k):
    p = os.path.join(FONT_DIR, FONTS[k]["file"])
    if not os.path.exists(p):
        sys.exit(f"서체 없음: {p}  (bash scripts/setup.sh 의 서체 블록)")
    return p


def sha(p):
    with open(p, "rb") as fp:
        return hashlib.sha256(fp.read()).hexdigest()


def paper_bg(seed):
    """§8-3 v1.2 톤의 한지 바탕: paper #F7F3EA x 한지 질감(15%) x 세피아 기미."""
    base = np.ones((AV, AV, 3), np.float32) * np.array([0xF7, 0xF3, 0xEA], np.float32)
    tex = v3.hanji_texture((AV, AV), seed=seed)[..., None]
    arr = base * (1 - 0.15 + 0.15 * tex) * np.array(v3.SEPIA, np.float32)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def art_overlay(bg):
    """원화 디테일을 바탕에 살짝: 채도 -20% + LUT, 불투명도 15%. 내용 변형 없음(크롭·톤·투명도만)."""
    src = os.path.join(v3.SRC_DIR, BG_SRC["file"])
    if not os.path.exists(src):
        sys.exit(f"원본 없음: {src}  (먼저 --download)")
    im = Image.open(src).convert("RGB").crop(tuple(BG_SRC["crop"])).resize((AV, AV), Image.LANCZOS)
    im = v3.common_lut(ImageEnhance.Color(im).enhance(0.80))
    return Image.blend(bg, im, 0.15), sha(src)


def ink_layer(v, seed):
    """글자 마스크 -> 먹 번짐(바깥 흐린 테) + 마른붓 그레인(알파 흔들림). RGBA."""
    SS = 2
    m = Image.new("L", (AV * SS, AV * SS), 0)
    d = ImageDraw.Draw(m)
    for txt, fk, size, cy in v["lines"]:
        f = ImageFont.truetype(font_path(fk), size * SS)
        d.text((v["x"] * SS, cy * SS), txt, font=f, fill=255, anchor="mm")
    m = m.resize((AV, AV), Image.LANCZOS)
    if v["weight"] > 1:  # 붓 획 굵기 보정(110px 판독용): 마스크 팽창 후 가장자리 부드럽게
        m = m.filter(ImageFilter.MaxFilter(v["weight"])).filter(ImageFilter.GaussianBlur(1.0))
    core = np.asarray(m).astype(np.float32) / 255
    bleed = np.asarray(m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255
    rng = np.random.default_rng(seed)
    g = rng.normal(0, 1, (AV // 3, AV // 3)).astype(np.float32)
    g = np.array(Image.fromarray(g).resize((AV, AV), Image.BILINEAR))
    g = (g - g.min()) / max(1e-6, g.max() - g.min())
    fine = rng.random((AV, AV)).astype(np.float32)
    a = np.maximum(core * (0.86 + 0.14 * g) * (0.93 + 0.07 * fine), bleed * 0.22)
    layer = Image.new("RGBA", (AV, AV), INK + (0,))
    layer.putalpha(Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8)))
    return layer


def render_one(v):
    seed = 2026 + ord(v["key"])
    bg = paper_bg(seed)
    steps = ["paper #F7F3EA", "hanji multiply 15% (procedural)", "sepia warm R x1.035 G x1.005 B x0.94 (estimate)"]
    art_sha = None
    if v["bg_art"]:
        bg, art_sha = art_overlay(bg)
        steps.append("original crop (v3 A) saturation -20% + lut-v1, opacity 15%")
    ink = ink_layer(v, seed)
    steps.append(f"ink: brush font mask dilate {v['weight']}px, bleed halo 22% (max5+blur6), dry-brush grain")
    seal = v3.seal_layer(v["seal"], seed=ord(v["key"]))
    steps.append("seal: render_avatar_v3.seal_layer (red #C8102E, '책' 도형 조립)")
    out = bg.convert("RGBA")
    out.alpha_composite(ink)
    out.alpha_composite(seal)
    out = out.convert("RGB")
    r_ink = rp.max_radius(ink, (AV / 2, AV / 2), thr=60)
    r_seal = rp.max_radius(seal, (AV / 2, AV / 2))
    fonts_used = sorted({fk for _, fk, _, _ in v["lines"]})
    rec = {
        "key": v["key"], "name": v["name"], "text": v["text"], "method": "code_render",
        "fonts": [{**{k: FONTS[fk][k] for k in ("family", "license", "source_url", "license_url")},
                   "sha256": sha(font_path(fk))} for fk in fonts_used],
        "background_art": ({k: BG_SRC[k] for k in ("title", "title_ko", "institution", "accession", "object_url",
                                                  "url", "license", "license_url", "credit_short", "crop")}
                           | {"src_sha256": art_sha, "opacity": 0.15, "saturation": -0.20}) if v["bg_art"] else None,
        "steps": steps,
        "max_radius": {"ink": r_ink, "seal": r_seal, "limit": SAFE_R},
        "ai_generated": False, "content_changed": False,
    }
    return out, rec


def contact(results, fonts):
    big, small, gap, pad, head = 320, 110, 64, 56, 70
    W = pad * 2 + big * 3 + gap * 2
    H = head + big + 36 + small + 140
    sheet = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(sheet)
    d.text((pad, 22), "프로필 사진 v4 — 원형 크롭 320px / 110px (붓글씨 3안)", font=rc.font(fonts["body"], 26), fill=rp.APP_TEXT)
    for i, (img, rec) in enumerate(results):
        x = pad + i * (big + gap)
        bg = rp.circle_crop(img, (AV / 2, AV / 2), AV, big)
        sheet.paste(bg, (x, head), bg)
        sm = rp.circle_crop(img, (AV / 2, AV / 2), AV, small)
        sy = head + big + 36
        sheet.paste(sm, (x + (big - small) // 2, sy), sm)
        ly = sy + small + 28
        d.text((x + big // 2, ly), f"{rec['key']}  {rec['name']}", font=rc.font(fonts["body"], 30),
               fill=rp.APP_TEXT, anchor="ma", stroke_width=1, stroke_fill=rp.APP_TEXT)
        d.text((x + big // 2, ly + 44), "코드 렌더", font=rc.font(fonts["body"], 22), fill="#6B6B6B", anchor="ma")
    return sheet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", action="store_true")
    a = ap.parse_args()
    if a.download:
        v3.download()
    fonts = rc.load_fonts()
    results = []
    for v in VARIANTS:
        img, rec = render_one(v)
        img.save(os.path.join(OUT_DIR, f"avatar-v4-{v['key']}.png"), optimize=True)
        img.resize((320, 320), Image.LANCZOS).save(os.path.join(OUT_DIR, f"avatar-v4-{v['key']}-320.png"), optimize=True)
        results.append((img, rec))
        print(v["key"], "r ink", rec["max_radius"]["ink"], "r seal", rec["max_radius"]["seal"])
    contact(results, fonts).save(os.path.join(OUT_DIR, "contact-profile-v4.png"), optimize=True)
    with open(os.path.join(OUT_DIR, "avatar-v4-RENDER.json"), "w", encoding="utf-8") as fp:
        json.dump([r for _, r in results], fp, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
