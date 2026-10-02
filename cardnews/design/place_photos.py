#!/usr/bin/env python3
"""researcher 사진 목록(cardnews/design/photos/C1-1-photos.json) -> 게시물별 <post_dir>/photos/PHOTOS.json (+ 사진 파일).

기본은 점검만(dry-run): 필수 필드·라이선스를 검사하고 배치 계획을 출력한다. 파일을 쓰지 않는다.
  --write     게시물별 photos/PHOTOS.json 작성(해당 날짜 항목만, 렌더러가 읽는 형식)
  --download  file_url 을 photos/card-NN.<ext> 로 내려받고 크기·sha256 기록(--write 포함)

목록 형식: [ {date, card, file_url | file, credit, license, source?, source_url?, author?, license_url?, focus?, pick?, rank?}, ... ]
또는 {"photos": [...]}. 같은 (date, card)에 후보가 여러 개면 pick=true -> rank 가 가장 작은 것 -> 첫 항목 순으로 하나만 쓴다.
크레딧(credit)·라이선스(license)가 없거나 상업 이용·변경이 안 되는 라이선스면 그 항목은 거부한다(렌더러도 같은 규칙으로 렌더를 거부).
렌더러 우선순위: 사진 > AI 플레이트 > 코드 도형. 마지막 장(출처·CTA)은 사진을 넣지 않는다.
"""
import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import shutil
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_cards import license_status  # noqa: E402  같은 라이선스 판정 규칙을 공유

REQUIRED = ["date", "card", "credit", "license"]


def load_list(path):
    with open(path, encoding="utf-8") as fp:
        data = json.load(fp)
    return data.get("photos", []) if isinstance(data, dict) else data


def choose(entries):
    """(date, card)별 후보 하나 선택."""
    groups = {}
    for e in entries:
        groups.setdefault((str(e.get("date")), int(e.get("card") or 0)), []).append(e)
    chosen = {}
    for k, cands in groups.items():
        picked = [c for c in cands if c.get("pick") is True]
        if picked:
            chosen[k] = picked[0]
        else:
            chosen[k] = sorted(cands, key=lambda c: (c.get("rank") is None, c.get("rank") or 0))[0]
        chosen[k]["_candidates"] = len(cands)
    return chosen


def ext_from(url, ctype=None):
    m = re.search(r"\.(jpe?g|png|webp)(?:$|[?#])", url.lower())
    if m:
        return ".jpg" if m.group(1) in ("jpg", "jpeg") else "." + m.group(1)
    if ctype:
        return {"image/png": ".png", "image/webp": ".webp"}.get(ctype.split(";")[0].strip(), ".jpg")
    return ".jpg"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", default=os.path.join(HERE, "photos", "C1-1-photos.json"))
    ap.add_argument("--posts", default=os.path.join(HERE, "..", "posts"))
    ap.add_argument("--sets", help="쉼표로 구분한 날짜")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--download", action="store_true")
    args = ap.parse_args()
    if not os.path.isfile(args.list):
        print(f"목록 없음: {args.list} (researcher 작업 대기)"); return 1
    sets = set(s.strip() for s in args.sets.split(",")) if args.sets else None
    entries = load_list(args.list)
    ok, bad = {}, []
    for (date, card), e in sorted(choose(entries).items()):
        if sets and date not in sets:
            continue
        miss = [f for f in REQUIRED if not str(e.get(f) or "").strip()]
        if not (e.get("file_url") or e.get("file")):
            miss.append("file_url|file")
        if miss:
            bad.append(f"{date} card {card}: 필드 없음 {miss}"); continue
        st = license_status(e["license"])
        if st == "blocked":
            bad.append(f"{date} card {card}: 라이선스 '{e['license']}' 상업 이용·변경 불가 또는 미확인 -> 거부"); continue
        post_dir = os.path.join(args.posts, date)
        if not os.path.isfile(os.path.join(post_dir, "cards.json")):
            bad.append(f"{date}: 게시물 폴더 없음"); continue
        with open(os.path.join(post_dir, "cards.json"), encoding="utf-8") as fp:
            total = len(json.load(fp).get("cards", []))
        if card >= total:
            bad.append(f"{date} card {card}: 마지막 장(출처·CTA)에는 사진을 넣지 않는다"); continue
        ok.setdefault(date, []).append(dict(e, license_status=st))
    for date, es in sorted(ok.items()):
        print(f"[{date}] 사진 {len(es)}장: " + ", ".join(f"card {e['card']}({e['license_status']}, 후보 {e['_candidates']})" for e in es))
    for b in bad:
        print("  거부:", b)
    if not (args.write or args.download):
        print("dry-run: 파일을 쓰지 않았다(--write / --download)"); return 0 if not bad else 3
    for date, es in sorted(ok.items()):
        pdir = os.path.join(args.posts, date, "photos")
        os.makedirs(pdir, exist_ok=True)
        out = []
        for e in es:
            rec = {k: v for k, v in e.items() if not k.startswith("_") and k not in ("pick", "rank")}
            n = int(e["card"])
            if args.download and e.get("file_url"):
                tmp = os.path.join(pdir, f".card-{n:02d}.part")
                with urllib.request.urlopen(e["file_url"], timeout=120) as r, open(tmp, "wb") as fp:
                    ctype = r.headers.get("Content-Type")
                    shutil.copyfileobj(r, fp)
                name = f"card-{n:02d}{ext_from(e['file_url'], ctype)}"
                os.replace(tmp, os.path.join(pdir, name))
                rec["file"] = name
            elif e.get("file"):
                src = e["file"] if os.path.isabs(e["file"]) else os.path.join(os.path.dirname(os.path.abspath(args.list)), e["file"])
                if os.path.isfile(src):
                    name = f"card-{n:02d}{os.path.splitext(src)[1].lower()}"
                    shutil.copyfile(src, os.path.join(pdir, name))
                    rec["file"] = name
            if rec.get("file") and os.path.isfile(os.path.join(pdir, rec["file"])):
                from PIL import Image
                p = os.path.join(pdir, rec["file"])
                with Image.open(p) as im:
                    rec["pixels"] = list(im.size)
                with open(p, "rb") as fp:
                    rec["sha256"] = hashlib.sha256(fp.read()).hexdigest()
            rec.setdefault("focus", [0.5, 0.5])
            out.append(rec)
        doc = {"set": date, "source_list": os.path.relpath(args.list, os.path.join(HERE, "..", "..")),
               "placed_at": _dt.datetime.utcnow().isoformat() + "Z", "photos": out}
        with open(os.path.join(pdir, "PHOTOS.json"), "w", encoding="utf-8") as fp:
            json.dump(doc, fp, ensure_ascii=False, indent=2)
        print(f"  -> {os.path.relpath(pdir)}/PHOTOS.json")
    return 0 if not bad else 3


if __name__ == "__main__":
    sys.exit(main())
