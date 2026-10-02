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


def blur_region(im, box, radius=24, feather=None):
    """box(0~1 또는 px) 영역만 가우시안 흐림(가장자리 부드럽게). 로고·각인·문자판 글자를 읽히지 않게 할 때만 쓴다."""
    w, h = im.size
    x0, y0, x1, y1 = box
    if max(box) <= 1.0:
        x0, x1, y0, y1 = x0 * w, x1 * w, y0 * h, y1 * h
    px = [int(round(v)) for v in (max(0, x0), max(0, y0), min(w, x1), min(h, y1))]
    f = feather if feather is not None else max(4, radius)
    mask = Image.new("L", im.size, 0)
    mask.paste(255, (px[0] + f // 2, px[1] + f // 2, max(px[0] + f // 2 + 1, px[2] - f // 2), max(px[1] + f // 2 + 1, px[3] - f // 2)))
    mask = mask.filter(ImageFilter.GaussianBlur(f / 2))
    return Image.composite(im.filter(ImageFilter.GaussianBlur(radius)), im, mask), px


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
    steps = []
    for b in edit.get("blur") or []:  # 로고·각인·문자판 글자 흐림(원본 좌표, 크롭 전). 내용 추가·삭제 아님
        im, px = blur_region(im, b["box"], int(b.get("radius", 24)))
        steps.append(f"blur {px} r{int(b.get('radius', 24))} ({b.get('why', 'text/logo')})")
    im, crop_px = crop_norm(im, edit.get("crop"))
    crop_size = im.size
    if max(im.size) > max_side:
        im.thumbnail((max_side, max_side), Image.LANCZOS)
    if crop_px:
        steps.insert(0, f"focus crop {crop_px}")
    grain = float(edit.get("grain", 0.06 if preset == "muted-warm" else 0.08))
    if preset == "archive":
        im = gentle_levels(im, 0.35); steps.append("levels 35% (0.5~99.5 percentile)")
        im = ImageEnhance.Color(im).enhance(0.90); steps.append("saturation -10%")
        im = common_lut(im); steps.append(LUT_VERSION)
        im = multiply_texture(im, 0.08); steps.append("hanji multiply 8% (procedural seed 2026)")
    elif preset == "muted-warm":
        im = ImageEnhance.Color(im).enhance(0.75); steps.append("saturation -25%")
        im = ImageEnhance.Contrast(im).enhance(0.96); steps.append("contrast -4%")
        im = Image.blend(im, Image.new("RGB", im.size, PAPER), 0.08); steps.append("hanji tint 8%")
        im = multiply_texture(im, grain); steps.append(f"grain multiply {grain:.0%}")
    elif preset == "hanji-duotone":
        g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1)
        im = tritone(g, NIGHT, KRAFT, PAPER); steps.append("tritone night/kraft/paper")
        im = multiply_texture(im, grain); steps.append(f"grain multiply {grain:.0%}")
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


# ---------- 3안 콜라주: 종이 찢김 테두리(코드 마스크) + 원화 프레임 ----------
def torn_mask(size, seed=11, depth=18, edges=("top", "bottom", "left", "right")):
    """찢은 종이 가장자리 알파 마스크(L). 가장자리마다 저주파 요동 + 고주파 거스러미. 결정적(seed)."""
    w, h = size
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    def profile(n, d):
        t = np.linspace(0, 1, n, dtype=np.float32)
        p = np.zeros(n, np.float32)
        for k, amp in ((2, 1.0), (5, 0.6), (11, 0.35), (23, 0.2)):
            p += amp * np.sin(2 * np.pi * (k * t + rng.random()))
        p += rng.normal(0, 0.25, n).astype(np.float32)
        p = (p - p.min()) / max(1e-6, p.max() - p.min())
        return d * (0.35 + 0.65 * p)

    m = np.ones((h, w), np.float32)
    if "top" in edges:
        m *= (yy >= profile(w, depth)[None, :])
    if "bottom" in edges:
        m *= (yy <= h - 1 - profile(w, depth)[None, :])
    if "left" in edges:
        m *= (xx >= profile(h, depth)[:, None])
    if "right" in edges:
        m *= (xx <= w - 1 - profile(h, depth)[:, None])
    mask = Image.fromarray((m * 255).astype(np.uint8))
    return mask.filter(ImageFilter.GaussianBlur(0.8))


def torn_photo(im, seed=11, depth=18, edge_light=True, rim="paper"):
    """사진에 찢김 테두리 적용 -> RGBA. rim="paper": 찢긴 가장자리 안쪽에 종이 섬유 느낌의 밝은 띠(1~2px).
    rim="ink": 찢긴 가장자리를 따라 먹선(약 3px, 먹 85%) = 프리셋 4단계 '잉크 테두리'."""
    im = im.convert("RGB")
    mask = torn_mask(im.size, seed, depth)
    out = im.copy()
    if rim == "ink":
        inner = mask.filter(ImageFilter.MinFilter(7))
        band = np.clip(np.asarray(mask).astype(np.int16) - np.asarray(inner).astype(np.int16), 0, 255) * 0.85
        out = Image.composite(Image.new("RGB", im.size, INK), out, Image.fromarray(band.astype(np.uint8)))
    elif edge_light:
        inner = mask.filter(ImageFilter.MinFilter(5))
        rim = Image.fromarray(np.clip(np.asarray(mask).astype(np.int16) - np.asarray(inner).astype(np.int16), 0, 255).astype(np.uint8))
        paper = Image.new("RGB", im.size, PAPER)
        out = Image.composite(paper, out, rim)
    out.putalpha(mask)
    return out


def frame_collage(frame_src, photo_rgba, size, inset, seed=3, frame_edit=None):
    """원화 디테일을 프레임(배경 띠)으로 깔고 그 위에 찢긴 사진을 얹는다. frame_src=원화 사본 경로, size=(w,h), inset=px."""
    w, h = size
    frame = ImageOps.exif_transpose(Image.open(frame_src)).convert("RGB")
    fw, fh = frame.size
    sc = max(w / fw, h / fh)
    frame = frame.resize((math.ceil(fw * sc), math.ceil(fh * sc)), Image.LANCZOS)
    fe = frame_edit or {}
    fx, fy = fe.get("focus", [0.5, 0.5])
    left = int(min(max(fx * frame.width - w / 2, 0), frame.width - w))
    top = int(min(max(fy * frame.height - h / 2, 0), frame.height - h))
    frame = frame.crop((left, top, left + w, top + h))
    frame = ImageEnhance.Color(frame).enhance(0.8)
    frame = Image.blend(frame, Image.new("RGB", frame.size, PAPER), 0.12)  # 프레임은 한 단계 물러선다
    frame = multiply_texture(frame, 0.10)
    canvas = frame.convert("RGBA")
    pw, ph = w - 2 * inset, h - 2 * inset
    ph_im = photo_rgba.resize((pw, ph), Image.LANCZOS) if photo_rgba.size != (pw, ph) else photo_rgba
    # 그림자: 먹 18%, 6px 오프셋
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sh_alpha = ph_im.getchannel("A").point(lambda a: int(a * 0.18))
    shadow.paste(Image.new("RGBA", (pw, ph), (17, 17, 17, 255)), (inset + 6, inset + 8), sh_alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(4))
    canvas = Image.alpha_composite(canvas, shadow)
    canvas.alpha_composite(ph_im, (inset, inset))
    return canvas.convert("RGB")
