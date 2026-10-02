# Instagram 게시 도구

- `ig_publish.py <post_dir> [--pr N] [--schedule ISO] [--dry-run|--execute]` — 기본 dry-run. `--execute`는 게이트 4개(approved 라벨 / 목업 아님 / AI 표시 문구 / 해시태그 ≤5) 통과 시에만 호출.
- 흐름: 자식 컨테이너 N개(`is_carousel_item`) → 캐러셀 컨테이너(caption) → `media_publish`.
- 이미지는 `IMAGE_HOST_BASE_URL/<파일명>` 공개 URL이어야 한다(인스타가 직접 받아감). 비공개 저장소 raw URL 불가.
- **예약**: Content Publishing API는 예약을 직접 지원하지 않는다. `--schedule`은 `cardnews/queue.json`에 `{post_dir, pr, at, status}`를 기록만 하고, Claude Code 루틴(/schedule)이 시각 도래 시 `--execute`를 실행하는 설계.
- `ig_token_refresh.py` — 장기 토큰 갱신(기본은 안내만, `--run`시 새 토큰을 화면에 찍지 않고 0600 파일로 저장).
- 키 값은 출력·로그·커밋 금지.
