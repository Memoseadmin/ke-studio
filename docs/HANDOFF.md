# HANDOFF — 2026-10-01 (Phase 2 EP001 목업 렌더 완료, 업로드 없음)

## 목표
KE Studio: Korea Explained 채널의 기획→대본→디자인→마케팅→업로드를 에이전트로 자동화. 수익 = 제휴·협찬·커머스.
첫 게이트: 링크 클릭률 1%, 첫 제휴 매출, 월 비용 20만원 이하(docs/PLAN.md).

## 현재 상태
- 작업 브랜치 `claude/admiring-clarke-beyyoi`(새 세션은 이걸 체크아웃). EP001 산출물은 `ep/EP001`(작업 브랜치를 병합해 둠).
- **PR #1 https://github.com/Memoseadmin/ke-studio/pull/1**: 라벨 0개, 코멘트·리뷰 0건(Phase 2 시작 시 GitHub MCP로 확인) → 대표 결정은 기본값 적용.
- EP001 risk.md **v3: BLOCK 0 / FIX 3 / PASS 7**. 업로드 조건 = approved + FIX 1b·5·7 해소 + real 모드 렌더를 legal이 재점검.
- 환경변수: GITHUB_TOKEN만 SET. TTS_API_KEY·IMAGE_API_KEY·YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN UNSET.
- 렌더 결과(목업)는 이 VM의 `render/EP001/`에만 있었다(커밋 제외, 세션 종료 시 사라짐). 재렌더는 `episodes/EP001/render-input/*.json` + 스킬로 2~4분.

## 완료 (Phase 2, 성공 기준 4/4)
1. 반려 코멘트 없음 → 해당 없음. risk BLOCK 0 유지.
2. producer: 스킬 2개 자체 작성(`.claude/skills/ffmpeg-assemble`, `shorts-cut`. 목업/실제 모드, docs/SKILLS.md "자체 작성(사내)").
   EN 목업 렌더: long 9:51(1920x1080) + short 1~5 = 57.6/58.4/56.0/59.2/32.4초(1080x1920), 무음, AI·외부 소재 0.
   `episodes/EP001/render-log.md`, `render-preview/long-contact.png`·`shorts-contact.png`, `render-input/*.json` 커밋.
3. legal-reviewer: FIX 5 재판정 → **FIX 유지**(목업 소재·대체 폰트는 문제없음, 최종 에셋과 라이선스 기록 없음). 추적 #8·#9 추가.
4. approved 없음 → publisher 미실행, 업로드 0건. `episodes/EP001/publish.log`에 게이트 STOP 기록.

## 실패한 시도와 이유 / 주의
- 키 없음 → TTS·AI 이미지·업로드 불가. 렌더는 텍스트 슬라이드 목업(MOCKUP 표기)으로 대체.
- 지정 폰트 3종 미설치 → Liberation Sans(OFL)·WenQuanYi Zen Hei(GPL-2+폰트 예외)로 대체. legal은 상업 번인 OK.
- 숏폼 1은 컷 플랜대로면 67.6초 → 훅·CTA 낭독을 빼고 57.6초로 맞춤(CTA는 화면 카드). marketer 확인 필요.
- 숏폼 4는 여유 0.8초 → 실제 TTS가 150wpm보다 느리면 60초 초과(shorts-cut이 파일 생성을 거부).
- 서브에이전트 산출물은 미추적으로 남아 stop hook이 경고. 스킬은 작업 브랜치, EP 산출물은 ep/EP001로 나눠 커밋해 PR diff를 깨끗하게 유지.

## 대표 결정 대기
1. PR #1: 승인(approved) 또는 ①~⑧ 번호로 반려 코멘트
2. 키: TTS·이미지 공급자와 키, YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN → TTS가 ElevenLabs면 elevenlabs-tts 설치. TTS·음악 상용 라이선스(플랜·약관 사본)
3. 제휴 상품 지정(가안 A 멀티팩·B 양은냄비), Amazon·쿠팡 계정/트래킹 ID, 쿠팡 고지 공식 원문 대조(FIX 1b), 링크 허브
4. KR판 별도 업로드 여부(현재 보류, EN만) / 제목 "Korean Screens" 확인
5. risk #9: publisher 게이트를 늘릴지(real 모드·MOCKUP 표기 없음·무음 아님·risk FIX 0까지 확인). 현재 publisher.md는 approved·설명란 첫 줄·AI 설정만 확인
6. 지정 폰트 3종을 setup.sh에 추가 · design-system.md 공용 위치 · PLAN.md 비진정성 정책 날짜 정정
7. (이월) PLAN.md 결정 1~4, 보류 스킬 nano-banana·ScrapeCreators

## 다음 할 일 (Phase 3 — EP001 마무리 + EP002 기획)
1. PR #1 상태 확인 → 반려 항목만 재작업. 공통 수정: S06 "Huntrix" → "HUNTR/X"(risk #8: writer→marketer·producer), 숏폼 1 편집안 marketer 확인.
2. 키가 SET이면 producer real 모드 렌더(장면 플레이트·TTS·지정 폰트, 생성 기록) → legal FIX 5 재판정. 없으면 건너뛰고 필요 키만 보고.
3. approved + FIX 0 + real 렌더일 때만 publisher 비공개 업로드. 아니면 publish.log에 STOP 기록.
4. EP002: 50:50 비율에 맞춰 문화·역사 설명형으로 researcher 소재 10개 → research.md(ep/EP002).
