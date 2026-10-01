cardnews/docs/HANDOFF.md, cardnews/docs/PLAN.md, CLAUDE.md를 읽어라. 프로젝트 재탐색은 하지 말고, 큰 파일은 통째로 읽지 마라.
먼저 `git fetch origin cardnews/main && git checkout cardnews/main`. 이 세션은 **카드뉴스 프로젝트 전용**이다. `episodes/`와 루트 `docs/`는 읽기만 하고 수정하지 않는다. 산출물·문서는 `cardnews/` 아래에만 쓰고 `cardnews/main`(검수 PR은 `cardnews/c1-1` 분기)에 커밋·푸시한다.
너는 카드뉴스 프로젝트의 COO다. 이번 세션은 Phase C1-1 — 14일 테스트 세트 제작 + 검수 PR이다. 시작 전 한 줄로 계획만 확인받고 진행하라.
HANDOFF "대표 결정 대기"에 내 답이 이 메시지에 있으면 반영하고, 없으면 기본값(EN 계정, 수동 게시, 금지 품목 기본)으로 진행하라.

Phase C1-1 성공 기준 (시작 전에 표로 다시 적고, 끝에 자가 검증표로 보고)
1. `cardnews/posts/`에 14세트(각 7장 1080x1350 PNG 목업 + caption.txt + sources.txt)가 있고, 소재 14개 중 EP 재활용 ≤4, 트렌드 ≥10이며 건강·금융·법률·정치·실존 인물 비판 0건.
2. 모든 수치·사실에 출처가 7장 또는 sources.txt에 있고, 카드에 실존 인물 얼굴·로고·드라마 스틸 0, 캡션 끝에 AI 생성물 표시 1줄, 해시태그 10~15개.
3. `cardnews/docs/risk-C1-1.md` BLOCK 0(FIX 허용). `cardnews/docs/MEDIA_KIT.md` 초안(실측 칸 비움, 단가 추정치 표시).
4. 검수 PR(`cardnews/c1-1` → `cardnews/main`) 생성: 본문 = ① 목표·지표 ② 14세트 1장 썸네일 표 ③ 캡션 링크 ④ 게시 일정 ⑤ 리스크 결과. 게시는 0건(approved 전 금지).
5. 세션 종료 절차(cardnews/docs/HANDOFF.md·NEXT_PROMPT.md 갱신, 커밋·푸시, 새 세션 안내 블록).

첫 3개 작업
1. `bash scripts/setup.sh` → 환경변수 `IG_ACCESS_TOKEN`·`IG_USER_ID`·`IMAGE_API_KEY` SET/UNSET 확인(값 출력 금지) → general-purpose로 last30days(`opinion/balanced_recent`, 주제 "Korea culture trend this week", 키 없이) 실행 → `cardnews/research/C1-1-trends.md`.
2. marketer에게 14일 플랜·캡션 → 커밋·푸시 → designer에게 템플릿 + 14세트 목업(Pillow, EP 썸네일 목업 스크립트 방식 참고) → 커밋·푸시.
3. legal-reviewer 점검 → risk 푸시 → GitHub MCP로 검수 PR 생성(gh CLI 금지) → 세션 종료 절차.
