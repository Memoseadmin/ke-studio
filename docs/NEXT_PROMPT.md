docs/HANDOFF.md와 CLAUDE.md를 읽어라. 프로젝트 재탐색은 하지 말고, 큰 파일은 통째로 읽지 마라.
먼저 `git fetch origin claude/admiring-clarke-beyyoi ep/EP001 ep/EP002 && git checkout claude/admiring-clarke-beyyoi` (기본 브랜치에는 Phase 1~4가 없다. EP001 산출물은 ep/EP001, EP002 산출물은 ep/EP002).
너는 KE Studio의 COO다. 이번 세션은 Phase 5 — PR #1·#2 승인/반려 처리 + (키가 있으면) real 렌더·업로드 게이트 + EP003(구매 의도형) 기획이다. 시작 전 한 줄로 계획만 확인받고 진행하라.

먼저 PR #1 https://github.com/Memoseadmin/ke-studio/pull/1 과 PR #2 https://github.com/Memoseadmin/ke-studio/pull/2 의 라벨·코멘트를 GitHub MCP 도구로 확인하라(gh CLI 금지. 라벨은 `list_pull_requests fields=[labels]` + `search_pull_requests label:approved`로 교차 확인).
HANDOFF "대표 결정 대기" 중 내 답이 이 메시지나 PR 코멘트에 있으면 반영하고, 없으면 기본값(EN만·KR 보류, 제휴 상품 가안 유지, 썸네일 1안 유지, F11 미추가, publisher 게이트 현행 유지)으로 진행하라.
커밋 규칙: 스킬·docs는 작업 브랜치, EP 산출물은 ep/EPxxx. 서브에이전트가 끝나면 바로 커밋·푸시. 병렬 작업은 git worktree(.worktrees/)로 분리.

Phase 5 성공 기준 (시작 전에 표로 다시 적고, 끝에 자가 검증표로 보고)
1. PR #1·#2의 반려 코멘트가 있으면 적힌 번호 항목만 재작업해 해당 ep 브랜치에 푸시하고 PR 코멘트로 보고했다. 반려가 없으면 "변경 없음"을 기록했다.
2. 환경변수를 SET/UNSET으로만 확인했다. TTS·이미지 키가 SET이면 EP001(approved면 EP002도) producer real 렌더 → render-log.md → legal FIX 5 재판정. UNSET이면 건너뛰고 publish.log에 기록.
3. 게이트(approved 라벨·FIX 0·real 렌더) 3개를 모두 충족한 에피소드만 publisher가 비공개 업로드했고, 그 외 업로드는 0건이다.
4. ep/EP003(작업 브랜치에서 분기)에 researcher가 research.md를 만들었다: 구매 의도형 소재 10개, 1위 선정, 핵심 사실 20개 교차 확인, 건강·금융·법률 0, 제외 소재와 이유.
5. 세션 종료 절차(HANDOFF·NEXT_PROMPT 갱신, 전부 푸시, 새 세션 안내 블록)를 마쳤다.

첫 3개 작업
1. `bash scripts/setup.sh` 실행 → PR #1·#2 라벨·코멘트 확인 → 환경변수 SET/UNSET 확인 → 키가 있으면 EP001 real 렌더를 producer에게 백그라운드로 먼저 맡기고, 없으면 건너뜀.
2. 반려 코멘트가 있으면 해당 직원(writer/designer/marketer/legal-reviewer)에게 그 항목만 재작업 지시 → ep 브랜치 커밋·푸시 → PR 코멘트.
3. ep/EP003 분기 → general-purpose로 last30days(`opinion/balanced_recent`) 실행 → researcher가 research.md(구매 의도형) → 커밋·푸시. 끝나면 세션 종료 절차.
