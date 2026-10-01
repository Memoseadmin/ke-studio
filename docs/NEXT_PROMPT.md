docs/HANDOFF.md와 CLAUDE.md를 읽어라. 프로젝트 재탐색은 하지 말고, 큰 파일은 통째로 읽지 마라.
먼저 `git fetch origin claude/admiring-clarke-beyyoi && git checkout claude/admiring-clarke-beyyoi` (기본 브랜치에는 Phase 1-0이 없다).
너는 KE Studio의 COO다. 이번 세션은 Phase 1 — EP001 반자동 검수 PR이다. 시작 전 한 줄로 계획만 확인받고 진행하라.

HANDOFF "대표 결정 대기" 중 내 답이 이 메시지에 있으면 반영하고, 없으면 기본값(인스타 캐러셀은 marketing.md에 캐러셀 1안만 추가, 보류 스킬은 그대로 보류)으로 진행하라.

Phase 1 성공 기준 (시작 전에 표로 다시 적고, 끝에 자가 검증표로 보고)
1. 브랜치 ep/EP001에 research.md(소재 10개·출처), script.en.md·script.kr.md(8~12분), design/(디자인 시스템·썸네일 3·장면 프롬프트), marketing.md, risk.md가 있다.
2. PR 하나가 열리고 본문이 검수 시트 ①~⑧ 순서를 따른다. 폰에서 스크롤 한 번에 판단 가능.
3. 설명란 첫 줄에 제휴 고지 문구가 있고, risk.md에 BLOCK이 0개다(있으면 수정 후 재점검).
4. 모든 사실 주장에 출처가 있거나 "미검증" 표시가 있다.

첫 3개 작업
1. `bash scripts/setup.sh` 실행(last30days용 Python 3.12) → researcher 에이전트로 EP001 소재 10개 생성(구매 의도형 우선, K-드라마 속 음식·장소·제품) → 1개 선정 이유를 한 줄로.
2. writer → designer → marketer 순으로 서브에이전트 실행(산출물만 받고 메인은 요약만).
3. legal-reviewer 점검 후 ep/EP001 브랜치 푸시, 검수 시트 PR 생성. 끝나면 세션 종료 절차.
