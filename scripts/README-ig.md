# Instagram 게시 도구

- `ig_publish.py <post_dir> [--pr N] [--schedule ISO] [--dry-run|--execute]` — 기본 dry-run. `--execute`는 게이트 4개(approved 라벨 / 목업 아님 / AI 표시 문구 / 해시태그 ≤5) 통과 시에만 호출.
- 흐름: 자식 컨테이너 N개(`is_carousel_item`) → 캐러셀 컨테이너(caption) → `media_publish`.
- 이미지는 `IMAGE_HOST_BASE_URL/<파일명>` 공개 URL이어야 한다(인스타가 직접 받아감). 비공개 저장소 raw URL 불가.
- **예약**: Content Publishing API는 예약을 직접 지원하지 않는다. `--schedule`은 `cardnews/queue.json`에 `{post_dir, pr, at, status}`를 기록만 하고, Claude Code 루틴(/schedule)이 시각 도래 시 `--execute`를 실행하는 설계.
- `ig_token_refresh.py` — 장기 토큰 갱신(기본은 안내만, `--run`시 새 토큰을 화면에 찍지 않고 0600 파일로 저장).
- 키 값은 출력·로그·커밋 금지.

## 이미지 호스팅: Cloudflare R2 (대표용 설정 5줄)
1. Cloudflare → R2에서 버킷 생성(`R2_BUCKET`), 계정 ID 확인(`R2_ACCOUNT_ID`).
2. 버킷 설정 → 공개 액세스: r2.dev 서브도메인 허용 또는 커스텀 도메인 연결 → 그 주소가 `IMAGE_HOST_BASE_URL`.
3. R2 → API 토큰 관리 → 해당 버킷 "객체 읽기·쓰기" 토큰 발급 → `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`.
4. 위 5개를 클라우드 환경 설정에 입력(저장소·채팅에 값 금지).
5. `scripts/r2_upload.py <post_dir> --execute` → `urls.json` 생성 → `ig_publish.py`가 이를 우선 사용.
