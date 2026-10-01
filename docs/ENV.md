# 환경 설정 (값은 대표가 클라우드 환경 설정에 직접 입력, 저장소에는 이름만)

## setup script
클라우드 환경 설정의 **setup script**에 아래 한 줄을 등록:
```
bash scripts/setup.sh
```
설치 항목: ffmpeg, python3 패키지(google-api-python-client, google-auth-oauthlib, pillow). Phase 2에서 사용.

## 환경변수
| 이름 | 용도 | 담당 | 필요 시점 |
|---|---|---|---|
| `YOUTUBE_CLIENT_ID` | YouTube Data API OAuth 클라이언트 | publisher, analyst | Phase 2 |
| `YOUTUBE_CLIENT_SECRET` | 위 OAuth 시크릿 | publisher, analyst | Phase 2 |
| `YOUTUBE_REFRESH_TOKEN` | 채널 업로드 권한 리프레시 토큰 | publisher, analyst | Phase 2 |
| `TTS_API_KEY` | TTS(공급자 선정 후 이름 확정) | producer | Phase 2 |
| `IMAGE_API_KEY` | 이미지 생성(공급자 선정 후 이름 확정) | designer, producer | Phase 1~2 |
| `GITHUB_TOKEN` | 루틴에서 approved 라벨 확인·PR 생성(세션 기본 GitHub 연동으로 충분하면 불필요) | publisher | Phase 2~3 |
| `SCRAPECREATORS_API_KEY` | (보류) TikTok·Instagram·YouTube 트렌드 수집 스킬 | researcher | 대표 OK 후 |

## 규칙
- 키 값은 저장소·로그·PR·채팅에 절대 출력하지 않는다. `.env` 파일은 만들지도 읽지도 않는다.
- 공급자가 정해지면 변수 이름을 이 표에서 확정하고 커밋한다.
