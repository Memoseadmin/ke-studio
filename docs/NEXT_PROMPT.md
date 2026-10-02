docs/PROJECTS.md(통합 현황판), docs/HANDOFF.md, cardnews/docs/HANDOFF.md, CLAUDE.md를 읽어라. 프로젝트 재탐색은 하지 말고, 큰 파일은 통째로 읽지 마라.
먼저 `git fetch origin claude/admiring-clarke-beyyoi ep/EP001 ep/EP002 cardnews/main && git checkout claude/admiring-clarke-beyyoi`. 그다음 worktree를 만든다: `git worktree add .worktrees/cardnews cardnews/main`, 필요 시 `.worktrees/ep001`·`ep002`(`.git/info/exclude`에 `.worktrees/` 등록).
너는 KE Studio의 COO이며 **두 프로젝트(A 유튜브 EN, B 카드뉴스 **KR·한국 브랜드 제휴 광고 중심**)를 이 세션 하나에서 통합 관리**한다. 세션을 나누지 않는다. A 산출물은 `ep/EPxxx`, A 문서는 작업 브랜치, B 산출물·문서는 `cardnews/main`(검수 PR은 `cardnews/c1-x`)에만 커밋한다. 시작 전 한 줄로 계획만 확인받고 진행하라.

먼저 docs/PROJECTS.md "세션 위생 규칙"대로 하위 세션 표를 전부 확인·회수·아카이브하라(get_session → fetch → 표 갱신 → archive_session). 그다음 GitHub MCP로 PR #1·#2·#3(및 열려 있는 cardnews PR)의 라벨·코멘트를 확인하라(gh CLI 금지). #3(ECC)이 approved면 작업 브랜치에 머지. docs/PROJECTS.md "대표 결정 큐"에 내 답이 이 메시지나 PR 코멘트에 있으면 반영하고, 없으면 기본값으로 진행하라.
환경변수는 SET/UNSET으로만 확인한다(값 출력 금지).

환경변수 주의: 직전 검증에서 `R2_ACCESS_KEY_ID`(20자, 32자여야 함)와 `IG_USER_ID`(페이스북 페이지 ID가 들어감)가 틀렸고 `/me/accounts`가 비어 있었다. 대표가 고쳤는지 먼저 Sonnet 세션으로 재검증하고, 페이스북 경유가 계속 안 되면 Instagram 직접 로그인 API(graph.instagram.com, 토큰 IGAA…, `me?fields=user_id,username`)로 전환해 scripts/ig_publish.py에 `IG_API_BASE` 분기를 추가하라. 하위 세션이 git push를 막히면 보고만 list_events로 회수하고 대신 푸시하지 않는다.

이번 세션 성공 기준 (시작 전에 표로 다시 적고, 끝에 자가 검증표로 보고)
[A1] PR #1·#2 반려 코멘트가 있으면 해당 번호만 재작업·푸시·코멘트. 없으면 "변경 없음" 기록.
[A2] TTS·이미지 키가 SET이면 EP002 S01로 음성·이미지 샘플 1개씩 → render/sample/ → 보고 → EP001·EP002 real 렌더 → legal FIX 5 재판정 → 게이트(approved·FIX 0·real 렌더) 충족 시에만 publisher 비공개 업로드. UNSET이면 건너뛰고 publish.log 기록.
[A3] ep/EP003에 researcher가 research.md(구독형 혼합 기준: 시리즈 후보 + 고수수료 제휴 후보, 소재 10개, 사실 20개, 민감 주제 0).
[B1] PR #4(approved)의 14세트를 `--final`로 재렌더 → legal PNG 재점검(risk v3 BLOCK 0) → cardnews/c1-1을 cardnews/main에 머지. 키 검증이 통과하면 R2 업로드(`r2_upload.py --execute`)와 게시 큐(`ig_publish.py --schedule`, approved·final 게이트) 등록 + 매일 KST 게시 루틴. 통과 못 하면 수동 게시 패키지(날짜 폴더 PNG+caption)로 10/9 첫 게시 준비.
[B2] 릴스 C1-1b: `cardnews/posts/C1-1b-reels-plan.md`·`reel.json`×14가 없으면 marketer에게 재작성(무음·자막·15~30초·캐러셀 6시간 뒤) → producer가 ffmpeg로 14개 렌더(목업) → C1-1b 검수 PR. 프로필 패키지(프로필 사진 후보·소개 150자·하이라이트 커버·링크 허브 구성·고정 댓글)도 같은 PR에.
[공통] docs/PROJECTS.md 상태표·결정 큐 갱신, 두 HANDOFF 갱신, 전부 푸시, 새 세션 안내 블록 1개(프로젝트 두 개 모두 포함).

첫 3개 작업
1. `bash scripts/setup.sh` → PR 라벨·코멘트 확인 → 환경변수 확인 → 키가 있으면 A2 샘플 생성을 producer에게 백그라운드로 먼저.
2. B1을 worktree `.worktrees/cardnews`에서 시작: marketer 14일 플랜 → 커밋·푸시 → designer 템플릿+14세트 목업 → 커밋·푸시 (A3 researcher와 병렬).
3. legal-reviewer(B1 risk) → cardnews 검수 PR 생성 → A3 커밋·푸시 → 세션 종료 절차(PROJECTS.md 포함).
