# 카드뉴스 HANDOFF — 2026-10-02 (C1-1 final 머지 · v3 디자인 전환 · 세트 11 첫 게시 준비)

## 목표
인스타 "책가도 노트" @chaekgado.note(한국어·한국 독자, 당분간 한국어 유지). 정체성: 한국 문화를 축으로 **여행·음식·축제·전시까지 통합한 최신 트렌드 카드뉴스**. 수익 = 한국 브랜드 협찬(보조 쿠팡). 게이트 C1 = 90일 팔로워 2,000 + 저장률 3% + 미디어킷 + 협찬 제안 5건, 월 5만원 이하.

## 현재 상태
- `cardnews/main`: C1-1 14세트 **final 렌더(v2 Pillow)** + legal v3 BLOCK 0 + F1 반영(293d962) + `cardnews/docs/DESIGN_SOURCES.md`(디자인 소싱 리서치) + `cardnews/publish/C1-1-manual.md`(수동 게시 패키지, v3 전환 후 갱신 필요).
- `cardnews/c1-1-design`: **v3 렌더러** `cardnews/design/v3/`(HTML/CSS → Playwright Chromium, 서체 세트 B 함렛/마루부리/Black Han Sans + Noto Serif KR 폴백, `render_v3.py --strict`) · 세트 11(2026-10-19) **3안 1판**(사진 1/8, 위키미디어 429) · VISUAL-BRIEF.md · DESIGN-v3.md · PHILOSOPHY-v3.md · 캡션 A안(AI 줄 삭제, 출처만) · 사진 후보 42장 `cardnews/design/photos/`. 사진 원본은 `photos/src/`(gitignore, PHOTOS.json URL로 재다운로드).
- `cardnews/c1-1b`: PR #5(릴스 14 목업 + 프로필 패키지, legal BLOCK 0/FIX 1 반영). PROFILE.md v3(이름 필드 확정 `책가도 노트 | 민화 원화로 보는 오늘의 한국`, 허브 UTM, 고정 순서) → bio v4(민화 원화 표현 제거) 세션 진행 중. 프로필 사진 A/B/C는 폐기 → v3 톤으로 재제작 예정.
- 키: IG 경로 B 통과, R2 통과. 게시 게이트 = approved·final·출처 줄·해시태그 ≤5(AI 문구 선택).
- **대표 결정(2026-10-02)**: v3 = **3안 하이브리드 콜라주**(편집 실사 주인공 + 원화 프레임·낙관·띠) · **이미지는 장 내용에서 출발**(VISUAL-BRIEF 필수) · AI 고지 문구 삭제(카드·캡션 출처만) · 세트 11 = 10/2 첫 게시(3안으로) · 세트 01(10/9) AI 없이 · 02~14 AI 배경 + 편집 실사(원본 그대로 금지) · 릴스는 19:00일 **21:00** · 링크 허브 = 무료 서비스(URL 대표) · 호작도 PD 원화 허용 · 포스트 제작은 Opus 자식 세션 병렬.

## 완료 (이번 세션)
- PR #4 승인 후 final 렌더 → legal v3 → 머지. 릴스 14개 목업 렌더 + 프로필 패키지 + PR #5.
- v3 렌더러·세트 11 1판·캡션 재초안·사진 후보 42장·디자인 소싱 리서치(원화 31점·서체 실측·스킬 초안 3).

## 실패한 시도와 이유
- v2 Pillow 렌더(중국어 대체 서체·클립아트 반복·빈 띠·옛한글 깨짐) → 대표 "품질 불가" → v3 HTML 렌더러로 교체.
- v3 1안(원화 디테일만) → 주제·이미지 불일치 → "장 내용에서 출발" 규칙.
- 위키미디어 429 → 사진 소싱 세션이 박물관 CDN·CC0 사이트로 우회 중. 대안: 대표 PC 수동 다운로드.

## 대표 결정 대기
bio v4 선택 · 세트 11 캡션 A안 확정 · 프로필 사진 v3 방향 · 링크 허브 URL · PR #5 승인 · 이중언어(C1-2).

## 다음 할 일
1. 사진 소싱 결과 → 세트 11 2판(Opus 세션) → 대표 확인 → legal → PR → 승인 → 새 Sonnet 세션에서 R2 업로드·게시(10/2).
2. 세트 01~14 v3 제작을 Opus 세션 5개로 병렬(브랜치 cardnews/v3-sets-A~E) → legal → PR. 릴스 14개 v3 카드로 재렌더(`render_reels.py`). 수동 패키지·MEDIA_KIT 갱신(AI 문구 삭제).
3. 프로필 사진 v3 재제작, bio v4 반영, 허브 URL 받으면 PROFILE §5 완성. 10/9부터 매일 게시 큐(`ig_publish.py --schedule`) + 루틴.
