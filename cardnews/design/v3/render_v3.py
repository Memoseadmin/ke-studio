#!/usr/bin/env python3
"""책가도 노트 카드뉴스 v3 렌더러: cards.json(형식 그대로) -> HTML/CSS 템플릿 3종 -> Playwright Chromium -> 1080x1350 PNG.

사용:
  python3 cardnews/design/v3/render_v3.py cardnews/posts/2026-10-19                 # 미리보기(MOCKUP 표기)
  python3 cardnews/design/v3/render_v3.py cardnews/posts/2026-10-19 --final         # 게시용(approved 후에만)
  python3 cardnews/design/v3/render_v3.py --all cardnews/posts --out /tmp/prev      # 결과만 다른 곳에
  옵션: --strict(검수 실패 1건이라도 있으면 종료 코드 3), --keep-html

준비: bash cardnews/design/v3/fetch_fonts.sh (scripts/setup.sh 가 호출). Node Playwright + Chromium(VM 기본 설치).
이미지(장별 1개): <post_dir>/photos/PHOTOS.json(원화·실사, 원본은 photos/src/) > <post_dir>/plates/card-NN.png(AI) > 없음(타이포만).
  원본은 바꾸지 않고 렌더 때마다 render/cardnews-v3/<날짜>/ 에 편집 사본을 만든다(imaging.py 프리셋, 내용 변형 없음).
검수(자동): 줄 수 상한·넘침·안전 영역(사방 88px, 위아래 92px)·실제 사용 서체(CDP)·글리프 누락(fontTools cmap)·이미지 로드.
기존 Pillow 렌더러 cardnews/design/render_cards.py 는 그대로 둔다(v2, 대체됨).
"""
import argparse
import datetime as _dt
import glob
import hashlib
import html
import json
import os
import re
import string
import subprocess
import sys
import urllib.parse

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import imaging  # noqa: E402
from render_cards import license_status  # noqa: E402  v2와 같은 라이선스 판정(공공누리 1유형·CC0·CC BY ok, NC·ND·2~4유형 거부)

FONT_DIR = os.path.join(HERE, "fonts")
FONTS = [  # (CSS family, 파일, weight 범위, 라이선스, 출처)
    ("Hahmlet", "Hahmlet[wght].ttf", "100 900", "OFL-1.1 (OFL-Hahmlet.txt)", "https://github.com/google/fonts/tree/main/ofl/hahmlet"),
    ("MaruBuri", "MaruBuri-Regular.ttf", "400", "네이버 글꼴 오픈 라이선스(상업적 사용 허용, OFL 기반)", "https://hangeul.naver.com/fonts/search?f=maru"),
    ("MaruBuri", "MaruBuri-Bold.ttf", "700", "네이버 글꼴 오픈 라이선스(상업적 사용 허용, OFL 기반)", "https://hangeul.naver.com/fonts/search?f=maru"),
    ("Black Han Sans", "BlackHanSans-Regular.ttf", "400", "OFL-1.1 (OFL-BlackHanSans.txt)", "https://github.com/google/fonts/tree/main/ofl/blackhansans"),
    ("Noto Serif KR", "NotoSerifKR[wght].ttf", "200 900", "OFL-1.1 (OFL-NotoSerifKR.txt)", "https://github.com/google/fonts/tree/main/ofl/notoserifkr"),
]
ALLOWED_FAMILIES = {"Hahmlet", "MaruBuri", "Black Han Sans", "Noto Serif KR"}
STACKS = {"title": ["Hahmlet[wght].ttf", "NotoSerifKR[wght].ttf"], "body": ["MaruBuri-Regular.ttf", "NotoSerifKR[wght].ttf"],
          "num": ["BlackHanSans-Regular.ttf", "NotoSerifKR[wght].ttf"]}
BRAND, HANDLE = "책가도 노트", "@chaekgado.note"
# AI 표시 라벨은 카드에 넣지 않는다(대표 결정 2026-10-02). AI 고지는 캡션(marketer)이 담당. 마지막 장 = 출처 줄만.
SAFE = (88, 92, 1080 - 88, 1350 - 92)
RENDERER_VERSION = "v3.2-collage-2 (2026-10-02, 3안 하이브리드 콜라주 2판: LAYOUT.v3·흐림·잉크 테두리·코드 오버레이·rev 레이아웃·슬롯 실측)"
OVERLAY_ORANGE = "#E2701F"  # 4장 밑줄(cards.json visual "주황"). 코드 그래픽, 사진 픽셀은 바꾸지 않음


def fail_fonts():
    missing = [f for _, f, *_ in FONTS if not os.path.isfile(os.path.join(FONT_DIR, f))]
    if missing:
        raise SystemExit(f"서체 없음: {missing}. 먼저 bash cardnews/design/v3/fetch_fonts.sh")


def file_url(p):
    return "file://" + urllib.parse.quote(os.path.abspath(p))


def font_faces():
    css = []
    for fam, f, wt, *_ in FONTS:
        css.append(f'@font-face{{font-family:"{fam}";src:url("{file_url(os.path.join(FONT_DIR, f))}");font-weight:{wt};font-display:block;}}')
    return "\n".join(css)


_CMAPS = {}


def cmap(fname):
    if fname not in _CMAPS:
        from fontTools.ttLib import TTFont
        _CMAPS[fname] = set(TTFont(os.path.join(FONT_DIR, fname), lazy=True).getBestCmap())
    return _CMAPS[fname]


def tofu(text, stack):
    return sorted({ch for ch in text if ch not in "\n " and not any(ord(ch) in cmap(f) for f in STACKS[stack])})


def font_log():
    out = []
    for fam, f, wt, lic, src in FONTS:
        p = os.path.join(FONT_DIR, f)
        with open(p, "rb") as fp:
            sha = hashlib.sha256(fp.read()).hexdigest()
        ver = None
        try:
            from fontTools.ttLib import TTFont
            ver = TTFont(p, lazy=True)["name"].getDebugName(5)
        except Exception:
            pass
        out.append({"family": fam, "file": f, "weight": wt, "version": ver, "license": lic, "source": src, "sha256": sha})
    return out


def grain_tile(work):
    p = os.path.join(work, "grain.png")
    if not os.path.exists(p):
        import numpy as np
        tex = imaging.hanji_texture((1080, 1350), seed=7)
        s = 0.07  # 바탕 한지 결 7%(글자 위에는 올리지 않음: 배경 레이어)
        arr = np.array(imaging.PAPER, np.float32)[None, None, :] * (1 - s + s * tex[..., None])
        Image.fromarray(arr.clip(0, 255).astype("uint8")).save(p)
    return p


def load_images(post_dir, post, total, work):
    """장별 이미지 결정 + 편집 사본 생성. 반환 {n: {...}}. 크레딧·라이선스 없으면 SystemExit(렌더 거부)."""
    out = {}
    pdir = os.path.join(post_dir, "photos")
    jpath = os.path.join(pdir, "PHOTOS.json")
    if os.path.isfile(os.path.join(pdir, "PHOTOS.v3.json")):
        jpath = os.path.join(pdir, "PHOTOS.v3.json")  # COO 별도 세션이 넣는 사진 목록이 우선
    if os.path.isfile(os.path.join(pdir, "LAYOUT.v3.json")):
        jpath = os.path.join(pdir, "LAYOUT.v3.json")  # 2판: 장별 배치(사진 선택·편집·프레임·오버레이). 사진 메타는 PHOTOS.v3.json에서 ref로 병합
    if os.path.isfile(jpath):
        with open(jpath, encoding="utf-8") as fp:
            data = json.load(fp)
        entries = (data.get("cards") or data.get("photos", [])) if isinstance(data, dict) else data
        if isinstance(data, dict) and data.get("notes"):
            out["_notes"] = data["notes"]
        if jpath.endswith("LAYOUT.v3.json"):
            entries = [resolve_ref(e, pdir) for e in entries]
        elif entries and "file" not in entries[0]:
            raise SystemExit(f"{jpath}: researcher 후보 목록 형식(file 없음) -> photos/LAYOUT.v3.json 으로 장별 배치를 지정")
        for e in entries:
            if e.get("date") and str(e["date"]) != str(post.get("date")):
                continue
            n = int(e["card"])
            credit, lic = str(e.get("credit") or "").strip(), str(e.get("license") or "").strip()
            if not credit or not lic:
                raise SystemExit(f"{jpath}: card {n} credit/license 없음 -> 렌더 거부(출처 표기 강제)")
            st = license_status(lic)
            if st == "blocked":
                raise SystemExit(f"{jpath}: card {n} license '{lic}' 상업 이용·변경 불가 또는 미확인 -> 렌더 거부")
            src = os.path.join(pdir, e["file"])
            if not os.path.isfile(src):
                raise SystemExit(f"{jpath}: card {n} 원본 없음 {src}")
            kind = e.get("kind", "photo")
            dst = os.path.join(work, f"img-{n:02d}.jpg")
            rec = imaging.process(src, dst, e.get("edit"), kind=kind)
            out[n] = {"kind": kind, "path": dst, "entry": e, "edit": rec, "license_status": st, "src": src}
            if kind == "photo" and e.get("frame"):
                build_collage(out[n], pdir, work, n, jpath)
    notes = out.pop("_notes", None)
    _plates(out, post_dir, total)
    if notes:
        out["_notes"] = notes
    return out


def resolve_ref(e, pdir):
    """LAYOUT.v3.json 항목에 PHOTOS.v3.json(researcher) 메타를 병합. 출처 줄은 이 병합 결과에서 자동 생성된다."""
    e = dict(e)
    ref = e.get("ref")
    if ref:
        with open(os.path.join(pdir, "PHOTOS.v3.json"), encoding="utf-8") as fp:
            cands = json.load(fp)
        hit = [c for c in cands if int(c["card"]) == int(ref["card"]) and c["role"] == ref["role"]]
        if not hit:
            raise SystemExit(f"LAYOUT.v3.json card {e['card']}: ref {ref} 가 PHOTOS.v3.json 에 없음")
        c = hit[0]
        if c.get("status") not in ("ok", "partial"):
            raise SystemExit(f"LAYOUT.v3.json card {e['card']}: ref {ref} status={c.get('status')} -> 사용 불가")
        for k in ("title", "author", "license", "license_url", "page_url", "file_url", "credit", "risk_note", "source_check", "status"):
            if c.get(k) and not e.get(k):
                e[k] = c[k]
        e.setdefault("credit_short", c.get("author"))
        e.setdefault("file", f"src/{ref['card']}-{ref['role']}.jpg")
    return e


def build_collage(img, pdir, work, n, jpath, slot=None):
    """3안 콜라주: 편집 사진(초점 크롭·톤·그레인) -> 찢김 + 잉크 테두리 -> 원화 디테일 프레임(archive 프리셋 + 한 단계 물러섬)."""
    e, rec = img["entry"], img["edit"]
    fr = e["frame"]
    fsrc = os.path.join(pdir, fr["file"])
    if not os.path.isfile(fsrc):
        raise SystemExit(f"{jpath}: card {n} 프레임 원화 없음 {fsrc}")
    if not fr.get("credit_short") or license_status(fr.get("license", "")) == "blocked":
        raise SystemExit(f"{jpath}: card {n} 프레임 원화 credit_short/license 없음 또는 불가 -> 렌더 거부")
    fcopy = os.path.join(work, f"frame-{n:02d}.jpg")
    frec = imaging.process(fsrc, fcopy, {"preset": "archive", "crop": fr.get("crop")}, kind="artwork")
    slot = tuple(slot or fr.get("slot", [904, 584]))
    inset = int(fr.get("inset", 14))
    seed, depth, rim = int(fr.get("seed", n * 7 + 3)), int(fr.get("depth", 18)), fr.get("rim", "ink")
    photo = Image.open(img["path"]).convert("RGB")
    photo, sc = _cover(photo, slot[0] - 2 * inset, slot[1] - 2 * inset, *rec.get("focus", [0.5, 0.5]))
    torn = imaging.torn_photo(photo, seed=seed, depth=depth, rim=rim)
    fdst = os.path.join(work, f"img-{n:02d}-collage.jpg")
    imaging.frame_collage(fcopy, torn, slot, inset, frame_edit=fr).save(fdst, quality=92)
    rec["collage"] = {"frame_file": fr["file"], "frame_credit": fr["credit_short"], "frame_crop_px": frec.get("crop_px"),
                      "frame_steps": frec["steps"] + ["frame: saturation -20%, hanji 12%, grain 10% (한 단계 물러섬)"],
                      "slot": list(slot), "inset": inset, "photo_scale": round(sc, 3),
                      "torn_edge": {"seed": seed, "depth": depth}, "ink_border": rim == "ink"}
    img["collage_path"] = fdst


def _plates(out, post_dir, total):
    for i in range(1, total + 1):
        if i in out:
            continue
        plate = os.path.join(post_dir, "plates", f"card-{i:02d}.png")
        if os.path.isfile(plate) and i != total:
            meta = {}
            try:
                with open(os.path.join(post_dir, "plates", "PLATES.json"), encoding="utf-8") as fp:
                    pm = json.load(fp)
                meta = {k: pm.get(k) for k in ("model", "endpoint", "model_license", "terms_url")}
                meta.update({k: c.get(k) for c in pm.get("cards", []) if int(c.get("card", 0)) == i
                             for k in ("seed", "generated_at", "prompt_sha256", "human_review")})
            except Exception:
                pass
            out[i] = {"kind": "ai_plate", "path": plate, "entry": {"file": f"plates/card-{i:02d}.png", **meta}, "edit": None}
    return out


def _cover(im, bw, bh, fx=0.5, fy=0.5):
    """비율 유지 확대 후 초점 기준 크롭(늘리기 없음)."""
    import math as _m
    iw, ih = im.size
    sc = max(bw / iw, bh / ih)
    im = im.resize((max(bw, _m.ceil(iw * sc)), max(bh, _m.ceil(ih * sc))), Image.LANCZOS)
    left = int(round(min(max(fx * im.width - bw / 2, 0), im.width - bw)))
    top = int(round(min(max(fy * im.height - bh / 2, 0), im.height - bh)))
    return im.crop((left, top, left + bw, top + bh)), sc


def plate_html(img, cls="plate"):
    if not img:
        return ""
    fx, fy = (img["edit"] or {}).get("focus", [0.5, 0.5]) if img.get("edit") else (0.5, 0.5)
    pill = ""
    e = img["entry"]
    if img["kind"] == "photo" and e.get("credit_on_image", True):
        pill = f'<span class="credit-pill" data-check="사진 크레딧" data-maxlines="1" data-font>{html.escape(e["credit"])}</span>'
    path = img["path"]
    if img.get("collage_path"):
        cls += " collage"
        fx, fy = 0.5, 0.5
        path = img["collage_path"]
    return (f'<figure class="{cls}"><img src="{file_url(path)}" alt="" '
            f'style="object-position:{fx * 100:.1f}% {fy * 100:.1f}%">{pill}{overlay_html(e.get("overlay"))}</figure>')


def _box_style(o):
    return f'left:{o["x"] * 100:.1f}%;top:{o["y"] * 100:.1f}%;width:{o["w"] * 100:.1f}%;height:{o["h"] * 100:.1f}%'


def overlay_html(o):
    """코드 그래픽 오버레이(사진 픽셀은 그대로, 위에 얹는 별도 층). underline = 4장 주황 밑줄,
    script-pair = 6장 같은 글줄의 정자·흘림 2종, record = 7장 날짜·책 제목 칸 + 체크박스 5개."""
    if not o:
        return ""
    import random
    t = o["type"]
    if t == "underline":
        r = random.Random(o.get("seed", 4))
        paths = []
        for ln in o.get("lines") or [[o["x0"], o["x1"], o["y"]]]:
            x0, x1, y = ln[0] * 1000, ln[1] * 1000, ln[2] * 1000
            rise = float(ln[3] if len(ln) > 3 else o.get("rise", 0)) * 1000
            pts = [(x0 + (x1 - x0) * k / 6, y - rise * k / 6 + r.uniform(-1.5, 1.5)) for k in range(7)]
            paths.append(f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(f"L{px:.1f},{py:.1f}" for px, py in pts[1:]))
        return (f'<svg class="ov ov-underline" viewBox="0 0 1000 1000" preserveAspectRatio="none">'
                f'<path d="{" ".join(paths)}" stroke="{OVERLAY_ORANGE}" stroke-width="{o.get("width", 14)}" stroke-linecap="round" '
                f'stroke-linejoin="round" fill="none" opacity="0.92" vector-effect="non-scaling-stroke"/></svg>')
    if t == "script-pair":
        r = random.Random(o.get("seed", 6))
        W, H, n = 520, 120, int(o.get("glyphs", 5))
        cell = (W - 20) / n
        upper, anchors, y0 = [], [], 60
        for i in range(n):  # 같은 글줄(같은 글자 자리)을 두 번: 위 = 또박또박 끊어 쓴 획, 아래 = 이어 흘린 획
            cx = 10 + cell * (i + 0.5)
            anchors.append(cx)
            kind, s_ = r.randrange(3), cell * 0.36
            if kind == 0:
                upper.append(f"M{cx - s_:.0f},{y0 - s_ * .6:.0f} H{cx + s_:.0f} M{cx:.0f},{y0 - s_ * .6:.0f} V{y0 + s_:.0f} M{cx - s_ * .7:.0f},{y0 + s_ * .3:.0f} H{cx + s_ * .7:.0f}")
            elif kind == 1:
                upper.append(f"M{cx - s_ * .8:.0f},{y0 - s_ * .8:.0f} V{y0 + s_ * .2:.0f} H{cx + s_ * .8:.0f} M{cx - s_:.0f},{y0 + s_:.0f} H{cx + s_:.0f}")
            else:
                upper.append(f"M{cx - s_ * .7:.0f},{y0 - s_ * .8:.0f} H{cx + s_ * .7:.0f} V{y0 - s_ * .05:.0f} H{cx - s_ * .7:.0f} Z M{cx:.0f},{y0 - s_ * .05:.0f} V{y0 + s_:.0f}")
        d = f"M{anchors[0] - cell * .4:.0f},{y0 + 6:.0f}"
        for cx in anchors:
            a_, b_ = r.uniform(22, 40), r.uniform(12, 28)
            d += (f" C{cx - cell * .25:.0f},{y0 - a_:.0f} {cx + cell * .05:.0f},{y0 - a_:.0f} {cx:.0f},{y0 + b_ * .2:.0f}"
                  f" S{cx + cell * .3:.0f},{y0 + b_:.0f} {cx + cell * .45:.0f},{y0 + r.uniform(-6, 6):.0f}")
        g = '<svg viewBox="0 0 {W} {H}"><path d="{d}" fill="none" stroke="#111" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        lab = o.get("labels", ["정자", "흘림"])
        return (f'<div class="ov ov-slip ov-pair" style="{_box_style(o)}">'
                f'<div class="ov-row"><span class="ov-lab" data-font>{html.escape(lab[0])}</span>{g.format(W=W, H=H, d=" ".join(upper), sw=12)}</div>'
                f'<div class="ov-sep"></div>'
                f'<div class="ov-row"><span class="ov-lab" data-font>{html.escape(lab[1])}</span>{g.format(W=W, H=H, d=d, sw=9)}</div></div>')
    if t == "record":
        labels = o.get("labels", ["날짜", "책 제목"])
        boxes = "".join('<i class="ov-box"><svg viewBox="0 0 40 40"><path d="M9,21 L17,29 L32,11" fill="none" stroke="#C8102E" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg></i>'
                        if k < int(o.get("checked", 5)) else '<i class="ov-box"></i>' for k in range(int(o.get("boxes", 5))))
        date = '<span class="ov-cells">' + "".join('<b></b>' * k + ('<em>.</em>' if j < 2 else '') for j, k in enumerate((4, 2, 2))) + '</span>'
        return (f'<div class="ov ov-slip ov-record" style="{_box_style(o)}">'
                f'<div class="ov-row"><span class="ov-lab" data-font>{html.escape(labels[0])}</span>{date}</div>'
                f'<div class="ov-row"><span class="ov-lab" data-font>{html.escape(labels[1])}</span><span class="ov-line"></span></div>'
                f'<div class="ov-row ov-checks">{boxes}</div></div>')
    raise SystemExit(f"알 수 없는 overlay type {t}")


def overlay_text(o):
    return "".join((o or {}).get("labels", ["정자", "흘림"] if (o or {}).get("type") == "script-pair" else
                                  ["날짜", "책 제목"] if (o or {}).get("type") == "record" else []))


def _lic_short(lic):
    l = str(lic).lower()
    if "cc0" in l or "public domain" in l:
        return "CC0"
    m = re.search(r"cc by[\w\s.-]*?\d\.\d", l)
    return m.group(0).upper() if m else str(lic)


def art_credit_line(images):
    """마지막 장 고정 출처 줄(§8-4). '그림: 기관 〈작품명〉 라이선스'(원화 + 프레임 원화) + '사진: 작가 · 라이선스'(쓰인 실사 전부).
    LAYOUT.v3.json/PHOTOS.v3.json에서 자동 생성(수기 누락 방지). 사진은 라이선스별로 작가를 묶는다."""
    arts, by_lic = [], {}
    for n in sorted(images):
        img = images[n]
        e = img["entry"]
        s = e.get("credit_short") or e.get("credit")
        if img["kind"] == "artwork" and s and s not in arts:
            arts.append(s)
        elif img["kind"] == "photo" and not e.get("credit_on_image", True):
            who = e.get("author") or s
            if e.get("institution") or not e.get("author"):
                if s and s not in arts:
                    arts.append(s)  # 원화 스캔을 사진 칸에 쓴 경우(1판 6장)
            else:
                lst = by_lic.setdefault(_lic_short(e.get("license")), [])
                if who not in lst:
                    lst.append(who)
        fr = (e.get("frame") or {}).get("credit_short")
        if fr and fr not in arts:
            arts.append(fr)
    nb = lambda x: x.replace(" ", "\u00a0")  # 이름·작품 단위로만 줄바꿈(작가명·'〈책가도〉 CC0'이 갈라지지 않게)
    parts = []
    if arts:
        parts.append("그림: " + " · ".join(nb(a) for a in arts))
    if by_lic:
        parts.append("사진: " + " / ".join(" · ".join(nb(w) for w in v) + " · " + k for k, v in by_lic.items()))
    return "\n".join(parts)


def build_html(post, card, idx, total, images, css, mockup):
    tpl_name = "cover" if idx == 0 else "last" if idx == total - 1 else "body"
    with open(os.path.join(HERE, "templates", f"{tpl_name}.html"), encoding="utf-8") as fp:
        tpl = string.Template(fp.read())
    n = card.get("n", idx + 1)
    img = images.get(n)
    esc = lambda s: re.sub(r"(^|\s)([□☑→·(『「①②③④⑤]) ", lambda m: m.group(1) + m.group(2) + "\u00a0", html.escape(s or ""))  # 줄 끝 금칙(기호를 다음 단어에 붙임)
    credit = art_credit_line(images)
    vals = {
        "css": css, "brand": BRAND, "handle": HANDLE, "num": f"{n:02d}", "total": f"{total:02d}",
        "headline": esc(card.get("headline")), "body": esc(card.get("body")).replace("\n", "<br>"),
        "kind": f'<span class="kind" data-font>{esc(post.get("type"))}</span>' if post.get("type") else "",
        "plate": plate_html(img, "plate band" if tpl_name == "last" else "plate"),
        "extra": ("" if img else "no-image") + (" " + img["entry"]["layout"] if img and img["entry"].get("layout") else ""),
        "credit": f'<p class="credit" data-check="그림·사진 출처 줄" data-maxlines="4" data-font>{esc(credit).replace(chr(10), "<br>")}</p>' if credit else "",
        "mockup": "" if not mockup else '<div class="mockup">MOCKUP</div>',
    }
    texts = {"title": card.get("headline", ""), "body": card.get("body", "") + BRAND + HANDLE + (post.get("type") or "") + credit
             + (overlay_text(img["entry"].get("overlay")) if img else "")
             + "".join(images[k]["entry"].get("credit", "") for k in images if images[k]["kind"] == "photo"),
             "num": f"{n:02d}{total:02d}"}
    return tpl.substitute(vals), texts, tpl_name


def contact_sheet(paths, title, out, tile=(360, 450), per_row=4, big=(540, 675)):
    """검수용 한 장: 위 = 8장 원본(1/2 축소, 540x675) 4x2, 아래 = 피드 폭 360x450 8장 한 줄(실제 피드 크기)."""
    pad, head, lab = 24, 70, 34
    rows = (len(paths) + per_row - 1) // per_row
    w_big = pad + per_row * (big[0] + pad)
    w_small = pad + len(paths) * (tile[0] + pad)
    W = max(w_big, w_small)
    H = head + rows * (big[1] + pad + lab) + 50 + tile[1] + lab + pad
    sheet = Image.new("RGB", (W, H), "#1B1F2A")
    d = ImageDraw.Draw(sheet)
    try:
        f1 = ImageFont.truetype(os.path.join(FONT_DIR, "MaruBuri-Bold.ttf"), 26)
        f2 = ImageFont.truetype(os.path.join(FONT_DIR, "MaruBuri-Regular.ttf"), 20)
    except Exception:
        f1 = f2 = ImageFont.load_default()
    d.text((pad, 22), title + "   |   위: 원본 1/2 (540x675)   아래: 피드 폭 360x450", font=f1, fill="#FFD23F")
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB")
        x = pad + (i % per_row) * (big[0] + pad)
        y = head + (i // per_row) * (big[1] + pad + lab)
        sheet.paste(im.resize(big, Image.LANCZOS), (x, y))
        d.text((x, y + big[1] + 6), os.path.basename(p), font=f2, fill="#FFFFFF")
    y0 = head + rows * (big[1] + pad + lab) + 30
    d.text((pad, y0 - 6), "360px (feed)", font=f2, fill="#FFD23F")
    for i, p in enumerate(paths):
        x = pad + i * (tile[0] + pad)
        sheet.paste(Image.open(p).convert("RGB").resize(tile, Image.LANCZOS), (x, y0 + 20))
    sheet.save(out, optimize=True)


def render_post(post_dir, out_dir, final, keep_html):
    with open(os.path.join(post_dir, "cards.json"), encoding="utf-8") as fp:
        post = json.load(fp)
    cards = sorted(post.get("cards", []), key=lambda c: c.get("n", 0))
    total = len(cards)
    date = post.get("date") or os.path.basename(os.path.normpath(post_dir))
    work = os.path.join(REPO, "render", "cardnews-v3", date)
    os.makedirs(work, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    images = load_images(post_dir, post, total, work)
    notes = images.pop("_notes", None)
    css = font_faces() + "\n" + open(os.path.join(HERE, "tokens.css"), encoding="utf-8").read().replace(
        "var(--grain)", f'url("{file_url(grain_tile(work))}")')
    job, texts_by_n, tpl_by_n = {"cards": []}, {}, {}
    for i, c in enumerate(cards):
        n = c.get("n", i + 1)
        doc, texts, tpl = build_html(post, c, i, total, images, css, mockup=not final)
        hp = os.path.join(work, f"card-{n:02d}.html")
        with open(hp, "w", encoding="utf-8") as fp:
            fp.write(doc)
        job["cards"].append({"n": n, "html": hp, "png": os.path.join(out_dir, f"card-{n:02d}.png")})
        texts_by_n[n], tpl_by_n[n] = texts, tpl
    jp = os.path.join(work, "job.json")
    with open(jp, "w", encoding="utf-8") as fp:
        json.dump(job, fp)
    env = dict(os.environ)
    env["NODE_PATH"] = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()

    def shoot():
        r = subprocess.run(["node", os.path.join(HERE, "shoot.cjs"), jp], capture_output=True, text=True, env=env, timeout=600)
        if r.returncode != 0:
            raise SystemExit(f"Chromium 렌더 실패: {r.stderr[-2000:]}")
        return {s["n"]: s for s in json.loads(r.stdout)}
    shots = shoot()
    # 콜라주 슬롯 실측 맞춤: 그림 칸 실제 크기로 콜라주를 다시 만들어 CSS cover 가 원화 프레임 테두리를 자르지 않게 한다(2판)
    refit = False
    for n, img in images.items():
        if not img.get("collage_path"):
            continue
        box = next((im["box"] for im in shots[n]["metrics"]["imgs"] if "collage" in urllib.parse.unquote(im["src"])), None)
        if box:
            want = [int(round(box[2] - box[0])), int(round(box[3] - box[1]))]
            if want != img["edit"]["collage"]["slot"]:
                build_collage(img, os.path.join(post_dir, "photos"), work, n, "LAYOUT", slot=want)
                refit = True
    if refit:
        shots = shoot()
    fails, warns, per_card = [], [], {}
    layouts = {}
    for c in job["cards"]:
        img = images.get(c["n"])
        layouts[c["n"]] = tpl_by_n[c["n"]] + (("-" + img["entry"]["layout"]) if img and img["entry"].get("layout") else "")
    seq = [layouts[c["n"]] for c in job["cards"]]
    for i in range(len(seq) - 2):
        if seq[i] == seq[i + 1] == seq[i + 2]:
            fails.append(f"card-{job['cards'][i]['n']:02d}~{job['cards'][i + 2]['n']:02d}: 같은 레이아웃 3연속({seq[i]})")
    for n, img in images.items():
        sc = (img["edit"] or {}).get("collage", {}).get("photo_scale", 0)
        if sc > 1.6:
            warns.append(f"card-{n:02d}: 사진 {sc:.2f}배 확대(해상도 낮음)")
    for c in job["cards"]:
        n = c["n"]
        s = shots[n]
        m = s["metrics"]
        rec = {"template": tpl_by_n[n], "layout": layouts[n], "fonts_used": s["fonts"], "checks": []}
        for ch in m["checks"]:
            item = {"check": ch["check"], "lines": ch["lines"], "max": ch["max"]}
            if ch["max"] and ch["lines"] > ch["max"]:
                fails.append(f"card-{n:02d}: 줄 초과 {ch['check']} {ch['lines']}줄 > {ch['max']}줄")
            if ch["overflow"]:
                fails.append(f"card-{n:02d}: 넘침 {ch['check']}")
            x0, y0, x1, y1 = ch["box"]
            if x0 < SAFE[0] - 1 or y0 < SAFE[1] - 1 or x1 > SAFE[2] + 1 or y1 > SAFE[3] + 1:
                fails.append(f"card-{n:02d}: 안전 영역 밖 {ch['check']} {[round(v) for v in ch['box']]}")
            rec["checks"].append(item)
        if m["contentBottom"] > 1350 - SAFE[1] + 1:
            fails.append(f"card-{n:02d}: 세로 넘침(내용 끝 y {round(m['contentBottom'])})")
        for im in m["imgs"]:
            if not im["ok"]:
                fails.append(f"card-{n:02d}: 이미지 로드 실패 {im['src']}")
            else:
                w = im["box"][2] - im["box"][0]
                h = im["box"][3] - im["box"][1]
                if h < 300 and tpl_by_n[n] == "body":
                    warns.append(f"card-{n:02d}: 그림 칸 높이 {round(h)}px(<300)")
                scale = max(w / max(1, im["natural"][0]), h / max(1, im["natural"][1]))
                if scale > 1.6:
                    warns.append(f"card-{n:02d}: 이미지 {scale:.2f}배 확대(해상도 낮음)")
        bad_fonts = [f for f in s["fonts"] if "(system)" in f or not any(f.startswith(a) for a in ALLOWED_FAMILIES)]  # 가변 서체는 "Noto Serif KR ExtraLight"처럼 보고됨
        if bad_fonts:
            fails.append(f"card-{n:02d}: 지정 외 서체 사용 {bad_fonts}")
        tf = tofu(texts_by_n[n]["title"], "title") + tofu(texts_by_n[n]["body"], "body") + tofu(texts_by_n[n]["num"], "num")
        if tf:
            fails.append(f"card-{n:02d}: 글리프 누락 {''.join(tf)}")
        if n in images:
            img = images[n]
            rec["image"] = {"kind": img["kind"], **{k: img["entry"].get(k) for k in (
                "ref", "file", "title", "title_ko", "author", "institution", "page_url", "object_url", "image_url", "file_url", "downloaded_from",
                "license", "license_url", "credit", "credit_short", "accession", "model", "endpoint", "model_license", "terms_url", "seed",
                "generated_at", "why", "overlay") if img["entry"].get(k)},
                "license_status": img.get("license_status"), "edit": img["edit"]}
            if img["entry"].get("frame"):
                fr = img["entry"]["frame"]
                rec["image"]["frame"] = {k: fr.get(k) for k in ("file", "title", "institution", "accession", "object_url", "credit_short", "license", "crop", "detail") if fr.get(k)}
        per_card[f"card-{n:02d}"] = rec
    paths = [c["png"] for c in job["cards"]]
    cpath = os.path.join(out_dir, "contact.png")
    contact_sheet(paths, f"{post.get('post_id', date)}  v3 contact (360x450 = feed width)  {'final' if final else 'MOCKUP'}", cpath)
    log = {"mode": "final" if final else "mockup", "rendered_at": _dt.datetime.utcnow().isoformat() + "Z",
           "renderer": "cardnews/design/v3/render_v3.py", "renderer_version": RENDERER_VERSION,
           "engine": "HTML/CSS + Playwright Chromium (node playwright 1.56.1, /opt/pw-browsers/chromium-1194)",
           "cards": total, "fonts": font_log(), "font_rule": "지정 4서체 외(시스템 폴백) 사용 시 실패",
           "ai_label_on_card": False, "content_changed": False,
           "content_rule": "사진·원화는 크롭·톤·그레인·흐림(로고·각인·문자판)·테두리만. 합성·사물 추가·생성형 채우기 없음. 4·6·7장 그래픽은 사진 위 별도 코드 층(오버레이)",
           "layout_sequence": seq, "notes": notes, "ai_label_note": "AI 표시 라벨은 카드에 없음(대표 결정 2026-10-02). 캡션 담당",
           "art_credit_line": art_credit_line(images), "images_used": sorted(f"card-{k:02d}:{v['kind']}" for k, v in images.items()),
           "checks_failed": fails, "warnings": warns, "per_card": per_card}
    with open(os.path.join(out_dir, "RENDER.json"), "w", encoding="utf-8") as fp:
        json.dump(log, fp, ensure_ascii=False, indent=2)
    if not keep_html:
        for c in job["cards"]:
            pass  # HTML은 render/ (커밋 제외)에 남겨 재현·디버그용으로 둔다
    print(f"[{post_dir}] {total}장 -> {out_dir} | 실패 {len(fails)} · 경고 {len(warns)} | 서체 {sorted({f for s in shots.values() for f in s['fonts']})}")
    for f in fails:
        print("  FAIL:", f)
    for w in warns:
        print("  warn:", w)
    return fails, warns


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("post_dir", nargs="?")
    ap.add_argument("--all", metavar="POSTS_DIR")
    ap.add_argument("--out", metavar="DIR", help="결과를 DIR/<날짜>/ 에 저장(기본: 게시물 폴더)")
    ap.add_argument("--final", action="store_true", help="게시용(MOCKUP 없음). approved 후에만")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--keep-html", action="store_true")
    args = ap.parse_args()
    fail_fonts()
    targets = [d for d in sorted(glob.glob(os.path.join(args.all, "*"))) if os.path.isfile(os.path.join(d, "cards.json"))] \
        if args.all else ([args.post_dir] if args.post_dir else [])
    if not targets:
        ap.error("post_dir 또는 --all")
    nf = 0
    for t in targets:
        out = os.path.join(args.out, os.path.basename(os.path.normpath(t))) if args.out else t
        f, _ = render_post(t, out, args.final, args.keep_html)
        nf += len(f)
    print(f"합계: {len(targets)}세트, 검수 실패 {nf}")
    return 3 if (args.strict and nf) else 0


if __name__ == "__main__":
    sys.exit(main())
