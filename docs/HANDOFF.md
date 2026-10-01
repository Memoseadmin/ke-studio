# HANDOFF — 2026-10-01 (Phase 3 EP001 마무리 + EP002 기획 착수 완료)

## 목표
KE Studio: Korea Explained 채널의 기획→대본→디자인→마케팅→업로드를 에이전트로 자동화. 수익 = 제휴·협찬·커머스.
첫 게이트: 링크 클릭률 1%, 첫 제휴 매출, 월 비용 20만원 이하(docs/PLAN.md).

## 현재 상태
- 작업 브랜치 `claude/admiring-clarke-beyyoi`(새 세션은 이걸 체크아웃). EP001 산출물 `ep/EP001`, EP002 산출물 `ep/EP002`(둘 다 작업 브랜치에서 분기).
- **PR #1 https://github.com/Memoseadmin/ke-studio/pull/1**: 라벨 0, 코멘트·리뷰 0(Phase 3 시작 시 GitHub MCP 확인) → 대표 결정은 기본값 적용. 승인 대기 중.
- EP001 risk.md **v4: BLOCK 0 / FIX 3(1b·5·7) / PASS 7**. #8(HUNTR/X) 해소. 업로드 조건 = approved + FIX 0 + real 렌더.
- 환경변수: GITHUB_TOKEN만 SET. TTS_API_KEY·IMAGE_API_KEY·YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN UNSET → real 렌더·업로드 모두 미실행.
- 영상 파일은 어디에도 없다(목업은 Phase 2 VM에서 소멸). 재렌더는 `episodes/EP001/render-input/*.json` + 스킬로 2~4분.
- EP002 선정 1위: "Korea Banned Its Own Alphabet: The 580-Year Fight for Hangul"(문화·역사 설명형). 2026 = 훈민정음 반포 580돌 + 한글날 제정 100돌, 10/9 한글날 시의성.

## 완료 (Phase 3, 성공 기준 4/4)
1. 반려 코멘트 없음. writer: S06 "Huntrix"→"HUNTR/X"(script.en.md, scenes.en.json + TTS 발음 note). marketer: 캡션·캐러셀 치환, 숏폼 1 편집안 승인(57.6초, 훅=화면 문구만, CTA=무음 엔드 카드 4초, shorts.en.json 변경 없음). legal v4 BLOCK 0 유지. ep/EP001 4커밋 푸시.
2. 환경변수 SET/UNSET만 확인(값 미출력). TTS·이미지 키 UNSET → 렌더 건너뜀. 필요 키: TTS_API_KEY, IMAGE_API_KEY(공급자 선택 필요), 업로드용 YOUTUBE_* 3개.
3. 게이트 3개 전부 미충족(approved 없음·FIX 3·real 렌더 없음) → publisher 업로드 0건, publish.log 25~38행 STOP 기록. 수동 패키지는 real 렌더 후에만 만든다.
4. ep/EP002: general-purpose가 last30days 8회 실행(키 없음, 37건) → trends-last30days.md. researcher가 research.md(157줄, 후보 10개 전부 문화·역사 설명형, 1위 핵심 사실 20개 ✅13/△3/단일4/미검증0, 건강·금융·법률 0). 2커밋 푸시.

## 실패한 시도와 이유 / 주의
- last30days `intent=concept/evergreen_ok` 플랜은 서브쿼리 2개만 실행 → `opinion/balanced_recent`로 재실행해야 결과가 찬다. YouTube 자막·댓글은 봇체크·429로 대부분 실패.
- EP002 제외 소재: 세월호(참사), 대만 택시(정치·외교), "조선=중국 속국", 한국전쟁 밈·민주화(정치 보류), 배우 유카타(인물), 피카츄(IP). 후보1 대본 금지 수치: "10년 만에 문해", 전근대 문해율.
- EP002 2차 출처 미확보: Monash·Yale 페이지 접근 실패(F3·F4). 후보10 리메이크 차이 미시청.
- 숏폼 1 엔드 카드는 S03 마지막 문장 낭독과 겹친다(총 길이에 안 더함). 자막 y1400은 카드 밖이라 가려지지 않으나 real 렌더 컨택트시트에서 확인.
- 병렬 작업은 `.worktrees/ep002`(git worktree, `.git/info/exclude` 등록)로 분리해 충돌 없이 진행했다. 새 세션은 새로 클론하므로 worktree는 없다.
- GitHub MCP `pull_request_read get`에는 labels 필드가 없다 → `list_pull_requests fields=[labels]` 또는 `search_pull_requests label:approved`로 확인.

## 대표 결정 대기
1. PR #1: 승인(approved) 또는 ①~⑧ 번호로 반려 코멘트
2. 키 입력: TTS·이미지 공급자 선택 + TTS_API_KEY·IMAGE_API_KEY(상용 라이선스 플랜), YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN. TTS가 ElevenLabs면 elevenlabs-tts 설치
3. 제휴 상품 지정(가안 A 멀티팩·B 양은냄비), Amazon·쿠팡 계정/트래킹 ID, 쿠팡 고지 원문 대조(FIX 1b), 링크 허브(FIX 7)
4. EP002 1위 후보(한글) 확정 여부 / 차순위: 후보2 저승사자, 후보7 5대궁(10/7~11 궁중문화축전)
5. 인스타 캐러셀 2주 테스트 여부, KR판 업로드 여부(현재 보류·EN만), risk #9 publisher 게이트 확장 여부
6. (이월) 지정 폰트 setup.sh 추가, PLAN.md 비진정성 정책 날짜 정정, PLAN.md 결정 1~4, 보류 스킬 nano-banana·ScrapeCreators

## 다음 할 일 (Phase 4 — EP002 대본·디자인·마케팅·검수 PR + EP001 키 확보 시 렌더)
1. ep/EP002: writer(script.en.md·script.kr.md, 제휴는 꼬리에 한글 워크북·붓펜 등 1~2개) → designer → marketer → legal → 검수 PR ①~⑧ 생성.
2. 키가 SET이면 EP001 producer real 렌더(ffmpeg-assemble·shorts-cut) → legal FIX 5 재판정 → 게이트 충족 시 publisher.
3. PR #1 반려 코멘트가 있으면 적힌 항목만 재작업.
