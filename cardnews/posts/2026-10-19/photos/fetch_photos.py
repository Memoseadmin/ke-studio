#!/usr/bin/env python3
"""PHOTOS.v3.json의 file_url을 photos/src/<card>-<role>.<ext>로 내려받는다.
원본은 커밋하지 않는다(.gitignore: cardnews/posts/*/photos/src/). status가 missing/not_needed인 항목은 건너뛴다."""
import json, os, sys, time
from urllib.parse import urlparse
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "KEStudioPhotoResearch/1.0 (https://github.com/memoseadmin/ke-studio; card news photo sourcing) python-requests"}

def main():
    items = json.load(open(os.path.join(HERE, "PHOTOS.v3.json"), encoding="utf-8"))
    os.makedirs(os.path.join(HERE, "src"), exist_ok=True)
    failed = []
    for it in items:
        url = it.get("file_url")
        if not url:
            continue
        ext = os.path.splitext(urlparse(url).path)[1].lower() or ".jpg"
        dest = os.path.join(HERE, "src", f"{it['card']}-{it['role']}{ext}")
        if os.path.exists(dest):
            print("skip (exists)", dest); continue
        for wait in (0, 10, 30, 60):  # Wikimedia 429 대비 백오프
            time.sleep(wait)
            try:
                r = requests.get(url, headers=UA, timeout=120)
            except requests.RequestException as e:
                r = None; err = str(e)
            if r is not None and r.status_code == 200:
                open(dest, "wb").write(r.content)
                print("ok", dest, len(r.content)); break
            err = f"HTTP {r.status_code}" if r is not None else err
        else:
            print(f"FAIL card {it['card']} {it['role']} ({it.get('title')}): {err} {url}", file=sys.stderr)
            failed.append(it)
        time.sleep(3)
    # 2판: Wikimedia 429 대비 미러(LAYOUT.v3.json downloaded_from = 같은 원본의 Unsplash/Pexels CDN) + 프레임·띠 원화(image_url)
    lp = os.path.join(HERE, "LAYOUT.v3.json")
    if os.path.isfile(lp):
        lay = json.load(open(lp, encoding="utf-8"))
        jobs = []
        for c in lay.get("cards", []):
            if c.get("ref") and c.get("downloaded_from"):
                jobs.append((f"src/{c['ref']['card']}-{c['ref']['role']}.jpg", c["downloaded_from"]))
            for e in (c, c.get("frame") or {}):
                if e.get("file", "").startswith("src/") and e.get("image_url"):
                    jobs.append((e["file"], e["image_url"]))
        for rel, url in jobs:
            dest = os.path.join(HERE, rel)
            if os.path.exists(dest):
                continue
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 " + UA["User-Agent"]}, timeout=120)
            if r.status_code == 200:
                open(dest, "wb").write(r.content); print("ok (mirror)", dest)
                failed = [it for it in failed if f"src/{it['card']}-{it['role']}" not in rel]
            else:
                print(f"FAIL mirror {rel}: HTTP {r.status_code}", file=sys.stderr)
    if failed:
        sys.exit(1)

if __name__ == "__main__":
    main()
