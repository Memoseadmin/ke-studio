# EP003 트렌드 원자료 — last30days (2026-09-02 ~ 2026-10-02)

> 이 파일은 수집 원자료다. 기준은 구독형 혼합(서사형 60~70% + 구매 의도형 30~40%, docs/PLAN.md "수익 구조")이다. 외국인 시청자가 최근 30일 동안 한국에 대해 묻고 공유한 것을 모았다. 수치(upvotes·조회수)는 수집 시점 값이라 추정치로 다룬다. §2 표에는 엔진 결과에 실제로 나온 URL만 넣었다. 엔진이 아닌 호스트 WebSearch로 찾은 보강분은 §4에 따로 표시했다.

## 1. 실행 메타
- 실행일: 2026-10-02 (UTC 00:24:57~00:32:06). 조사 기간은 엔진 보고 기준 2026-09-02 ~ 2026-10-02.
- 엔진: last30days **v3.26.0** (`.claude/skills/last30days-last30days/scripts/last30days.py`, 저장소 사본을 고치지 않고 그대로 썼다).
- 실행 환경
  - `python3.12`
  - `FROM_BROWSER=off`, `--no-browser-cookies`
  - `LAST30DAYS_NATIVE_SEARCH=1`, `--emit=compact`, `--plan <tmpfile>`, `--subreddits=…`
  - `--save-dir`: 세션 스크래치 디렉터리(저장소 밖)
- 키·자격증명: `~/.config/last30days/.env` 없음(`config_source: env_only`). 셋업 마법사, 쿠키 읽기, 키 입력은 하지 않았다. 환경변수 확인 결과는 `SCRAPECREATORS_API_KEY`·`X_BEARER_TOKEN`·`BRAVE_API_KEY`·`EXA_API_KEY`·`SERPER_API_KEY` 모두 UNSET이다. 값은 보지 않았다.
- 사전 `doctor`(라이브 프로브) 결과
  - **WORKING**: reddit(공개 키리스), youtube(yt-dlp), hackernews, polymarket, github
  - **COULD BE ON**: x, tiktok, instagram, threads 등(미설정, 미사용)
- 플랜: 6회 모두 LAW 7에 따라 직접 작성했다(`intent=opinion, freshness=balanced_recent, cluster_mode=debate`, 서브쿼리 4개). 엔진 로그에 6회 모두 `subqueries=4, source=external`로 찍혀 4개가 전부 실행됐다(EP002 메모대로 `intent=concept`는 쓰지 않았다).

| # | topic(엔진 인자) | 대상 서브레딧 | 결과(엔진 Stats) | 소요 |
|---|---|---|---|---|
| 1 | Korea explained | korea, AskAKorean, Living_in_Korea, todayilearned, korea_travel, Korean | Reddit 22 · YT 1 · HN 11 · PM 12 | 67s |
| 2 | why do Koreans | korea, AskAKorean, KDRAMA, Korean, NoStupidQuestions, todayilearned | Reddit 13 · YT 3 · HN 12 | 90s |
| 3 | K-drama October 2026 | KDRAMA, kdramas, kdramarecommends, netflix, korea, AsianDrama | Reddit 13 · YT 6 · HN 5 · PM 3 | 59s |
| 4 | Korean history for foreigners | korea, history, AskHistorians, todayilearned, KoreanHistory, Korean | Reddit 18 · YT 1 · HN 4 | 79s |
| 5 | Korea travel autumn | koreatravel, korea, seoul, travel, solotravel, JapanTravel, Busan | Reddit 24 · YT 4 · HN 11 | 71s |
| 6 | Korean food questions | KoreanFood, korea, Cooking, AskAKorean, seoul, koreatravel | Reddit 27 · YT 5 · HN 4 | 63s |

**source_status (6회 통합)**
- Reddit: **OK**. 6회 모두 결과를 받았다.
- YouTube: **부분(partial)**.
  - 검색은 됐지만 1·2·4·6회는 "0~2 within date range, keeping all"로 대부분 기간 밖 결과였다.
  - 자막은 yt-dlp "Sign in to confirm you're not a bot"과 HTTP 429가 반복돼 일부만 받았다.
  - 기간 안 항목 중 관련 있는 것은 여행 3건(JustinHanguk 2·Lais 1)과 1건(Amy in Seoul)뿐이다.
- Hacker News: OK이지만 전부 무관(북한·경제·기술)이라 표에 넣지 않았다.
- Polymarket: 15건, 전부 금융(EWY·BoK·인플레이션)·정치(북미·대통령)·스포츠라 제외했다.
- Jobs: 매회 **unreachable**(프록시 502). 엔진이 자동으로 붙인 소스라 이번 조사와 무관하다.
- X / TikTok / Instagram / Threads: **skipped-unconfigured**. 숏폼 플랫폼 신호는 이번 자료에 없다(커버리지 한계).
- 호스트 WebSearch는 엔진 실행과 별도로 썼다. 엔진이 김장·단풍·수능 같은 시즌 신호를 거의 잡지 못해 보강이 필요했다. 보강분은 §4에 W번호로 따로 적었다.

## 2. 수집 항목 (기간 내, 관련 있는 것만, 중복 제거)
| T# | 날짜 | 소스 | 반응 | 내용 | 쓰임 |
|---|---|---|---|---|---|
| T1 | 09-13 | r/todayilearned | 23,373↑ 785c | TIL 한국 "도파민 사이트": 가짜 쇼핑·배달 추적 앱(결제·배송 없음) https://www.reddit.com/r/todayilearned/comments/1wetdn3/ | 후보7 |
| T2 | 09-25 | r/korea | 1,635↑ 53c | "Chuseok in South Korea 30~40 years ago"(옛 명절 사진) https://www.reddit.com/r/korea/comments/1wps4xh/chuseok_in_south_korea_3040_years_ago/ | 후보1·2(세시·향수) |
| T3 | 10-01 | r/AskAKorean | 7↑ 32c | "Who is the Korean god who judges Korea?" https://www.reddit.com/r/AskAKorean/comments/1wuustw/who_is_the_korean_god_who_judges_korea/ | 후보4 |
| T4 | 09-23 | r/AskAKorean | 5↑ 23c | "Are there any Korean words that tells Korea's culture?" https://www.reddit.com/r/AskAKorean/comments/1wo5fsc/ | 참고(EP002 후보6과 겹침) |
| T5 | 09-14 | r/todayilearned | 765↑ 43c | TIL 1504 연산군 한글 금지(EP002 T2와 같은 글) https://www.reddit.com/r/todayilearned/comments/1wgfxx3/ | 후보2·3("금지" 시리즈 수요) |
| T6 | 10-01 | r/KDRAMA | 466↑ 35c | Netflix 'Dead-End Job' 티저 포스터(10/30 공개, 판타지·호러) https://www.reddit.com/r/KDRAMA/comments/1wukzpg/ | 후보4 훅 |
| T7 | 10-01 | r/kdramas | 270↑ 23c | 'Dead-End Job' 예고편 https://www.reddit.com/r/kdramas/comments/1wuqlbc/ | 후보4 |
| T8 | 10-01 | r/KdramaCasualTalk | 123↑ 22c | "NEW K-DRAMAS RELEASING IN OCTOBER 2026" https://www.reddit.com/r/KdramaCasualTalk/comments/1wuy5rv/ | 10월 라인업 |
| T9 | 09-29 | r/KDRAMA | 468↑ 34c | TVING 'Make Me Tingle' 메인 포스터(10/15) https://www.reddit.com/r/KDRAMA/comments/1wsvsur/ | 10월 라인업 |
| T10 | 09-30 | r/KDRAMA | 296↑ 18c | JTBC 'Final Table' 포스터(10/24) https://www.reddit.com/r/KDRAMA/comments/1wu4vjq/ | 10월 라인업(음식 소재 여부 미확인) |
| T11 | 09-10 | r/seoul | 292↑ 14c | "Fall has arrived in Korea. The weather is so nice!" https://www.reddit.com/r/seoul/comments/1wcgltx/ | 후보8 |
| T12 | 09-24 | YouTube JustinHanguk | 11,154뷰 | "must visit autumn spots and cafes in seoul" https://www.youtube.com/watch?v=LKRKOkOOV2A | 후보8 |
| T13 | 09-30 | YouTube JustinHanguk | 5,081뷰 | "more cafes and autumn foliage spots in Seoul" https://www.youtube.com/watch?v=4SMpAP0HhCs | 후보8 |
| T14 | 09-25 | YouTube Lais | 8,685뷰 | "21 Best Places to Visit in Seoul in Autumn 2026" https://www.youtube.com/watch?v=r5p1nwYu1NY | 후보8 |
| T15 | 09-06 | r/koreatravel | 2↑ 6c | "Fall trip to Korea — Hwadam Forest vs other spots?" https://www.reddit.com/r/koreatravel/comments/1w8v3we/ | 후보8 |
| T16 | 09-07 | r/JapanTravel | 5c | 한·일 4주 일정 점검(Oct/Nov 2026) https://www.reddit.com/r/JapanTravel/comments/1w9nrpn/ | 후보8(가을 여행 수요) |
| T17 | 10-01 | r/koreatravel | 1↑ 1c | "How do you usually pay while traveling in Korea?" https://www.reddit.com/r/koreatravel/comments/1wur1kb/ | 후보9 보조 |
| T18 | 09-23 | r/seoul | 191↑ 41c | 명동 야시장 늦은 밤 길거리 음식 https://www.reddit.com/r/seoul/comments/1woa7g0/ | 후보2·9 |
| T19 | 09-15 | r/KoreanFood | 550↑ 27c | ₩9,500 무한리필 한식+생맥주 https://www.reddit.com/r/KoreanFood/comments/1wgxor4/ | 후보9 |
| T20 | 09-04 | r/KoreanFood | 1,281↑ 36c | "My Summer Korean Office Lunch" https://www.reddit.com/r/KoreanFood/comments/1w7e0vl/ | 후보10 |
| T21 | 10-01 | r/KoreanFood | 24↑ 17c | "Korean moms always give WAY too much food" https://www.reddit.com/r/KoreanFood/comments/1wumy6s/ | 후보1(나눔 정서) |
| T22 | 09-16 | r/AskAKorean | 30c | "What Korean food have you NEVER tried, as a native Korean?" https://www.reddit.com/r/AskAKorean/comments/1whlkqd/ | 후보1·10 |
| T23 | 09-22 / 09-14 | r/KoreanFood | 545↑ / 568↑ | "Korean unc's hangover ramen" / "Jaecheop Ramen" https://www.reddit.com/r/KoreanFood/comments/1wnnvcc/ · …/1wghe24/ | EP001(라면)과 겹침 → 신호로만 |
| T24 | 09-30 | r/korea | 60↑ 13c | 노포 빵집이 센베이와 현대 디저트를 함께 판다 https://www.reddit.com/r/korea/comments/1wu0sqj/ | 참고 |
| T25 | 09-27 | r/koreatravel | 376↑ 91c | "The people of South Korea generally are incredibly kind" https://www.reddit.com/r/koreatravel/comments/1wrffkf/ | 여행 정서 |
| T26 | 09-11 | r/koreatravel | 334↑ 55c | "10 days in Korea as a Filipino Tourist" https://www.reddit.com/r/koreatravel/comments/1wdd5nk/ | 후보8 |
| T27 | 09-30 | YouTube Amy in Seoul | 13뷰 | "Why Do Koreans Work So Much? It's Not Just Culture." https://www.youtube.com/watch?v=txMX8aIqhbY | 신호 약함(노동 이슈 → 보류) |
| T28 | 09-06 | YouTube Bedtime & Historian | 67,175뷰 | "The ENTIRE History of Korea | How One Nation Became Two" https://www.youtube.com/watch?v=UfBm6Mt3rjY | 통사 수요(분단 → 정치 회피) |
| T29 | 09-09 | YouTube Klassy Korea | 137,398뷰 | "HOPE Movie Breakdown and Ending Explained" https://www.youtube.com/watch?v=p92qC3PTl-0 | 한국 영화 신호(작품 정보 미확인) |
| T30 | 10-01 | r/korea | 17↑ | "Korean culture is gaining popularity in my homeland Kazakhstan" https://www.reddit.com/r/korea/comments/1wv2732/ | 참고 |

## 3. 제외 (건강·금융·법률·정치·사건·실존 인물·우열 비교)
- **법률·사건·실존 인물** 5건: Cornell 소송 관련 r/korea 4건(1wsz217·1wts18t·1wsp14v·1wuuais), Taiwanese 택시 기사 사건(1wukbnj).
- **정치·외교** 6건: Ukraine POW 3건(1wt8rk3·1wryy7x·1wu0w81), Trump·북핵(r/worldnews 1wuxwhg), 중국 'two states'(1w720xr), 대안역사 "한반도가 일본이었다면"(1wjtwgu).
- **참사**: 세월호 여론조사 TIL(1wap539).
- **건강**: hospital food(1whitgu), HSV-2(1wu127w), "why are korean slim"(1w6rdmm), 남북 평균 키 TIL(1wb4xs5).
- **금융**: Polymarket 15건 전부.
- **우열 비교**: "Korea seemed much more like China than Japan?"(1wb5c3d).
- **실존 인물 비판**: 배우 유카타 논란(1w7gboi, EP002에서 이미 처리).
- **차별·노동**(톤 리스크로 보류): 무슬림 구직, 동북인도 인종차별, 비학위 경력, 외국인 체감 변화.
- **무관**: r/NoStupidQuestions 일반 질문 6건, Avengers 영상, EDC·포켓몬 행사(IP), 언어교환 글.

## 4. 호스트 WebSearch 보강 (엔진 밖, 리서처가 research.md에서 사용)
| W# | 날짜 | 출처 | 내용 |
|---|---|---|---|
| W1 | 2026-09-09 | seoulz.com "Korea kimchi crisis" | 가정 김장 참여 2024년 64.5% → 2025년 62.3%(농촌경제연구원 인용), 고랭지 배추 면적 감소, 정부 배추 1.5만 톤 비축 |
| W2 | 2025(김장 시즌) | 농식품부/뉴스서울 | 2025 김장 의향 62.3%, 감소 이유 1위 '비용 부담', 11월 하순 이후 김장 62.3% |
| W3 | 2026-09-22 | 경향신문(EN) | 산림청 2026 단풍 절정 예측: 설악산 10/20, 속리산 10/28, 내장산 11/4, 한라산 11/6 |
| W4 | 2026 | dhnews 외 | 2027학년도 수능 2026-11-19(목). 영어듣기 시간 항공기 이착륙 통제 |
| W5 | 2026 | whats-on-netflix | 10월 넷플릭스 K-드라마: Take Charge of My Heart(10/9), Dead-End Job(10/30) |
| W6 | 2026-07-06 | Oman Observer | "To tackle a kimchi crisis, South Korea banks on massive cabbage warehouses" |
| W7 | 상시 | Klook 활동 페이지 | 서울 김치 만들기 클래스(평점 4.6, 리뷰 1,000+ 표기) — 제휴 후보 |
