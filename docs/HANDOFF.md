# HANDOFF — 2026-10-02 (운영 규범 개정 · 카드뉴스 v3 전환 · 세트 11 첫 게시 준비 · 유튜브 런칭 계획 완성)

## 목표
KE Studio 통합 운영(현황판 = docs/PROJECTS.md). A 유튜브(EN, 구독형 혼합) + B 카드뉴스 "책가도 노트"(KR 인스타, 한국 협찬·여행·음식·축제·전시 트렌드).
**운영 규범(대표 2026-10-02)**: COO 세션은 명령·총괄 결정·기획만. 실작업은 난이도별 자식 세션(판단·리서치·제작 = Opus, 반복·검증 = Sonnet). **대표가 결정하지 않은 사항은 기본값으로 진행하지 않고 끝까지 묻는다.** 자식 세션은 PROJECTS.md 하위 세션 표에 즉시 등록·회수·아카이브.

## 현재 상태
- 브랜치: 작업 `claude/admiring-clarke-beyyoi`(docs·scripts·스킬) / A `ep/EP001`·`ep/EP002`(approved, 업로드 0)·`ep/EP003`(research+대본 EN·KR 완료 fa19eef) / B `cardnews/main`(C1-1 14세트 final 머지, DESIGN_SOURCES.md, 수동 게시 패키지) · `cardnews/c1-1b`(PR #5 릴스 14+프로필, 검수 중) · `cardnews/c1-1-design`(**v3 렌더러 HTML/CSS→Chromium + 세트 11 3안 1판**, 사진 대기).
- 키: **IG 경로 B 통과**(IGAA, @chaekgado.note BUSINESS) · **R2 통과**(PNG 왕복 OK) · FAL_KEY 보류(대표 PC GPU 있음, LoRA는 나중) · A쪽 TTS·이미지·YouTube 키 전부 UNSET.
- 게시 도구: `scripts/ig_publish.py`(IG_API_BASE 경로 A/B 자동, `--check`, 게이트 = approved 라벨·mode=final·**출처 줄**·해시태그 ≤5; AI 문구는 선택) · `r2_upload.py` · 수동 패키지 `cardnews/publish/C1-1-manual.md`.
- **오늘(10/2) 첫 게시 = 세트 11 필사 입문(`cardnews/posts/2026-10-19/`)** v3 3안(편집 실사 콜라주 + 원화 프레임, AI 라벨 없음, 출처만). 상태: 1판은 사진 1/8(위키미디어 429) → 사진 소싱 세션 결과 대기 → designer 2판 → 대표 확인 → legal → 검수 PR(cardnews/c1-1-design → cardnews/main) → approved → **새 Sonnet 세션에서** `r2_upload.py --execute` → `ig_publish.py --pr N --execute`(IGAA 토큰은 새 세션에서만 읽힘).
- 대표 결정 완료(PROJECTS.md "대표 결정 큐" 7~9, 6-1·6-2): v3 = 3안 하이브리드 콜라주 · 서체 B · AI 고지 삭제(출처만) · 이미지는 장 내용에서 출발 · 세트 01 = AI 없이(10/9) · 02~14 = AI 배경+편집 실사 · 이름 필드 확정 · 릴스 21:00 · 링크 허브 = 무료 서비스 · 한국어 유지(이중언어는 C1-2) · 유튜브 N2~N7·N9·N10·N13 · 호작도 PD 원화 허용 · 디자인 시스템 v1.1 추가.
- **대표 결정 대기**: 채널명(Korea 없는 이름, 세션 결과 후) · bio v4 선택 · 세트 11 캡션 A안 확정 · 프로필 사진 v3 재제작 방향 · N8 유료 프로모션(legal 후) · N12 도메인·상표(이름 후) · PR #5 승인.

## 진행 중 자식 세션 (PROJECTS.md 표 참조, 세션 시작 시 get_session으로 전부 확인)
- 세트 11 사진 소싱 `session_01LN42UszjCU2PRCMQyZiRJV`(Opus, cardnews/c1-1-design, PHOTOS.v3.json+fetch_photos.py)
- 채널명 재탐색 `session_016zt8mJerJYqG1MGQU8jGNc`(Opus, research/channel-name, docs/CHANNEL_NAME.md)
- bio v4 `session_017b2PHN9TM8TMubVawfVykv`(Opus, cardnews/c1-1b, PROFILE.md)
- 디자인 시스템 v1.1 `session_01927v4EQ12E5YM2ieLPcc6u`(Sonnet, 작업 브랜치, design-system.md)
- COO 서브에이전트 designer(세트 11 3안 2판 대기)는 세션 재시작 시 사라짐 → 새 세션에서는 **Opus 자식 세션**으로 재지시(DESIGN-v3.md·VISUAL-BRIEF.md·PHOTOS.v3.json 기준).

## 완료 (이번 세션)
- PR #4 final 렌더·legal v3 BLOCK 0 → cardnews/main 머지(98d2a96) · legal C1-1b F1 반영(293d962) · PR #5 생성(릴스 14 목업+프로필 패키지).
- EP003 대본 EN·KR · EP001·002 publish.log 기록 · 스킬 4개 복사 설치(frontend-design·webapp-testing·taste-skill·ui-ux-pro-max).
- 리서치: DESIGN_SOURCES.md(세계 수준 디자인 소싱, 원화 31점·서체 실측·스킬 초안 3) · YOUTUBE_LAUNCH_PLAN.md(549행, 결정 N1~N13) · 사진 후보 42장(C1-1-photos.json).
- 키 검증 5회(R2 값 3회 오입력 끝에 통과) · ig_publish 경로 B·게이트 변경.

## 실패한 시도와 이유
- 위키미디어 커먼즈 429: 클라우드 출구 전체 차단 → 박물관 CDN·CC0 사이트로 우회(진행 중). 대안: 대표 PC에서 수동 다운로드.
- 세트 11 v3 1판: 원화 디테일만 써서 주제·이미지 불일치(대표 지적) → "장 내용에서 출발" 규칙 + VISUAL-BRIEF 도입.
- Black Han Sans·Pretendard는 옛한글 없음 → 서체 세트 B + Noto Serif KR 폴백으로 해결.
- 하위 세션의 값 맞바꾸기 시험은 권한 분류기 차단(자격증명 탐색) → 대표가 직접 재입력.

## 다음 할 일 (docs/NEXT_PROMPT.md)
1. 세션 위생 → 사진 소싱 결과 회수 → 세트 11 2판(Opus) → 대표 확인 → legal → PR → 승인 → 새 세션 게시.
2. 채널명·bio v4·디자인 시스템 v1.1 결과 회수 → 대표 질문 → 반영.
3. 세트 01(10/9, AI 없이)·02~14(AI 배경+편집 실사) 제작을 Opus 자식 세션 5개로 병렬 배분(브랜치 cardnews/v3-sets-A~E) → legal → PR. 릴스는 v3 카드로 재렌더. 유튜브는 채널명 확정 후 개설 체크리스트(YOUTUBE_LAUNCH_PLAN §5) 대표 실행 안내.
