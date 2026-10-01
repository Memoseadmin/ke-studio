# EP001 트렌드 원자료 — last30days (2026-09-01 ~ 2026-10-01)

> 수집 원자료(raw evidence)다. 수치는 수집 시점 값이며 이후 바뀔 수 있다. 아래 표의 항목은 모두 엔진 실행 결과에 실제로 나온 URL만 담았다.

## 1. 실행 메타

- 실행일: 2026-10-01 (UTC 04:40~04:47), 조사 기간 2026-09-01 ~ 2026-10-01
- 엔진: last30days **v3.26.0** (`.claude/skills/last30days-last30days/scripts/last30days.py`), 업스트림 SHA `5103ba478b380552207a3754b74c7655d64208cd` (docs/SKILLS.md 기준)
- 실행 환경: `LAST30DAYS_PYTHON=/usr/bin/python3.12`, `FROM_BROWSER=off`, `--no-browser-cookies`, `LAST30DAYS_NATIVE_SEARCH=1`, `--emit=compact`
- 셋업 마법사, 쿠키 읽기, 키 입력은 모두 실행하지 않았다. 키 없이 동작하는 소스만 썼다.
- 사전 `doctor` 결과: WORKING = reddit, youtube(yt-dlp), hackernews, polymarket, github / 미설정 = x, tiktok, instagram, threads, bluesky 등
- 엔진 실행 총 6회, 합계 약 11분:

| # | topic | 방식 | 서브쿼리 / 대상 |
|---|---|---|---|
| 1 | K-drama food | `--plan`, 기본 깊이 | kdrama food / korean drama snack ramyeon convenience store / kdrama recipe korean food · subs KoreanFood, korea, koreatravel, kdramarecommends + 전용 KDRAMA, kdramas |
| 2 | Netflix Korean drama | `--plan`, 기본 깊이 | korean drama netflix / made in korea season 2 the scandal / korean variety show netflix · subs netflix, korea, kdramarecommends, KoreanVarietyShows + 전용 KDRAMA, kdramas |
| 3 | Korean food and places from K-content | `--plan`, 기본 깊이 | kdrama·KPDH 음식 / 편의점 스낵 / 촬영지 / 추석 |
| 4 | Korean food | `--plan --quick` | korean food / kpop demon hunters / seoul must eat · 전용 KoreanFood, koreatravel |
| 5 | KPop Demon Hunters | `--quick --search=reddit,youtube` | subs KpopDemonHunters, kpop, korea |
| 6 | Chuseok | `--quick --search=reddit,youtube` | subs korea, seoul, koreatravel, KoreanFood |

**source_status (6회 통합)**
- Reddit: **OK**. 공개 키리스 경로와 arctic-shift 보강으로 6회 모두 결과를 받았다(14 / 15 / 4 / 4 / 6 / 6건).
- YouTube: **부분(partial)**. 검색은 됐지만 자막 수집이 막혔다. yt-dlp가 "Sign in to confirm you're not a bot"을 반환했고 HTTP 429도 1회 있었다. 기간 안 결과는 0 / 5 / 0 / 2 / 0 / 4건이다.
- Hacker News: OK이나 주제와 무관하다(North Korea 기사 등). 전부 제외했다.
- Polymarket: 1회차에 무관한 마켓 2건(CS2 "Drama eSports")이 나왔고 나머지는 no-results였다. 제외했다.
- Jobs: **unreachable**. 프록시 502 Bad Gateway, connection reset이 났다. 엔진이 자동으로 붙인 소스라 무관하다.
- X / TikTok / Instagram / Threads: **skipped-unconfigured**. 자격증명이 필요해 규칙상 쓰지 않았다. 숏폼 플랫폼 신호는 이번 자료에 없다.
- 엔진 측 web 검색: 끔(호스트 WebSearch 사용 모드). 쿼리 설계를 위해 호스트 WebSearch를 2회 썼지만 그 결과는 아래 표에 넣지 않았다.

## 2. 트렌드 트리거 목록 (19건)

### A. 음식·제품 (구매 의도형)

| # | 작품/화제 | 날짜 | 무엇이 화제인가 (음식·장소·제품 연결) | engagement | URL |
|---|---|---|---|---|---|
| 1 | "A Tray of Chuseok Jeon" (r/KoreanFood) | 2026-09-24 | 추석 전(jeon) 한 판 사진. 댓글은 "하나씩 다 뒤집느라 고생했다"는 반응. 명절 음식, 부침 재료로 연결된다 | 1,914 upvotes · 44 comments | https://www.reddit.com/r/KoreanFood/comments/1wp04p2/a_tray_of_chuseok_jeon/ |
| 2 | "Happy Chuseok everyone!" (r/KoreanFood) | 2026-09-25 | 추석 상차림 사진. 댓글에 "양념게장!!!!!" 반응이 있다. 명절 한상 차림으로 연결된다 | 1,277 upvotes · 45 comments | https://www.reddit.com/r/KoreanFood/comments/1wq5h8u/happy_chuseok_everyone/ |
| 3 | "Chuseok" (r/KoreanFood) | 2026-09-25 | 추석 음식 게시물(제목만 수집, 구체 메뉴 미확인) | 667 upvotes · 40 comments | https://www.reddit.com/r/KoreanFood/comments/1wpwfia/chuseok/ |
| 4 | CORTIS "Chuseok Cooking" (YouTube 공식 채널) | 2026-09-25 | K-pop 그룹의 추석 요리 영상. 아이돌과 명절 음식을 잇는 고리(구체 메뉴 미확인) | 2,604,347 views · 151,567 likes · 6,400 comments | https://www.youtube.com/watch?v=Xq46_fQcVzg |
| 5 | ATEEZ "그 많던 송편은 누가 다 먹었을까 \| 2026 추석 특집" | 2026-09-25 | 아이돌 추석 특집 영상. 제목에 송편(songpyeon)이 들어 있다 | 537,860 views · 21,961 likes · 1,000 comments | https://www.youtube.com/watch?v=TP21JTSLmJA |
| 6 | Thursday "A quiet weekend alone \| Nor'east in New York, Chuseok and the moon" | 2026-09-29 | 해외 거주 한국인 브이로그. "송편을 만들었는데 생각보다 쉽지 않았다"는 내용으로 송편 만들기, 재료 키트 수요에 연결된다 | 9,629 views · 445 likes · 65 comments | https://www.youtube.com/watch?v=6eVzVWRDNUg |
| 7 | MaddyEats "VIRAL SPICY CHEESY BULDAK NOODLES ONION WRAP, SPICY KOREAN CHICKEN DRUMSTICKS…" | 2026-09-30 | 불닭볶음면 바이럴 레시피와 매운 한국식 치킨. 라면 제품 구매로 바로 이어진다 | 97,852 views · 1,507 likes · 66 comments | https://www.youtube.com/watch?v=s9vP2PaoPkg |
| 8 | "Korean hospital food" (r/KoreanFood) | 2026-09-16 | 한국 병원 식단 사진. 한식 일상식 관심을 보여준다. ⚠ 건강 주제와 가까우니 활용 시 주의 | 1,016 upvotes · 50 comments | https://www.reddit.com/r/KoreanFood/comments/1whitgu/korean_hospital_food/ |
| 9 | "Korean moms always give WAY too much food" (r/KoreanFood) | 2026-10-01 | 한국 엄마 반찬, 음식 인심 밈. 문화 설명형으로 쓸 수 있다 | 11 upvotes · 6 comments | https://www.reddit.com/r/KoreanFood/comments/1wumy6s/korean_moms_always_give_way_too_much_food/ |
| 10 | Rockstar Eater "BEST NEW All You Can Eat Korean BBQ Buffet in Los Angeles!" | 2026-09-29 | LA 신규 K-BBQ 무한리필(MJD Korean BBQ). 해외 K-BBQ 수요를 보여준다 | 14,839 views · 242 likes · 16 comments | https://www.youtube.com/watch?v=tYB1glz6KfA |
| 11 | KPop Demon Hunters × Magic: The Gathering Secret Lair (r/kpop) | 2026-09-30 | KPDH 카드 스킨 협업. 굿즈·카드 구매로 연결되며 반발 댓글도 있다 | 226 upvotes · 37 comments | https://www.reddit.com/r/kpop/comments/1wuawgl/kpop_demon_hunters_kpop_comes_to_magic_the/ |
| 12 | 같은 협업 (r/KpopDemonhunters) | 2026-09-30 | 같은 소식에 대한 팬덤 서브 반응 | 182 upvotes · 49 comments | https://www.reddit.com/r/KpopDemonhunters/comments/1wu8wee/kpop_demon_hunters_coming_to_magic_the_gathering/ |

### B. 장소 (방문 의도형)

| # | 작품/화제 | 날짜 | 무엇이 화제인가 | engagement | URL |
|---|---|---|---|---|---|
| 13 | "Late-night street food cravings at the vibrant Myeongdong Night Market" (r/seoul) | 2026-09-23 | 명동 야시장 길거리 음식 | 191 upvotes · 41 comments | https://www.reddit.com/r/seoul/comments/1woa7g0/latenight_street_food_cravings_at_the_vibrant/ |
| 14 | "Only ₩9,500 (US$6) for AYCE Korean food + draft beer" (r/KoreanFood) | 2026-09-15 | 9,500원 한식 무한리필과 생맥주. 여행자 가성비 맛집 훅 | 550 upvotes · 27 comments | https://www.reddit.com/r/KoreanFood/comments/1wgxor4/only_9500_us6_for_ayce_korean_food_draft_beer/ |
| 15 | "K-DRAMA EXHIBITION at Seoul Station" (r/koreatravel) | 2026-09-30 | 서울역 K-드라마 전시. K-콘텐츠와 장소가 직접 이어진다 | 10 upvotes · 2 comments | https://www.reddit.com/r/koreatravel/comments/1wtr0f3/kdrama_exhibition_at_seoul_station/ |
| 16 | "Seoul Forest: Where you need to be in Chuseok Holiday 2026" (r/seoul) | 2026-09-25 | 추석 연휴 서울숲 | 2 upvotes · 2 comments | https://www.reddit.com/r/seoul/comments/1wpnucq/seoul_forest_where_you_need_to_be_in_chuseok/ |

### C. K-콘텐츠·문화·역사 훅

| # | 작품/화제 | 날짜 | 무엇이 화제인가 | engagement | URL |
|---|---|---|---|---|---|
| 17 | The Scandal (Netflix, 9/18 공개) | 2026-09-08 트레일러 / 2026-09-18 Reddit | 조선 배경 사극(트레일러 설명: "In Joseon, a secret proposal…"). Reddit에서는 18+ 수위 논쟁이 붙었다. 조선 양반 문화를 설명하는 역사 훅으로 쓸 수 있다 | 트레일러 712,782 views · 3,497 likes · 251 comments / Reddit 1,477 upvotes · 423 comments | https://www.youtube.com/watch?v=FeISX5E1uJc · https://www.reddit.com/r/kdramas/comments/1wk0bao/scandal_netflixs_new_kdrama_18/ |
| 18 | 100 Days of Deception (Netflix, 10/10 공개 예정) | 2026-09-29 | 일제강점기 경성(Gyeongseong)을 배경으로 소매치기가 총독부에 잠입하는 이야기. 경성 시대를 설명하는 역사 훅 | 264,087 views · 3,004 likes · 95 comments | https://www.youtube.com/watch?v=P0ElxnFyfXY |
| 19 | "Chuseok in South Korea 30~40 years ago" (r/korea) | 2026-09-25 | 옛 추석 귀성길 사진. 댓글은 "5~6시간 차멀미", "할머니 음식이 그립다" 등. 명절 문화사 훅 | 1,621 upvotes · 51 comments | https://www.reddit.com/r/korea/comments/1wps4xh/chuseok_in_south_korea_3040_years_ago/ |

참고로 표에서 뺀 고신호 항목도 남긴다. Doctor X: Mafia in White 티저는 2026-09-21, 1,958,063 views, https://www.youtube.com/watch?v=p8w-mvmIykc 로 의료 소재라 건강 주제 금지 규칙에 가깝다. Take Charge of My Heart 트레일러는 2026-09-28, 375,723 views, https://www.youtube.com/watch?v=z_D5uXaDsVU 인데 음식·장소 연결이 확인되지 않았다. KOREA NOW의 추석 귀성 영상은 2026-09-24, 23,442 views, https://www.youtube.com/watch?v=CHVmEebL2oM 이다. KPDH 속편 "broad theatrical release" 기사 공유는 2026-10-01, 1 upvote, https://www.reddit.com/r/KpopDemonhunters/comments/1wunyvk/kpop_demon_hunters_sequel_will_get_a_broad/ 이다.

## 3. 관찰

- **가장 강한 음식 훅은 추석 명절 음식(전·송편·상차림)이다.** r/KoreanFood 상위 글(1,914 / 1,277 / 667 upvotes)과 아이돌 추석 영상(CORTIS 260만 뷰, ATEEZ 54만 뷰)이 같은 주(9/24~25)에 몰렸다. "K-pop 아이돌이 먹는 추석 음식"에 전 재료나 송편 키트를 붙이는 각도가 가능하다. 다만 시즌성이 강해 다음 명절(설)까지 그대로 쓰기는 어렵다(추정).
- **구매 의도가 가장 직접적인 것은 불닭(Buldak) 계열 바이럴 레시피다**(9.8만 뷰). 라면이나 소스 제품을 서사 끝에 자연스럽게 둘 수 있다. 해외 K-BBQ 무한리필 수요(LA 영상)도 보조 신호다.
- **넷플릭스 시대극 2편이 문화·역사 설명형 50%에 맞는다.** The Scandal은 조선 배경이고, 100 Days of Deception은 10/10 공개 예정인 경성 배경 작품이다. 공개 직후 "실제 경성/조선은 어땠나" 설명 영상 수요가 생길 수 있다(추정).
- **장소 훅은 명동 야시장, 9,500원 한식 무한리필, 서울역 K-드라마 전시다.** 셋 다 여행자 가성비나 K-콘텐츠 성지로 엮을 수 있다. KPDH는 MTG 협업처럼 굿즈 화제는 있지만 음식 연결 증거는 이번 수집에서 나오지 않았다.
- **한계:** "드라마 속 특정 음식" 직접 증거는 거의 없었다. r/kdramas 상위 글은 대부분 작품 감상이었다. X·TikTok·Instagram을 수집하지 못했고 YouTube 자막도 막혔으니, 리서처 단계에서 별도 검색으로 보강해야 한다.
