# EP001 리스크 점검: "Why Ramyeon Keeps Showing Up on Korean Screens"

**BLOCK 1 / FIX 5 / PASS 4** (8개 항목 중 1번을 1a·1b·1c로 나눠 10행으로 셈)
**판정: 지금 상태로는 승인 불가.** KR판은 영상 안에서 쿠팡 고지가 시작과 끝에 나오지 않아 BLOCK이다(1c). EN판에는 BLOCK이 없고 FIX 5건만 업로드 전에 처리하면 된다. KR판 대본을 고치거나 KR판을 이번 범위에서 빼면 BLOCK은 0이 된다.

> **법률 자문이 아니라 사전 점검이다.** 최종 판단은 대표와 전문가가 한다.
> 점검: legal-reviewer / 기준일 2026-10-01 / 브랜치 ep/EP001 / 기준 문서: `.claude/agents/legal-reviewer.md` 1~8번, `docs/PLAN.md` "리스크", CLAUDE.md
> 대상 파일: research.md, script.en.md, script.kr.md, design/(design-system.md, thumbnails.md, scene-prompts.md, thumb-1~3.png, thumbs-compare.png), marketing.md
> 판정 기준: **BLOCK** = 콘텐츠 자체에 결함이 있어 대표가 승인하면 안 됨 / **FIX** = 승인은 가능하지만 업로드 전에 조치가 필요함(담당자와 시점 명시) / **PASS** = 문제 없음

## 1. 체크리스트

| # | 항목 | 판정 | 근거(한 줄) | 조치: 담당 / 시점 |
|---|---|---|---|---|
| 1a | 설명란 첫 줄 제휴 고지 (EN, "commission") | PASS | marketing.md:41 첫 줄에 "...affiliate links. I may earn a commission..."가 있다. 고정 댓글(:137)과 숏폼 5 캡션(:206~207)도 첫머리에 고지한다. Amazon 필수 문장도 :45에 있다 | 문구 개선은 §5 권고 1 참고 |
| 1b | 설명란 첫 줄 제휴 고지 (KR, 쿠팡 지정 문구) | FIX | marketing.md:73 문구는 제3자 자료와만 일치하고 공식 원문은 확인하지 못했다(§3). "이 포스팅은 / 이 게시물은 / 본 게시물은" 세 가지 변형이 돌아다니고 쉼표 유무도 다르다 | 대표: 쿠팡 링크를 만들 때 파트너스 로그인 화면의 안내 문구와 한 글자씩 대조 → marketer·writer: marketing.md §2.2·§4, script.kr.md S11 낭독·자막에 그대로 반영 / 업로드 전 |
| 1c | 영상 안 고지 위치 (KR판) | **BLOCK** | 고지는 S11 앞뒤 낭독뿐이다(script.kr.md:121, :127). 하단 자막도 S11 구간에만 있다(:129). 공정위 심사지침은 동영상에 대해 "제목 또는 시작 부분과 끝부분에 넣고 반복 표시"를 요구한다(§4). 설명란은 '더보기' 안이라 이를 대신하지 못한다 | writer: S01 또는 S02 끝, 그리고 S12 끝에 쿠팡 고지를 낭독하고 자막도 넣는다. S11은 그대로 둔다 → legal-reviewer 재점검 / PR 승인 전. 아니면 KR판을 이번 범위에서 뺀다(COO·대표 결정) |
| 2 | 협찬 여부와 유료 광고 표시 | PASS | 협찬 계약이나 무상 제공이 없다(marketing.md:29 "협찬 아님"). 수익은 제휴 수수료뿐이고 농심·GS25·CU 언급은 사실 서술이다 | KR판을 올리면 YouTube "유료 프로모션 포함"도 체크하기를 권고한다. 이 체크를 하면 영상 시작에 라벨이 뜬다(§4) |
| 3 | 민감 주제 제외, 효능·건강 주장 없음 | PASS | 건강·금융·법률 주제가 아니다. 냄비 관련 문장은 "heats up fast"([F20], script.en.md:135) 하나이고, 안전·건강 표현 금지가 :143에 적혀 있다. 수출 수치는 투자 조언이 아니다 | 참고: 인용 출처 S26에는 알루미늄 용출 보도도 들어 있다(research.md:85). 댓글에 답할 때도 건강 주장은 하지 않는다 |
| 4 | 비진정성 3유형 해당 없음 | PASS | 서사가 고유하고, 사실과 해석을 구분해 썼다(script.en.md:15). 제목 5안(marketing.md:26~30)과 썸네일 3안에 낚시가 없다. 민감 주제 AI 페르소나도 없다 | 참고: AI 이미지와 AI 음성으로 만든 영상이라 "image slideshow with minimal narrative"로 보이지 않게 모션과 편집을 유지한다(producer) |
| 5 | 저작권: 이미지, 음악·보이스, 드라마 장면 | FIX | 목업 3장을 직접 봤고 로고·실존 인물·스틸은 없다. 대사는 한 줄을 텍스트로만 인용한다. 하지만 최종 AI 플레이트는 아직 만들지 않았다(thumbnails.md:4, scene-prompts.md:4). 생성 기록 표도 비어 있다(scene-prompts.md:210~212). TTS·음악 공급자와 라이선스도 정해지지 않았다(HANDOFF.md:33, ENV.md:16) | designer·producer: 생성할 때 모델·날짜·시드·라이선스를 기록하고, 렌더 로그에 TTS·음악 라이선스 출처를 남긴다 → legal-reviewer가 최종 이미지를 재점검한다 / 렌더 후 업로드 전 |
| 6 | 사실 주장에 출처 있음 | FIX | 감사 38건 가운데 출처 없는 주장은 0건이다(§2). 다만 공개 Sources 블록(marketing.md:93~108)에 URL 3개가 빠져 있다. 그래서 고정 댓글의 "Every number in the video has a source in the description"(:145)은 지금은 사실이 아니다. 라면 라이브러리가 2026년에도 운영 중인지도 확인하지 못했다 | marketer: Sources 블록에 S22·S25·S1 URL을 추가한다(§6-4) / researcher: 운영 여부를 확인하고, 확인하지 못하면 writer·marketer가 S08 현재형과 숏폼 4 훅을 바꾼다 / 업로드 전 |
| 7 | 제휴 약관 (Amazon 오프라인 금지, 쿠팡 가격 표기 등) | FIX | 오프라인 금지(marketing.md:119)와 가격 미표기(:49, :120)는 Amazon Program Policies(2026-04-14)와 맞는다. 그러나 링크가 전부 자리표시자이고(:7) 상품도 아직 가안이다(script.en.md:13). 쿠팡 채널 등록과 subId 형식도 확인되지 않았다(:116, :122) | 대표: 상품 지정, 계정 링크 생성, 쿠팡 활동 채널(YouTube·허브) 등록, Associates Central 사이트 등록 여부 확인 / marketer: 실제 링크로 교체하고 허브 맨 위에 고지 / 업로드 전 |
| 8 | AI 생성물 공개 라벨 | FIX | 공개 라벨은 설명란(marketing.md:65, :85), S12 낭독·자막(script.en.md:153, script.kr.md:140), 숏폼 마지막 1초와 캡션에 있다. 그런데 설명란 마지막 문장 "the facts were reviewed by a person before publishing"은 사람이 검수한 기록이 없으면 사실이 아니다. 지금은 그 기록이 없다 | 대표: 사실 검수 후 PR에 누가·언제 했는지 기록 / 기록이 없으면 marketer가 그 문장을 지운다 / 업로드 전. YouTube 합성 콘텐츠 토글은 비사실적 일러스트이고 실존 인물이 나오지 않아 필수는 아니다(§4). 켜도 문제없다 |

## 2. 사실 주장 감사 (성공 기준 4)

범위: script.en.md, script.kr.md, marketing.md(제목, 설명란, 고정 댓글, 숏폼 훅·캡션, 캐러셀, §6.5 수수료). EN·KR·마케팅에 같은 내용이 여러 번 나오면 1건으로 셌다. 위치 표기: EN = script.en.md, KR = script.kr.md, M = marketing.md 줄 번호.

| # | 주장 요약 | 위치 | 분류 |
|---|---|---|---|
| C01 | 2001년 영화, "라면 먹을래요?" 대사 | EN·KR S01/S03, M:166, :187, :247 | 출처 있음 F7 |
| C02 | 대사가 "더 있다 가라"는 초대가 됨 | EN·KR S01/S03, M:27, :187, :247 | 출처 있음 F7 |
| C03 | 허진호 감독, 이영애·유지태 배역 | EN·KR S03, M:186~187 | 출처 있음 F7 |
| C04 | 2026년 3월, 25년 만의 재회 발표 | EN·KR S03 | 출처 있음 F7 |
| C05 | 2024년 1인당 79.2개 (WINA) | EN·KR S04, M:250 | 출처 있음 F14 |
| C06 | 베트남 81개에 이어 세계 2위 | EN·KR S04, M:250 | 출처 있음 F14 |
| C07 | 주 약 1.5개 (79.2÷52) | EN·KR S04, M:250 | 출처 있음 F14 (계산값) |
| C08 | 짜파구리 = 짜파게티+너구리 (기생충, 2019) | EN·KR S05/S11, M:192, :248 | 출처 있음 F9 |
| C09 | 달시 파켓이 'ram-don'을 만듦 | EN·KR S02/S05, M:167, :192, :248 | 출처 있음 F9 |
| C10 | 2020.2.10~11 GS25 약 60% 증가 | EN·KR S05, M:47, :192, :251 | 출처 있음 F10 |
| C11 | KPDH는 넷플릭스 역대 최다 시청 영화 | EN·KR S02/S06, M:168 | 출처 있음 F13 |
| C12 | 영화 초반 헌트릭스 3인이 컵라면을 먹음 | EN·KR S06, M:197, :249 | 출처 있음 F11 |
| C13 | 농심 한정 1,000세트, 2025.8.28 예약 | EN·KR S06, M:197, :249 | 출처 있음 F11 |
| C14 | 2025년 7~8월 CU 외국인 결제 +185% | EN·KR S06, M:197, :251 | 출처 있음 F12 |
| C15 | 라면 +99%, 김밥 +231% (김밥 1위) | EN·KR S06 (KR:81) | 출처 있음 F12 |
| C16 | 한강 라면은 나 혼자 산다·런닝맨으로 알려짐 | EN·KR S07 | 출처 있음 F17 (S22) |
| C17 | 한강 라면은 관광객의 대표 K-푸드 체험 | EN·KR S07, M:202 | 출처 있음 F17 (S23) |
| C18 | CU 라면 라이브러리 홍대 1호, 2023.12 | EN·KR S08, M:202 | 출처 있음 F19 |
| C19 | 2024년 200종 이상, 즉석 조리기 | EN·KR S08, M:202 | 출처 있음 F19 |
| C20 | 외국인 매출 비중 약 65~68% (2024) | EN·KR S08 | 출처 있음 F19 |
| C21 | 라면 라이브러리가 지금도 운영 중 ("visit") | EN·KR S08 현재형, M:169 | "미검증" 표시됨 (M:176) |
| C22 | 2025년 라면 수출 첫 15억 달러, 약 22% 증가 | EN·KR S09, M:47 | 출처 있음 F15 |
| C23 | 2026년 상반기 9억3,539만 달러, 28% 증가, 반기 최대 | EN·KR S09 | 출처 있음 F16 |
| C24 | 신라면 1986년 10월 출시, 이번 달 40주년 | EN·KR S02/S10, M:11, :47 | 출처 있음 F1 |
| C25 | 소고기 장국에서 착안해 국물 설계 | EN·KR S10 | 출처 있음 F2 (단일) |
| C26 | 1991~2025년 35년 연속 국내 1위 | EN·KR S10 | 출처 있음 F3 |
| C27 | 2025년 말 누적 약 425억 봉 | EN·KR S10 | 출처 있음 F4 |
| C28 | 100여 개국 판매 | EN·KR S10 | 출처 있음 F5 |
| C29 | 누적 약 20조 원 중 약 40%가 해외 | EN·KR S10 | 출처 있음 F5 |
| C30 | 신라면 로제는 소비자 레시피에서 착안 | EN·KR S10 | 출처 있음 F6 |
| C31 | 로제, 2026년 5월 한국·일본 먼저 출시 | EN·KR S10 | 출처 있음 F6 |
| C32 | 게임스컴 2026 쾰른 '신라면 공장' 부스 | EN·KR S10 | 출처 있음 F20 |
| C33 | 양은냄비는 한국의 대표 라면 냄비 | EN·KR S11, M:170, :206~207 | 출처 있음 F20 |
| C34 | 실제로는 알루미늄, 이름은 옛 합금 '양은' | EN·KR S11, M:170, :207 | 출처 있음 F20 |
| C35 | 열이 빨리 올라 라면용으로 씀 | EN·KR S11 | 출처 있음 F20 (△) |
| C36 | 세 작품 = 영화 3편 (애니메이션 1편 포함) | 썸네일 3, M:28, :246 | 출처 있음 F7·F9·F11 |
| C37 | Amazon 수수료 Grocery 1%, Kitchen 4.5% | M:231~232 | 출처 있음 S39 URL |
| C38 | 쿠팡 수수료 3% | M:233~234 | "미검증" 표시됨 (추정치) |

**집계: 총 38 / 출처 있음 36 / "미검증" 표시됨 2 / 출처 없음 0.** 출처 없음이 0건이라 BLOCK 사유는 없다.

리스크 담당 원문 대조 (2026-10-01 WebFetch)
- C15: [ANN/Korea Herald 2025-09-16](https://asianews.network/south-koreas-largest-convenience-store-chain-cu-sees-185-jump-in-foreign-sales-on-kpop-demon-hunters-buzz/)에 김밥 231%, 간편식 143%, 라면 99%가 나온다. KR:81 "1등은 김밥"은 기사에 나온 품목 기준으로 맞다.
- C16: [Korea Times 2024-02-01](https://www.koreatimes.co.kr/www/culture/2024/09/135_368003.html)에 "variety shows 'Home Alone' and 'Running Man'"이 있다('나 혼자 산다'의 다른 영문 제목). 반면 설명란 Sources 블록에 올린 [MT 2026-08-31](https://www.mt.co.kr/en/living/2026/08/31/2026083111130096276)에는 예능 언급이 없다. 그래서 S22를 추가해야 한다.
- C19~C20: [KOCIS 2024-05-03](https://www.mcst.go.kr/english/policy/kocis/newsView.jsp?pSeq=219)은 "about 65 percent", [JoongAng 2024-08-06](https://www.koreajoongangdaily.com/business/cu-cooks-up-expansion-of-ramyeon-libraries-nationwide/12063729)은 "68 percent"다. 68%의 출처(S25)가 Sources 블록에 없다. 참고로 Korea Times 2024-02는 62%라고 보도했다(§5 권고 4).
- C11: 2026년 중반에도 최다 시청이라는 보도는 제3자 기사만 확인했고 Netflix 공식 자료는 확인하지 못했다. 업로드 직전에 다시 확인하기를 권고한다.

제작 과정 진술(사실 주장 집계에서 뺌): "No film or TV footage is used"(M:65)는 제작 규칙과 맞으므로 렌더 후 확인한다. "facts were reviewed by a person"(M:65, :85)은 1번 표 8행의 FIX다.

## 3. 쿠팡파트너스 지정 고지 문구

- **결과: 공식 원문을 확인하지 못해 FIX로 남긴다.**
- 시도 1: partners.coupang.com WebFetch는 HTTP 403으로 막혔다.
- 시도 2: coupang.com·partners.coupang.com·news.coupang.com 도메인으로 한정해 검색했지만 고지 문구 안내 페이지는 나오지 않았다.
- 시도 3: 쿠팡 파트너스 공식 YouTube 가이드 재생목록(marketing.md:265)은 영상이라 문구 원문을 확인할 수 없었다.
- 제3자 자료에서만 확인한 것:
  - "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다." (marketing.md:73에서 쓰는 문구)
  - [lilys.ai 요약](https://lilys.ai/ko/notes/youtube-shopping-shorts-20251128/coupang-partners-youtube-guide-disclosure): 크리에이터 영상(2025-09-23)을 요약한 페이지다. "쿠팡 관계자에게 문의했다"고 하지만 공식 링크는 없다. 쉼표 없는 형태를 쓰고, 설명란이나 고정 댓글 첫 줄에 두라고 안내한다.
  - "본 게시물은…" 변형은 검색 요약에서, "이 게시물은…" 변형은 marketing.md:264에서 나왔다.
- FIX로 남기는 이유: 공식 원문이 로그인 뒤에만 보이는 것으로 추정되고, 세 가지 변형이 함께 돌아다닌다. 대표가 파트너스에 로그인해 문구를 복사하면, 설명란·고정 댓글·S11 낭독·자막·허브에 한 글자도 바꾸지 않고 넣는다.
- 참고: 2024-12-01 시행 개정은 "'소정의 수수료를 지급받을 수 있음'과 같은 조건부·불확정적인 표현"을 불명확한 표시의 예로 추가했다([세종 2024-11-19](https://shinkim.com/kor/media/newsletter/2613)). 지금 KR 문구 "제공받습니다"는 확정 표현이라 이 점은 문제없다.

## 4. 정책·지침 근거 (확인한 출처만)

- **YouTube 수익 창출 정책** ([공식 도움말 1311392](https://support.google.com/youtube/answer/1311392?hl=en))
  - Inauthentic content: "AI-generated content made with generic or unoriginal templates", "Image slideshows, templated storylines, or scrolling text with minimal narrative"
  - "AI Personas Related to Sensitive Topics" 섹션이 따로 있다.
  - "relies heavily on emotionally manipulative formulas"는 Unsatisfying or off-putting content 섹션에 있다.
  - 3유형의 내용은 공식 페이지에서 확인했다. 하지만 페이지에 표시된 최근 정책 날짜는 2025-07-15(repetitious → inauthentic 명칭 변경)뿐이다. PLAN.md:37의 "2026-07-16 개정"이라는 날짜는 확인하지 못했다. COO가 PLAN 표기를 확인해야 한다(EP001 판정에는 영향 없음).
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
  - EN판 S11의 고지(상품 소개 직전·직후 낭독 + 구간 내내 하단 바)는 추천하는 지점에 고지한 것이라 이 기준에 맞는다.
- **Amazon Associates**
  - [Program Policies 2026-04-14 갱신](https://affiliate-program.amazon.com/help/operating/policies): 오프라인(printed material, ebook, mailing, oral solicitation) 금지. 가격은 Amazon이 제공한 링크나 API로 받은 값만 쓰고 시각을 표시해야 한다.
  - [Operating Agreement 2025-10-15 갱신](https://affiliate-program.amazon.com/help/operating/agreement): "As an Amazon Associate I earn from qualifying purchases"를 명확하고 눈에 띄게 표시해야 한다.

## 5. 권고 (판정에 넣지 않음)

1. EN 고지 "I may earn a commission"을 "I earn a commission on purchases made through these links"로 바꾸기를 권고한다. FTC 예시와 같고, 공정위 2024 개정의 조건부 표현 예시도 피할 수 있다(KE Studio는 국내 사업자다).
2. EN판도 S02에 고지를 한 줄 넣기를 권고한다. FTC는 시작 부분을 선호한다. 국내 지침이 EN판에 적용될 가능성은 낮다고 보지만 1c와 같은 결함이 될 수 있고, 고치는 비용이 작다.
3. S11 하단 바에 "AI voice"를 함께 표시하기를 권고한다. AI 음성이 1인칭("The one I've linked")으로 상품을 소개하는 구간이라, 가상인물 개정이 확정될 때를 대비하는 것이다.
4. S08 "roughly 65 to 68 percent"를 "about two-thirds"로 바꾸기를 권고한다. 같은 해에 62%라는 보도도 있다.
5. 화면 텍스트와 캡션의 그룹명은 공식 표기(HUNTR/X로 알려짐, 제3자 자료)를 확인한 뒤 쓴다(marketing.md:175).
6. 제목 4에 브랜드명 "Shin Ramyun"이 들어간다. 협찬으로 오해받을 가능성은 낮다. 이 제목을 쓴다면 설명란에 "Not sponsored by any brand mentioned." 한 줄을 넣는 것을 고려한다.
7. S06 플레이트(창가 카운터의 컵 3개, scene-prompts.md:102~104)는 생성한 뒤 원작 장면과 구도가 비슷하지 않은지 비교한다(design-system.md §6-4).
8. KR판을 (b) 방식(EN 영상에 한국어 설명란만 붙이기, marketing.md:124)으로 가는 것은 권하지 않는다. 쿠팡 링크는 붙는데 영상 안 쿠팡 고지가 없어진다.

## 6. 수정 요청

| # | 판정 | 파일 | 무엇을 | 담당 직원 |
|---|---|---|---|---|
| 1 | BLOCK (1c) | script.kr.md S01 또는 S02, S12 / marketing.md §2.4 | 시작과 끝에 쿠팡 고지 낭독 + 자막 추가(S11은 유지). KR 업로드 시 유료 프로모션 체크를 메모에 추가. 수정 후 재점검. KR판을 범위에서 빼면 해당 없음 | writer, marketer (범위 결정: COO·대표) |
| 2 | FIX (1b) | marketing.md §2.2·§4 KR, script.kr.md S11 낭독·자막 | 파트너스 공식 안내 문구와 한 글자씩 대조한 뒤 그대로 반영 | 대표(대조) → marketer, writer |
| 3 | FIX (5) | design/thumbnails.md, design/scene-prompts.md 생성 기록, 렌더 로그 | 최종 플레이트 생성(모델·날짜·시드·라이선스 기록), TTS·음악 상용 라이선스 출처 기록, 최종 이미지 재점검 | designer, producer → legal-reviewer |
| 4 | FIX (6) | marketing.md §2.3 Sources 블록 | Korea Times S22(예능 근거), JoongAng S25(68%), Wikipedia S1(F1·F2) URL 추가 | marketer |
| 5 | FIX (6) | script.en.md·script.kr.md S08, marketing.md §5 컷 4·§6.1 | 라면 라이브러리가 2026년에도 운영 중인지 확인. 확인하지 못하면 현재형 문장과 숏폼 4 훅(`RAMYEON ON THE HAN RIVER`)을 바꿈 | researcher(확인) → writer, marketer |
| 6 | FIX (7) | marketing.md §2.1·§2.2·§4·§6.5 | 상품 지정, 실제 링크와 트래킹 ID·subId로 교체, 쿠팡 활동 채널 등록, Associates 사이트 등록 확인, 링크 허브를 만들고 맨 위에 고지 | 대표(계정·지정) → marketer |
| 7 | FIX (8) | marketing.md:65, :85 | 사람이 사실 검수한 기록을 PR에 남김. 기록이 없으면 "facts were reviewed by a person..." 문장 삭제 | 대표(검수) → marketer |
