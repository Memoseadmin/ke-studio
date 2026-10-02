# STATUS
갱신: 2026-10-02 06:35Z (COO 세션 e90e44c+)

## 현재 상태
- 운영: COO 세션 `claude/admiring-clarke-beyyoi`(7e4a4e9). CLAUDE.md에 토큰 절약·세션 관리 규범 추가(10/2). 자식 세션 분배·회수·아카이브 표 = docs/PROJECTS.md "하위 세션". 대표 결정 큐 = PROJECTS.md 1~17.
- B 카드뉴스 첫 포스트 = 세트 11 필사 입문 `cardnews/posts/2026-10-19/`(브랜치 cardnews/c1-1-design a079604). 3판(C 틀·3:4·카피 ①·원화+코드) 대표 판정 **수정**: 원화+AI 플레이트+윤동주 사진, 영양소(장당 사실 1+출처, 세트당 인용 2·수치 3). 게시 = PR #5 승인 뒤.
- PR #5(cardnews/c1-1b 7426609+): bio v5 C 확정·릴스 21:00·프로필 v4 A 확정. **대표 approved 라벨 대기**. PR #6 ruflo 스킬 approved·작업 브랜치 머지.
- 디자인 시스템 v1.3(§7 3:4, §9-6 C 틀) ca5f11a. 하우스 스킬 `.claude/skills/cardnews-copy` v1(c1-1-design 6e96cbe).
- 키: IG·R2 SET. MUAPI·FAL·IMAGE·TTS·YOUTUBE UNSET → AI 생성은 집 PC ComfyUI(docs/LOCAL_GPU_PROMPT.md).
- 카피 직원 6개 완료(cd03c80: .claude/agents/copy-*.md, cardnews-copy v1.1 §8 사실 밀도·§9 분담표).
- 자식 세션 6 중 **완료·아카이브 2**(10/2 06:33): 4판 준비 `session_011twGRG…`(c1-1-design cb85a57: RESEARCH-v4·PHOTOS-yun·plates/PROMPTS-v4·VISUAL-BRIEF-v4, 결정 큐 18) / 사업 방향 `session_014Y1ydg…`(research/cn-business a6fb846, B1~B4 = 결정 큐 19). **진행 중 4**: 성장 플레이북 `session_016Mgo4LJwXasP64iKJpFTq1`(research/cn-growth 미푸시) / 참여 설계 `session_013kDvnneJpccpdRACuQCrsU` / 배포 전략 `session_01BCdvrogHr2z9zXdXiV1MmB`(research/cn-distribution 미푸시) / 시각 벤치마크 2차 `session_013t5A9foC3kpm2L1QTFA7fm`. 체크인 trig_01VTSDpJNX4yJwBT2HXC8TBW(06:41Z).
- 집 PC 플레이트: `plates/v4/*.png` 원격 0장 → 대표 미푸시, 카피 재작성·4판 렌더 보류.
- A 유튜브: 보류(대표 10/2 "카드뉴스 집중"). 채널명 1·2차 후보 docs/CHANNEL_NAME.md, EP001·002 approved·업로드 0.

## 다음 할 일
1. 남은 자식 세션 4개 회수(체크인 06:41Z 예약, 완료 전까지 8분마다 재예약): get_session → fetch → PROJECTS 표 갱신 → archive. 전부 모이면 대표 결정 G1~G4·E1~E4·D1~D5·V1~V3 + 큐 18(P1~P5, 윤동주 PD)·19(B1~B4)를 **한 번에** AskUserQuestion(4개씩) → PROJECTS 결정 큐에 기록.
2. 대표가 집 PC에서 AI 플레이트 생성·푸시(`cardnews/posts/2026-10-19/plates/`, README-homepc.md) → copy-* 직원으로 카피 재작성 → 4판 렌더(Opus) → contact.png 대표 확인.
3. 윤동주 사진 PD 판정(PHOTOS-yun.md) + §9-2 v1.4(스톡 L1 ⓑ·L2) legal 세션 → 디자인 시스템 반영.
4. legal(세트 11) → 검수 PR(cardnews/c1-1-design → cardnews/main) → approved → 새 Sonnet 세션 `r2_upload.py --execute` → `ig_publish.py --pr N --execute`(PR #5 승인 뒤).
5. 리서치 5건 결과를 cardnews/main에 머지, 세트 01~14 병렬 5세션(cardnews/v3-sets-A~E)은 4판 승인 후.

## 검증 방법
- 세션 표: `grep -c "진행 중 |" docs/PROJECTS.md` → 0이면 전부 회수.
- 3판/4판 자동 점검: `python3 -c "import json;print(json.load(open('cardnews/posts/2026-10-19/RENDER.json'))['checks_failed'])"` → `[]`.
- 라벨: GitHub MCP `list_pull_requests fields=[labels]` PR #5 `approved`.
- 게시 게이트: `scripts/ig_publish.py --check` 경로 B·username=chaekgado.note.

## 미해결 / 주의
- L3(AI 표시 스톡 사용) 미결. 링크 허브 URL 미정. @trend_portal 핸들 확인 불가.
- 캡션 초안에 "AI로 생성" 문구 금지(대표: 출처만). 건강·효능 주장 금지.
- 세트 11 7장 원화 1.74배 확대 경고 → 국립중앙박물관 책가도(공공누리1) 수동 다운로드로 교체 가능.
- 자식 세션 push 거부 시 대신 푸시하지 않음. 비밀값 출력 금지(SET/UNSET만).

## 실패한 시도
- 2판(b032e09): 서양 스톡 사진 → "AI 생성물 같다" 반려. 3판(a079604): 원화만 → "영양소 부족" 수정.
- bio v4: "저장해 두고 꺼내 보세요" 류 안내문 → AI틱 반려 → v5 명사구·구어로 해결.
- 워크트리에서 `git pull --rebase` 실행 → 분리 HEAD 충돌. 워크트리는 `checkout --detach origin/<branch>`만.
- Open-Generative-AI 웹 빌드 분류기 차단 2회. muapi CLI만 사용.
