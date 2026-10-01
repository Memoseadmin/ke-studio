# EP002 리스크 점검 v1: "Korea Banned Its Own Alphabet: The 580-Year Fight for Hangul"

**v1 2026-10-01 (업로드 전 점검, EN만 업로드·KR판 보류)**

**v1.1 (COO 반영 후): BLOCK 0 / FIX 3(1b·5·7) / PASS 10** · v1: BLOCK 0 / FIX 5 / PASS 8 (9개 항목을 1a·1b·1c, 9a·9b·9c로 나눠 13행으로 셈)
**판정(v1): 대표가 승인해도 된다. BLOCK 0. 업로드는 FIX 5건(AI 라벨 문구, S07 한 문장, 최종 에셋·라이선스 기록, 실제 제휴 링크·계정, 쿠팡 문구는 KR 재개 시)을 끝내고, 목업이 아닌 real 렌더를 legal-reviewer가 재점검한 뒤에만 한다.** FIX 중 EN 업로드를 실제로 막는 것은 4건(1b는 KR 보류라 EN 비차단).

> **법률 자문이 아니라 사전 점검이다.** 최종 판단은 대표와 전문가가 한다.
> 점검: legal-reviewer / 브랜치 ep/EP002 / 기준 문서: `.claude/agents/legal-reviewer.md` 1~8번 + COO 추가 항목 9, `docs/PLAN.md` "리스크", CLAUDE.md
> 대상 파일: research.md(§3 F1~F20, §4), script.en.md(전문), script.kr.md(쿠팡 플레이스홀더·AI 고지만 grep), marketing.md(§1~§9), design/thumbnails.md(헤더·자가 점검·생성 기록), design/scene-prompts.md(공통 규칙·S05·생성 기록). 썸네일 목업 이미지 3장은 COO가 별도로 눈으로 확인한다(이 점검에서는 열지 않았다).
> 판정 기준: **BLOCK** = 콘텐츠 자체에 결함이 있어 대표가 승인하면 안 됨 / **FIX** = 승인은 가능하지만 업로드 전에 조치가 필요함(담당자와 시점 명시) / **PASS** = 문제 없음
> 줄 번호는 v1 시점 파일 기준. EN = script.en.md, KR = script.kr.md, M = marketing.md, R = research.md, TH = design/thumbnails.md, SP = design/scene-prompts.md

## 1. 체크리스트

| # | 항목 | 판정 | 근거(한 줄) | 조치: 담당 / 시점 |
|---|---|---|---|---|
| 1a | 설명란 첫 줄 제휴 고지 (EN, "commission") | PASS | M:42 첫 줄 "Disclosure: Some links below are affiliate links. I may earn a commission at no extra cost to you." 고정 댓글(M:164)과 숏폼 5 캡션 첫머리(M:238~239)도 같은 문장. Amazon 필수 문장은 M:46·M:170·M:238~239에 있다 | 문구 개선("may" 제거)은 §4 권고 1 |
| 1b | 설명란 첫 줄 제휴 고지 (KR, 쿠팡 지정 문구) | FIX (KR 재개 조건부, EN 비차단) | M:82·M:177의 "이 포스팅은 쿠팡 파트너스 활동의 일환으로…"는 공식 원문 미대조(M:99, M:305, EP001 §3과 같은 상태). KR 대본은 플레이스홀더 3곳(KR:38, :136, :154)과 자막 고정 3곳(KR:42, :142, :159)에 임시 문구 "이 영상의 설명란에는 제휴 링크가 포함되어 있으며, 구매 시 일정액의 수수료를 제공받습니다."를 두고 있다. 임시 문구는 "제공받습니다"로 확정 표현이라 공정위 2024 개정의 조건부 표현 문제는 없다 | 대표: 쿠팡 링크 생성 시 파트너스 안내 문구와 한 글자씩 대조 → marketer(M:82·177)·writer(KR 6곳) 일괄 교체 / KR 업로드 재개 시 |
| 1c | 영상 안 구두 고지 위치 (EN S12) | PASS | 상품 언급 직전 낭독(EN:153 "this channel earns a commission", 확정 표현) + S12 전 구간 하단 바(EN:160). FTC가 권하는 "영상 안, 추천 지점" 고지에 맞는다(§3). 숏폼 5는 낭독 대신 전 구간 고지 바 + 캡션 첫머리(M:208, :238~239)로 대체했고 링크 위치("in my profile")도 사실과 맞다 | 참고: 시작 부분 고지는 없다(EP001 EN과 같음). §4 권고 2 |
| 2 | 협찬 여부와 유료 광고 표시 | PASS | 협찬·무상 제공 없음(과제 명시, M:7). 수익은 제휴 수수료만. SBS 드라마·영화·국립한글박물관·세종시 한글런 언급은 사실 서술이고 브랜드명·상품 브랜드 없음(EN:14, EN:161, M:33). 유료 프로모션 체크는 제휴만 있는 EN판에서 필수가 아니다(§3) | — |
| 3 | 민감 주제 제외, 효능·학습 효과 주장 없음 | PASS | 건강·금융·법률 0(EN:20). "ten days"는 3곳 모두 해례본 인용으로 화자 특정 없이 쓰였다(EN:49 "the Haerye ... puts", EN:83 해석 단락 "anyone could learn in days", EN:151 "by the Haerye's own estimate"). S12에서는 인용 → "find out how long it takes you"(열린 질문) → 고지 단락 → 상품 단락 순으로 상품 문장과 분리됐고(EN:151~155), 고정 댓글이 "quoted, not a promise"를 명시한다(M:172). 숏폼 5·캐러셀은 "ten days" 자체를 뺐다(M:208, :242, :296). 태그 "learn hangul"은 효과 주장이 아니다(M:157) | 참고: 댓글 답변에서도 "며칠이면 배운다"류 약속은 하지 않는다 |
| 4 | 비진정성 3유형 해당 없음 | PASS | 고유 서사(사료 연대기 + 해석 문장을 "Here's my read / I think / to my ear"로 구분, EN:16). 제목 5안(M:26~30)은 전부 대본이 답하는 문장이고 2안은 괄호로 기간을 미리 밝힘. 썸네일 3안 문구(TH:11~13 `WHO WROTE THESE?` / `4 LETTERS VANISHED` / `WHY OCTOBER 9?`)에 Secret·Shocking류 없음. 숏폼 훅 5개는 연도·사실만(M:196~200). 민감 주제 AI 페르소나 없음 | 참고: 썸네일 1안의 질문은 영상이 "익명·불명"으로만 답한다 → §4 권고 5. AI 이미지+AI 음성이라 "image slideshow with minimal narrative"로 보이지 않게 모션 유지(producer, SP 모션 메모 다수) |
| 5 | 저작권: 초상·로고·스틜·해례본 실물·폰트·TTS·음악 | FIX | 설계는 문제없다: 세종 표준영정·광화문 동상·배우 전부 제외(EN:22, SP:10, TH:114), 드라마·영화는 텍스트 카드만(EN:53, SP:77), 해례본 실물 사진은 라이선스 확인 전 자체 일러스트(EN:22·133, SP:11, TH:119), 로고·국기 없음(TH:115·120, SP:12), 지도는 퍼블릭 도메인 Natural Earth 윤곽(SP:12·111·201), 목업 폰트 WenQuanYi는 목업 전용이고 번인 상업 이용 가능(TH:17, EP001 §7), 최종 폰트 Anton·Black Han Sans·Pretendard는 OFL(EP001 RL:41 확인). 그러나 업로드할 최종 에셋이 없다: 플레이트 미생성(TH:4, SP:4), 생성 기록 표 전부 공란(TH:128~133, SP:271~286), TTS 공급자 미정(ENV.md:16), 음악 미정, 폐지 4자용 대체 폰트(Noto Sans KR 등) 미확정(SP:9) | designer·producer: 생성 시 모델·날짜·시드·이용약관을 TH·SP 표에 기록, 렌더 로그에 TTS·음악·폰트(버전·출처, 4자 대체 폰트 포함) 라이선스 기록 → legal-reviewer가 최종 이미지·오디오 재점검 / 렌더 후 업로드 전 |
| 6 | 사실 주장에 출처 있음 | PASS (v1.1 해결됨) | 감사 45건 중 출처 없음 0건, 금지 수치 0건(§2). 단일 출처 F3·F7·F4·F9·F14는 메타 표(EN:17)대로 hedge가 붙어 있다. 예외 1건: EN:96 "No one at court was promoting it."은 F7(단일, "조정은 한자 중심으로 회귀")의 범위를 넘는 전칭 서술이고 hedge가 없다. 세조 간경도감 간행물·『용비어천가』 등 조정의 한글 간행 사례가 있어 역사에 밝은 시청자의 반박 여지가 있다 | writer: EN:96을 "The court was not promoting it." 또는 S13과 같은 "It had no official backing."으로 완화, KR 대응 문장 함께 / 렌더 전. 그 외 §4 권고 3(S11 전시 시제) |
| 7 | 제휴 약관 (Amazon 오프라인 금지, 가격 미표기, Associates 문장, 서브ID) | FIX | 규칙은 맞게 적혔다: 오프라인·이메일·PDF·QR 금지(M:76, :146), 가격 미표기(M:50 "Prices change, so none are listed here", EN:160), Associates 문장(M:46·170·238~239), 서브ID `ke-EP002-workbook/brushpen`·허브 UTM(M:139~145, EN:14). 그러나 링크가 전부 자리표시자(M:7, :43~45), 상품은 가안(EN:14), 트래킹 ID 미생성, Amazon 확정 자체가 대표 결정 대기(M:275)이고 확정 시 S12 낭독에 Associates 문장 추가가 조건부로 걸려 있다(EN:161, M:150). 수수료율은 검색 요약 확인이라 Associates Central 재확인 조건(M:301) | 대표: 상품 지정·Amazon 확정·트래킹 ID 생성·YouTube 채널과 허브 도메인의 Associates 사이트 등록 / marketer: 실제 링크 교체·허브 생성·허브 맨 위 고지(M:149) / writer: Amazon 확정 시 S12 문장 추가·단어 수 갱신 / 업로드 전 |
| 8 | AI 생성물 공개 라벨 | PASS (v1.1 해결됨) | 라벨 위치는 전부 있다: 설명란(M:67), S13 낭독(EN:172)·자막(EN:175, SP:254), 숏폼 마지막 1초 "AI voice & images"(M:192, :203), 캡션 15개·캐러셀 캡션(M:218~239, :293). 문제는 문구다. "the script was written and fact-checked by a human editor"(EN:15·172, M:67)와 자막 "human-written, fact-checked script"(EN:175, SP:254), KR 대응 문장(KR:17·156·158, M:94)은 두 가지를 단정한다. (a) "fact-checked by a human": 대표의 PR 검수 기록이 없으면 성립하지 않는다(EP001 §6 #7과 같은 기준, marketer도 M:75에서 조건부로 인정). (b) "written by a human": 대본은 writer 서브에이전트 산출(EN:3)이라 어떤 검수 기록으로도 뒷받침되지 않는다. 그대로 올리면 AI 고지 자체가 오해를 낳는다. YouTube 합성 콘텐츠 토글은 비사실적 일러스트·실존 인물 없음이라 필수는 아니고 켜도 문제없다(§3, M:151 질문에 대한 답) | writer·marketer·designer: 문장을 "The voice and images in this video were generated with AI."로 줄이고 자막은 "AI-generated voice & images"만 남긴다(EN:15·172·175, SP:254, M:67, KR:17·156·158, M:94). 대표가 PR 승인 시 사실 검수 기록을 남기면 "fact-checked by a human editor"만 조건부로 되살릴 수 있다. "written by a human"은 어떤 경우에도 넣지 않는다 / 렌더 전 |
| 9a | 추가 민감 축: 1444년 상소문 민족명 열거(S05, 숏폼 2) | PASS (댓글 운영 메모 수준) | 낭독은 "they wrote … in their logic"으로 상소문 화자에 귀속(EN:70), 자막은 따옴표(EN:75, SP:110), 지도 모션은 네 영역을 같은 색·크기로 처리하고 국경·국기 금지(SP:12·111), 숏폼 2 캡션은 민족명을 열거하지 않으며(M:205·241) 댓글이 한일·한중 비교로 흐르면 고정 댓글로 "1444년 상소문 인용"을 한 번 더 적기로 돼 있다(M:205). 고정 댓글 초안에 이미 "'Only barbarians' is the 1444 petition's phrase, quoted"가 있다(M:172). 대본 수정 불필요 | 참고: 숏폼은 무음·스크롤 시청이 많아 오버레이 따옴표만으로는 인용임이 약하다 → §4 권고 4(오버레이에 "— 1444 petition" 출처 표기) |
| 9b | 추가 민감 축: 일제강점기 서술 부재(F11 보류) | PASS | 1894→1912→1926→1940 구간에서 통치 상황을 말하지 않는 것은 "생략"이고 거짓 진술은 없어 "역사 왜곡" 비판의 근거가 약하다. 보류 사유가 사료 규율(단일 출처, R:87)이고 writer가 2차 출처 확보 시 넣을 1문장을 이미 준비했다(EN:18). 다만 S09 "a society of Korean language scholars, not a government"(EN:118)는 "왜 정부가 아니었나"를 시청자가 묻게 만드는 문장이라, 한국사에 밝은 시청자·KR판 재개 시에는 공백이 눈에 띈다 | 권고 수준: researcher가 F11 2차 출처를 확보하면 writer가 EN:18 준비 문장을 S09 끝에 추가(§4 권고 6). KR 재개 전에는 강하게 권고 |
| 9c | 추가 민감 축: 연산군 서술 | PASS | S06은 날짜·벽서·금지·역서 번역 지시(사료 기록, F6)만 쓰고 "Here's my read" 단락을 해석으로 표시(EN:81~85, :89). 처벌 조항(참수)은 단일 출처라 제외(EN:89). 제목·캡션·숏폼 1 오버레이에 "tyrant" 등 평가어 0건(M:33, :204, grep 확인) | — |

## 2. 사실 주장 감사

범위: script.en.md 낭독문 S01~S13 전부, marketing.md(제목 5안, 설명란 요약, 고정 댓글, 숏폼 훅·캡션, 캐러셀, §6.5 수수료), 썸네일 3안 문구. 같은 내용이 여러 곳에 나오면 1건. 해석 표시 문장("Here's my read / Here's the twist I like / to my ear / Notice the logic")은 사실 주장이 아니므로 세지 않았다. KR 대본은 EN과 같은 사실을 쓰므로 별도 집계하지 않았다(KR 보류).

| # | 주장 요약 | 위치 | 분류 |
|---|---|---|---|
| C01 | 1504년 여름, 수도에 왕을 비판하는 익명 벽서 3장 | EN S01/S06/S13, M:48, :218~220, TH 1안 | 출처 있음 F6 ✅ |
| C02 | 벽서는 한글, 조정이 약 60년 전 도입 | EN S02, M:219 | 출처 있음 F1·F6 ✅ (1446→1504 계산값, "roughly") |
| C03 | 오늘 한글은 국경일로 기념 | EN S02 | 출처 있음 F14 △ (시행연도 기준) |
| C04 | 2026 = 반포 580돌 + 한글날 100돌 | EN S02/S09/S11/S13, M:29, :48, :288 | 출처 있음 F16 ✅ |
| C05 | 1440년대 조선, 문자 = 한자 | EN S03 | 출처 있음 F1·F7 (배경 서술) |
| C06 | 1443년 세종이 28자를 조정에 제시 | EN S03, M:48, :224, :284 | 출처 있음 F1·F2 ✅ |
| C07 | 1446년 『훈민정음』으로 반포, 서명 영역 "Correct Sounds for the Instruction of the People" | EN S03, M:110 | 출처 있음 F1 ✅ |
| C08 | 서문(세종 귀속): 백성이 뜻을 펴지 못해 28자를 만들어 쉽게 익혀 날마다 쓰게 함 | EN S03/S04/S06 | 출처 있음 F3 단일 → hedge "attributed to / According to it" 있음 |
| C09 | 해례: 슬기로운 이 아침나절, 어리석은 이 열흘 | EN S03/S06/S12, M:172, :198, :285 | 출처 있음 F4 △ → hedge "the Haerye says / by the Haerye's own estimate" 있음, 화자 특정 없음 |
| C10 | 『뿌리깊은 나무』 SBS 2011, 『나랏말싸미』 2019, 극화 | EN S03 | 출처 있음 F19·F20 ✅ (배우 이름 없음) |
| C11 | 영화의 승려 협업 서사는 영화적 해석 | EN S03 | 출처 있음 F20 ✅ → hedge "cinematic interpretation, not settled history" 있음 |
| C12 | 28자 = 자음 17 + 모음 11 | EN S04, M:200, :284 | 출처 있음 F2 ✅ |
| C13 | 4자(ㆁ ㅿ ㆆ ㆍ) 폐지, 현대 24자 | EN S04/S12, M:28, :238~239, :287, TH 2안 | 출처 있음 F2 ✅ |
| C14 | 1444년 집현전 부제학 최만리 등 상소 | EN S05, M:48, :197, :224 | 출처 있음 F5 ✅ |
| C15 | 상소 논리: 제 글자는 오랑캐(몽골·여진·일본·티베트)만 가짐, 문명은 한자 | EN S05, M:48, :224~225 | 출처 있음 F5 ✅ (인용 표시) |
| C16 | 상소 2년 뒤 1446년 반포 | EN S05 | 출처 있음 F1·F5 ✅ (계산값) |
| C17 | 그 태도가 이후 400년 한글 대우를 규정 | EN S05/S13, M:224 | 출처 있음 F7·F8 (1446→1894 범위, 요약 서술) |
| C18 | 연산군, 1504-07-19 벽서 발견 | EN S06, M:204 오버레이 | 출처 있음 F6 ✅ |
| C19 | 금지: 학습·교육·사용 | EN S06, M:219 | 출처 있음 F6 ✅ |
| C20 | 같은 해 12월 역서 한글 번역 지시 → 약 5개월 만에 사실상 해제 | EN S06/S13, M:26~27, :48, :218~220, :286 | 출처 있음 F6 ✅ (계산값 "about five months") |
| C21 | 조정·관료는 대체로 한자 회귀, 별칭 '언문' | EN S07/S08, M:48 | 출처 있음 F7 단일 → hedge "mostly" 있음 |
| C22 | 초기 사용층은 주로 여성·불교계 | EN S07 | 출처 있음 F7 단일 → hedge "According to the historical accounts / mostly" 있음 |
| C23 | "No one at court was promoting it." | EN:96 | **출처 있음 F7 단일 — 범위 초과·hedge 없음** → §5 #2 |
| C24 | 1894년 11월 칙령: 공문서 국문 우선, 국한문 혼용 허용 | EN S08, M:48, :119 | 출처 있음 F8 ✅ (일자 미사용) |
| C25 | 448년 만에 처음 국가 공식 문자 | EN S08 | 출처 있음 F1·F8 ✅ (계산값) |
| C26 | 국문 = "national script" | EN S08 | 출처 있음 F8 ✅ |
| C27 | 1912년경 주시경이 '한글' 명명 | EN S09, M:48 | 출처 있음 F9 △ → hedge "around" 있음 |
| C28 | 한 = great, 글 = letters/writing | EN S09, M:121 | 출처 있음 F9 (어원 설명, 출처 표기대로) |
| C29 | '언문'→'한글' 약 20년(1894→1912경) | EN S09 | 출처 있음 F8·F9 (계산값 "roughly") |
| C30 | 1926년 조선어연구회(정부 아님)가 가갸날 제정 | EN S09, M:48, :122 | 출처 있음 F10 ✅ |
| C31 | 이후 한글날로 개칭 | EN S09 | 출처 있음 F10 ✅ (1928 미사용) |
| C32 | 해례본은 글자 설계 설명서, 수백 년간 현존 사본 불명 | EN S10, M:198, :229 | 출처 있음 F12 ✅ (1940 '발견'을 풀어 쓴 것) |
| C33 | 1940년 안동(경북) 발견, 전형필 소장 | EN S10, M:48, :228~230 | 출처 있음 F12 ✅ |
| C34 | 국보 70호(1962), 유네스코 세계기록유산(1997) | EN S10, M:228~229 | 출처 있음 F12 ✅ |
| C35 | 정인지 후서 "1446년 9월 상순" → 양력 환산 10월 9일 | EN S10, M:234, TH 3안 | 출처 있음 F13 ✅ (환산 세부 미사용) |
| C36 | 1946년부터 10/9 고정 | EN S10, M:234 | 출처 있음 F13 ✅ |
| C37 | 공휴일 1949 지정 → 1991 제외 → 2013 복귀 | EN S11, M:48, :233~235 | 출처 있음 F14 △ → 시행연도 기준 표기 |
| C38 | 2026 = 훈맹정음(한글 점자, 1926) 100돌 | EN S11 | 출처 있음 F16 ✅ |
| C39 | 10/9 광화문광장 한글 축제 | EN S11 | 출처 있음 F17 ✅ (시제: 10/9 이후 업로드면 과거형, EN:146) |
| C40 | 국립한글박물관 특별전 개최 중 | EN S11 | 출처 있음 F17 ✅ — 단, 개막일 미확인(R:93)인데 "is holding … for the occasion"이 10/9 시점 개최를 단정 → §4 권고 3 |
| C41 | 세종시 한글런, 같은 날, 10.9 km | EN S11 | 출처 있음 F18 ✅ |
| C42 | "Did Korea ban its own alphabet? Yes, for about five months in 1504." | EN S13, M:26~27, :48, :87 | 출처 있음 F6 ✅ |
| C43 | Amazon 수수료 Physical Books 4.50%, All Other 4.00% | M:266~267, :301 | 출처 있음 Associates 공식 URL (검색 요약 확인 → 지정 시 재확인 조건, M:301) |
| C44 | 쿠팡 수수료 3% | M:268~269 | "미검증" 표시됨 (추정치, KR 보류) |
| C45 | "Every date in the video has a source in the description" | M:172 | 출처 있음 — Sources 블록 24건이 팩트 출처 표 사용 F 18개의 URL 전부(M:105, :325)이고 C01~C42가 모두 F번호에 귀속되므로 성립 |

**집계: 총 45 / 출처 있음 44(그중 범위 초과·hedge 없음 1건 C23) / "미검증" 표시됨 1(C44) / 출처 없음 0.** 출처 없음 0건이라 BLOCK 사유는 없다.
**대본 금지 수치: 0건.** T11 "10년 만에 문해" 전언 미사용(EN:19), 전근대 문해율 숫자 없음(grep `literacy|literate|percent|%`: EN·M 낭독·캡션에 해당 없음, M의 %는 수수료율·썸네일 면적 비율만). "ten days"는 해례본 인용 3곳만(C09).

리스크 담당 메모(원문 대조는 하지 않았다, research ✅ 교차 확인에 의존)
- C23: F7 출처 요지는 "조정은 한자 중심으로 회귀"다. "아무도 조정에서 밀지 않았다"는 전칭은 세조 간경도감(1461~)의 불경 언해, 『용비어천가』·『월인천강지곡』 등 조정 주도 한글 간행 사례와 충돌한다. 1문장 완화로 해결되며 S13 "lived without official backing"(공식 문자 지위 기준)은 F8로 성립한다.
- C28: '한'의 뜻은 학계에서 '크다' 외에 '한(韓)'·'하나' 설도 있다. F9가 "한=크다"로 적었고 두 출처가 같으므로 출처 있음으로 두되, 댓글 반박이 오면 "one common reading"으로 답하면 된다. 대본 수정 요구는 아니다.
- C39~C41: 모두 2026 예고 기사 기반(F17·F18). 10/9 이후 업로드면 시제 교체(EN:21·146)가 사실 정확성 문제가 되므로 writer의 교체를 렌더 전 확인한다.

## 3. 정책·지침 근거 (EP001 risk.md §4, 103~129행 인용. 재조사 없음)

- **YouTube 수익 창출 정책(1311392)**: Inauthentic content = 템플릿 반복 AI 콘텐츠, 이미지 슬라이드쇼·서사 최소; "AI Personas Related to Sensitive Topics" 별도 섹션; 감정 조작 공식은 Unsatisfying content 섹션. EP002는 고유 사료 연대기 + 모션 설계라 해당 없음(1번 표 4). PLAN.md "2026-07-16 개정" 날짜 미확인 건은 EP001과 같이 COO 확인 사항.
- **YouTube 합성 콘텐츠 공개(14328491)**: 실존 인물의 가짜 언행, 실제 사건·장소 변조, 사실적 가짜 장면일 때 필수. EP002는 비사실적 일러스트, 실존 인물 초상 0, 실제 영상 변조 0 → 토글 필수 아님, 켜도 무방(1번 표 8).
- **YouTube 유료 프로모션(154235)**: branded content·sponsorship·endorsement 공개. 제휴 링크만 있는 EN판은 명시 대상이 아니고 라벨은 "appears at the beginning". 협찬 없음(1번 표 2).
- **미국 FTC Endorsement Guides FAQ**: 영상 안 고지가 최선, 끝부분 고지는 놓치기 쉬움, 문구 예 "I get commissions for purchases made through links". EN S12 낭독·하단 바(EN:153·160)와 숏폼 5 고지 바(M:208)가 이에 맞는다(1번 표 1c).
- **Amazon Associates**: Program Policies(2026-04-14) 오프라인·인쇄·이메일 금지, 가격은 API/링크 제공값만 + 시각 표시 → EP002는 가격 미표기(M:50). Operating Agreement(2025-10-15) "As an Amazon Associate I earn from qualifying purchases" 명확·눈에 띄게 → M:46·170·238~239. 소셜 프로필 링크 경로(숏폼 5)는 채널·허브를 Associates 사이트로 등록한 뒤 쓴다(EP001 §1 7 동일 조건).
- **공정위 추천·보증 심사지침(2020-09-01, 2024-12-01 시행)**: 동영상은 시작·끝 + 반복 표시, 조건부 표현("수수료를 지급받을 수 있음")은 불명확 표시 예. KR판 보류라 이번 판정에 쓰지 않았고, KR 재개 시 KR:38·136·154 3곳(시작·상품 직전·끝)이 이미 구조상 충족한다. AI 가상인물 표시 의무 개정안(2026-04 행정예고)은 확정·시행일 미확인 — KR 재개 전 재확인.
- **쿠팡파트너스 지정 문구**: EP001 §3과 같이 공식 원문 미확인(403·검색 불가), 변형 3종 유통. 1b FIX 사유.
- 이번 편에서 새로 조사한 정책은 없다. 광화문 세종대왕 동상(2009)·세종 표준영정(1973)은 저작권 보호 대상일 가능성이 있으나 EP002가 둘 다 쓰지 않으므로 법리 판단을 하지 않았다.

## 4. 권고 (판정에 넣지 않음)

1. EN 고지 "I may earn a commission"(M:42, :164, :238~239, :293)을 "I earn a commission on purchases made through these links"로. S12 낭독(EN:153)과 고지 바(EN:160)는 이미 확정 표현이라 설명란만 맞추면 전 채널이 같아진다(EP001 권고 1 승계).
2. EN판도 S02 끝("I'll show you the simplest way to try the alphabet yourself" 뒤)에 고지 한 문장을 넣으면 FTC가 선호하는 시작 부분 고지가 되고 KR판 구조(KR:38)와 같아진다(EP001 권고 2 승계).
3. EN:142 "the National Hangeul Museum is holding a special exhibition for the occasion" → "is holding a special exhibition this autumn". 개막일 미확인(R:93)이라 10/9 시점 개최 단정을 피한다. 10/9 이후 업로드 시 시제 교체(EN:146)와 함께 writer가 처리.
4. S05 오버레이 `"Mongols · Jurchens · Japanese · Tibetans"`(EN:75, SP:110)와 숏폼 2 같은 컷에 출처 표기 `— 1444 petition`을 덧붙인다. 무음·스크롤 시청에서 따옴표만으로는 인용임이 전달되지 않는다. 9a를 댓글 운영 메모 수준으로 둔 전제이기도 하다.
5. 썸네일 1안 `WHO WROTE THESE?`는 영상이 "익명, 신원 불명"으로만 답한다(EN:30·81). 영상 요지("누구든 쓸 수 있었다는 것이 문제")와 어긋나지 않아 FIX는 아니지만, 질문형 썸네일이 답을 주지 않는다는 지적이 가능하다. 기본안 제목 1과 짝지을 썸네일은 2안·3안을 먼저 고려하고, 1안을 쓰면 S06 "Here's my read" 단락이 사실상의 답이 되게 편집에서 강조한다(COO·designer).
6. researcher가 F11(1938 조선어 제한, 1942 조선어학회 사건) 2차 출처를 확보하면 writer가 EN:18의 준비 문장을 S09 끝에 넣는다. EN 업로드 조건은 아니나 KR 재개 전에는 강하게 권고한다(9b).
7. S12 하단 바(EN:160)에 "AI voice"를 함께 표시한다. AI 음성이 1인칭으로 상품을 소개하는 구간이라 공정위 가상인물 개정 확정에 대비한다(EP001 권고 3 승계).
8. 이름이 아닌 역사 인물 호칭 "the collector Jeon Hyeong-pil"(EN:129)은 사실 서술이라 문제없다. 다만 간송미술관 관련 소장품·전시 사진은 라이선스 확인 전까지 쓰지 않는다는 규칙(EN:22)을 최종 렌더에서도 유지한다.
9. 대본 S04 메모의 코드포인트 오기(EN:66 "ㆁ(U+318D) ㆆ(U+318E)")는 designer가 바로잡았다(TH:17, SP:9). 리스크 사항은 아니나 writer가 EN:66을 고쳐 두면 다음 편 재사용 시 혼선이 없다.
10. publisher 업로드 직전 확인에 "risk.md FIX 0건·real 렌더·MOCKUP 표기 없음·오디오 무음 아님"을 넣을지는 EP001 §6 #9(COO 결정 대기)와 같은 건이다. EP002도 같은 조건을 전제로 판정했다.

## 5. 수정 요청

| # | v1 판정 | 파일·행 | 무엇을 | 담당 직원 | 시점 |
|---|---|---|---|---|---|
| 1 | FIX (8) | EN:15·172·175, SP:254, M:67·75, KR:17·156·158, M:94 | AI 라벨에서 "written and fact-checked by a human editor" / "human-written, fact-checked script" / "대본은 사람이 쓰고 사실 확인을 했습니다" / "대본은 사람이 작성·검수"를 삭제. 남기는 문장: EN "The voice and images in this video were generated with AI." 자막 "AI-generated voice & images". KR "이 영상의 음성과 이미지는 AI로 생성했습니다." 대표가 PR 승인 시 사실 검수 기록을 남기면 "fact-checked by a human editor"만 조건부로 추가 가능. "written by a human"은 넣지 않는다. 단어 수·자막 길이 갱신 | writer(EN·KR), marketer(M), designer(SP:254 "한 글자도 변경 금지" 메모 포함 갱신) | 렌더 전 | **해결됨(v1.1, COO 2026-10-01)**: EN:15·172·175, SP:254, M:67·75·94, KR:17·156·158에서 "AI로 생성" 문장으로 축소 확인 |
| 2 | FIX (6) | EN:96, KR 대응 문장(S07) | "No one at court was promoting it." → "The court was not promoting it." 또는 "It had no official backing." F7 범위 안으로 완화 | writer | 렌더 전 | **해결됨(v1.1, COO 2026-10-01)**: EN:96 "It had no official backing." / KR:89 "공식적인 뒷받침은 없었습니다." |
| 3 | FIX (5) | TH:128~133, SP:271~286, 렌더 로그(생성 시) | 최종 플레이트 생성 시 모델·날짜·시드·해상도·이용약관·검수자 기록. TTS·음악 공급자와 상용 라이선스 출처, 최종 폰트 3종 + 폐지 4자 대체 폰트의 버전·출처를 렌더 로그에 기록 → legal-reviewer 최종 이미지·오디오 재점검 | designer, producer → legal-reviewer | 렌더 후, 업로드 전 |
| 4 | FIX (7) | M §2.1(:43~46)·§2.4·§4(:168~170)·§6.5(:266~270), EN S12(:157·161) | 대표: 상품 지정, Amazon 확정, Associates Central 트래킹 ID 2개 생성, YouTube 채널·허브 도메인 사이트 등록, 수수료율 재확인. marketer: 자리표시자를 실제 링크로 교체, 허브 생성과 맨 위 고지, 숏폼 5 캡션 링크 경로 확인. writer: Amazon 확정 시 S12 마지막 문장 뒤 "As an Amazon Associate I earn from qualifying purchases." 추가와 단어 수 갱신 | 대표 → marketer, writer | 업로드 전 |
| 5 | FIX (1b, KR 보류) | M:82·177·99, KR:38·42·136·142·154·159 | 쿠팡파트너스 공식 안내 문구와 한 글자씩 대조 후 설명란·고정 댓글·KR 낭독 3곳·자막 3곳 일괄 교체. 쿠팡 subId 하이픈·대문자 허용 여부(M:142)와 활동 채널 등록도 함께 확인 | 대표(대조) → marketer, writer | KR 업로드 재개 시(EN 비차단) |
| 6 | 권고 추적 (§4 3) | EN:142·146, KR 대응 문장 | 특별전 문장에 "this autumn" 추가, 10/9 이후 업로드 시 "hosts/is holding" 과거형 교체 | writer | 렌더 전 | **반영(v1.1)**: EN:142 "hosted … this autumn … there was", KR:127 "열렸고 … 올가을 … 열렸는데" |
| 7 | 권고 추적 (§4 4) | EN:75, SP:110, M:197·205(숏폼 2) | 민족명 오버레이에 `— 1444 petition` 출처 표기 추가 | writer → designer, marketer | 렌더 전 |
| 8 | 권고 추적 (§4 6) | R §3 F11, EN S09(:118 뒤), EN:18 | F11 2차 출처 확보 → S09 끝 1문장 추가(사실 나열만) | researcher → writer | KR 재개 전(EN은 선택) |
| 9 | 권고 추적 (§4 1·7) | M:42·164·238~239·293, EN:160 | "I may earn" → "I earn"; S12 하단 바에 "AI voice" 병기 | marketer, writer | 렌더 전(선택) |

FIX로 세는 것은 #1~#5(5건). #6~#9는 권고 추적이며 판정 집계에 넣지 않는다.


## 6. v1.1 (Phase 4, COO 반영 기록)

- 2026-10-01 COO가 §5 #1(FIX 8)·#2(FIX 6)·#6(권고 3)을 직접 반영하고 §1 행 6·8을 PASS로 올렸다. 변경 내용은 각 행에 기록. 남은 FIX는 1b(KR 재개 시)·5(real 렌더 후)·7(대표 계정·링크)이며 EP001과 같은 유형이다.
- v1.1은 COO 반영이므로 legal-reviewer 재판정은 real 렌더 후 FIX 5 재점검 때 함께 한다.
