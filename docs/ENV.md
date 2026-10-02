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
| `MUAPI_API_KEY` | 후보 · muapi.ai(이미지·영상 500+ 모델 중계, TTS 없음). CLI `~/.venvs/muapi/bin/muapi`가 읽음. muapi.ai → API Keys에서 발급 | designer, producer | 공급자 확정 시 |
| `IG_ACCESS_TOKEN` | 카드뉴스 프로젝트 · Meta Graph API 예약 게시(인스타 비즈니스 계정) | cardnews publisher | 카드뉴스 C1 승인 후 |
| `IG_USER_ID` | 카드뉴스 프로젝트 · 인스타그램 비즈니스 계정 ID(비밀 아님). **페이스북 페이지 ID 아님**(경로 A = `/me/accounts`의 instagram_business_account id, 경로 B = `graph.instagram.com/me?fields=user_id`) | cardnews publisher | 동일 |
| `IG_API_BASE` | 카드뉴스 · 선택. 게시 API 경로: `https://graph.facebook.com/v21.0`(경로 A, EAA 토큰) / `https://graph.instagram.com/v21.0`(경로 B, IGAA 토큰). 비우면 토큰 접두사로 자동 선택(scripts/README-ig.md) | cardnews publisher | 경로 B 전환 시 |
| `IMAGE_HOST_BASE_URL` | 카드뉴스 이미지 공개 호스팅 주소 = R2 버킷 공개 URL(r2.dev 또는 커스텀 도메인, 비밀 아님). 인스타가 `<주소>/card-01.png`를 직접 읽을 수 있어야 함 | cardnews publisher | 카드뉴스 C1 승인 후 · **현재 값(비밀 아님): `https://pub-e567e3bf81444a8d9dfe29577c7b3e56.r2.dev`** (버킷 chaekgado-cards, APAC, 2026-10-02 대표 전달) |
| `R2_ACCOUNT_ID` | 카드뉴스 · Cloudflare 계정 ID(R2 엔드포인트용, 비밀 아님) | cardnews publisher | 카드뉴스 C1 승인 후 |
| `R2_ACCESS_KEY_ID` | 카드뉴스 · R2 API 토큰 액세스 키 ID(**비밀**, **32자**. 20자면 잘못 붙여넣은 값) | cardnews publisher | 동일 |
| `R2_SECRET_ACCESS_KEY` | 카드뉴스 · R2 API 토큰 시크릿(**비밀**, **64자**) | cardnews publisher | 동일 |
| `R2_BUCKET` | 카드뉴스 · R2 버킷 이름(비밀 아님) | cardnews publisher | 동일 |
| `GITHUB_TOKEN` | 루틴에서 approved 라벨 확인·PR 생성(세션 기본 GitHub 연동으로 충분하면 불필요) | publisher | Phase 2~3 |
| `SCRAPECREATORS_API_KEY` | (보류) TikTok·Instagram·YouTube 트렌드 수집 스킬 | researcher | 대표 OK 후 |
| `OPENAI_API_KEY` | 선택 · last30days (보조 검색·요약) | researcher | 필요 시 |
| `XAI_API_KEY` | 선택 · last30days (X 검색, 쿠키 대신) | researcher | 필요 시 |
| `X_BEARER_TOKEN` | 선택 · last30days (X API v2 app-only) | researcher | 필요 시 |
| `OPENROUTER_API_KEY` | 선택 · last30days | researcher | 필요 시 |
| `PERPLEXITY_API_KEY` | 선택 · last30days (웹 검색) | researcher | 필요 시 |
| `PARALLEL_API_KEY` | 선택 · last30days (웹 검색) | researcher | 필요 시 |
| `BRAVE_API_KEY` | 선택 · last30days (웹 검색) | researcher | 필요 시 |
| `APIFY_API_TOKEN` | 선택 · last30days | researcher | 필요 시 |
| `AUTH_TOKEN` | 선택 · last30days (X 브라우저 쿠키, 비권장) | researcher | 필요 시 |
| `CT0` | 선택 · last30days (X 브라우저 쿠키, 비권장) | researcher | 필요 시 |
| `BSKY_HANDLE` | 선택 · last30days (Bluesky) | researcher | 필요 시 |
| `BSKY_APP_PASSWORD` | 선택 · last30days (Bluesky 앱 비밀번호) | researcher | 필요 시 |
| `TRUTHSOCIAL_TOKEN` | 선택 · last30days (Truth Social) | researcher | 필요 시 |
| `XIAOHONGSHU_API_BASE` | 선택 · last30days (샤오훙수 API 주소, 비밀 아님) | researcher | 필요 시 |

last30days는 키 없이도 Reddit·HN·Polymarket·GitHub·웹을 수집한다. 위 "선택" 키와 `SCRAPECREATORS_API_KEY`(TikTok·Instagram 추가)는 모두 선택이며, 목록은 스킬 SKILL.md의 `optionalEnv`를 그대로 옮긴 것이다.

## 규칙
- 키 값은 저장소·로그·PR·채팅에 절대 출력하지 않는다. `.env` 파일은 만들지도 읽지도 않는다.
- 공급자가 정해지면 변수 이름을 이 표에서 확정하고 커밋한다.
