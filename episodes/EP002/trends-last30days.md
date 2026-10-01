# EP002 트렌드 원자료 — last30days (2026-09-01 ~ 2026-10-01)

> 수집 원자료(raw evidence)다. EP002 유형은 **문화·역사 설명형**이라 역사·한글·전통문화·민속·사극·역사 명소 화제만 담았다. 수치는 수집 시점 값이며 이후 바뀔 수 있다. 아래 표의 항목은 모두 엔진 실행 결과에 실제로 나온 URL만 담았다. 엔진 결과 밖의 WebSearch 보강은 하지 않았다(리서처 몫).

## 1. 실행 메타

- 실행일: 2026-10-01 (UTC 07:46~08:00), 조사 기간 2026-09-01 ~ 2026-10-01
- 엔진: last30days **v3.26.0** (`.claude/skills/last30days-last30days/scripts/last30days.py`, 저장소 사본 그대로)
- 실행 환경: `LAST30DAYS_PYTHON=/usr/bin/python3.12`(3.12.3), `FROM_BROWSER=off`, `--no-browser-cookies`, `LAST30DAYS_NATIVE_SEARCH=1`, `--emit=compact`, `--plan <tmpfile>`, `--subreddits=…`, `--save-dir`는 세션 스크래치 디렉터리(저장소 밖). 호스트는 `CLAUDECODE=1`.
- 첫 실행 게이트: `~/.config/last30days/.env` 없음 → `FIRST_RUN_DETECTED`. 규칙상 셋업 마법사·쿠키 읽기·키 입력·`.env` 생성을 모두 하지 않고 키 없이 동작하는 소스만 썼다. 엔진은 `config_source: env_only`로 보고. 엔진이 스스로 `~/.config/last30days/doctor-cache.json`·`last-report.json`(캐시, 비밀값 없음)만 만들었고 `.env`는 생성되지 않았다.
- 사전 `doctor`(UTC 07:46:22, 라이브 프로브) 결과
  - **WORKING**: reddit(공개 키리스), youtube(yt-dlp 2026.08.19), hackernews, polymarket, github(gh 2.89.0)
  - **COULD BE ON(미설정, 미사용)**: x, web(엔진측), digg, techmeme, arxiv, trustpilot, amazon, meta_ads, tiktok, instagram, threads, telegram, bluesky, truthsocial, perplexity, linkedin, pinterest, xiaohongshu
  - `--diagnose` `available_sources` = reddit, youtube, hackernews, polymarket, github
- 사전 조사(Step 0.5/0.55): X 비활성이라 핸들 해석은 해당 없음. 서브레딧은 호스트 WebSearch 없이 지식으로 추론해 `--subreddits`로 넘겼고, 쿼리 플랜은 LAW 7대로 직접 작성(토픽당 서브쿼리 4개).
- 엔진 실행 **총 8회**, 엔진 보고 소요 합계 약 10분 38초(벽시계 07:47:08~07:59:46):

| # | topic (엔진 인자) | plan intent | 서브쿼리 | 대상 서브레딧 | 결과(기간 내 필터 전) | 소요 |
|---|---|---|---|---|---|---|
| 1 | Korean history explained | concept / evergreen_ok | 4개 작성, 엔진이 **2개만 실행** | korea, history, AskHistorians, Korean, KDRAMA, kdramas, KoreanHistory | Reddit 4 · YT 1 · HN 4 | 103s |
| 2 | Korean traditional culture | concept / evergreen_ok | 4개 작성, 엔진이 **2개만 실행** | korea, hanbok, KoreanFood, koreatravel, Korean, seoul, Hanguk | Reddit 3 · YT 4 · HN 4 | 60s |
| 3 | K-drama culture questions | concept / evergreen_ok | 2개 실행 | KDRAMA, kdramas, kdramarecommends, korea, Korean, AskAKorean, KoreanAdvice | Reddit 12 · YT 3 · HN 6 | 60s |
| 4 | Korea travel history sites | opinion / balanced_recent | 4개 실행 | koreatravel, korea, seoul, travel, solotravel, Busan, KoreaTravelTips | Reddit 19 · YT 0 · HN 10 | 42s |
| 5 | Hangul Korean alphabet | opinion / balanced_recent | 4개 실행 | Korean, korea, languagelearning, hangul, AskAKorean, linguistics, todayilearned | Reddit 13 · YT 6 · HN 4 | 88s |
| 6 | Korean mythology folklore | opinion / balanced_recent | 4개 실행 | korea, mythology, folklore, KDRAMA, kdramas, Paranormal, KpopDemonHunters | Reddit 11 · YT 2 · HN 4 | 112s |
| 7 | Korean history (1 재실행) | opinion / balanced_recent | 4개 실행 | korea, history, AskHistorians, Korean, KDRAMA, kdramas, todayilearned | Reddit 7 · YT 3 · HN 4 · PM 3 | 87s |
| 8 | Korean traditional culture hanbok hanok (2 재실행) | opinion / balanced_recent | 4개 실행 | korea, hanbok, KoreanFood, koreatravel, Korean, seoul, AskAKorean | Reddit 15 · YT 1 · HN 4 | 86s |

- 1·2회차는 `intent=concept, freshness_mode=evergreen_ok` 플랜을 넘기자 엔진 로그에 `subqueries=2`로 찍히며 뒤 2개 서브쿼리(사극·궁궐·음식 유래)가 실행되지 않았다. 같은 플랜을 `opinion / balanced_recent`로 바꿔 7·8회차로 재실행하니 4개 모두 실행됐다. 3회차도 2개만 실행됐으나 결과가 충분해 재실행하지 않았다.
- 6회는 선택 토픽으로 "Korean mythology folklore"를 골랐다(Chuseok은 EP001 자료에 이미 있음).

**source_status (8회 통합)**
- Reddit: **OK**. 공개 키리스 경로 + arctic-shift 보강으로 8회 모두 결과를 받았다(4 / 3 / 12 / 19 / 13 / 11 / 7 / 15건, 중복 포함). 다만 관련도 필터가 매 회 수백 건을 떨어뜨려 상위 노출은 적다.
- YouTube: **부분(partial)**. 검색은 되지만 (a) 검색 결과 대부분이 기간 밖(엔진 로그 "0 within date range, keeping all", 항목에 `[date:low]` 표시), (b) 자막·댓글 수집은 yt-dlp "Sign in to confirm you're not a bot"과 HTTP 429가 반복됐다. 기간 안 YouTube 항목은 8회 통틀어 4건이고 그중 2건(필리핀 애니 "Forgotten Island")은 무관해 뺐다.
- Hacker News: OK이나 전부 무관(북한 해킹·핵실험·경제 기사 등). 표에 넣지 않았다.
- Polymarket: 7회차에만 3건(시진핑-이재명 회담 93%, KBO 한국시리즈, USD/KRW). 전부 무관 또는 금융이라 제외.
- GitHub: 8회 모두 0건. Jobs: 8회 모두 **unreachable**(프록시 502 Bad Gateway, 엔진이 자동으로 붙인 소스라 무관).
- X / TikTok / Instagram / Threads / Bluesky: **skipped-unconfigured**. 자격증명이 필요해 규칙상 쓰지 않았다. 숏폼 플랫폼 신호는 이번 자료에 없다.
- 엔진측 web 검색: 끔(`LAST30DAYS_NATIVE_SEARCH=1`). 호스트 WebSearch는 쓰지 않았다.
- **제외 14건**(건강·금융·법률 주제, 중복 제거): 건강 2(병원 식단 글, "Illegal To Be Fat" 영상) / 금융 6(401k·Bitget 해킹 2건·연금 허점·USD/KRW 마켓·수출 기록) / 법률 6(개인정보 과징금, Cornell 소송 2건, Winston Lee 군복무, 영국 대법원 스파이웨어, 스토킹 추적). 그 외 무관 항목(북한 핵·해킹, 아시안게임 운영 논란, 재생에너지, 구축함, 솔로여행 일반 글 등)은 단순 미수록.

## 2. 수집 결과 (T1~T37)

### A. 역사 (고대~현대)

| # | 소스 | 제목 | 날짜 | 참여도 | 무엇이 화제인가 | URL |
|---|---|---|---|---|---|---|
| T1 | Reddit r/HistoryMemes | Korean war was wild | 2026-09-24 | 7,476 upvotes · 300 comments | 한국전쟁 밈 + OP가 올린 다큐. 댓글 u/CallMeGlarthir(312): "Korean war doesn't get the talk it should." 외국인에게 '잊힌 전쟁' 설명 수요 | https://www.reddit.com/r/HistoryMemes/comments/1wpcs18/korean_war_was_wild/ |
| T2 | Reddit r/todayilearned | TIL in 1504, King Yeonsangun of Joseon banned the use of Hangul… | 2026-09-14 | 765 upvotes · 43 comments | 연산군 한글 금지. 댓글 u/pleasurism_(197) "임시 금지, 익명 투서 범인 색출용", u/amievenrelevant(155) "세종 이후 왕실은 다시 한자로 돌아갔다". 3회 실행(1·5·7)에서 모두 등장 | https://www.reddit.com/r/todayilearned/comments/1wgfxx3/til_in_1504_king_yeonsangun_of_joseon_banned_the/ |
| T3 | Reddit r/todayilearned | TIl that in a 2014 poll, South Korean citizens voted the sinking of the MV Sewol as the second most important event in the country's history, beaten only by the Korean War | 2026-09-08 | 2,788 upvotes · 100 comments | 한국 현대사 인식. ⚠ 참사 소재라 설명형으로 쓰려면 톤 주의 | https://www.reddit.com/r/todayilearned/comments/1wap539/til_that_in_a_2014_poll_south_korean_citizens/ |
| T4 | Reddit r/HistoryAnimemes | Historical Figures Who Became Deities in Korean Shamanism | 2026-09-15 | 2,438 upvotes · 65 comments | 한국 무속에서 신이 된 역사 인물(맥아더 등). 댓글 u/Junjki_Tito(450) "MacArthur makes sense, but Joan of Arc?", 유관순 언급. 역사+민속 교차 훅 | https://www.reddit.com/r/HistoryAnimemes/comments/1wgn9x8/historical_figures_who_became_deities_in_korean/ |
| T5 | Reddit r/korea | How One War in 400 AD Redefined Armor Across the Entire Korean Peninsula (Silla, Gaya, and Baekje) | 2026-09-22 | 214 upvotes · 8 comments | 삼국·가야 갑옷 역사 설명 글 | https://www.reddit.com/r/korea/comments/1wnjuim/how_one_war_in_400_ad_redefined_armor_across_the/ |
| T6 | Reddit r/korea | Goguryeo, Baekje, Silla, Tang Dynasty \| Dubbed in Ancient Korean" | 2026-09-26 | 128 upvotes · 10 comments | 고대 한국어 더빙 영상 공유. 삼국시대 언어 호기심 | https://www.reddit.com/r/korea/comments/1wqilyj/goguryeo_baekje_silla_tang_dynasty_dubbed_in/ |
| T7 | Reddit r/AskHistorians | Did Korea's history of colonial resistance against Japan influence or impact South Korea's democratization movement?… | 2026-09-26 | 11 upvotes · 5 comments | 식민지 저항사와 민주화의 연결을 묻는 질문 | https://www.reddit.com/r/AskHistorians/comments/1wqf96a/did_koreas_history_of_colonial_resistance_against/ |
| T8 | YouTube Bedtime & Historian | The ENTIRE History of Korea \| How One Nation Became Two \| Korean History | 2026-09-06 | 66,135 views · 747 likes · 110 comments | 통사 설명 영상(자막 수집됨). 하이라이트: 빗살무늬토기(기원전 6000년경), 단군 신화(쑥과 마늘), 『삼국유사』(일연). 기간 내 유일한 한국사 설명 영상 | https://www.youtube.com/watch?v=UfBm6Mt3rjY |
| T9 | Reddit r/korea | Unlicensed Tour Guides Spread Historical Misinformation, Claiming "Joseon Kings Could Do Nothing Without the Chinese Emperor's Permission"… | 2026-09-12 | 639 upvotes · 89 comments | 궁궐 무자격 가이드의 역사 왜곡 논란. 댓글 u/amazinghadenMM(268). "조선은 중국 속국이었나" 바로잡기 수요. ⚠ 중국 관련 민감 | https://www.reddit.com/r/korea/comments/1weglsa/unlicensed_tour_guides_spread_historical/ |
| T10 | Reddit r/korea | Taiwanese taxi driver refuses Korean passengers, throws their luggage and calls them a "country of traitors". | 2026-09-30 | 459 upvotes · 164 comments | 댓글 u/Any-Tension-3808(234)이 1992년 한-대만 단교사를 설명. 현대 외교사 훅이나 ⚠ 정치·외교 민감 | https://www.reddit.com/r/korea/comments/1wukbnj/taiwanese_taxi_driver_refuses_korean_passengers/ |

### B. 한글 (10월 9일 한글날 시의성)

| # | 소스 | 제목 | 날짜 | 참여도 | 무엇이 화제인가 | URL |
|---|---|---|---|---|---|---|
| T11 | Reddit r/korea | It is true that Hangul came into widespread use after being invented by the king during the Joseon Dynasty; novels serve as evidence of this | 2026-09-30 | 67 upvotes · 20 comments | 한글 보급 시점 논쟁. u/masquedmarauderxyz(52) "10년 만에 문해" 전언, u/hidden-semi-markov(30) "전근대 문해율 추정은 틀렸다", u/brrkat(13) 연산군 처형 기록 인용. '한글 역사는 교과서보다 복잡하다' 각도 | https://www.reddit.com/r/korea/comments/1wu1l0p/it_is_true_that_hangul_came_into_widespread_use/ |
| T12 | Reddit r/coolguides | A cool guide for Korean alphabet, I wanted to let redditors know how to write "강남스타일"(Gangnam style)… | 2026-09-21 | 384 upvotes · 63 comments | 한글 자모 가이드 이미지. 비전공자 대상 '한글은 쉽다' 포맷 | https://www.reddit.com/r/coolguides/comments/1wmg2ds/a_cool_guide_for_korean_alphabet_i_wanted_to_let/ |
| T13 | Reddit r/Korean | How did you personally learn Hangul? | 2026-09-17 | 27 upvotes · 47 comments | 학습법 공유. u/the_sweetest_peach(21) Letslearnhangul.com, u/swordplay235(14) "플래시카드 1시간" | https://www.reddit.com/r/Korean/comments/1wiesv7/how_did_you_personally_learn_hangul/ |
| T14 | Reddit r/BeginnerKorean | hangul writing question | 2026-09-14 | 46 upvotes · 26 comments | ㅈ 손글씨 모양·획순 질문. 댓글 17·17 upvotes | https://www.reddit.com/r/BeginnerKorean/comments/1wgfu0k/hangul_writing_question/ |
| T15 | Reddit r/BeginnerKorean | I created a free interactive website to learn Hangul(Hangeul) through K-Food words and visual syllable building… | 2026-09-26 | 18 upvotes · 2 comments | K-푸드 단어로 한글 배우기(음식×한글 결합 포맷). 댓글은 AI 작성 의혹 | https://www.reddit.com/r/BeginnerKorean/comments/1wqi4hl/i_created_a_free_interactive_website_to_learn/ |
| T16 | Reddit r/AskAKorean | Do Korean kids struggle with differences between some letters when they're learning to speak/read/write? | 2026-09-02 | 27 comments | 한글 자모 혼동 질문(ㅐ/ㅔ 류 추정, 본문 미확인) | https://www.reddit.com/r/AskAKorean/comments/1w5eebb/do_korean_kids_struggle_with_differences_between/ |

기간 밖이라 표에서 뺀 한글 영상(수요 규모 참고용, 날짜는 업로드일): GO! Billy Korean "Learn Hangul in 90 Minutes" 2017-07-27, 9,290,701 views, 댓글 @AliKing-pg8pd(23,000 likes) "Y'all k pop lovers really dedicated to be learning a whole language", https://www.youtube.com/watch?v=s5aobqyEaMQ · Korean with Miss Vicky "Learn Hangeul in 30 minutes" 2019-07-16, 8,373,094 views, https://www.youtube.com/watch?v=85qJXvyFrIc · Real Korean with Morning "…Hangul in 10 Minutes" 2024-02-06, 4,113,759 views, https://www.youtube.com/watch?v=rBDrM1VPJX0 · Talk To Me In Korean "[1 hour] Full Hangeul Course" 2025-08-07, 1,023,791 views, https://www.youtube.com/watch?v=uNDf0V06m0w

### C. 전통문화·관습·정서

| # | 소스 | 제목 | 날짜 | 참여도 | 무엇이 화제인가 | URL |
|---|---|---|---|---|---|---|
| T17 | Reddit r/korea | Ansel Elgort Criticized for Yukata at Korean Event | 2026-09-04 | 690 upvotes · 155 comments | 한국 행사에 일본 유카타 착용 논란. u/Immediate-Pepper-516(550) "유카타는 평상복, 블랙타이 행사, 식민 역사". 한복 vs 기모노·유카타 구분 설명 수요. ⚠ 실존 인물 비판 소재 | https://www.reddit.com/r/korea/comments/1w7gboi/ansel_elgort_criticized_for_yukata_at_korean_event/ |
| T18 | Reddit r/korea | Chuseok in South Korea 30~40 years ago | 2026-09-25 | 1,626 upvotes · 51 comments | 옛 귀성길 사진. u/FunctionAlive(156) "5~6시간 차멀미", u/alexx3064(145) "할머니 음식이 그립다". EP001 자료 #19와 동일 글(수치 갱신) | https://www.reddit.com/r/korea/comments/1wps4xh/chuseok_in_south_korea_3040_years_ago/ |
| T19 | Reddit r/AskAKorean | Are there any Korean words that tells Korea's culture? | 2026-09-23 | 5 upvotes · 23 comments | 댓글: 눈치·재벌·흥·한·정·홧병·김치·전세 / "한이 역사를 가장 잘 보여준다" / 존댓말 체계와 "빨리빨리" / "안녕"의 어원. 문화 키워드 설명 영상 뼈대 | https://www.reddit.com/r/AskAKorean/comments/1wo5fsc/are_there_any_korean_words_that_tells_koreas/ |
| T20 | Reddit r/AskAKorean | What's Korean work culture actually like in 2026? | 2026-09-13 | 34 upvotes · 24 comments | 회식·야근 등 직장 문화 질문(K-드라마 관습 궁금증 계열) | https://www.reddit.com/r/AskAKorean/comments/1wflf3z/whats_korean_work_culture_actually_like_in_2026/ |
| T21 | Reddit r/AskAKorean | Is there a Korean equivalent for the word/concept of "ragebait?" | 2026-09-22 | 37 upvotes · 29 comments | 한국어 신조어·인터넷 문화 질문 | https://www.reddit.com/r/AskAKorean/comments/1wmy3pm/is_there_a_korean_equivalent_for_the_wordconcept/ |
| T22 | Reddit r/AskAKorean | Why is the perspective of Korean Americans toward Korea like this? | 2026-09-16 | 51 upvotes · 89 comments | 교포와 본국 인식 차이 토론 | https://www.reddit.com/r/AskAKorean/comments/1whxh1w/why_is_the_perspective_of_korean_americans_toward/ |
| T23 | Reddit r/AskAKorean | Korean-Canadians/Korean-Americans, what was it like growing up between two cultures? | 2026-09-10 | 16 upvotes · 38 comments | 디아스포라 정체성 토론 | https://www.reddit.com/r/AskAKorean/comments/1wco0qg/koreancanadianskoreanamericans_what_was_it_like/ |
| T24 | Reddit r/KoreanAdvice | Can you teach me more about my culture? | 2026-09-29 | 5 upvotes · 16 comments | 교포가 한국 문화를 배우고 싶다는 글. 댓글은 LoL·Faker 농담(25·23) | https://www.reddit.com/r/KoreanAdvice/comments/1wt3b7x/can_you_teach_me_more_about_my_culture/ |
| T25 | YouTube 쇼미코리아 | 아이 둘 데리고 전통 한옥에 묵은 미국 엄마 경악한 이유? | 2026-09-14 | 20,793 views · 139 likes · 3 comments | 외국인 가족 한옥 숙박 반응(한국어 채널). 기간 내 유일한 한옥 영상 | https://www.youtube.com/watch?v=stsOyTHJrWg |
| T26 | Reddit r/PokemonGoRaids | It's two Pikachus wearing Hanbok, a traditional Korean garment… | 2026-09-24 | 4 upvotes · 30 comments | 포켓몬 GO 한복 피카츄 이벤트. 한복이 글로벌 게임 소재로 쓰인 신호. ⚠ 브랜드 IP 이미지 사용 불가 | https://www.reddit.com/r/PokemonGoRaids/comments/1wovclt/its_two_pikachus_wearing_hanbok_a_traditional/ |

### D. 민속·신화

| # | 소스 | 제목 | 날짜 | 참여도 | 무엇이 화제인가 | URL |
|---|---|---|---|---|---|---|
| T27 | Reddit r/Paranormal | Thinking about the Hat Man. In Korean folklore, the traditional Jeoseung Saja. An interesting take.. | 2026-09-24 | 777 upvotes · 52 comments | 저승사자(갓 쓴 사자)와 서구 'Hat Man' 괴담 비교. 2회 실행(2·6)에서 모두 등장 | https://www.reddit.com/r/Paranormal/comments/1wovcxb/thinking_about_the_hat_man_in_korean_folklore_the/ |
| T28 | Reddit r/KDRAMA | SPOTLIGHT ON Fantasy and Korean Folklore - September, 2026 | 2026-09-02 | 20 upvotes · 3 comments | 서브레딧 공식 월간 주제가 '판타지와 한국 민속'. 도깨비·구미호 류 설명 수요의 간접 신호 | https://www.reddit.com/r/KDRAMA/comments/1w4vmq4/spotlight_on_fantasy_and_korean_folklore/ |
| T29 | Reddit r/ZZZ_Unhinged | Considering ZZZ takes a lot from Korean and Chinese mythology I feel like this book cover is basically a leak | 2026-09-07 | 8 upvotes · 1 comment | 게임(Zenless Zone Zero) 팬이 한국 신화 차용을 언급. 약한 신호 | https://www.reddit.com/r/ZZZ_Unhinged/comments/1w9zpwp/considering_zzz_takes_a_lot_from_korean_and/ |

(T4 무속 신격화 글도 이 묶음에 해당)

### E. 사극·K-드라마

| # | 소스 | 제목 | 날짜 | 참여도 | 무엇이 화제인가 | URL |
|---|---|---|---|---|---|---|
| T30 | Reddit r/kdramas | Lim Ji Yeon pulled me to watch My Royal Nemisis and i am its sets the bar for best 2026 drama really | 2026-09-30 | 69 upvotes · 33 comments | 2026년 신작 호평. 제목으로 보아 궁중 소재로 추정되나 장르·배경 미확인 | https://www.reddit.com/r/kdramas/comments/1wu9p2s/lim_ji_yeon_pulled_me_to_watch_my_royal_nemisis/ |
| T31 | Reddit r/kdramas | K/J - Drama: which version of Marry My Husband is better? | 2026-09-09 | 893 upvotes · 226 comments | 한국판 vs 일본 리메이크 비교. u/Nabinew(42) "일본판이 낫다", u/sempiterno000(27) "한국판 악역 커플이 압도". 한일 연출·문화 차이 설명 훅 | https://www.reddit.com/r/kdramas/comments/1wbth1g/kj_drama_which_version_of_marry_my_husband_is/ |
| T32 | Reddit r/kdramas | What's a K-drama you wish you could watch for the first time again? | 2026-09-24 | 947 upvotes · 563 comments | Crash Landing on You, My Mister 등. 고전 K-드라마 속 문화 코드 설명의 진입점 | https://www.reddit.com/r/kdramas/comments/1wovbht/whats_a_kdrama_you_wish_you_could_watch_for_the/ |
| T33 | Reddit r/KDRAMA | Winners Of The Seoul International Drama Awards 2026 | 2026-09-29 | 37 upvotes · 2 comments | 2026 서울드라마어워즈 수상작(수상작 명단 본문 미확인) | https://www.reddit.com/r/KDRAMA/comments/1wt94z3/winners_of_the_seoul_international_drama_awards/ |
| T34 | Reddit r/KDRAMA | K-Drama Day is HERE! | 2026-09-25 | 206 upvotes · 10 comments | 서브레딧 기념일 이벤트 | https://www.reddit.com/r/KDRAMA/comments/1wq1psz/kdrama_day_is_here/ |

### F. 여행·역사 명소

| # | 소스 | 제목 | 날짜 | 참여도 | 무엇이 화제인가 | URL |
|---|---|---|---|---|---|---|
| T35 | Reddit r/korea | I'm so glad I visited this exhibition during my trip to Korea! | 2026-09-28 | 225 upvotes · 8 comments | 여행 중 전시 관람 후기(전시명 본문 미확인) | https://www.reddit.com/r/korea/comments/1ws3ja4/im_so_glad_i_visited_this_exhibition_during_my/ |
| T36 | Reddit r/koreatravel | Looking for a knowledgeable Seoul guide focused on Korean history and religion | 2026-09-30 | 1 upvote · 10 comments | 역사·종교 전문 가이드 수요. 궁궐·사찰 설명 콘텐츠 수요의 직접 신호 | https://www.reddit.com/r/koreatravel/comments/1wu34wk/looking_for_a_knowledgeable_seoul_guide_focused/ |
| T37 | Reddit r/koreatravel | The people of South Korea generally are incredibly kind and hospitable | 2026-09-27 | 369 upvotes · 90 comments | u/sattlerreader(57) "한국인은 소통하려 애쓴다, 일본과 비교". 정(情) 설명과 연결 가능. 보조: "10 days in Korea as a Filipino Tourist" 2026-09-11, 333 upvotes · 55 comments, https://www.reddit.com/r/koreatravel/comments/1wdd5nk/10_days_in_korea_as_a_filipino_tourist/ | https://www.reddit.com/r/koreatravel/comments/1wrffkf/the_people_of_south_korea_generally_are/ |

경복궁·창덕궁·DMZ·경주·부산을 직접 다룬 글은 4회차 서브쿼리(palaces / dmz / gyeongju_busan)를 돌렸는데도 기간 내 결과에 없었다. 명소별 화제는 리서처가 별도 확인해야 한다.

## 3. 요약 관찰

- **한글날(10/9) 직전인데 한글 '역사 논쟁'이 살아 있다.** 연산군 한글 금지(T2, 765 upvotes, 3회 실행 모두 등장)와 한글 보급 시점 논쟁(T11)이 겹친다. 댓글이 이미 "세종 이후 왕실은 한자로 회귀", "임시 금지였다", "문해율 추정은 과장"처럼 교과서식 서사를 반박하고 있어, '한글은 발명 즉시 보급되지 않았다'는 역사 설명형 각도가 가능하다. 학습 쪽(T12~T15)은 꾸준하고, 기간 밖 한글 강의 영상이 100만~930만 뷰라 상시 수요가 크다(추정).
- **역사 쪽 최상위 참여는 한국전쟁(T1, 7,476)과 세월호 인식 조사(T3, 2,788)다.** 다만 T3는 참사 소재, T9·T10은 중국·대만 외교 민감 소재라 설명형으로 쓰려면 리스크 검토가 선행돼야 한다. 안전한 고대사 훅은 삼국 갑옷(T5)·고대 한국어 더빙(T6)·통사 영상(T8, 단군·삼국유사 언급)이다.
- **민속·무속이 역사와 교차하는 지점이 가장 '설명하고 싶은' 소재다.** 무속에서 신이 된 역사 인물(T4, 2,438)과 저승사자 vs Hat Man(T27, 777)은 서구 독자가 스스로 비교하며 질문하는 형태다. r/KDRAMA가 9월 주제를 '판타지와 한국 민속'으로 잡았고(T28), 게임 팬덤도 한국 신화 차용을 언급한다(T29). 도깨비·구미호·저승사자 설명은 사극·판타지 드라마와 자연스럽게 연결된다.
- **'한국 문화를 설명하는 단어' 질문이 그대로 대본 뼈대가 된다.** T19 댓글(눈치·한·정·흥·홧병·빨리빨리·존댓말·'안녕'의 뜻)과 직장 문화 질문(T20), 정(情)을 체감했다는 여행 후기(T37)가 서로 보강한다. 교포 정체성 글(T22~T24)은 "내 문화를 배우고 싶다"는 2차 수요를 보여준다.
- **복식·전통 공간 훅: 한복 vs 유카타 논란(T17, 690)과 한옥 숙박(T25).** T17은 실존 인물 비판이라 인물 언급 없이 '한복·기모노·유카타 구분' 설명으로만 쓰는 편이 안전하다. 한복 피카츄(T26)는 한복의 글로벌 소재화 신호지만 IP 이미지는 쓸 수 없다. 궁궐 한복 대여·경복궁 직접 글은 수집되지 않았다.
- **사극 신호는 약하다.** 기간 내 사극 전용 화제는 My Royal Nemesis(T30, 장르 미확인) 정도이고, EP001 자료의 The Scandal·100 Days of Deception(10/10 공개) 이후 이어지는 글은 이번 수집에 없었다. 대신 한일 리메이크 비교(T31, 893)와 고전 드라마 회고(T32, 947)가 문화 코드 설명의 진입점이 된다.
- **한계:** X·TikTok·Instagram 미수집, YouTube는 기간 내 항목이 4건뿐이고 자막·댓글 수집이 대부분 막혔다. 1~3회차는 플랜의 서브쿼리 절반만 실행됐다(7·8회차로 보완). 역사 명소(경복궁·창덕궁·DMZ·경주·부산)와 추석 외 명절, 전통 음식 유래는 기간 내 결과가 없어 리서처가 별도 검색으로 채워야 한다.
