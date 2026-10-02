# STATUS
갱신: 2026-10-02 08:41Z (COO 세션 claude/admiring-clarke-beyyoi, 대표 퇴근 → 집에서 새 세션)

## 현재 상태
- 운영: COO 세션 `claude/admiring-clarke-beyyoi`(7e4a4e9). CLAUDE.md에 토큰 절약·세션 관리 규범 추가(10/2). 자식 세션 분배·회수·아카이브 표 = docs/PROJECTS.md "하위 세션". 대표 결정 큐 = PROJECTS.md 1~17.
- B 카드뉴스 첫 포스트 = 세트 11 필사 입문 `cardnews/posts/2026-10-19/`(브랜치 cardnews/c1-1-design a079604). 3판(C 틀·3:4·카피 ①·원화+코드) 대표 판정 **수정**: 원화+AI 플레이트+윤동주 사진, 영양소(장당 사실 1+출처, 세트당 인용 2·수치 3). 게시 = PR #5 승인 뒤.
- PR #5(cardnews/c1-1b 7426609+): bio v5 C 확정·릴스 21:00·프로필 v4 A 확정. **대표 approved 라벨 대기**. PR #6 ruflo 스킬 approved·작업 브랜치 머지.
- 디자인 시스템 v1.3(§7 3:4, §9-6 C 틀) ca5f11a. 하우스 스킬 `.claude/skills/cardnews-copy` v1(c1-1-design 6e96cbe).
- 키: IG·R2 SET. MUAPI·FAL·IMAGE·TTS·YOUTUBE UNSET → AI 생성은 집 PC ComfyUI(docs/LOCAL_GPU_PROMPT.md).
- 카피 직원 6개 완료(cd03c80: .claude/agents/copy-*.md, cardnews-copy v1.1 §8 사실 밀도·§9 분담표).
- 자식 세션 6개 **전부 완료·아카이브**(07:00Z). 리서치 3건 cardnews/main 머지(ef699d8). 대표 결정 23건 → PROJECTS 큐 18~21(G1~4·E1~4·D1~6·V1~3·B1~4·P1~5·훅 1안).
- 세트 11 **카피 v5**(c1-1-design 7718d2d): 띠 본문 사실(P2)·1장 "시집 한 권"(P3)·8장 "윤동주처럼 통째로 옮길 시집은?"(E1 ⑤)·훅 1안 확정. copy-editor 조건부 통과(REVIEW-v5.md: 반려 2 → 리서치 세션). 플레이트 프롬프트 v4.1 한지 콜라주(V2) 같은 커밋. ⚠ 이 작업은 COO 세션 서브에이전트로 했음(규칙 위반, 대표 지적) → 이후 전부 자식 세션 분리.
- 프로필 사진: v4 A·v5 반려 → **v6 6안**(c1-1b 30f0fd8, 서체 3×크롭 2, 추천 v6-bx) PR #5 본문 ③ 삽입·컨택트시트 전송 → 전부 반려 → **v7 틀 교체 3안**(c1-1b b98bc20, 글자 0: a 책가도 화병(추천) / b 민화 수탉 / c 책장 칸 기호) 대표 전송 → **대표 지시: v4 A 구도 복귀(바탕 20%·낙관 제외·붓글씨 제대로)** → **v8 세션** `session_01XjZ5qB893hP46mizH9Z3xk`(Opus, c1-1b, OFL 붓 서체 3 × 먹 질감 처리). 체크인 09:27Z. **T1~T10 기획안** 검수 **PR #7** 라벨 대기(T-D6 상위 8 확정). **창의 직원 v1 설치 완료**(agents/creative-v1 dd5f0e9: CD·AD·illustrator Opus / photo-editor·typographer Sonnet, designer → docs/agents-retired, ke-visual-critique 스킬, REFERENCE_BOARD 16, Remotion 무료 해당) → 검수 **PR #8** 라벨 대기. 진행 중 자식 세션 1(프로필 v8).
- 집 PC 플레이트: `plates/v4/*.png` 원격 0장 → 대표 미푸시(프롬프트 팩은 v4.1 한지 콜라주로 갱신됨, 집 PC에서 다시 받아 생성). 4판 렌더 보류.
- A 유튜브: 보류(대표 10/2 "카드뉴스 집중"). 채널명 1·2차 후보 docs/CHANNEL_NAME.md, EP001·002 approved·업로드 0.

## 다음 할 일
1. **대표 집 PC**: ComfyUI 플레이트 40장(`cardnews/posts/2026-10-19/plates/README-homepc.md` v4.1 한지 콜라주, pull 먼저) → `plates/v4/P{장}{a|b}-s{시드}.png` → cardnews/c1-1-design 푸시. 이게 4판 게이트.
2. v8 세션 회수 → contact-profile-v8.png 대표 전송 → PR #5 본문 ③ 갱신 → 택1 → approved · PR #7(기획안 approved → cardnews/main 머지 → AGENDA "기획", C1-1 14건 "제작") · PR #8(창의 직원 approved → claude/admiring-clarke-beyyoi 머지, PROJECTS "공용 자원" 갱신).
3. 라벨 확인 명령: GitHub MCP `list_pull_requests state=open fields=[number,labels]` → #5·#7·#8.
4. 플레이트 푸시되면 **4판 렌더 Opus 세션**(cards.v5.json + caption.v5.txt + V1 35:15:25:25 + V3 소자 + P5 Nanum Brush + Y1 사진 추정 사용 + v4.1 플레이트) → contact.png → 대표. PR #8 승인됐으면 A9 파일럿 공정(art-director 브리프 → 3안 → creative-director 비평(ke-visual-critique, 평균 7·최저 6) → 1회 수정 → 통과본+점수표만 대표에게)으로.
5. legal(세트 11: 윤동주 L1~L6·§9-5 AI 라벨 D6 반영·§9-2 v1.4) → 검수 PR(c1-1-design → cardnews/main) → approved → Sonnet 세션 `r2_upload.py --execute` → `ig_publish.py --pr N --execute`(PNG→JPEG 변환 필요, DISTRIBUTION_2026 발견 1).
6. 트렌드 리서치는 루틴 아님 — 대표에게 물은 뒤 단발(Opus). 세트 01~14 병렬 세션은 4판 승인 후.

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
