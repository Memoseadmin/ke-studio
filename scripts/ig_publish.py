#!/usr/bin/env python3
"""Instagram 카드뉴스 캐러셀 게시 (Content Publishing API). 기본은 dry-run.

사용:
  python3 scripts/ig_publish.py cardnews/posts/2026-10-09 --pr 12            # dry-run
  python3 scripts/ig_publish.py <post_dir> --pr 12 --schedule "2026-10-09T09:00+09:00"
  python3 scripts/ig_publish.py <post_dir> --pr 12 --execute                 # 실제 호출

환경변수(값은 출력하지 않는다): IG_ACCESS_TOKEN, IG_USER_ID, IMAGE_HOST_BASE_URL, GITHUB_TOKEN
"""
import argparse, glob, json, os, re, sys, time
from pathlib import Path

GRAPH = "https://graph.facebook.com/v21.0"
REPO = os.environ.get("GITHUB_REPOSITORY", "memoseadmin/ke-studio")
AI_MARK = re.compile(r"AI")  # 캡션 AI 표시 문구("AI로 생성" 등)
QUEUE = Path("cardnews/queue.json")


def gate_label(pr):
    """(1) PR에 approved 라벨이 있는가."""
    tok = os.environ.get("GITHUB_TOKEN")
    if not pr:
        return False, "--pr 없음"
    if not tok:
        return False, "GITHUB_TOKEN UNSET"
    try:
        import requests
        r = requests.get(f"https://api.github.com/repos/{REPO}/issues/{pr}/labels",
                         headers={"Authorization": f"Bearer {tok}",
                                  "Accept": "application/vnd.github+json"}, timeout=20)
        if r.status_code != 200:
            return False, f"GitHub HTTP {r.status_code}"
        names = [l["name"] for l in r.json()]
        return ("approved" in names), f"labels={names}"
    except Exception as e:  # 실패 시 중단
        return False, f"GitHub 조회 실패: {type(e).__name__}"


def gate_mockup(d):
    """(2) RENDER.json mode가 mockup이 아니어야 한다. 파일/필드 없으면 불명 → 실패."""
    f = d / "RENDER.json"
    if not f.exists():
        return False, "RENDER.json 없음(모드 확인 불가)"
    mode = json.loads(f.read_text(encoding="utf-8")).get("mode")
    return (mode is not None and mode != "mockup"), f"mode={mode}"


def read_caption(d):
    f = d / "caption.txt"
    return f.read_text(encoding="utf-8").rstrip("\n") if f.exists() else None


def gate_ai(cap):
    """(3) 캡션 마지막 줄(해시태그 줄은 제외한 마지막 줄)에 AI 표시 문구."""
    if cap is None:
        return False, "caption.txt 없음"
    lines = [l for l in cap.splitlines() if l.strip()]
    body = [l for l in lines if not l.strip().startswith("#")]
    if not body:
        return False, "본문 없음"
    ok = bool(AI_MARK.search(body[-1]))
    note = "마지막 줄" if lines and lines[-1] is body[-1] else "마지막 비해시태그 줄(해시태그가 맨 끝)"
    return ok, f"{note}: {body[-1][:40]}"


def gate_tags(cap):
    """(4) 해시태그 ≤5."""
    n = len(re.findall(r"(?<!\S)#\S+", cap or ""))
    return n <= 5, f"hashtags={n}"


def image_urls(d, cards):
    """urls.json(r2_upload.py 산출)이 있으면 그 URL, 없으면 IMAGE_HOST_BASE_URL + 파일명."""
    f = d / "urls.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    base = os.environ.get("IMAGE_HOST_BASE_URL", "<IMAGE_HOST_BASE_URL>").rstrip("/")
    return [f"{base}/{os.path.basename(c)}" for c in cards]


def build_plan(d, cap):
    cards = sorted(glob.glob(str(d / "card-[0-9][0-9].png")))
    uid = "{IG_USER_ID}"
    urls = image_urls(d, cards)
    reqs = []
    for i, u in enumerate(urls, 1):
        reqs.append({"step": f"child {i}", "method": "POST", "url": f"{GRAPH}/{uid}/media",
                     "fields": {"image_url": u, "is_carousel_item": "true"}})
    reqs.append({"step": "carousel", "method": "POST", "url": f"{GRAPH}/{uid}/media",
                 "fields": {"media_type": "CAROUSEL", "children": "<child ids>", "caption": cap}})
    reqs.append({"step": "publish", "method": "POST", "url": f"{GRAPH}/{uid}/media_publish",
                 "fields": {"creation_id": "<carousel id>"}})
    return cards, reqs


def post(path, data):
    import requests
    data = dict(data, access_token=os.environ["IG_ACCESS_TOKEN"])
    r = requests.post(f"{GRAPH}/{os.environ['IG_USER_ID']}/{path}", data=data, timeout=60)
    j = r.json()
    if r.status_code != 200 or "id" not in j:
        sys.exit(f"API 오류 {path}: {json.dumps(j.get('error', j), ensure_ascii=False)}")
    return j["id"]


def execute(d, cards, cap):
    import requests
    kids = [post("media", {"image_url": u, "is_carousel_item": "true"}) for u in image_urls(d, cards)]
    cid = post("media", {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": cap})
    for _ in range(10):  # 컨테이너 처리 대기
        s = requests.get(f"{GRAPH}/{cid}", params={"fields": "status_code",
                         "access_token": os.environ["IG_ACCESS_TOKEN"]}, timeout=30).json()
        if s.get("status_code") == "FINISHED":
            break
        time.sleep(3)
    return post("media_publish", {"creation_id": cid})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("post_dir")
    ap.add_argument("--schedule", help='"YYYY-MM-DDTHH:MM+09:00" → queue.json 기록(API 예약 미지원)')
    ap.add_argument("--dry-run", action="store_true", help="기본값")
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--pr", type=int)
    a = ap.parse_args()
    d = Path(a.post_dir)
    cap = read_caption(d)
    cards, reqs = build_plan(d, cap or "")
    gates = [("approved 라벨", gate_label(a.pr) if a.execute or a.pr else (False, "--pr 없음")),
             ("목업 아님", gate_mockup(d)), ("AI 표시 문구", gate_ai(cap)), ("해시태그 ≤5", gate_tags(cap))]
    print(f"[{'EXECUTE' if a.execute else 'DRY-RUN'}] {d}  cards={len(cards)}")
    print("게이트:")
    for n, (ok, m) in gates:
        print(f"  {'PASS' if ok else 'FAIL'}  {n}  ({m})")
    allok = all(ok for _, (ok, _) in gates) and len(cards) >= 2
    if not a.execute:
        print("요청 목록(토큰 제외):")
        for r in reqs:
            print(f"  {r['method']} {r['url']}\n    {json.dumps(r['fields'], ensure_ascii=False)[:200]}")
        if a.schedule:
            print(f"  (schedule) cardnews/queue.json 에 기록될 항목: {a.schedule} — dry-run이라 기록 안 함")
        print("전체 게이트:", "PASS" if allok else "FAIL")
        return
    if not allok:
        sys.exit("게이트 실패 — 중단")
    for v in ("IG_ACCESS_TOKEN", "IG_USER_ID"):
        if not os.environ.get(v):
            sys.exit(f"{v} UNSET — 중단")
    if a.schedule:
        q = json.loads(QUEUE.read_text()) if QUEUE.exists() else []
        q.append({"post_dir": str(d), "pr": a.pr, "at": a.schedule, "status": "queued"})
        QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n")
        print(f"queued: {a.schedule} (루틴이 시각에 --execute 실행)")
        return
    print("published media id:", execute(d, cards, cap))


if __name__ == "__main__":
    main()
