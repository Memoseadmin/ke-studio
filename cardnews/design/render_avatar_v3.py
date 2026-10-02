#!/usr/bin/env python3
"""책가도 노트 프로필 사진 v3: 퍼블릭 도메인 민화 원화 디테일 크롭 + 한지 톤 + 붉은 낙관 하나.

사용:
  python3 cardnews/design/render_avatar_v3.py --download   # 원화 3점 내려받기 -> render/avatar-v3/src/ (커밋 제외)
  python3 cardnews/design/render_avatar_v3.py              # 렌더 -> cardnews/profile/

산출물(cardnews/profile/):
  avatar-v3-A/B/C.png        1080x1080 (핵심 요소 = 중앙 지름 860 원 안. 낙관도 그 안)
  avatar-v3-A/B/C-320.png    320x320 축소본
  contact-profile.png        3안 원형 크롭 미리보기(320px + 110px) 나란히

원칙(대표 결정 2026-10-02, design-system v1.2 §8):
- 원화는 Met·Cleveland CC0만. 원본은 커밋하지 않는다(이 파일의 URL로 다시 받는다). SHA-256을 SOURCES.json에 남긴다.
- 내용 변형 금지: 크롭·톤·질감만. 그리기·지우기·합성 없음. 그림 속 글자는 크롭 밖.
- 톤 = §8-3 v1.2 archive 프리셋: 레벨 35% -> 채도 -20% -> 공통 LUT v1 -> 한지 multiply 15% -> 세피아 기미 약하게(추정치).
- 낙관 = 코드 그래픽(red 정사각 + 종이색 '책', render_profile.glyph_chaek 재사용, 글꼴 미사용). AI 생성 0, 자체 그림 0.
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_cards as rc  # noqa: E402  (토큰·폰트 재사용, 수정하지 않음)
import render_profile as rp  # noqa: E402  (Pen·glyph_chaek·circle_crop·max_radius 재사용, 수정하지 않음)

T = rc.TOKENS
ROOT = os.path.dirname(os.path.dirname(HERE))
SRC_DIR = os.path.join(ROOT, "render", "avatar-v3", "src")
OUT_DIR = os.path.join(os.path.dirname(HERE), "profile")
AV = 1080
SAFE_R = 430
LUT_VERSION = "lut-v1 (contrast x1.06, highlight warm R+3 G+1 B-4)"
SEPIA = (1.035, 1.005, 0.94)  # 세피아 기미(색온도 약 +6%, 추정치 -> 실측 후 교체)

# crop = 원본 픽셀 [x0, y0, x1, y1] (정사각). seal = 낙관 중심(1080 캔버스 기준)
SOURCES = [
    {"key": "A", "name": "책장 칸", "file": "cleveland-2011.37.jpg",
     "url": "https://openaccess-cdn.clevelandart.org/2011.37/2011.37_print.jpg",
     "title": "Books and Scholars' Accoutrements", "title_ko": "책가도", "institution": "클리블랜드미술관",
     "accession": "2011.37", "object_url": "https://clevelandart.org/art/2011.37",
     "license": "CC0", "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
     "credit_short": "클리블랜드미술관 〈책가도〉 CC0",
     "crop": [1372, 182, 2028, 838], "seal": (762, 762), "detail": "10폭 중 5~6폭 위 2단: 쌓인 책과 문방 기물"},
    {"key": "B", "name": "필통과 두루마리", "file": "met-853896.jpg",
     "url": "https://images.metmuseum.org/CRDImages/as/original/DP-40204-001.jpg",
     "title": "Books and Scholarly Accoutrements", "title_ko": "책가도", "institution": "메트로폴리탄미술관",
     "accession": "2024.89.6", "object_url": "https://www.metmuseum.org/art/collection/search/853896",
     "license": "CC0", "license_url": "https://www.metmuseum.org/policies/image-resources",
     "credit_short": "메트로폴리탄미술관 〈책가도〉 CC0",
     "crop": [1676, 557, 2277, 1158], "seal": (762, 762), "detail": "오른쪽 폭 맨 위: 필통에 꽂힌 붓·두루마리·부채, 옆의 책"},
    {"key": "C", "name": "모란과 나비", "file": "met-45063.jpg",
     "url": "https://images.metmuseum.org/CRDImages/as/original/LC-1977_448-005.jpg",
     "title": "Butterflies and Peonies", "title_ko": "모란나비도", "institution": "메트로폴리탄미술관",
     "accession": "1977.448", "object_url": "https://www.metmuseum.org/art/collection/search/45063",
     "license": "CC0", "license_url": "https://www.metmuseum.org/policies/image-resources",
     "credit_short": "메트로폴리탄미술관 〈모란나비도〉 CC0",
     "crop": [832, 1901, 1724, 2793], "seal": (318, 762), "detail": "가운데 보랏빛 모란 한 송이와 그 위 검은 나비"},
]


def download():
    os.makedirs(SRC_DIR, exist_ok=True)
    for s in SOURCES:
        p = os.path.join(SRC_DIR, s["file"])
        if os.path.exists(p):
            continue
        req = urllib.request.Request(s["url"], headers={"User-Agent": "ke-studio-cardnews/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(p, "wb") as fp:
            fp.write(r.read())
        print("downloaded", p)


# ---------- 톤(§8-3 v1.2 archive) ----------
def hanji_texture(size, seed=2026):
    """v3 imaging.hanji_texture 와 같은 레시피(0.8~1.0, 고정 seed)."""
    w, h = size
    rng = np.random.default_rng(seed)
    base = rng.normal(0, 1, (max(1, h // 2), max(1, w // 2))).astype(np.float32)
    base = np.array(Image.fromarray(base).resize((w, h), Image.BILINEAR))
    fib = rng.normal(0, 1, (max(1, h // 3), max(1, w // 24))).astype(np.float32)
    fib = np.array(Image.fromarray(fib).resize((w, h), Image.BICUBIC))
    t = 0.55 * base + 0.45 * fib
    t = (t - t.min()) / max(1e-6, t.max() - t.min())
    return 0.80 + 0.20 * t


def gentle_levels(im, amount=0.35, lo_pct=0.5, hi_pct=99.5):
    arr = np.asarray(im).astype(np.float32)
    out = arr.copy()
    for c in range(3):
        lo, hi = np.percentile(arr[..., c], [lo_pct, hi_pct])
        if hi - lo > 1:
            out[..., c] = (arr[..., c] - lo) * 255.0 / (hi - lo)
    out = (1 - amount) * arr + amount * np.clip(out, 0, 255)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def common_lut(im):
    t = np.arange(256, dtype=np.float32) / 255.0
    s = np.clip(0.5 + (t - 0.5) * 1.06, 0, 1)
    r = np.clip(s * 255 + 3 * t, 0, 255)
    g = np.clip(s * 255 + 1 * t, 0, 255)
    b = np.clip(s * 255 - 4 * t, 0, 255)
    return im.point([int(round(v)) for v in np.concatenate([r, g, b])])


def archive_v12(im):
    steps = []
    im = gentle_levels(im, 0.35); steps.append("levels 35% (0.5~99.5 percentile)")
    im = ImageEnhance.Color(im).enhance(0.80); steps.append("saturation -20%")
    im = common_lut(im); steps.append(LUT_VERSION)
    arr = np.asarray(im).astype(np.float32)
    tex = hanji_texture(im.size)[..., None]
    arr = arr * (1 - 0.15 + 0.15 * tex); steps.append("hanji multiply 15% (procedural seed 2026)")
    arr = arr * np.array(SEPIA, np.float32); steps.append("sepia warm R x1.035 G x1.005 B x0.94 (estimate)")
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)), steps


# ---------- 낙관(코드 그래픽) ----------
SEAL = 150  # 한 변(px). 110px 프로필에서 약 15px 붉은 점


def seal_layer(center, seed):
    """붉은 정사각 도장 + 종이색 '책'(백문). 가장자리 거스러미·찍힘 얼룩은 고정 seed 노이즈."""
    pen = rp.Pen((AV, AV))
    cx, cy = center
    h = SEAL / 2
    pen.rect((cx - h, cy - h, cx + h, cy + h), fill=T["red"])
    g = SEAL * 0.66
    rp.glyph_chaek(pen, (cx - g / 2, cy - g / 2, g), T["paper"])
    layer = pen.result()
    # 찍힘 얼룩: 알파를 0.80~0.95 사이로 흔든다(붉은 면만, 글자 면은 종이색 그대로)
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (AV // 6, AV // 6)).astype(np.float32)
    n = np.array(Image.fromarray(n).resize((AV, AV), Image.BILINEAR))
    n = (n - n.min()) / max(1e-6, n.max() - n.min())
    a = np.asarray(layer.getchannel("A")).astype(np.float32) * (0.80 + 0.15 * n)
    # 가장자리 거스러미
    edge = Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    layer.putalpha(edge)
    return layer


def render_one(s):
    src = os.path.join(SRC_DIR, s["file"])
    if not os.path.exists(src):
        sys.exit(f"원본 없음: {src}  (먼저 --download)")
    if not (s.get("license") and s.get("credit_short")):
        sys.exit(f"{s['key']}: license/credit 누락 -> 렌더 거부")
    with open(src, "rb") as fp:
        sha = hashlib.sha256(fp.read()).hexdigest()
    im = Image.open(src).convert("RGB")
    src_size = im.size
    crop = im.crop(tuple(s["crop"]))
    crop_side = crop.size[0]
    crop = crop.resize((AV, AV), Image.LANCZOS)
    toned, steps = archive_v12(crop)
    seal = seal_layer(s["seal"], seed=ord(s["key"]))
    out = toned.convert("RGBA")
    out.alpha_composite(seal)
    out = out.convert("RGB")
    r_seal = rp.max_radius(seal, (AV / 2, AV / 2))
    rec = {k: s[k] for k in ("key", "name", "title", "title_ko", "institution", "accession", "object_url", "url",
                             "license", "license_url", "credit_short", "crop", "detail")}
    rec.update({"src_sha256": sha, "src_size": list(src_size), "crop_side_px": crop_side,
                "upscale": round(AV / crop_side, 2), "steps": steps, "seal": {"center": list(s["seal"]), "side": SEAL,
                "max_radius": r_seal, "glyph": "책 (render_profile.glyph_chaek, 도형 조립, 글꼴 미사용)"},
                "content_changed": False, "ai_generated": False})
    return out, rec


def contact(results, fonts):
    pad, gap, big, small = 48, 56, 320, 110
    W = pad * 2 + 3 * big + 2 * gap
    head = 84
    H = head + big + 36 + small + 28 + 44 + 36 + pad
    sheet = Image.new("RGB", (W, H), T["white"])
    d = ImageDraw.Draw(sheet)
    d.text((pad, 28), "프로필 사진 v3 후보 (민화 원화 디테일 + 낙관, 원형 320px / 110px)",
           font=rc.font(fonts["body"], 28), fill=rp.APP_TEXT)
    for i, (img, rec) in enumerate(results):
        x = pad + i * (big + gap)
        b = rp.circle_crop(img, (AV / 2, AV / 2), AV, big)
        sheet.paste(b, (x, head), b)
        sm = rp.circle_crop(img, (AV / 2, AV / 2), AV, small)
        sy = head + big + 36
        sheet.paste(sm, (x + (big - small) // 2, sy), sm)
        ly = sy + small + 28
        d.text((x + big // 2, ly), f"{rec['key']}  {rec['name']}", font=rc.font(fonts["body"], 32),
               fill=rp.APP_TEXT, anchor="ma", stroke_width=1, stroke_fill=rp.APP_TEXT)
        d.text((x + big // 2, ly + 44), rec["credit_short"], font=rc.font(fonts["body"], 20),
               fill="#6B6B6B", anchor="ma")
    return sheet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", action="store_true")
    a = ap.parse_args()
    if a.download:
        download()
    fonts = rc.load_fonts()
    results = []
    for s in SOURCES:
        img, rec = render_one(s)
        img.save(os.path.join(OUT_DIR, f"avatar-v3-{s['key']}.png"), optimize=True)
        img.resize((320, 320), Image.LANCZOS).save(os.path.join(OUT_DIR, f"avatar-v3-{s['key']}-320.png"), optimize=True)
        results.append((img, rec))
        print(s["key"], "seal r", rec["seal"]["max_radius"], "upscale", rec["upscale"])
    contact(results, fonts).save(os.path.join(OUT_DIR, "contact-profile.png"), optimize=True)
    with open(os.path.join(OUT_DIR, "avatar-v3-SOURCES.json"), "w", encoding="utf-8") as fp:
        json.dump([r for _, r in results], fp, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
