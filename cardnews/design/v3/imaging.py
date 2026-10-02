"""v3 이미지 처리: 원화(퍼블릭 도메인·공공누리 1유형)와 실사 사진의 크롭·톤·질감. 원본 파일은 바꾸지 않고 렌더용 사본만 만든다.

원칙(DESIGN_SOURCES §8 톤 처리, 대표 지시 2026-10-02): 내용은 바꾸지 않는다(그리기·지우기·합성·변형 없음). 크롭·톤·질감만.
프리셋
- archive       원화용. 레벨 보정 약하게(35%) -> 채도 -10% -> 공통 LUT v1 -> 한지 multiply 8%. 균열·얼룩 보존(노이즈 제거 없음)
- muted-warm    사진용. 채도 -25%, 대비 -4%, 한지 톤 틴트 8% -> 그레인 multiply 6%
- hanji-duotone 사진용. 흑백 -> 먹(#1B1F2A)·크라프트(#C9A877)·한지(#F7F3EA) 3색 매핑 -> 그레인 multiply 8%
- ink-cut       사진용. 흑백 -> 3단 포스터(먹·크라프트·한지), 판화 느낌 -> 그레인 multiply 8%
선택: vignette 0~0.35 (가장자리 먹 multiply)
"""
import hashlib
import math

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

PAPER = (247, 243, 234)
INK = (17, 17, 17)
NIGHT = (27, 31, 42)
KRAFT = (201, 168, 119)
LUT_VERSION = "lut-v1 (contrast x1.06, highlight warm R+3 G+1 B-4)"
PRESETS = ("archive", "muted-warm", "hanji-duotone", "ink-cut")


def hanji_texture(size, seed=2026):
    """한지 결 텍스처(0~1 float, 1 = 흰 종이). 고정 seed 라 매번 같다. 자체 한지 스캔이 생기면 그 파일로 교체."""
    w, h = size
    rng = np.random.default_rng(seed)
    base = rng.normal(0, 1, (max(1, h // 2), max(1, w // 2))).astype(np.float32)
    base = np.array(Image.fromarray(base).resize((w, h), Image.BILINEAR))
    fib = rng.normal(0, 1, (max(1, h // 3), max(1, w // 24))).astype(np.float32)  # 세로로 긴 섬유
    fib = np.array(Image.fromarray(fib).resize((w, h), Image.BICUBIC))
    t = 0.55 * base + 0.45 * fib
    t = (t - t.min()) / max(1e-6, t.max() - t.min())
    return 0.80 + 0.20 * t  # 0.8~1.0


def multiply_texture(im, strength, seed=2026):
    arr = np.asarray(im).astype(np.float32)
    tex = hanji_texture(im.size, seed)[..., None]
    out = arr * (1 - strength + strength * tex)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


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
    lut = [int(round(v)) for v in np.concatenate([r, g, b])]
    return im.point(lut)


def vignette(im, strength):
    if not strength:
        return im
    w, h = im.size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / math.sqrt(2)
    m = 1 - strength * np.clip((d - 0.55) / 0.45, 0, 1) ** 1.6
    arr = np.asarray(im).astype(np.float32) * m[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def tritone(gray, dark, mid, light):
    g = np.asarray(gray).astype(np.float32) / 255.0
    dark, mid, light = (np.array(c, np.float32) for c in (dark, mid, light))
    lo = np.clip(g * 2, 0, 1)[..., None]
    hi = np.clip(g * 2 - 1, 0, 1)[..., None]
    out = np.where(g[..., None] < 0.5, dark + (mid - dark) * lo, mid + (light - mid) * hi)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def crop_norm(im, box):
    """box = [x0, y0, x1, y1] 0~1(원본 기준) 또는 픽셀(>1)."""
    if not box:
        return im, None
    w, h = im.size
    x0, y0, x1, y1 = box
    if max(box) <= 1.0:
        x0, x1, y0, y1 = x0 * w, x1 * w, y0 * h, y1 * h
    px = [int(round(v)) for v in (max(0, x0), max(0, y0), min(w, x1), min(h, y1))]
    return im.crop(px), px


def process(src, out_path, edit=None, kind="artwork", max_side=2200):
    """원본 -> 렌더용 사본(JPEG). 편집 기록(dict) 반환."""
    edit = dict(edit or {})
    preset = edit.get("preset") or ("archive" if kind == "artwork" else "muted-warm")
    if preset not in PRESETS:
        raise ValueError(f"알 수 없는 편집 프리셋 '{preset}' (가능: {', '.join(PRESETS)})")
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    src_size = im.size
    im, crop_px = crop_norm(im, edit.get("crop"))
    crop_size = im.size
    if max(im.size) > max_side:
        im.thumbnail((max_side, max_side), Image.LANCZOS)
    steps = []
    if preset == "archive":
        im = gentle_levels(im, 0.35); steps.append("levels 35% (0.5~99.5 percentile)")
        im = ImageEnhance.Color(im).enhance(0.90); steps.append("saturation -10%")
        im = common_lut(im); steps.append(LUT_VERSION)
        im = multiply_texture(im, 0.08); steps.append("hanji multiply 8% (procedural seed 2026)")
    elif preset == "muted-warm":
        im = ImageEnhance.Color(im).enhance(0.75); steps.append("saturation -25%")
        im = ImageEnhance.Contrast(im).enhance(0.96); steps.append("contrast -4%")
        im = Image.blend(im, Image.new("RGB", im.size, PAPER), 0.08); steps.append("hanji tint 8%")
        im = multiply_texture(im, 0.06); steps.append("grain multiply 6%")
    elif preset == "hanji-duotone":
        g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1)
        im = tritone(g, NIGHT, KRAFT, PAPER); steps.append("tritone night/kraft/paper")
        im = multiply_texture(im, 0.08); steps.append("grain multiply 8%")
    elif preset == "ink-cut":
        g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=2).filter(ImageFilter.MedianFilter(3))
        arr = np.asarray(g)
        out = np.where(arr[..., None] < 85, np.array(INK), np.where(arr[..., None] < 170, np.array(KRAFT), np.array(PAPER)))
        im = Image.fromarray(out.astype(np.uint8)); steps.append("3-level posterize ink/kraft/paper")
        im = multiply_texture(im, 0.08); steps.append("grain multiply 8%")
    v = float(edit.get("vignette") or 0)
    if v:
        im = vignette(im, min(0.35, v)); steps.append(f"vignette {min(0.35, v):.2f}")
    im.save(out_path, quality=92)
    with open(src, "rb") as fp:
        sha = hashlib.sha256(fp.read()).hexdigest()
    return {"preset": preset, "steps": steps, "crop_px": crop_px, "src_size": list(src_size), "crop_size": list(crop_size),
            "out_size": list(im.size), "focus": edit.get("focus", [0.5, 0.5]), "src_sha256": sha,
            "content_changed": False}
