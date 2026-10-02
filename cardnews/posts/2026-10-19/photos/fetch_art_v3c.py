#!/usr/bin/env python3
"""3판(C안) 원화 원본 받기 -> photos/src/ (커밋 제외). 라이선스는 실행 때 공식 API로 다시 확인한다."""
import json, os, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
FILES = {
    "cma-2011.37-full.tif": "https://openaccess-cdn.clevelandart.org/2011.37/2011.37_full.tif",
    "met-73134-DP163173.jpg": "https://images.metmuseum.org/CRDImages/as/original/DP163173.jpg",
    "met-73134-DP163174.jpg": "https://images.metmuseum.org/CRDImages/as/original/DP163174.jpg",
}
CHECK = {"met 73134": ("https://collectionapi.metmuseum.org/public/collection/v1/objects/73134", lambda d: d["isPublicDomain"] is True),
         "cma 2011.37": ("https://openaccess-api.clevelandart.org/api/artworks/2011.37", lambda d: d["data"]["share_license_status"] == "CC0")}
os.makedirs(SRC, exist_ok=True)
for k, (u, ok) in CHECK.items():
    d = json.load(urllib.request.urlopen(u, timeout=60))
    if not ok(d):
        raise SystemExit(f"{k}: 라이선스 확인 실패 -> 받지 않음")
    print(k, "CC0 확인")
for f, u in FILES.items():
    p = os.path.join(SRC, f)
    if not os.path.exists(p):
        print("받는 중", f)
        urllib.request.urlretrieve(u, p)
print("완료", sorted(os.listdir(SRC)))
