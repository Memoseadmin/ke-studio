# Instagram 게시 도구

- `ig_publish.py <post_dir> [--pr N] [--schedule ISO] [--dry-run|--execute]` — 기본 dry-run. `--execute`는 게이트 4개(approved 라벨 / 목업 아님 / 출처 줄 / 해시태그 ≤5 — AI 표시 문구는 2026-10-02 대표 결정으로 선택) 통과 시에만 호출.
- 흐름: 자식 컨테이너 N개(`is_carousel_item`) → 캐러셀 컨테이너(caption) → `media_publish`.
- 이미지는 `IMAGE_HOST_BASE_URL/<파일명>` 공개 URL이어야 한다(인스타가 직접 받아감). 비공개 저장소 raw URL 불가.
- **예약**: Content Publishing API는 예약을 직접 지원하지 않는다. `--schedule`은 `cardnews/queue.json`에 `{post_dir, pr, at, status}`를 기록만 하고, Claude Code 루틴(/schedule)이 시각 도래 시 `--execute`를 실행하는 설계.
- `ig_token_refresh.py` — 장기 토큰 갱신(기본은 안내만, `--run`시 새 토큰을 화면에 찍지 않고 0600 파일로 저장). 경로 B는 `ig_refresh_token`(앱 시크릿 불필요).
- **API 경로(2026-10-02 추가)**: `IG_API_BASE`로 고른다. 비어 있으면 토큰 접두사로 자동 선택.
  - 경로 A 페이스북 로그인: `https://graph.facebook.com/v21.0`, 토큰 `EAA…`, `IG_USER_ID` = `/me/accounts?fields=instagram_business_account`의 IG 계정 ID(페이지 ID 아님).
  - 경로 B Instagram 로그인: `https://graph.instagram.com/v21.0`, 토큰 `IGAA…`(앱 대시보드 → Instagram 제품 → "Instagram 로그인으로 API 설정" → 계정 추가 → 토큰 생성), `IG_USER_ID` = `me?fields=user_id`. 페이스북 페이지 연결이 필요 없다.
  - 확인: `python3 scripts/ig_publish.py --check` → 경로·username·IG_USER_ID 일치 여부(값 출력 없음).
- 키 값은 출력·로그·커밋 금지.

## 이미지 호스팅: Cloudflare R2 (대표용 설정 5줄)
1. Cloudflare → R2에서 버킷 생성(`R2_BUCKET`), 계정 ID 확인(`R2_ACCOUNT_ID`).
2. 버킷 설정 → 공개 액세스: r2.dev 서브도메인 허용 또는 커스텀 도메인 연결 → 그 주소가 `IMAGE_HOST_BASE_URL`.
3. R2 → API 토큰 관리 → 해당 버킷 "객체 읽기·쓰기" 토큰 발급 → `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`.
4. 위 5개를 클라우드 환경 설정에 입력(저장소·채팅에 값 금지).
5. `scripts/r2_upload.py <post_dir> --execute` → `urls.json` 생성 → `ig_publish.py`가 이를 우선 사용.
