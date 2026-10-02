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
    if failed:
        sys.exit(1)

if __name__ == "__main__":
    main()
