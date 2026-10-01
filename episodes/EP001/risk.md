# EP001 리스크 점검: "Why Ramyeon Keeps Showing Up on Korean Screens"

**v2 재점검 2026-10-01** (v1 수정 요청 #1·#4·#5·#7 반영분을 실제 파일에서 확인했다. 커밋 b8f25ad·b42a64a·49349f5는 COO가 알려 준 해시이고, 내용은 파일에서 직접 대조했다)

**BLOCK 0 / FIX 3 / PASS 7** (8개 항목 중 1번을 1a·1b·1c로 나눠 10행으로 셈. v1은 BLOCK 1 / FIX 5 / PASS 4)
**판정: 대표가 승인해도 된다. 다만 업로드는 FIX 3건(쿠팡 문구 공식 대조, 최종 에셋과 라이선스 기록, 실제 제휴 링크와 계정)을 끝낸 뒤에만 한다.**

> **법률 자문이 아니라 사전 점검이다.** 최종 판단은 대표와 전문가가 한다.
> 점검: legal-reviewer / 브랜치 ep/EP001 / 기준 문서: `.claude/agents/legal-reviewer.md` 1~8번, `docs/PLAN.md` "리스크", CLAUDE.md
> 대상 파일: research.md, script.en.md, script.kr.md, design/(design-system.md, thumbnails.md, scene-prompts.md, thumb-1~3.png, thumbs-compare.png), marketing.md
> 판정 기준: **BLOCK** = 콘텐츠 자체에 결함이 있어 대표가 승인하면 안 됨 / **FIX** = 승인은 가능하지만 업로드 전에 조치가 필요함(담당자와 시점 명시) / **PASS** = 문제 없음
> 줄 번호는 v2 시점 파일 기준이다. EN = script.en.md, KR = script.kr.md, M = marketing.md

## 1. 체크리스트

| # | 항목 | 판정 | 근거(한 줄) | 조치: 담당 / 시점 |
|---|---|---|---|---|
| 1a | 설명란 첫 줄 제휴 고지 (EN, "commission") | PASS | M:41 첫 줄에 "...affiliate links. I may earn a commission..."가 있다. 고정 댓글(M:142)과 숏폼 5 캡션(M:211~212)도 첫머리에 고지한다. Amazon 필수 문장은 M:45에 있다 | 문구 개선은 §5 권고 1 참고 |
| 1b | 설명란 첫 줄 제휴 고지 (KR, 쿠팡 지정 문구) | FIX | M:73·M:155의 문구는 제3자 자료와만 일치하고 공식 원문은 확인하지 못했다(§3). 이 문구가 이제 KR 대본 네 곳(KR:33, :126, :132, :145)과 자막 고정 두 곳(KR:37, :150)에 들어간다. S11 하단 바(KR:134)만 줄인 변형이다 | 대표: 쿠팡 링크를 만들 때 파트너스 로그인 화면의 안내 문구와 한 글자씩 대조 → 다르면 marketer·writer가 설명란·고정 댓글·S02·S11·S12 낭독·자막을 공식 문구로 한꺼번에 바꾼다(KR:15에 절차가 적혀 있다) / 업로드 전 |
| 1c | 영상 안 고지 위치 (KR판) | PASS (해결됨) | 고지가 시작에 있다: S02 첫머리 낭독(KR:33)과 그 구간 하단 자막 고정(KR:37). 끝에도 있다: S12 낭독(KR:145)과 마지막 프레임까지 자막 고정(KR:150). 반복도 된다: S11 앞뒤(KR:126, :132). 공정위 동영상 기준인 "시작 부분과 끝부분 + 반복"(§4)을 충족한다 | 참고: 첫 고지는 약 15초 훅(S01) 뒤에 나온다. 첫 프레임부터 덮으려면 KR 업로드 때 유료 프로모션을 체크한다(M:129, 대표 판단). §5 권고 9 |
| 2 | 협찬 여부와 유료 광고 표시 | PASS | 협찬 계약이나 무상 제공이 없다(M:29 "협찬 아님", M:129). 수익은 제휴 수수료뿐이고 농심·GS25·CU 언급은 사실 서술이다 | KR 업로드 때 유료 프로모션 체크를 권고한다. 이미 M:129 메모에 들어가 있다 |
| 3 | 민감 주제 제외, 효능·건강 주장 없음 | PASS | 건강·금융·법률 주제가 아니다. 냄비 관련 문장은 "heats up fast"([F20], EN:136) 하나이고, 안전·건강 표현 금지가 EN:144에 적혀 있다. 수출 수치는 투자 조언이 아니다 | 참고: 인용 출처 S26에는 알루미늄 용출 보도도 들어 있다(research.md:88). 댓글에 답할 때도 건강 주장은 하지 않는다 |
| 4 | 비진정성 3유형 해당 없음 | PASS | 서사가 고유하고, 사실과 해석을 구분해 썼다(EN:16). 제목 5안(M:26~30)과 썸네일 3안에 낚시가 없다. 민감 주제 AI 페르소나도 없다 | 참고: AI 이미지와 AI 음성으로 만든 영상이라 "image slideshow with minimal narrative"로 보이지 않게 모션과 편집을 유지한다(producer) |
| 5 | 저작권: 이미지, 음악·보이스, 드라마 장면 | FIX | v1과 같다. 목업 3장에는 로고·실존 인물·스틸이 없다. 하지만 최종 AI 플레이트는 아직 만들지 않았다(thumbnails.md:4, scene-prompts.md:4). 생성 기록 표도 비어 있다(scene-prompts.md:210~212). TTS·음악 공급자와 라이선스도 정해지지 않았다(HANDOFF.md:33, ENV.md:16) | designer·producer: 생성할 때 모델·날짜·시드·라이선스를 기록하고, 렌더 로그에 TTS·음악 라이선스 출처를 남긴다 → legal-reviewer가 최종 이미지를 재점검한다 / 렌더 후 업로드 전 |
| 6 | 사실 주장에 출처 있음 | PASS (해결됨) | 감사 39건 가운데 출처 없는 주장은 0건이다(§2). Sources 블록에 S22(M:104), S25(M:106), S1(M:107)이 추가됐다. 그래서 고정 댓글 "Every number ... has a source in the description"(M:150)도 이제 성립한다. 라면 라이브러리가 2026년에도 운영 중인지도 확인됐다(research.md:73~74, S42·S44는 원문을 직접 대조) | — |
| 7 | 제휴 약관 (Amazon 오프라인 금지, 쿠팡 가격 표기 등) | FIX | v1과 같다. 오프라인 금지(M:122)와 가격 미표기(M:49, :123)는 Amazon Program Policies(2026-04-14)와 맞는다. 그러나 링크가 전부 자리표시자이고(M:7) 상품도 아직 가안이다(EN:13). 쿠팡 subId 형식과 채널 등록도 확인되지 않았다(M:119, :125) | 대표: 상품 지정, 계정 링크 생성, 쿠팡 활동 채널(YouTube·허브) 등록, Associates Central 사이트 등록 여부 확인 / marketer: 실제 링크로 교체하고 허브 맨 위에 고지(M:126) / 업로드 전 |
| 8 | AI 생성물 공개 라벨 | PASS (해결됨) | 사실 검수를 단정하던 문장을 EN·KR 모두에서 뺐다(M:65, :85, 기록 :130). 공개 라벨은 설명란, S12 낭독·자막(EN:154, KR:147), 숏폼 마지막 1초와 캡션에 남아 있다. YouTube 합성 콘텐츠 토글은 비사실적 일러스트이고 실존 인물이 나오지 않아 필수는 아니다(§4, M:128 질문에 대한 답). 켜도 문제없다 | 체크리스트와 별개로, CLAUDE.md의 "인간 검수 기록" 규칙은 대표가 PR을 검수·승인할 때 남긴다. 기록이 남으면 M:130에 따라 그 문장을 다시 넣을 수 있다 |

## 2. 사실 주장 감사 (성공 기준 4)

범위: script.en.md, script.kr.md, marketing.md(제목, 설명란, 고정 댓글, 숏폼 훅·캡션, 캐러셀, §6.5 수수료). EN·KR·마케팅에 같은 내용이 여러 번 나오면 1건으로 셌다. v2에서 C21 판정을 바꾸고 C39를 새로 넣었다.

| # | 주장 요약 | 위치 | 분류 |
|---|---|---|---|
| C01 | 2001년 영화, "라면 먹을래요?" 대사 | EN·KR S01/S03, M:171, :192, :252 | 출처 있음 F7 |
| C02 | 대사가 "더 있다 가라"는 초대가 됨 | EN·KR S01/S03, M:27, :192, :252 | 출처 있음 F7 |
| C03 | 허진호 감독, 이영애·유지태 배역 | EN·KR S03, M:191~192 | 출처 있음 F7 |
| C04 | 2026년 3월, 25년 만의 재회 발표 | EN·KR S03 | 출처 있음 F7 |
| C05 | 2024년 1인당 79.2개 (WINA) | EN·KR S04, M:255 | 출처 있음 F14 |
| C06 | 베트남 81개에 이어 세계 2위 | EN·KR S04, M:255 | 출처 있음 F14 |
| C07 | 주 약 1.5개 (79.2÷52) | EN·KR S04, M:255 | 출처 있음 F14 (계산값) |
| C08 | 짜파구리 = 짜파게티+너구리 (기생충, 2019) | EN·KR S05/S11, M:197, :253 | 출처 있음 F9 |
| C09 | 달시 파켓이 'ram-don'을 만듦 | EN·KR S02/S05, M:172, :197, :253 | 출처 있음 F9 |
| C10 | 2020.2.10~11 GS25 약 60% 증가 | EN·KR S05, M:47, :197, :256 | 출처 있음 F10 |
| C11 | KPDH는 넷플릭스 역대 최다 시청 영화 | EN·KR S02/S06, M:173 | 출처 있음 F13 |
| C12 | 영화 초반 헌트릭스 3인이 컵라면을 먹음 | EN·KR S06, M:202, :254 | 출처 있음 F11 |
| C13 | 농심 한정 1,000세트, 2025.8.28 예약 | EN·KR S06, M:202, :254 | 출처 있음 F11 |
| C14 | 2025년 7~8월 CU 외국인 결제 +185% | EN·KR S06, M:202, :256 | 출처 있음 F12 |
| C15 | 라면 +99%, 김밥 +231% (김밥 1위) | EN·KR S06 (KR:86) | 출처 있음 F12 |
| C16 | 한강 라면은 나 혼자 산다·런닝맨으로 알려짐 | EN·KR S07 | 출처 있음 F17 (S22, M:104) |
| C17 | 한강 라면은 관광객의 대표 K-푸드 체험 | EN·KR S07, M:207 | 출처 있음 F17 (S23) |
| C18 | CU 라면 라이브러리 홍대 1호, 2023.12 | EN·KR S08, M:207 | 출처 있음 F19 |
| C19 | 2024년 200종 이상, 즉석 조리기 | EN·KR S08, M:207 | 출처 있음 F19 |
| C20 | 외국인 매출 비중 약 65~68% (2024) | EN·KR S08 (KR:100) | 출처 있음 F19 (S24·S25, M:105~106) |
| C21 | 라면 라이브러리가 지금도 운영 중 ("visit") | EN·KR S08 현재형, M:174 | 출처 있음 S43·S44·S45 (v1: "미검증" 표시됨 → v2 변경) |
| C22 | 2025년 라면 수출 첫 15억 달러, 약 22% 증가 | EN·KR S09, M:47 | 출처 있음 F15 |
| C23 | 2026년 상반기 9억3,539만 달러, 28% 증가, 반기 최대 | EN·KR S09 | 출처 있음 F16 |
| C24 | 신라면 1986년 10월 출시, 이번 달 40주년 | EN·KR S02/S10, M:11, :47 | 출처 있음 F1 (S1, M:107) |
| C25 | 소고기 장국에서 착안해 국물 설계 | EN·KR S10 | 출처 있음 F2 (단일, M:107) |
| C26 | 1991~2025년 35년 연속 국내 1위 | EN·KR S10 | 출처 있음 F3 |
| C27 | 2025년 말 누적 약 425억 봉 | EN·KR S10 | 출처 있음 F4 |
| C28 | 100여 개국 판매 | EN·KR S10 | 출처 있음 F5 |
| C29 | 누적 약 20조 원 중 약 40%가 해외 | EN·KR S10 | 출처 있음 F5 |
| C30 | 신라면 로제는 소비자 레시피에서 착안 | EN·KR S10 | 출처 있음 F6 |
| C31 | 로제, 2026년 5월 한국·일본 먼저 출시 | EN·KR S10 | 출처 있음 F6 |
| C32 | 게임스컴 2026 쾰른 '신라면 공장' 부스 | EN·KR S10 | 출처 있음 F20 |
| C33 | 양은냄비는 한국의 대표 라면 냄비 | EN·KR S11, M:175, :211~212 | 출처 있음 F20 |
| C34 | 실제로는 알루미늄, 이름은 옛 합금 '양은' | EN·KR S11, M:175, :212 | 출처 있음 F20 |
| C35 | 열이 빨리 올라 라면용으로 씀 | EN·KR S11 (EN:136) | 출처 있음 F20 (△) |
| C36 | 세 작품 = 영화 3편 (애니메이션 1편 포함) | 썸네일 3, M:28, :251 | 출처 있음 F7·F9·F11 |
| C37 | Amazon 수수료 Grocery 1%, Kitchen 4.5% | M:236~237 | 출처 있음 S39 URL |
| C38 | 쿠팡 수수료 3% | M:238~239 | "미검증" 표시됨 (추정치) |
| C39 | 홍대점이 지금도 있다 (현재형 캡션) | M:207 "there's CU's Ramyeon Library in Hongdae" | 출처 있음 S42 (단일) + S44 (지역 단위) |

**집계: 총 39 / 출처 있음 38 / "미검증" 표시됨 1 / 출처 없음 0.** 출처 없음이 0건이라 BLOCK 사유는 없다.

리스크 담당 원문 대조 (2026-10-01 WebFetch)
- C15: [ANN/Korea Herald 2025-09-16](https://asianews.network/south-koreas-largest-convenience-store-chain-cu-sees-185-jump-in-foreign-sales-on-kpop-demon-hunters-buzz/)에 김밥 231%, 간편식 143%, 라면 99%가 나온다. KR:86 "1등은 김밥"은 기사에 나온 품목 기준으로 맞다.
- C16: [Korea Times 2024-02-01](https://www.koreatimes.co.kr/www/culture/2024/09/135_368003.html)에 "variety shows 'Home Alone' and 'Running Man'"이 있다('나 혼자 산다'의 다른 영문 제목). 이 URL은 이제 Sources 블록 M:104에 있다.
- C20: [KOCIS 2024-05-03](https://www.mcst.go.kr/english/policy/kocis/newsView.jsp?pSeq=219)은 "about 65 percent", [JoongAng 2024-08-06](https://www.koreajoongangdaily.com/business/cu-cooks-up-expansion-of-ramyeon-libraries-nationwide/12063729)은 "68 percent"다. 두 URL 모두 Sources 블록에 있다(M:105~106). 참고로 Korea Times 2024-02는 62%라고 보도했다(§5 권고 4).
- C21: [데일리안 2026-07-27](https://www.dailian.co.kr/news/view/1670592/%E2%80%9C%ED%8E%B8%EC%9D%98%EC%A0%90-%EC%B0%8D%EA%B3%A0-%EA%B0%84%EB%8B%A4%E2%80%9D%EC%99%B8%EA%B5%AD%EC%9D%B8-%ED%8E%B8%EC%9D%98%EC%A0%90%EC%84%9C-2026)에 "CU는 ... 명동과 홍대, 인천공항 등을 중심으로 '라면 라이브러리'와 '스낵 라이브러리' 등 특화 점포를 운영"이라고 나온다.
- C39: [파이낸셜뉴스 2026-02-01](https://v.daum.net/v/20260201100306400)에 "지난달 30일 ... CU 홍대상상점 라면라이브러리에서" 방문 취재한 내용이 있다. 홍대점 하나만 다룬 2026년 근거는 이 1곳이다. S44는 "홍대"를 지역 단위로 언급한다.
- C11: 2026년 중반에도 최다 시청이라는 보도는 제3자 기사만 확인했고 Netflix 공식 자료는 확인하지 못했다. 업로드 직전에 다시 확인하기를 권고한다.

제작 과정 진술(사실 주장 집계에서 뺌): "No film or TV footage is used"(M:65, KR판 M:85)는 제작 규칙과 맞으므로 렌더 후 확인한다. 사람 검수 문장은 v2에서 삭제됐다.

## 3. 쿠팡파트너스 지정 고지 문구

- **결과: v1과 같다. 공식 원문을 확인하지 못해 FIX로 남긴다(1b).**
- 시도 1: partners.coupang.com WebFetch는 HTTP 403으로 막혔다.
- 시도 2: coupang.com·partners.coupang.com·news.coupang.com 도메인으로 한정해 검색했지만 고지 문구 안내 페이지는 나오지 않았다.
- 시도 3: 쿠팡 파트너스 공식 YouTube 가이드 재생목록(M:270)은 영상이라 문구 원문을 확인할 수 없었다.
- 제3자 자료에서만 확인한 것:
  - "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다." (M:73, :155, KR:33, :126, :132, :145에서 쓰는 문구)
  - [lilys.ai 요약](https://lilys.ai/ko/notes/youtube-shopping-shorts-20251128/coupang-partners-youtube-guide-disclosure): 크리에이터 영상(2025-09-23)을 요약한 페이지다. "쿠팡 관계자에게 문의했다"고 하지만 공식 링크는 없다. 쉼표 없는 형태를 쓴다.
  - "본 게시물은…" 변형은 검색 요약에서, "이 게시물은…" 변형은 M:269에서 나왔다.
- FIX로 남기는 이유: 공식 원문이 로그인 뒤에만 보이는 것으로 추정되고, 세 가지 변형이 함께 돌아다닌다. v2에서 이 문구가 KR 영상 안 여섯 곳(낭독 4 + 자막 고정 2)으로 늘었다. 그래서 대조 결과가 다르면 고칠 범위도 커진다. 일괄 교체 절차는 KR:15에 있다.
- 참고: 2024-12-01 시행 개정은 "'소정의 수수료를 지급받을 수 있음'과 같은 조건부·불확정적인 표현"을 불명확한 표시의 예로 추가했다([세종 2024-11-19](https://shinkim.com/kor/media/newsletter/2613)). 지금 KR 문구 "제공받습니다"는 확정 표현이라 이 점은 문제없다.

## 4. 정책·지침 근거 (확인한 출처만, v1과 같음)

- **YouTube 수익 창출 정책** ([공식 도움말 1311392](https://support.google.com/youtube/answer/1311392?hl=en))
  - Inauthentic content: "AI-generated content made with generic or unoriginal templates", "Image slideshows, templated storylines, or scrolling text with minimal narrative"
  - "AI Personas Related to Sensitive Topics" 섹션이 따로 있다.
  - "relies heavily on emotionally manipulative formulas"는 Unsatisfying or off-putting content 섹션에 있다.
  - 3유형의 내용은 공식 페이지에서 확인했다. 하지만 페이지에 표시된 최근 정책 날짜는 2025-07-15(명칭 변경)뿐이다. PLAN.md:37의 "2026-07-16 개정"이라는 날짜는 확인하지 못했다. COO가 PLAN 표기를 확인해야 한다(EP001 판정에는 영향 없음).
- **YouTube 합성 콘텐츠 공개** ([14328491](https://support.google.com/youtube/answer/14328491?hl=en))
  - 공개가 필요한 경우: 실존 인물이 하지 않은 말·행동을 한 것처럼 보이게 할 때, 실제 사건·장소 영상을 바꿀 때, 사실적인 가짜 장면을 만들 때
  - 필요 없는 경우: 명백히 비현실적인·애니메이션 콘텐츠, 대본·썸네일·인포그래픽에 생성형 AI를 생산성 도구로 쓸 때
- **YouTube 유료 프로모션** ([154235](https://support.google.com/youtube/answer/154235?hl=en))
  - "branded content, sponsorships, endorsements, or other commercial relationships"를 공개해야 한다.
  - 라벨은 "appears at the beginning of your video". 제휴 링크를 명시하지는 않는다.
  - 현지 법(KFTC 등) 준수는 크리에이터 책임이다.
- **공정위 추천·보증 심사지침**
  - 공식 보도자료: [2020-06-23 개정](https://www.korea.kr/briefing/pressReleaseView.do?newsId=156397064)(2020-09-01 시행), [2024-11-15 개정](https://www.korea.kr/briefing/pressReleaseView.do?newsId=156660604)(2024-12-01 시행). 본문이 hwp·pdf 첨부라 원문은 열어 보지 못했다.
  - 동영상 기준은 법무법인 해설로 확인했다. [지평 2020-08-26](https://jipyong.com/kr/board/news_view.php?seq=9615): "게시물 제목 또는 시작 부분과 끝부분에 삽입하고, 방송의 일부만을 시청하는 소비자도 ... 반복적으로 표시"
  - AI 가상인물 표시 의무 개정안: [세종 2026-04-15](https://shinkim.com/kor/media/newsletter/pdf/3230)에서 행정예고(2026-04-08~28 의견수렴)를 확인했다. 확정·시행일(2026-07-01이라는 검색 요약)은 확인하지 못했다.
- **미국 FTC Endorsement Guides FAQ** ([ftc.gov](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking))
  - 영상 안에 고지하는 것이 가장 좋고, 설명란만으로는 놓치기 쉽다.
  - "Viewers are more likely to miss a disclosure at the end of the video", 여러 번 고지하면 더 좋다.
  - 문구 예: "I get commissions for purchases made through links in this post"
  - EN판 S11의 고지(EN:134, :140, 구간 내내 하단 바 :143)는 추천하는 지점에 고지한 것이라 이 기준에 맞는다.
- **Amazon Associates**
  - [Program Policies 2026-04-14 갱신](https://affiliate-program.amazon.com/help/operating/policies): 오프라인(printed material, ebook, mailing, oral solicitation) 금지. 가격은 Amazon이 제공한 링크나 API로 받은 값만 쓰고 시각을 표시해야 한다.
  - [Operating Agreement 2025-10-15 갱신](https://affiliate-program.amazon.com/help/operating/agreement): "As an Amazon Associate I earn from qualifying purchases"를 명확하고 눈에 띄게 표시해야 한다.

## 5. 권고 (판정에 넣지 않음, v2 기준 아직 반영 안 됨)

1. EN 고지 "I may earn a commission"을 "I earn a commission on purchases made through these links"로 바꾸기를 권고한다(M:41, :142, :211~212, EN:134, :140, :143). FTC 예시와 같고, 공정위 2024 개정의 조건부 표현 예시도 피할 수 있다.
2. EN판도 S02에 고지를 한 줄 넣기를 권고한다. KR판과 구조가 같아지고, FTC도 시작 부분을 선호한다. 국내 지침이 EN판에 적용될 가능성은 낮다고 보지만, 적용되면 v1의 1c와 같은 결함이 된다.
3. S11 하단 바에 "AI voice"를 함께 표시하기를 권고한다. AI 음성이 1인칭으로 상품을 소개하는 구간이라, 가상인물 개정이 확정될 때를 대비하는 것이다.
4. S08 "65 to 68 percent"(KR:100은 "65~68%")를 "about two-thirds"로 바꾸기를 권고한다. 같은 해에 62%라는 보도도 있다.
5. 화면 텍스트와 캡션의 그룹명은 공식 표기(HUNTR/X로 알려짐, 제3자 자료)를 확인한 뒤 쓴다(M:180).
6. 제목 4에 브랜드명 "Shin Ramyun"이 들어간다. 이 제목을 쓴다면 설명란에 "Not sponsored by any brand mentioned." 한 줄을 넣는 것을 고려한다.
7. S06 플레이트(창가 카운터의 컵 3개, scene-prompts.md:102~104)는 생성한 뒤 원작 장면과 구도가 비슷하지 않은지 비교한다.
8. KR판을 (b) 방식(EN 영상에 한국어 설명란만 붙이기, M:127)으로 가는 것은 권하지 않는다. v2에서 넣은 KR 영상 안 고지가 빠지게 된다.
9. 1c를 가장 엄격하게 읽는다면 S02 고지 문장을 S01 맨 앞으로 옮기거나, KR 업로드 때 유료 프로모션을 체크해 첫 프레임 라벨을 붙인다.

## 6. 수정 요청

| # | v1 판정 | 파일 | 무엇을 | 담당 직원 | v2 상태 |
|---|---|---|---|---|---|
| 1 | BLOCK (1c) | script.kr.md S02·S12, marketing.md §2.4 | 시작과 끝에 쿠팡 고지 낭독 + 자막 추가(S11 유지), KR 유료 프로모션 메모 | writer, marketer | **해결됨(커밋 b8f25ad·b42a64a)**: KR:33, :37, :145, :150, M:129에서 확인 |
| 2 | FIX (1b) | M §2.2·§4 KR, KR S02·S11·S12 낭독·자막 | 파트너스 공식 안내 문구와 한 글자씩 대조한 뒤 그대로 반영 | 대표(대조) → marketer, writer | **미해결**: 쿠팡 링크를 만들 때, 업로드 전 |
| 3 | FIX (5) | design/thumbnails.md, design/scene-prompts.md 생성 기록, 렌더 로그 | 최종 플레이트 생성(모델·날짜·시드·라이선스 기록), TTS·음악 상용 라이선스 출처 기록, 최종 이미지 재점검 | designer, producer → legal-reviewer | **미해결**: 렌더 후, 업로드 전 |
| 4 | FIX (6) | M §2.3 Sources 블록 | S22, S25, S1 URL 추가 | marketer | **해결됨(커밋 b42a64a)**: M:104, :106, :107에서 확인 |
| 5 | FIX (6) | research.md, EN·KR S08, M §5 컷 4 | 라면 라이브러리 2026년 운영 확인. 확인하지 못하면 문구 교체 | researcher → writer, marketer | **해결됨(커밋 49349f5)**: research.md:73~74(S42~S47). 대본은 바꾸지 않았는데 그 근거(EN:15, KR:16)가 타당하다고 본다. S42·S44는 원문을 대조했다 |
| 6 | FIX (7) | M §2.1·§2.2·§4·§6.5 | 상품 지정, 실제 링크와 트래킹 ID·subId로 교체, 쿠팡 활동 채널 등록, Associates 사이트 등록 확인, 링크 허브를 만들고 맨 위에 고지 | 대표(계정·지정) → marketer | **미해결**: 업로드 전 |
| 7 | FIX (8) | M:65, :85 | 사람 사실 검수 문장 삭제(또는 PR에 검수 기록) | 대표 → marketer | **해결됨(커밋 b42a64a)**: 문장 삭제를 M:65, :85, :130에서 확인 |
