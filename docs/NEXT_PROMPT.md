docs/HANDOFF.md와 CLAUDE.md를 읽어라. 프로젝트 재탐색은 하지 말고, 큰 파일은 통째로 읽지 마라.
먼저 `git fetch origin claude/admiring-clarke-beyyoi ep/EP001 ep/EP002 && git checkout claude/admiring-clarke-beyyoi` (기본 브랜치에는 Phase 1~3이 없다. EP001 산출물은 ep/EP001, EP002 산출물은 ep/EP002).
너는 KE Studio의 COO다. 이번 세션은 Phase 4 — EP002 대본·디자인·마케팅·리스크 점검 후 검수 PR 생성 + (키가 있으면) EP001 real 렌더·업로드 게이트다. 시작 전 한 줄로 계획만 확인받고 진행하라.

먼저 PR https://github.com/Memoseadmin/ke-studio/pull/1 의 라벨·코멘트를 GitHub MCP 도구로 확인하라(gh CLI 금지. 라벨은 `list_pull_requests fields=[labels]` 또는 `search_pull_requests label:approved`로).
HANDOFF "대표 결정 대기" 중 내 답이 이 메시지나 PR 코멘트에 있으면 반영하고, 없으면 기본값(EP002는 research.md 1위 "한글" 후보, 제휴 상품은 꼬리에 한글 워크북·붓펜 세트 가안, KR판 보류·EN만, publisher 게이트 현행 유지)으로 진행하라.
커밋 규칙: 스킬·docs는 작업 브랜치, EP 산출물은 ep/EPxxx. 서브에이전트가 끝나면 바로 커밋·푸시. 병렬 작업은 git worktree로 분리.

Phase 4 성공 기준 (시작 전에 표로 다시 적고, 끝에 자가 검증표로 보고)
1. ep/EP002에 writer가 script.en.md(8~12분, 1,200~1,700단어, 문화·역사 설명형, 출처 있는 사실만, research.md "대본 금지 수치" 미사용)와 script.kr.md를 만들고, 제휴 상품 1~2개가 서사 꼬리에만 놓였다. AI 공개 라벨·제휴 고지 낭독이 EN에 들어 있다.
2. designer가 썸네일 후보 3개(실존 인물·로고·스틸 없음)와 장면 프롬프트를, marketer가 제목 5안·설명란(첫 줄 고지)·태그·숏폼 컷 플랜 5개(각 60초 이내 추정)·캡션을 만들었다.
3. legal-reviewer가 risk.md를 만들었고 BLOCK 0이다(FIX는 허용). 사실 주장 감사에서 출처 없음 0건.
4. ep/EP002 검수 PR(①~⑧ 검수 시트, 폰에서 스크롤 한 번)을 생성했고, 업로드는 0건이다(approved 없이는 절대 금지).
5. 환경변수를 SET/UNSET으로만 확인했다. TTS·이미지 키가 SET이면 EP001 producer real 렌더 → render-log.md 기록 → legal FIX 5 재판정 → 게이트(approved·FIX 0·real 렌더) 충족 시에만 publisher 비공개 업로드. UNSET이면 건너뛰고 publish.log에 기록.

첫 3개 작업
1. `bash scripts/setup.sh` 실행 → PR #1 라벨·코멘트 확인 → 환경변수 SET/UNSET 확인 → 키가 있으면 EP001 real 렌더를 producer에게 먼저 맡기고(백그라운드), 없으면 건너뜀.
2. ep/EP002 체크아웃 → writer 실행(입력: episodes/EP002/research.md §2-1 서사 초안·§3 핵심 사실) → 커밋·푸시 → designer와 marketer 병렬 실행 → 커밋·푸시.
3. legal-reviewer 점검 → risk.md 푸시 → GitHub MCP로 ep/EP002 검수 PR 생성(base: claude/admiring-clarke-beyyoi, 본문 = 검수 시트 ①~⑧, 썸네일 3개 나란히). 끝나면 세션 종료 절차.
