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
AI_NOTICE_AI = "이미지·초안은 AI로 생성, 사실 확인은 사람이 했습니다"   # legal v3 통과 문구(AI 이미지가 있는 게시물)
AI_NOTICE_NO_AI = "초안은 AI 도움을 받았고, 사실 확인은 사람이 했습니다"  # 1안(AI 이미지 0) 제안 문구 - 대표 결정 대기(DESIGN_SOURCES §8 #7)
SAFE = (88, 92, 1080 - 88, 1350 - 92)
RENDERER_VERSION = "v3.0-proto1 (2026-10-02)"


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
    if os.path.isfile(jpath):
        with open(jpath, encoding="utf-8") as fp:
            data = json.load(fp)
        for e in data.get("photos", []) if isinstance(data, dict) else data:
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
            out[n] = {"kind": kind, "path": dst, "entry": e, "edit": rec, "license_status": st}
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


def plate_html(img, cls="plate"):
    if not img:
        return ""
    fx, fy = (img["edit"] or {}).get("focus", [0.5, 0.5]) if img.get("edit") else (0.5, 0.5)
    pill = ""
    e = img["entry"]
    if img["kind"] == "photo" and e.get("credit_on_image", True):
        pill = f'<span class="credit-pill" data-check="사진 크레딧" data-maxlines="1" data-font>{html.escape(e["credit"])}</span>'
    return (f'<figure class="{cls}"><img src="{file_url(img["path"])}" alt="" '
            f'style="object-position:{fx * 100:.1f}% {fy * 100:.1f}%">{pill}</figure>')


def art_credit_line(images):
    """마지막 장 고정 출처 줄: '그림: 메트로폴리탄미술관 〈책가도〉 CC0 · ...' (PHOTOS.json credit_short, 중복 제거)."""
    seen = []
    for n in sorted(images):
        e = images[n]["entry"]
        if images[n]["kind"] in ("artwork",) or (images[n]["kind"] == "photo" and not e.get("credit_on_image", True)):
            s = e.get("credit_short") or e.get("credit")
            if s and s not in seen:
                seen.append(s)
    return ("그림: " + " · ".join(seen)) if seen else ""


def build_html(post, card, idx, total, images, css, mockup):
    tpl_name = "cover" if idx == 0 else "last" if idx == total - 1 else "body"
    with open(os.path.join(HERE, "templates", f"{tpl_name}.html"), encoding="utf-8") as fp:
        tpl = string.Template(fp.read())
    n = card.get("n", idx + 1)
    img = images.get(n)
    esc = lambda s: re.sub(r"(^|\s)([□☑→·(『「①②③④⑤]) ", lambda m: m.group(1) + m.group(2) + "\u00a0", html.escape(s or ""))  # 줄 끝 금칙(기호를 다음 단어에 붙임)
    any_ai = any(v["kind"] == "ai_plate" for v in images.values())
    credit = art_credit_line(images)
    vals = {
        "css": css, "brand": BRAND, "handle": HANDLE, "num": f"{n:02d}", "total": f"{total:02d}",
        "headline": esc(card.get("headline")), "body": esc(card.get("body")).replace("\n", "<br>"),
        "kind": f'<span class="kind" data-font>{esc(post.get("type"))}</span>' if post.get("type") else "",
        "plate": plate_html(img, "plate band" if tpl_name == "last" else "plate"),
        "extra": "" if img else "no-image",
        "credit": f'<p class="credit" data-check="그림 출처 줄" data-maxlines="2" data-font>{esc(credit)}</p>' if credit else "",
        "ai": esc(AI_NOTICE_AI if any_ai else AI_NOTICE_NO_AI),
        "mockup": "" if not mockup else '<div class="mockup">MOCKUP</div>',
    }
    texts = {"title": card.get("headline", ""), "body": card.get("body", "") + BRAND + HANDLE + (post.get("type") or "") + credit
             + vals["ai"] + "".join(images[k]["entry"].get("credit", "") for k in images if images[k]["kind"] == "photo"),
             "num": f"{n:02d}{total:02d}"}
    return tpl.substitute(vals), texts, tpl_name


def contact_sheet(paths, title, out, tile=(360, 450), per_row=4):
    pad, head = 24, 70
    rows = (len(paths) + per_row - 1) // per_row
    cols = min(per_row, len(paths))
    sheet = Image.new("RGB", (pad + cols * (tile[0] + pad), head + rows * (tile[1] + pad + 30) + pad), "#1B1F2A")
    d = ImageDraw.Draw(sheet)
    try:
        f1 = ImageFont.truetype(os.path.join(FONT_DIR, "MaruBuri-Bold.ttf"), 26)
        f2 = ImageFont.truetype(os.path.join(FONT_DIR, "MaruBuri-Regular.ttf"), 20)
    except Exception:
        f1 = f2 = ImageFont.load_default()
    d.text((pad, 22), title, font=f1, fill="#FFD23F")
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB").resize(tile, Image.LANCZOS)
        x = pad + (i % per_row) * (tile[0] + pad)
        y = head + (i // per_row) * (tile[1] + pad + 30)
        sheet.paste(im, (x, y))
        d.text((x, y + tile[1] + 6), os.path.basename(p), font=f2, fill="#FFFFFF")
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
    r = subprocess.run(["node", os.path.join(HERE, "shoot.cjs"), jp], capture_output=True, text=True, env=env, timeout=600)
    if r.returncode != 0:
        raise SystemExit(f"Chromium 렌더 실패: {r.stderr[-2000:]}")
    shots = {s["n"]: s for s in json.loads(r.stdout)}
    fails, warns, per_card = [], [], {}
    for c in job["cards"]:
        n = c["n"]
        s = shots[n]
        m = s["metrics"]
        rec = {"template": tpl_by_n[n], "fonts_used": s["fonts"], "checks": []}
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
                "file", "title", "title_ko", "institution", "object_url", "image_url", "license", "license_url", "credit",
                "credit_short", "accession", "model", "endpoint", "model_license", "terms_url", "seed", "generated_at") if img["entry"].get(k)},
                "license_status": img.get("license_status"), "edit": img["edit"]}
        per_card[f"card-{n:02d}"] = rec
    paths = [c["png"] for c in job["cards"]]
    cpath = os.path.join(out_dir, "contact.png")
    contact_sheet(paths, f"{post.get('post_id', date)}  v3 contact (360x450 = feed width)  {'final' if final else 'MOCKUP'}", cpath)
    any_ai = any(v["kind"] == "ai_plate" for v in images.values())
    log = {"mode": "final" if final else "mockup", "rendered_at": _dt.datetime.utcnow().isoformat() + "Z",
           "renderer": "cardnews/design/v3/render_v3.py", "renderer_version": RENDERER_VERSION,
           "engine": "HTML/CSS + Playwright Chromium (node playwright 1.56.1, /opt/pw-browsers/chromium-1194)",
           "cards": total, "fonts": font_log(), "font_rule": "지정 4서체 외(시스템 폴백) 사용 시 실패",
           "ai_notice": AI_NOTICE_AI if any_ai else AI_NOTICE_NO_AI,
           "ai_notice_status": "legal v3 통과 문구" if any_ai else "제안 문구, 대표 결정 대기(DESIGN_SOURCES §8 #7)",
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
