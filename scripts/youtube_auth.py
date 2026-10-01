#!/usr/bin/env python3
"""YouTube 업로드용 REFRESH_TOKEN 1회 발급 스크립트 (대표 PC에서 실행).

준비: Google Cloud Console → 프로젝트 → "YouTube Data API v3" 사용 설정 → OAuth 동의 화면(외부, 테스트 사용자에 채널 계정 추가)
      → 사용자 인증 정보 → OAuth 클라이언트 ID(유형: 데스크톱 앱) → JSON 다운로드.
실행:  pip install google-auth-oauthlib
       python3 scripts/youtube_auth.py /path/to/client_secret.json
결과:  브라우저가 열리고 채널 계정으로 로그인·허용하면, 터미널에 환경변수 3개 값이 출력된다.
       그 값을 클라우드 환경 설정(세션 제목줄 환경 메뉴 → Edit)의 환경변수에 넣는다. 채팅·저장소에는 절대 붙이지 않는다.
"""
import json
import sys

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    sys.exit("먼저 실행: pip install google-auth-oauthlib")

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]

def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("사용법: python3 scripts/youtube_auth.py client_secret.json")
    secret_path = sys.argv[1]
    with open(secret_path, encoding="utf-8") as f:
        client = json.load(f)
    key = "installed" if "installed" in client else "web"
    flow = InstalledAppFlow.from_client_secrets_file(secret_path, SCOPES)
    # access_type=offline + prompt=consent 가 있어야 refresh_token 이 반드시 내려온다.
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
    if not creds.refresh_token:
        sys.exit("refresh_token 이 없습니다. Google 계정 → 보안 → 서드파티 액세스에서 이 앱을 제거한 뒤 다시 실행하세요.")
    print("\n아래 3줄을 클라우드 환경 설정의 환경변수에 넣으세요 (이 터미널 밖으로 복사하지 마세요):")
    print(f"YOUTUBE_CLIENT_ID={client[key]['client_id']}")
    print(f"YOUTUBE_CLIENT_SECRET={client[key]['client_secret']}")
    print(f"YOUTUBE_REFRESH_TOKEN={creds.refresh_token}")

if __name__ == "__main__":
    main()
