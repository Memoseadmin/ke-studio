# 카드뉴스 HANDOFF — 2026-10-01 (프로젝트 생성, 아직 산출물 없음)

## 목표
인스타그램 카드뉴스 계정(EN)으로 협찬·광고 수익. 게이트 C1 = 90일 내 팔로워 2,000 + 저장률 3% + 미디어킷 + 협찬 제안 5건, 월 비용 5만원 이하 (`cardnews/docs/PLAN.md`).

## 현재 상태
- 브랜치 `cardnews/main`(작업 브랜치 `claude/admiring-clarke-beyyoi`에서 분기). 산출물 0. 계정 미개설.
- 재활용 가능한 소재: `episodes/EP001/marketing.md` §7(라면, 7장 캐러셀 1안), `episodes/EP002/marketing.md` §7(사라진 네 글자, 7장). 디자인 토큰 `episodes/EP001/design/design-system.md`.
- 본 채널 결정: 구독형 혼합, 비주얼 "민화 플랫 × 한지 질감"(docs/TOOLING_TTS_IMAGE.md §D). 이미지 생성 키 UNSET → 카드 이미지는 당분간 Pillow 목업(EP 썸네일 목업 방식)으로 만든다.
- 환경변수: `IG_ACCESS_TOKEN`·`IG_USER_ID` UNSET(미발급). 자동 게시는 키 전까지 수동 패키지.

## 완료
- PLAN.md·HANDOFF·NEXT_PROMPT 작성, 브랜치 생성.

## 실패한 시도와 이유
- 없음(첫 세션 전).

## 대표 결정 대기
1. 계정 언어 EN 확정(기본값) / KR 병행 여부
2. 인스타그램 비즈니스 계정 개설 + 프로필 링크 허브 URL
3. Meta Graph API 토큰 발급 여부(없으면 14일간 수동 게시)
4. 협찬 금지 품목 추가 여부(기본: 건강·금융·법률·도박·주류)

## 다음 할 일 (Phase C1-1 — 14일 테스트 세트)
1. marketer: 14일치 캐러셀 플랜(소재 14개 = EP001·EP002 재활용 4 + 트렌드 10), 캡션·해시태그·게시 시각(ET·CEST), 게시물별 측정 지표.
2. designer: 카드 템플릿 1종(1080x1350, 디자인 시스템 토큰) + 14세트 × 7장 Pillow 목업 → `cardnews/posts/YYYY-MM-DD/`.
3. legal-reviewer: 14세트 일괄 점검(출처·실존 인물·로고·AI 표시·협찬 라벨 규칙) → `cardnews/docs/risk-C1-1.md` BLOCK 0.
4. 검수 PR(브랜치 `cardnews/c1-1` → base `cardnews/main`): 14세트 1장 썸네일을 한 표로, 캡션 링크. approved 후 수동 게시 패키지 확정.
