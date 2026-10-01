# HANDOFF — 2026-10-01 (Phase 4 EP002 검수 PR 생성 완료)

## 목표
KE Studio: Korea Explained 채널의 기획→대본→디자인→마케팅→업로드를 에이전트로 자동화. 수익 = 제휴·협찬·커머스.
첫 게이트: 링크 클릭률 1%, 첫 제휴 매출, 월 비용 20만원 이하(docs/PLAN.md).

## 현재 상태
- 작업 브랜치 `claude/admiring-clarke-beyyoi`(새 세션은 이걸 체크아웃). EP001 산출물 `ep/EP001`, EP002 산출물 `ep/EP002`.
- **PR #1 (EP001)** https://github.com/Memoseadmin/ke-studio/pull/1 : **approved 라벨 부착됨**(대표가 Phase 4 끝에 채팅으로 승인 → COO가 라벨 부착). risk v4 BLOCK 0 / FIX 3(1b·5·7).
- **PR #2 (EP002)** https://github.com/Memoseadmin/ke-studio/pull/2 : Phase 4에 생성, **approved 라벨 부착됨**(동일). risk v1.1 BLOCK 0 / FIX 3(1b·5·7) / PASS 10.
- 업로드 0건(두 편 모두). 게이트 1(approved)만 충족, 게이트 2(FIX 0)·3(real 렌더) 미충족. GITHUB_TOKEN만 SET, TTS·이미지·YouTube 키 UNSET(두 publish.log에 기록). 승인됐으니 AI 라벨의 "human-reviewed" 문구 재삽입은 다음 세션에서 판단.
- 대표 답변(Phase 4 채팅): **EN만 진행, KR판 보류**. 제휴 구조 설명함(Amazon Associates 가입은 대표 몫, 링크는 아직 자리표시자).
- 영상 파일은 어디에도 없다. EP001 재렌더는 `episodes/EP001/render-input/*.json` + ffmpeg-assemble·shorts-cut.

## Phase 4 후반 추가 작업 (대표 요청, 같은 세션)
- 대표 답: EN만 진행·KR 보류. 제휴 구조 설명(Amazon Associates 가입은 대표 몫).
- `docs/TOOLING_TTS_IMAGE.md`: TTS·이미지 공급자 3+3안(출처 61건). COO 추천 = ElevenLabs Creator + Gemini Nano Banana 2(≈48,000원/월) / 가성비 = Google Chirp3 + Recraft V4(≈8,000원/월). 비주얼 방향 "민화 플랫 × 한지 질감". **대표 선택 대기.**
- `docs/OPEN_GENERATIVE_AI_SETUP.md`: 대표가 준 설치 템플릿을 클라우드 기준으로 수행. muapi-cli 0.2.7 설치(venv, setup.sh 반영), `muapi image models` 103개 출력 ✅. muapi에 TTS 없음. 계정·키 없어 생성 검증 ❌, 웹 앱 빌드는 분류기 차단. ENV.md에 `MUAPI_API_KEY` 후보 행.
- **카드뉴스 프로젝트 분리(대표 결정)**: 협찬·광고 수익 목표, 별도 폴더·브랜치 `cardnews/main`이되 **관리는 이 COO 세션 하나가 통합**(docs/PROJECTS.md 현황판, 진입점은 루트 NEXT_PROMPT 하나), 문서 `cardnews/docs/`(PLAN·HANDOFF·NEXT_PROMPT). 본 채널 세션은 `cardnews/` 수정 금지. HANDOFF의 "인스타 캐러셀 2주 테스트" 항목은 그 프로젝트로 이관.
- MiniMax H3 `h3-prompt-writing` 스킬: 대표 요청으로 검토 → **설치 불가**(라이선스가 한국·미국·EU 제외, 출력물 표시도 금지). docs/SKILL_CANDIDATES.md에 기록. H3를 쓰려면 공식 API 약관 지역 조항을 legal-reviewer가 먼저 확인.
- `scripts/youtube_auth.py`: 대표 PC에서 1회 실행해 YOUTUBE_* 3개를 얻는 스크립트(미테스트, 실행은 대표 PC).

- **전략 결정(대표, 2026-10-01): 구독형 혼합.** 서사형 60~70% + 구매 의도형 30~40%, 게이트 = 90일 내 구독 1,000명 + 첫 제휴 매출 1건 + 월 비용 20만원. 수익 3겹(제휴→YPP 광고→멤버십). PLAN.md·CLAUDE.md·analyst.md 반영 완료. EP003부터 적용: 시리즈 기획(예: "한국이 금지했던 것들")과 건당 수수료 높은 제휴(여행·eSIM·숙소).

## 완료 (Phase 4, 성공 기준 5/5)
1. ep/EP002 writer: script.en.md S01~S13, 낭독문 1,580단어(wc -w 실측), 사실 18건 전부 F번호 출처, 금지 수치 0, 제휴 2개 S12에만, 고지·AI 라벨 낭독 포함. script.kr.md 1:1.
2. designer: 썸네일 3안 목업(WHO WROTE THESE? / 4 LETTERS VANISHED / WHY OCTOBER 9?) + scene-prompts S01~S13. marketer: 제목 5안, EN 설명란(첫 줄 고지), 태그 15, 숏폼 5개(42~55초), 캡션, 캐러셀 7장, 제휴 표(Amazon 4.5%/4.0%).
3. legal v1: BLOCK 0 / FIX 5 / PASS 8, 사실 주장 45건 중 출처 없음 0. COO가 FIX 8(AI 라벨 "사람이 검수" 문구 삭제)·FIX 6(S07 한 문장)·S11 과거형을 반영 → v1.1 FIX 3.
4. PR #2 생성, 업로드 0건, publish.log 기록.
5. EP001 publish.log에 Phase 4 게이트 STOP 추가(ep/EP001 ebffb9f).

## 실패한 시도와 이유 / 주의
- writer 서브에이전트는 Bash가 없어 단어 수를 수기 집계 → COO가 `wc -w`로 실측해 메타 표 교체(1,590→1,580).
- 대본 S04 폐지 4자 유니코드 오기(ㆁ U+3181, ㅿ U+317F, ㆆ U+3186, ㆍ U+318D가 맞음) → COO 수정. WenQuanYi Zen Hei는 4자 글리프 지원, 최종 KR 폰트는 설치 후 확인.
- AI 라벨에 "written and fact-checked by a human editor"는 대표 검수 기록 없이는 불성립(EP001과 같은 기준) → 두 편 모두 "generated with AI"로 축소. 검수 기록이 PR에 남으면 재삽입 검토.
- F11(1938~42 식민기 탄압)은 2차 출처 미확보로 대본에서 제외. KR 재개 전 S09 1문장 추가 권고.
- 병렬 작업은 `.worktrees/ep001`, `.worktrees/ep002`(git worktree, `.git/info/exclude`)로 분리. 새 세션은 새로 클론하므로 다시 만든다.
- GitHub MCP: 라벨은 `list_pull_requests fields=[labels]`(빈 배열이면 키 자체가 빠짐) + `search_pull_requests label:approved`로 교차 확인.

## 대표 결정 대기
1. ~~PR #1·#2 승인~~ 완료. 이제 업로드를 막는 건 키와 Amazon 계정뿐
2. **공급자 선택**(TOOLING_TTS_IMAGE.md 1안 또는 가성비안) → 키 입력: TTS_API_KEY·IMAGE_API_KEY(+ 선택 MUAPI_API_KEY), YOUTUBE_* 3개(scripts/youtube_auth.py). ElevenLabs면 elevenlabs-tts 설치. muapi 계정은 대표가 사이트에서 가입(OTP 메일)
3. Amazon Associates 가입·트래킹 ID(가입 후 180일 내 3건 판매 조건 → 첫 업로드 직전 권장), 제휴 상품 확정(EP001 멀티팩·양은냄비, EP002 워크북·붓펜), 링크 허브
4. EP002 썸네일 1안 "WHO WROTE THESE?" 유지 여부, F11 식민기 1문장 추가 여부
5. (이월) ~~인스타 캐러셀 2주 테스트~~(카드뉴스 프로젝트로 이관), risk #9 publisher 게이트 확장, 지정 폰트 setup.sh 추가, PLAN.md 비진정성 정책 날짜 정정, PLAN.md 결정 1~4, 보류 스킬 nano-banana·ScrapeCreators

## 다음 할 일 (Phase 5 — 승인·키 대기 처리 + EP003 기획)
1. PR #1·#2는 approved. 새 코멘트만 확인 → 키 SET이면 바로 EP001·EP002 real 렌더 → legal FIX 5 재판정 → FIX 7(링크)까지 끝나면 publisher 비공개 업로드.
2. 키 SET이면 EP001(승인 시 EP002도) producer real 렌더 → render-log → legal FIX 5 재판정 → 게이트 충족 시 publisher 비공개 업로드.
3. EP003 기획(구독형 혼합 기준): 서사형 시리즈 1편 또는 구매 의도형 1편을 researcher가 제안(소재 10개, 시리즈 묶음 가능성·건당 수수료 높은 제휴 후보 표시) → research.md → ep/EP003 분기.
4. (여유 시) analyst 주간 리포트 템플릿을 reports/에 1회 돌려 보기(데이터 0이라 형식 확인만).
