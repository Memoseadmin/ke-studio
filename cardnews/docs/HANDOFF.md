# 카드뉴스 HANDOFF — 2026-10-02 (C1-1 14일 세트 검수 PR #4 생성)

## 목표
인스타그램 **한국어** 카드뉴스 계정으로 **한국 브랜드 제휴·협찬 광고** 수익(대표 확정 2026-10-01). 게이트 C1 = 90일 내 팔로워 2,000 + 저장률 3% + 미디어킷 + 협찬 제안 5건, 월 비용 5만원 이하 (`cardnews/docs/PLAN.md`).

## 현재 상태
- 브랜치 `cardnews/main`(작업 브랜치 `claude/admiring-clarke-beyyoi`에서 분기). 산출물 0. 계정 미개설.
- 재활용 가능한 소재: `episodes/EP001/marketing.md` §7(라면, 7장 캐러셀 1안), `episodes/EP002/marketing.md` §7(사라진 네 글자, 7장). 디자인 토큰 `episodes/EP001/design/design-system.md`.
- 본 채널 결정: 구독형 혼합, 비주얼 "민화 플랫 × 한지 질감"(docs/TOOLING_TTS_IMAGE.md §D). 이미지 생성 키 UNSET → 카드 이미지는 당분간 Pillow 목업(EP 썸네일 목업 방식)으로 만든다.
- 환경변수: `IG_ACCESS_TOKEN`·`IG_USER_ID` UNSET(미발급). 자동 게시는 키 전까지 수동 패키지.

## 완료 (Phase C1-1)
- 계정 "책가도 노트" @chaekgado.note 확정(대표). 인스타 프로페셔널 전환·페이지 연결·토큰 발급은 대표가 완료 보고(환경변수 입력은 미확인 → UNSET).
- 리서치: C1-1-trends.md(14 소재), SPONSORSHIP_MARKET.md(단가·계정 이름·그리드).
- 제작: C1-1-plan.md, 14세트(cards.json·caption.txt·PNG 목업 103장·contact·RENDER.json), 템플릿(template.md·render_cards.py `--final` 옵션), MEDIA_KIT.md 초안, C1-1-overview.png.
- legal risk-C1-1.md v2: BLOCK 0 / FIX 3(승인 후 렌더 단계) / PASS 8. 사실 105건, 출처 없음 0. 13 세트는 넷플릭스→전시 체크리스트로 교체.
- 검수 PR #4 https://github.com/Memoseadmin/ke-studio/pull/4 (cardnews/c1-1 → cardnews/main). 게시 0건.
- 게시 도구(작업 브랜치에 머지): scripts/ig_publish.py(dry-run 기본·게이트 4개), r2_upload.py, ig_token_refresh.py, README-ig.md. 이미지 호스팅 = Cloudflare R2 버킷 chaekgado-cards, 공개 URL은 docs/ENV.md.
- C1-1 트렌드 리서치: `cardnews/research/C1-1-trends.md` — 카드뉴스 후보 14개(EP 재활용 2 + 한국 트렌드 12).

## 실패한 시도와 이유
- 렌더러 금지어 필터가 "로고 금지"처럼 부정 맥락도 잡아 모티프가 달·산으로 바뀜 → 절(clause) 단위로 부정어 제외하도록 수정.
- 공개 카드 마지막 장에 원본 URL·내부 "협찬 슬롯"이 찍힘 → 출처 이름 줄만, 슬롯은 기본 비표시.
- 13 세트 넷플릭스 공개일이 R22(미검증 재게시)만 근거라 오류 → 소재 교체. 뉴시스 1/29 '가갸'(가제)는 실제 '일구이륙 무한이륙'(대한민국역사박물관)로 확정돼 01·06 정정.
- 새 하위 세션에서도 IG_ACCESS_TOKEN·IG_USER_ID UNSET → 대표가 환경 설정 저장을 확인해야 함.

## 대표 결정 대기
1. ~~계정 언어~~ KR 확정(대표). 계정 이름·프로필 소개 문구 확정 필요
2. 인스타그램 비즈니스 계정 개설 + 프로필 링크 허브 URL
3. Meta Graph API 토큰 발급 여부(없으면 14일간 수동 게시)
4. 협찬 금지 품목 추가 여부(기본: 건강·금융·법률·도박·주류) / 쿠팡파트너스 계정 개설 여부(보조 수익)

## 다음 할 일 (Phase C1-2 — 승인 후 게시 가동)
1. PR #4 approved 확인 → `render_cards.py --all cardnews/posts --final` 재렌더 → legal PNG·RENDER.json 재점검(risk v3) → cardnews/main 머지.
2. Sonnet 세션으로 R2 업로드 1장 테스트 + IG 읽기 전용 검증(키 SET 확인) → 성공 시 `r2_upload.py --execute` 14세트 → `ig_publish.py --schedule` 큐 등록 → 게시 루틴(/schedule, 매일 KST 시각) 설정.
3. 첫 게시 후 analyst 주간 측정 틀(`cardnews/reports/`), 토큰 60일 갱신 알림 루틴.
4. C1-2 소재: 10/23~11/5(빼빼로데이 11/11·수능 11/19 역산), 8장 기본 검토.

## (기록) Phase C1-1 당시 계획
1. marketer: 14일치 캐러셀 플랜(소재 14개 = EP 재활용 ≤4 + 한국 트렌드 ≥10, **전부 한국어**), 캡션·해시태그·게시 시각(KST), 게시물별 측정 지표.
2. designer: 카드 템플릿 1종(1080x1350, 디자인 시스템 토큰) + 14세트 × 7장 Pillow 목업 → `cardnews/posts/YYYY-MM-DD/`.
3. legal-reviewer: 14세트 일괄 점검(출처·실존 인물·로고·AI 표시·협찬 라벨 규칙) → `cardnews/docs/risk-C1-1.md` BLOCK 0.
4. 검수 PR(브랜치 `cardnews/c1-1` → base `cardnews/main`): 14세트 1장 썸네일을 한 표로, 캡션 링크. approved 후 수동 게시 패키지 확정.
