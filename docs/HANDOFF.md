# HANDOFF — 2026-10-02 (Phase 4 후반: 카드뉴스 C1-1 PR #4 승인, 도구·전략 리서치 완료, ECC 설치 머지)

## 목표
KE Studio 통합 운영(docs/PROJECTS.md가 현황판). A 유튜브 Korea Explained(EN, 구독형 혼합) + B 카드뉴스 "책가도 노트"(KR 인스타, 한국 브랜드 협찬). 게이트는 PLAN.md·cardnews/docs/PLAN.md.

## 현재 상태 (세부는 docs/PROJECTS.md)
- 브랜치: 작업 `claude/admiring-clarke-beyyoi`(docs·스킬·scripts) / A 산출물 `ep/EP001`·`ep/EP002`·`ep/EP003`(리서치만) / B `cardnews/main` + 검수 `cardnews/c1-1`(PR #4 approved, 미머지) / `tooling/ig-publisher`(작업 브랜치에 머지됨, 단 마지막 검증 세션 커밋 f2330b5는 미푸시).
- PR: #1 EP001·#2 EP002 approved(업로드 0, 키 UNSET) · #3 ECC 10개 스킬 approved → 머지 완료(9c97b71) · #4 카드뉴스 14세트 approved → **final 렌더·R2 업로드 전**.
- 환경변수(새 세션에서 SET 확인): IG_ACCESS_TOKEN·IG_USER_ID·R2 5개 전부 SET이지만 **값 2개가 틀림**: `R2_ACCESS_KEY_ID` 20자(32자 필요), `IG_USER_ID`가 페이스북 페이지 ID. 또 토큰의 `/me/accounts`가 비어 있어(페이지 미연결, 계정 제한 추정) 페이스북 경유 게시 불가 → **Instagram 직접 로그인 API(경로 B)로 전환 권장**(앱 대시보드 Instagram 제품 → "Instagram 로그인으로 API 설정", 토큰은 IGAA…, ID는 `me?fields=user_id`).
- 대표 결정(이번 세션): 구독형 혼합 전략, ECC 선별 도입, 리서치는 별도 Opus 세션, 하위 세션 모델 규칙(Opus/Sonnet), 카드뉴스 KR·한국 협찬 중심, 계정 "책가도 노트", Meta API 자동 예약(썸네일·문구는 PR에서 선택), 제휴 프로그램 전부 등록, 이미지 호스팅 Cloudflare R2, 하루 캐러셀 1 + 릴스 1.
- 릴스 플랜(C1-1b): marketer 서브에이전트가 `cardnews/posts/C1-1b-reels-plan.md`·`reel.json`×14를 작성 중이었음 → 세션 종료 시점에 미완이면 `cardnews/c1-1` 워킹트리에 없을 수 있다. 새 세션에서 `git status`로 확인, 없으면 같은 지시로 재실행(PROJECTS.md 하위 세션 표 아래 "릴스 지시 요지" 참고).

## 완료 (이번 세션)
- 리서치 6건(EP003 김장 1위, 카드뉴스 소재 14, 협찬 시장·단가·계정 이름, 오픈소스 도구 OSS-③ 하이브리드, 성장 90일 플레이북·YPP 2027-02 문턱 2배, 제휴 프로그램 28개) 전부 문서화·머지.
- 카드뉴스 C1-1: 템플릿·렌더러(`--final`, RENDER.json), 14세트 목업 103장, 캡션, 미디어킷, legal v2 BLOCK 0, PR #4 approved.
- 게시 도구: scripts/ig_publish.py(게이트 4개, dry-run 기본)·r2_upload.py·ig_token_refresh.py·README-ig.md.
- 통합 현황판 docs/PROJECTS.md + 세션 위생 규칙 + 하위 세션 모델 규칙.

## 실패한 시도와 이유
- ECC 플러그인: 클라우드 세션은 플러그인을 로드하지 않음(공식 문서) → 복사 설치 10개만.
- MiniMax H3 스킬: 라이선스가 한국·미국·EU 제외(출력물 표시까지) → 보류(docs/SKILL_CANDIDATES.md).
- 하위 세션이 `git push`를 권한 분류기에 막힘(검증 세션) → 보고는 list_events로 회수, 코드 변경(ENV.md 메모·IG_CONNECTION.md)은 미반영. COO가 대신 푸시하지 않음(권한 우회 금지).
- 페이스북 경유 IG 연결: 페이지 옵트인·권한 전부 정상인데 `/me/accounts` 빈 배열 → 계정 일시 제한 추정. 경로 B 전환이 빠름.
- 렌더러 금지어 필터 오탐, 공개 카드에 URL·협찬 슬롯 노출 → 수정.

## 대표 결정 대기 (docs/PROJECTS.md "대표 결정 큐"와 동일)
1. R2_ACCESS_KEY_ID 재입력(32자), IG 경로 B 전환 후 `IG_ACCESS_TOKEN`(IGAA…)·`IG_USER_ID` 교체
2. [A] 제작 도구: OSS-③ 하이브리드 채택 / 음성 Gemini / LoRA 학습 — 전부 기본값 추천
3. [A] 성장 D1~D3(숏폼 주 7, 커뮤니티 범위, 콜라보) 기본값 / PLAN.md YPP 개정 PR 승인
4. [B] 호작도 모티프 예외, 8장 기본, 링크 허브 URL, 쿠팡파트너스·체험단 가입
5. [A] 키: TTS·IMAGE(GEMINI_API_KEY·FAL_KEY)·YOUTUBE_* 3개, Amazon 트래킹 ID
6. ECC 자작 hooks 2개·CLAUDE.md "위임 완결 계약" 반영 여부

## 다음 할 일 (Phase 5 — docs/NEXT_PROMPT.md)
1. 세션 위생(하위 세션 표 확인·아카이브) → PR 라벨 확인 → 환경변수 SET/UNSET.
2. [B] 키가 고쳐졌으면 Sonnet 세션으로 R2 왕복·IG(경로 B) 검증 → `render_cards.py --all cardnews/posts --final` → legal PNG 재점검(v3) → cardnews/c1-1 → cardnews/main 머지 → R2 업로드 → 10/9부터 게시 큐·루틴. 릴스 플랜 확인/재실행 → producer 렌더(무음, 자막) → C1-1b PR. 프로필 패키지(사진·소개·허브 구성) designer·marketer.
3. [A] 키 SET이면 EP002 S01 샘플(OSS-③: Remotion+Z-Image+Gemini TTS) → 대표 A/B → EP001·EP002 real 렌더 → FIX 5 재판정 → 업로드. EP003 writer(김장) 시작. PLAN.md YPP 개정 PR.
