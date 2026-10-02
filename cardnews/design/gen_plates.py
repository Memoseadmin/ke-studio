#!/usr/bin/env python3
"""카드뉴스 AI 민화 배경(플레이트) 생성기. fal `fal-ai/z-image/turbo`(Tongyi-MAI Z-Image-Turbo, Apache-2.0).

기본은 dry-run: 프롬프트만 만들어 <post_dir>/plates/prompts.json 에 저장하고 네트워크를 쓰지 않는다.
--execute 일 때만 환경변수 FAL_KEY 로 호출해 <post_dir>/plates/card-NN.png + PLATES.json 을 쓴다(키 값은 출력하지 않음).

사용:
  python3 gen_plates.py --posts cardnews/posts                                   # 14세트 dry-run
  python3 gen_plates.py --posts cardnews/posts --sets 2026-10-09,2026-10-12      # 일부 세트만
  python3 gen_plates.py --posts cardnews/posts --sets 2026-10-09 --variants 4 --execute   # 표지 시안 4개 + 나머지 장 1개
  python3 gen_plates.py --posts cardnews/posts --pick 2026-10-09:1=2             # 표지 시안 v2 를 card-01.png 로 채택

설정: plate_style.json(공통 스타일·팔레트·네거티브·크기·seed 규칙·금지어) + plate_subjects.json(세트 주제, 장별 덮어쓰기).
규칙: 마지막 장은 생성하지 않는다(렌더러 단청 띠). visual 에 "프로그램으로 그린"이 있으면 코드 도형 유지(생성 안 함).
금지: 실존 인물·브랜드·상품 포장·영화 장면·기존 작품 모사·호랑이·까치·글자(DESIGN-v2.md §3, 디자인 시스템 §6).
"""
import argparse
import datetime as _dt
import glob
import hashlib
import json
import os
import re
import shutil
import ssl
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
NEG_CLAUSE = re.compile(r"금지|없음|없는|없이|제외|않음|아님|모사")


def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError:
        return default


def sanitize_visual(visual, style):
    """cards.json visual(한국어 메모) -> 그림 주제. 금지·부정 절, 인용 글자, 숫자, 레이아웃 용어를 뺀다."""
    clauses = [c.strip() for c in re.split(r"[.\n]|,(?=\s)", visual or "") if c.strip()]
    keep = [c for c in clauses if not NEG_CLAUSE.search(c)]
    s = ", ".join(keep)
    s = re.sub(r"['\"‘’“”『』「」][^'\"‘’“”『』「」]*['\"‘’“”『』「」]", " ", s)  # 인용된 글자(그리면 안 되는 텍스트)
    s = re.sub(r"[①-⑳]", " ", s)
    # 숫자·날짜(그림 안 숫자 금지) + 바로 붙은 단위어
    s = re.sub(r"\d[\d,./~:+%\-→]*\s*(개|권|장|월|일|세기|열|년|자|명|곳|번|칸|돌)?", " ", s)
    for t in sorted(style.get("strip_terms", []), key=len, reverse=True):
        s = s.replace(t, " ")
    s = s.replace("→", " ").replace("+", " ")
    for _ in range(2):  # 지운 말 뒤에 홀로 남은 조사·연결어
        s = re.sub(r"(?<![가-힣])(은|는|이|가|을|를|로|으로|로만|와|과|의|에|도|만|대신|대)(?![가-힣])", " ", s)
    s = re.sub(r"\S+(은|는)(?=\s*(,|$))", " ", s)  # 술어를 지워 홀로 남은 주제어("전시명은", "제목은")
    s = re.sub(r"\(\s*[,·]?\s*\)", " ", s)
    s = re.sub(r"\s*([,·:])\s*", r"\1 ", s)
    s = re.sub(r"([,·]\s*){2,}", ", ", s)
    s = re.sub(r"\s{2,}", " ", s).strip(" ,·:")
    return s


def subject_quality(ko):
    """정리 뒤 주제가 너무 짧거나 깨졌으면 'review'(사람이 plate_subjects.json 덮어쓰기 검토)."""
    hangul = len(re.findall(r"[가-힣]", ko))
    if hangul < 10 or re.match(r"^[,·:(]", ko) or re.search(r"(?<![가-힣])(빈|옆에|세로|가로)$", ko):
        return "review"
    return "ok"


_PARTICLES = "을를이가은는와과의에도만로"


def english_hints(text, style):
    """한국어 주제에서 사전 단어를 찾아 영어 힌트(Z-Image 텍스트 인코더 보조). 단어 앞은 한글이 아니고 뒤는 조사·비한글."""
    hits = []
    for ko, en in sorted(style.get("lexicon", {}).items(), key=lambda kv: -len(kv[0])):
        if re.search(rf"(?<![가-힣]){re.escape(ko)}(?=$|[^가-힣]|[{_PARTICLES}](?![가-힣]))", text) and en not in hits:
            hits.append(en)
    return hits[:8]


def banned_terms(text, style):
    t = text.lower()
    return [w for w in style.get("banned_subject_terms", []) if w.lower() in t]


def seed_for(date, card, variant=0):
    """seed = MMDD*1000 + card*10 + variant (plate_style.json seed_rule)."""
    mmdd = int(date[5:7] + date[8:10])
    return mmdd * 1000 + int(card) * 10 + int(variant)


def build_prompt(role, subject, theme, style):
    """marketing-skills-image 공식: Subject + Setting + Style + Lighting + Composition + Constraints."""
    comp = style["composition"]["cover" if role == "cover" else "body"]
    parts = [subject.rstrip(". "),
             f"Theme: {theme}" if theme else "",
             style["style"], style["lighting"], comp, style["constraints"]]
    return ". ".join(p for p in parts if p) + "."


def plan_post(post_dir, style, subjects, variants=1, cards_filter=None):
    with open(os.path.join(post_dir, "cards.json"), encoding="utf-8") as fp:
        post = json.load(fp)
    date = post.get("date") or os.path.basename(os.path.normpath(post_dir))
    cards = sorted(post.get("cards", []), key=lambda c: c.get("n", 0))
    total = len(cards)
    sset = subjects.get("sets", {}).get(date, {})
    theme = sset.get("theme", "")
    rows = []
    for i, c in enumerate(cards):
        n = c.get("n", i + 1)
        if cards_filter and n not in cards_filter:
            continue
        role = "cover" if i == 0 else "last" if i == total - 1 else "body"
        row = {"card": n, "role": role, "visual": c.get("visual", "")}
        if role == "last":
            row["skip"] = "마지막 장: 렌더러 코드 단청 띠 유지(생성 안 함)"
            rows.append(row)
            continue
        if any(m in (c.get("visual") or "") for m in style.get("code_only_markers", [])):
            row["skip"] = "visual 이 프로그램 도형(막대 등)을 지정: 코드 도형 유지(생성 안 함)"
            rows.append(row)
            continue
        override = sset.get("cards", {}).get(str(n))
        if override:
            subj, src, quality = override, "override(plate_subjects.json)", "ok"
            hints = []
        else:
            ko = sanitize_visual(c.get("visual", ""), style)
            hints = english_hints(ko, style)
            subj = f"{ko} ({', '.join(hints)})" if hints else ko
            src, quality = "visual(cards.json, 정리)", subject_quality(ko)
        bad = banned_terms(subj + " " + theme, style)
        if bad:
            row.update({"skip": f"금지어 {bad} -> plate_subjects.json 덮어쓰기 필요", "subject": subj})
            rows.append(row)
            continue
        if not subj.strip():
            row.update({"skip": "주제가 비었다 -> plate_subjects.json 덮어쓰기 필요"})
            rows.append(row)
            continue
        prompt = build_prompt(role, subj, theme, style)
        nvar = max(1, variants) if role == "cover" else 1
        row.update({"subject": subj, "subject_source": src, "subject_quality": quality, "english_hints": hints, "prompt": prompt,
                    "prompt_words": len(prompt.split()), "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                    "seeds": [seed_for(date, n, v) for v in range(nvar)],
                    "crop_aspect": style["crop_aspect"]["cover" if role == "cover" else "body"]})
        rows.append(row)
    return post, date, theme, rows


def common_meta(style):
    return {k: style.get(k) for k in ["style_version", "model", "model_card", "model_license", "endpoint", "endpoint_url",
                                       "terms_url", "terms_note", "price_estimate", "seed_rule", "negative_note"]}


# ---------- 실행(--execute) ----------
def _ssl_ctx():
    ca = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE") or os.environ.get("CURL_CA_BUNDLE")
    return ssl.create_default_context(cafile=ca) if ca and os.path.isfile(ca) else ssl.create_default_context()


def call_fal(url, key, payload, timeout=180):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST",
                                 headers={"Authorization": f"Key {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx()) as r:
        return json.loads(r.read().decode())


def download(url, path, timeout=120):
    with urllib.request.urlopen(url, timeout=timeout, context=_ssl_ctx()) as r, open(path, "wb") as fp:
        shutil.copyfileobj(r, fp)


def crop_to_aspect(path, aspect):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    w, h = im.size
    target = aspect[0] / aspect[1]
    if w / h > target:
        nw = int(round(h * target)); x = (w - nw) // 2
        im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(round(w / target)); y = (h - nh) // 2
        im = im.crop((0, y, w, y + nh))
    im.save(path, optimize=True)
    return im.size


def execute_post(post_dir, date, rows, style, key):
    pdir = os.path.join(post_dir, "plates")
    os.makedirs(os.path.join(pdir, "variants"), exist_ok=True)
    meta_path = os.path.join(pdir, "PLATES.json")
    meta = load_json(meta_path, {}) or {}
    meta.update(common_meta(style))
    meta["set"] = date
    meta["license_note"] = "모델 가중치 Apache-2.0. 생성물 권리·책임은 fal 약관(terms_url) + 사람 검수"
    done = {int(c["card"]): c for c in meta.get("cards", [])}
    req_base = dict(style["request"])
    for row in rows:
        if row.get("skip"):
            continue
        n = row["card"]
        variants = []
        for v, seed in enumerate(row["seeds"]):
            payload = dict(req_base, prompt=row["prompt"], seed=seed)
            for attempt in range(3):
                try:
                    res = call_fal(style["endpoint_url"], key, payload)
                    break
                except Exception as e:  # 키 값은 출력하지 않는다
                    print(f"  [{date} card-{n:02d} v{v}] 호출 실패({type(e).__name__}), 재시도 {attempt + 1}/3", file=sys.stderr)
                    time.sleep(3 * (attempt + 1))
            else:
                print(f"  [{date} card-{n:02d} v{v}] 실패, 건너뜀", file=sys.stderr)
                continue
            nsfw = (res.get("has_nsfw_concepts") or [False])[0]
            if nsfw:
                print(f"  [{date} card-{n:02d} v{v}] 안전 검사 걸림(검은 이미지) -> 저장 안 함", file=sys.stderr)
                continue
            img = res["images"][0]
            out = os.path.join(pdir, "variants", f"card-{n:02d}-v{v}.png")
            download(img["url"], out)
            size = crop_to_aspect(out, row["crop_aspect"])
            variants.append({"variant": v, "seed": res.get("seed", seed), "file": os.path.relpath(out, post_dir),
                             "generated_at": _dt.datetime.utcnow().isoformat() + "Z", "size": list(size),
                             "timings": res.get("timings")})
            print(f"  [{date} card-{n:02d} v{v}] seed {seed} -> {os.path.relpath(out)} {size[0]}x{size[1]}")
        if not variants:
            continue
        shutil.copyfile(os.path.join(post_dir, variants[0]["file"]), os.path.join(pdir, f"card-{n:02d}.png"))
        done[n] = {"card": n, "role": row["role"], "file": f"plates/card-{n:02d}.png", "picked_variant": 0,
                   "prompt": row["prompt"], "prompt_sha256": row["prompt_sha256"], "negative": style["negative"],
                   "subject_source": row["subject_source"], "seed": variants[0]["seed"],
                   "generated_at": variants[0]["generated_at"], "request": dict(req_base), "variants": variants,
                   "human_review": "대기(사람이 글자·인물·로고·호랑이·까치·기존 작품 모사 없음 확인 후 '통과' 기록)"}
    meta["cards"] = [done[k] for k in sorted(done)]
    with open(meta_path, "w", encoding="utf-8") as fp:
        json.dump(meta, fp, ensure_ascii=False, indent=2)
    return meta_path


def pick(posts, spec):
    """--pick 2026-10-09:1=2 -> variants/card-01-v2.png 를 card-01.png 로, PLATES.json 기록 갱신."""
    m = re.match(r"(\d{4}-\d{2}-\d{2}):(\d+)=(\d+)$", spec)
    if not m:
        raise SystemExit(f"--pick 형식: YYYY-MM-DD:카드=시안 ({spec})")
    date, n, v = m.group(1), int(m.group(2)), int(m.group(3))
    pdir = os.path.join(posts, date, "plates")
    src = os.path.join(pdir, "variants", f"card-{n:02d}-v{v}.png")
    if not os.path.isfile(src):
        raise SystemExit(f"시안 파일 없음: {src}")
    shutil.copyfile(src, os.path.join(pdir, f"card-{n:02d}.png"))
    meta_path = os.path.join(pdir, "PLATES.json")
    meta = load_json(meta_path, {}) or {}
    for c in meta.get("cards", []):
        if int(c["card"]) == n:
            c["picked_variant"] = v
            vv = next((x for x in c.get("variants", []) if x["variant"] == v), None)
            if vv:
                c["seed"], c["generated_at"] = vv["seed"], vv["generated_at"]
            c["picked_at"] = _dt.datetime.utcnow().isoformat() + "Z"
    with open(meta_path, "w", encoding="utf-8") as fp:
        json.dump(meta, fp, ensure_ascii=False, indent=2)
    print(f"{date} card-{n:02d}: 시안 v{v} 채택")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--posts", default=os.path.join(HERE, "..", "posts"), help="날짜 폴더들이 있는 곳(기본 cardnews/posts)")
    ap.add_argument("--sets", help="쉼표로 구분한 날짜(예: 2026-10-09,2026-10-12). 없으면 전부")
    ap.add_argument("--cards", help="쉼표로 구분한 장 번호(예: 1,3). 없으면 마지막 장 제외 전부")
    ap.add_argument("--variants", type=int, default=1, help="표지(1장) 시안 개수. 본문 장은 1개")
    ap.add_argument("--style", default=os.path.join(HERE, "plate_style.json"))
    ap.add_argument("--subjects", default=os.path.join(HERE, "plate_subjects.json"))
    ap.add_argument("--execute", action="store_true", help="실제 생성(FAL_KEY 필요, 과금). 없으면 dry-run")
    ap.add_argument("--pick", metavar="DATE:CARD=VARIANT", help="표지 시안 채택")
    args = ap.parse_args()
    posts = os.path.normpath(args.posts)
    if args.pick:
        pick(posts, args.pick)
        return 0
    style = load_json(args.style)
    subjects = load_json(args.subjects, {"sets": {}})
    sets = [s.strip() for s in args.sets.split(",")] if args.sets else None
    cards_filter = {int(x) for x in args.cards.split(",")} if args.cards else None
    targets = [d for d in sorted(glob.glob(os.path.join(posts, "*"))) if os.path.isfile(os.path.join(d, "cards.json"))
               and (not sets or os.path.basename(d) in sets)]
    if not targets:
        print("대상 세트 없음"); return 1
    key = None
    if args.execute:
        key = os.environ.get("FAL_KEY") or os.environ.get("IMAGE_API_KEY")
        if not key:
            print("FAL_KEY 가 설정되지 않았다(값은 출력하지 않음). dry-run 으로 다시 실행하거나 키를 넣어라.", file=sys.stderr)
            return 2
    n_img = n_skip = 0
    mp = style["request"]["image_size"]["width"] * style["request"]["image_size"]["height"] / 1e6
    for d in targets:
        post, date, theme, rows = plan_post(d, style, subjects, args.variants, cards_filter)
        pdir = os.path.join(d, "plates")
        os.makedirs(pdir, exist_ok=True)
        doc = dict(common_meta(style), set=date, post_id=post.get("post_id"), theme=theme,
                   request=style["request"], negative=style["negative"], created_at=_dt.datetime.utcnow().isoformat() + "Z",
                   mode="execute" if args.execute else "dry-run", cards=rows)
        with open(os.path.join(pdir, "prompts.json"), "w", encoding="utf-8") as fp:
            json.dump(doc, fp, ensure_ascii=False, indent=2)
        imgs = sum(len(r.get("seeds", [])) for r in rows)
        skips = [r for r in rows if r.get("skip")]
        n_img += imgs
        n_skip += len(skips)
        print(f"[{date}] 생성 {imgs}장 · 건너뜀 {len(skips)}장 -> {os.path.relpath(pdir)}/prompts.json")
        for r in skips:
            if not r["skip"].startswith("마지막 장"):
                print(f"  card-{r['card']:02d}: {r['skip']}")
        for r in rows:
            if r.get("subject_quality") == "review":
                print(f"  card-{r['card']:02d}: 주제 검토 필요(정리 후 '{r['subject'][:40]}') -> plate_subjects.json 덮어쓰기 권장")
            if r.get("prompt_words", 0) > style.get("prompt_words_target", [40, 95])[1]:
                print(f"  card-{r['card']:02d}: 프롬프트 {r['prompt_words']}단어(목표 상한 {style['prompt_words_target'][1]})")
        if args.execute:
            print("  ->", execute_post(d, date, rows, style, key))
    print(f"합계: {len(targets)}세트 · 생성 예정 {n_img}장 · 건너뜀 {n_skip}장 · 예상 비용 약 ${n_img * mp * 0.005:.2f}"
          f" ({mp:.2f}MP/장 x $0.005/MP, 추정치)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
