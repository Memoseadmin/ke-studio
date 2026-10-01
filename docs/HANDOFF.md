# HANDOFF — 2026-10-01 (Phase 1 EP001 검수 PR 완료)

## 목표
KE Studio: Korea Explained 채널의 기획→대본→디자인→마케팅→업로드를 에이전트로 자동화. 수익 = 제휴·협찬·커머스.
첫 게이트: 링크 클릭률 1%, 첫 제휴 매출, 월 비용 20만원 이하(docs/PLAN.md).

## 현재 상태
- 작업 브랜치 `claude/admiring-clarke-beyyoi`(새 세션은 이걸 체크아웃). 에피소드 브랜치 `ep/EP001`은 여기서 분기.
- **EP001 검수 PR 열림: https://github.com/Memoseadmin/ke-studio/pull/1** (base = 작업 브랜치). 대표 `approved` 라벨/반려 코멘트 대기.
- EP001 = "Why Ramyeon Keeps Showing Up on Korean Screens"(구매 의도형, 신라면 40주년 2026-10). risk.md v2: BLOCK 0 / FIX 3 / PASS 7.
- 환경변수: GITHUB_TOKEN만 SET. YouTube·TTS·이미지 키 UNSET → 렌더·업로드 불가 상태.
- setup.sh 실행 시 /usr/bin/python3.12 사용 가능(last30days는 `LAST30DAYS_PYTHON=/usr/bin/python3.12`).

## 완료 (Phase 1, 성공 기준 4/4)
- last30days 엔진 6회 실행 → `episodes/EP001/trends-last30days.md`(19건, Reddit·YouTube 검색만 동작).
- researcher: 소재 10개(구매 7/문화 3), 팩트 20개, 출처 S1~S47. 라면 라이브러리 2026 운영 확인.
- writer: script.en.md(1,478단어 ≈ 9.9분)·script.kr.md(956어절 ≈ 9~10분 추정), S01~S12, 사실마다 [F#] 태그.
- designer: design-system.md, 썸네일 3안(Pillow 목업 PNG + thumbs-compare.png), scene-prompts.md S01~S12, make_thumbs.py.
- marketer: 제목 5안, 설명란(고지 첫 줄 EN/KR), 태그, 고정 댓글, 숏폼 5, 캡션·게시 시각(가설), 제휴 표, **인스타 캐러셀 1안(기본값)**.
- legal-reviewer: v1 BLOCK 1(KR 쿠팡 고지가 S11에만) → writer가 S02·S12에 낭독+자막 추가, marketer가 Sources 3개·AI 문구 수정 → v2 BLOCK 0. 사실 39개: 출처 38 / 미검증 1 / 출처 없음 0.

## 실패한 시도와 이유
- researcher에는 Bash가 없어 last30days 실행 불가 → general-purpose 에이전트로 엔진 실행, 결과 파일을 researcher에 입력.
- last30days: X·TikTok·IG는 키 필요로 스킵, YouTube 자막은 yt-dlp 봇 확인·429로 실패, Jobs 502. Reddit 본문 직접 열람도 차단.
- partners.coupang.com 403 → 쿠팡 고지 공식 문구 미검증(KR판 6곳에 사용 중, 대표 대조 후 일괄 교체).
- 이미지 생성 키 없음 → 썸네일은 레이아웃 목업(MOCKUP 표기). 지정 폰트(Anton·Black Han Sans·Pretendard, OFL) 미설치.
- "Every K-Drama" 제목: 사례가 영화 2·애니 1이라 부정확 → "Korean Screens"로 변경(대표 확인 필요).
- 서브에이전트 산출물은 미추적 상태로 남음 → stop hook 경고. 직원 작업마다 메인이 바로 커밋·푸시.

## 대표 결정 대기
1. PR #1: 승인(approved) 또는 ①~⑧ 번호로 반려 코멘트
2. 제휴 상품 지정(가안 A 라면 멀티팩·B 양은냄비), "이달의 상품 목록" 작성, Amazon·쿠팡 계정/트래킹 ID, 링크 허브
3. KR판 별도 업로드 vs EN 영상에 KR 설명 / 제목 "Korean Screens" 확인
4. 환경변수: 이미지·TTS 공급자와 키, YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN → TTS가 ElevenLabs면 elevenlabs-tts 설치
5. PLAN.md "비진정성 정책 2026-07-16 개정" 날짜가 YouTube 공식 페이지에서 미확인(최신 2025-07-15) → 문서 정정 여부
6. design-system.md 공용 위치(docs/로 이동?) · 폰트 3종 setup.sh 추가 · Amazon 트래킹 ID 100개 상한 운용
7. (이월) PLAN.md 결정 1~4, 보류 스킬 nano-banana·ScrapeCreators(이번에도 보류 유지)

## 다음 할 일 (Phase 2 — EP001 피드백 반영 → 렌더 → 승인 시 업로드)
1. PR #1 상태 확인: 반려 코멘트 항목만 재작업 → legal 재점검 → 푸시. approved면 다음으로.
2. producer: 키가 있으면 TTS·장면 이미지·롱폼·숏폼 5 렌더 + 라이선스·생성 기록(risk FIX 5). 없으면 목업 슬라이드+자막 프리뷰 렌더와 필요한 키 목록.
3. publisher: approved 라벨이 있을 때만 YouTube 비공개 업로드(키 없으면 수동 업로드 패키지). 필요 시 직접 작성 스킬(ffmpeg-assemble·shorts-cut·youtube-upload).
