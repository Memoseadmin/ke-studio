#!/usr/bin/env python3
"""장기 토큰 갱신 헬퍼 (자동 실행 금지 — 대표 승인 후 수동 실행).

절차(Facebook 로그인 기반 장기 사용자 토큰, 유효 60일):
  GET https://graph.facebook.com/v21.0/oauth/access_token
      ?grant_type=fb_exchange_token&client_id=<APP_ID>&client_secret=<APP_SECRET>
      &fb_exchange_token=<현재 장기 토큰>
필요 환경변수: META_APP_ID, META_APP_SECRET, IG_ACCESS_TOKEN (값은 출력하지 않는다)
경로 B(Instagram 로그인, IGAA 토큰 또는 IG_API_BASE=graph.instagram.com)는 앱 시크릿 없이
  GET https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=<현재 토큰>
  (발급 후 24시간이 지나고 만료 전인 장기 토큰만 갱신된다, 유효 60일)
새 토큰은 화면에 찍지 않는다. 클라우드 환경 설정의 IG_ACCESS_TOKEN을 대표가 직접 교체한다.
"""
import os, sys


def route_b():
    return ("graph.instagram.com" in os.environ.get("IG_API_BASE", "")
            or os.environ.get("IG_ACCESS_TOKEN", "").startswith("IGAA"))


def main():
    need = ("IG_ACCESS_TOKEN",) if route_b() else ("META_APP_ID", "META_APP_SECRET", "IG_ACCESS_TOKEN")
    if "--run" not in sys.argv:
        print(f"dry: 경로 {'B' if route_b() else 'A'}. 실행하려면 --run (이 세션에서는 실행하지 않음). 필요 변수:",
              {v: ("SET" if os.environ.get(v) else "UNSET") for v in need})
        return
    import requests
    if route_b():
        r = requests.get("https://graph.instagram.com/refresh_access_token", params={
            "grant_type": "ig_refresh_token", "access_token": os.environ["IG_ACCESS_TOKEN"]}, timeout=30)
    else:
        r = requests.get("https://graph.facebook.com/v21.0/oauth/access_token", params={
            "grant_type": "fb_exchange_token", "client_id": os.environ["META_APP_ID"],
            "client_secret": os.environ["META_APP_SECRET"],
            "fb_exchange_token": os.environ["IG_ACCESS_TOKEN"]}, timeout=30)
    j = r.json()
    if "access_token" not in j:
        sys.exit(f"갱신 실패: {j.get('error', {}).get('message', r.status_code)}")
    # 새 토큰은 출력하지 않는다. 프라이빗 파일로만 저장하고 안내.
    p = os.path.expanduser("~/.ig_token_new")
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(j["access_token"])
    print(f"갱신 완료(유효 {j.get('expires_in', '?')}초). 새 토큰은 {p}에 저장됨 — 내용을 환경 설정의 IG_ACCESS_TOKEN에 넣고 파일을 삭제하세요.")

if __name__ == "__main__":
    main()
