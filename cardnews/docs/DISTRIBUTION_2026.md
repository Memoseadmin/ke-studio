# 책가도 노트 — 배포 전략 리서치 2026 (인스타·Threads·도구)

- 작성: 리서처(플랫폼 전략) · 확인 날짜: **2026-10-02**(아래 URL 모두 이 날짜에 조회·검색).
- 대표 지시(2026-10-02): "채널 성공 가능성을 높이는 리서치. 첫 포스트가 첫 번째 목표."
- 태그: **[공식]** Meta·Instagram·Mosseri 1차 자료 또는 그 발언을 그대로 인용한 보도 / **[분석]** 제3자 연구·보도 / **[추정]** 리서처 추론. 모든 수치는 추정치이며 우리 실측이 생기면 교체한다.
- 전제: 게이트 C1 = 90일 팔로워 2,000 + 저장률 3% + 미디어킷 + 협찬 제안 5건, 월 5만원 이하(`cardnews/docs/PLAN.md`). 규제·표시는 `SPONSORSHIP_MARKET.md` §4(공정위 표시 3중: 1장 표시·캡션 첫 줄·유료 파트너십 라벨). 게시 도구는 `tooling/ig-publisher` 브랜치 `scripts/README-ig.md`(Graph API 캐러셀, 예약은 queue.json + 루틴).

## 0. 요약 — 첫 포스트 전에 할 것 (먼저 읽을 것)
1. **🔴 ig_publish.py가 PNG를 올린다 → API는 JPEG만 받는다.** `card-NN.png`를 JPEG(품질 90 이상, 8MB 이하)로 변환하는 단계를 R2 업로드 전에 넣어야 첫 자동 게시가 실패하지 않는다. [공식] [REF](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media)
2. **비율은 4:5(1080x1350) 유지.** v3 렌더러가 이미 1080x1350. API 공식 허용 범위는 4:5~1.91:1이라 3:4(1080x1440)는 범위 밖이다. 3:4 전환 금지. [공식]
3. **알고리즘 1순위 지표 = 보내기(DM 공유)/도달.** Mosseri 공식 3대 신호 = 시청 시간·좋아요·보내기. 비팔로워 추천은 보내기 비중이 조금 더 크다. 저장은 공식 언급 없음 → 저장률 게이트는 유지하되 7장 CTA는 "○○한 사람에게 보내기"를 1순위로. [공식]
4. **2장도 표지처럼.** 안 넘긴 사용자에게 캐러셀이 다시 뜰 때 2번째 장부터 보인다(Mosseri). 2장 헤드라인을 단독으로 읽혀도 되게 쓴다. [공식, 2024-10]
5. **원본성 = 생존 조건.** 2026-04-30부터 비독창적 사진·캐러셀 위주 계정은 추천에서 빠진다(워터마크·크레딧·자막만 얹은 것은 비독창). 편집 실사는 "원본 그대로 금지" 규칙(HANDOFF 대표 결정)을 철저히. [공식]
6. 게시 시각 19:00(캐러셀)은 국내·해외 자료와 맞다. 릴스 21:00 vs 22:00은 A/B 가치 있음.

## 1. 2026년 인스타그램 추천 알고리즘

| 항목 | 확인된 내용 | 근거 | 우리 적용 |
|---|---|---|---|
| 랭킹 신호 | "가장 중요한 3신호 = 시청 시간, 좋아요, 보내기(sends). 인사이트에서 평균 시청 시간·도달 대비 좋아요·도달 대비 보내기를 보라." 팔로워 노출은 좋아요, 비팔로워 추천은 보내기 비중이 **약간** 더 크다. **수치 가중치는 공식 미공개.** | [공식] Mosseri, [SMT 2025-01-22](https://www.socialmediatoday.com/news/instagram-shares-algorithm-insights-2025/738034/) · 2026-09 재언급 보도 [분석] [kompozy 2026-09-25](https://kompozy.io/news/instagram-mosseri-ranking-signals-guidance)("보내기=좋아요 N배"는 매체 추정) | analyst 주간 지표에 **보내기/도달** 추가. 7장 CTA = 보내기 유도(경품형 참여 유도는 금지) |
| 저장 | 위 공식 발언에 저장은 없다. 공식 가중치 없음 | [공식 부재] 위 두 출처 | 저장률은 게이트 지표(협찬 단가 근거)로 유지, 알고리즘 근거로는 쓰지 않음 [추정] |
| 캐러셀 2차 노출 | "캐러셀을 보고 넘기지 않으면 다시 보여 줄 수 있고, 그때는 2번째 장을 보여 준다." 2026년 변경 공지 없음 | [공식] Mosseri, [RouteNote 2024-10-18](https://routenote.com/blog/instagram-carousels-perform-better-than-single-photos-according-to-the-head-of-instagram/) | 2장 = 두 번째 표지. 2장 헤드라인 단독 이해 가능하게 |
| 3:4 vs 4:5 | 3:4 업로드 지원(2025-05-30), 그리드 세로형 전환(2025-01). **도달 차이 공식 근거 없음.** API는 4:5~1.91:1만 문서화 | [공식] [RouteNote 2025-05](https://routenote.com/blog/instagram-introduces-a-new-aspect-ratio-for-photos/) · [REF](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media) · API 업로드 시 3:4 잘림/거부 사례 [분석] [Sked](https://skedsocial.com/blog/best-instagram-image-and-video-size-recommendations.md) | **4:5 유지.** 3:4 그리드 썸네일에서 4:5 이미지는 좌우가 약 6%(양쪽 ~34px) 잘리므로 1장 핵심 글자는 좌우 여백 안쪽에(현 SAFE 좌우 88px이면 충분) [추정] |
| 릴스↔캐러셀 교차 | 음악을 넣은 사진·캐러셀은 릴스 탭에 노출될 수 있다 | [공식, 2차] [Lindsey Gamble 2024-10-18](https://www.lindseygamble.com/blog/instagram-expands-the-reach-of-carousels-and-photos-by-featuring-them-in-the-reels-tab-heres-why-it-matters) | **API로는 캐러셀 음악 불가**(Audio API는 릴스 전용, 2026-06-01 [공식] [changelog](https://developers.facebook.com/docs/instagram-platform/changelog)). 음악 붙이려면 앱 수동 게시 |
| 해시태그 | 게시물당 **최대 5개**(2025-12-18 @creators 공지, 첫 댓글로 우회 불가). Mosseri: "주제 이해엔 도움, 배포 수단으로 생각하지 말라" | [공식] [Social Samosa 2025-12-19](https://www.socialsamosa.com/news-2/instagram-hashtags-five-per-post-10923075) · [inro](https://www.inro.social/blog/instagram-hashtags) [분석 경유] | 현 게이트 ≤5 유지. 도달 효과는 작다 → 3개면 충분 [추정] |
| 검색·SEO | 2025-07-10부터 공개 프로페셔널 계정 게시물이 구글 등에 색인(기본 켜짐). 캡션·바이오·alt가 내부 검색에 쓰인다는 건 서드파티 가이드만 | [공식, 경유] [PPC Land 2025-07](https://ppc.land/instagram-content-becomes-searchable-on-google-starting-july-10/) · [분석] [Later](https://later.com/blog/instagram-seo/) | 캡션 첫 줄 = 검색어 포함 한 문장(협찬 시엔 공정위 문구가 첫 줄, 검색어는 둘째 줄). 장별 alt text 작성(API `alt_text` 지원) |
| 트라이얼 릴스 | 비팔로워에게만 배포, ~24h 후 지표, 72h 성과 좋으면 팔로워 자동 공유 옵션. **공개 계정 + 팔로워 1,000명 이상**(2025-07 전원 확대). 2026 기준 폐지 공지 없음. 캐러셀용은 없음. API `trial_params`(MANUAL/SS_PERFORMANCE) 2025-12-03 지원 | [공식] [Instagram Creators 2024-12-10](https://creators.instagram.com/blog/instagram-trial-reels) · [Social Samosa 2025-07-14](https://www.socialsamosa.com/news-2/instagram-introduces-wider-access-trial-reels-9493132) · [changelog](https://developers.facebook.com/docs/instagram-platform/changelog) | 팔로워 1,000 전엔 사용 불가 가능성 높음 [추정]. 1,000 도달 후 릴스 훅 A/B용 |
| 신규 계정 초기 도달 | 2024-04-30: 작은 크리에이터 배포 가중 입력 추가, 추천은 작은 관심 집단 → 반응 좋으면 단계 확대. 재게시물은 원본으로 대체, 애그리게이터 추천 제외 | [공식] [Creators: 추천과 독창성](https://creators.instagram.com/recommendations-and-originality) · [TechCrunch 2024-04-30](https://techcrunch.com/2024/04/30/instagram-is-updating-its-ranking-systems-to-surface-more-content-from-smaller-original-creators) | 첫 1~2시간 보내기·좋아요가 다음 단계 확산을 결정 [추정] → 게시 직후 대표 계정 스토리 공유 등 초기 반응 확보 |
| 원본 우대·재게시 패널티 | 2026-04-30: **주로 비독창적인 사진·캐러셀 계정은 추천 노출 제외**(팔로워 노출은 영향 없음). 테두리·워터마크·자막·크레딧만 추가 = 비독창. 최근 30일 롤링으로 대부분 독창적이면 복귀. 이의는 '계정 상태'에서 | [공식] [Creators 2026-04-30](https://creators.instagram.com/blog/rewarding-original-creators-on-instagram) · [PetaPixel 2026-04-30](https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/) · 미국 추천의 75% 원본 [분석] [TechCrunch 2026-04-30](https://techcrunch.com/2026/04/30/instagram-restricts-reach-of-content-aggregators-in-new-crackdown/) | 위키미디어·박물관 사진을 **그대로 + 출처**만 쓰면 비독창으로 분류될 위험 [추정]. v3 콜라주(원화 프레임·낙관·띠·재구성)로 변형 필수. 월 1회 '계정 상태' 점검 |
| AI 라벨 자동 부착 | Meta는 C2PA·IPTC "AI generated" 메타데이터(Google·OpenAI·Microsoft·Adobe·Midjourney·Shutterstock)를 감지해 "AI info" 라벨. 메타데이터 없이 감지하는 분류기 개발 중이라 밝힘. 2024-09부터 "AI 편집"만 된 콘텐츠는 라벨을 메뉴 안으로. API `is_ai_generated` 필드(2026-06-22) | [공식] [Meta 2024-02-06](https://about.fb.com/news/2024/02/labeling-ai-generated-images-on-facebook-instagram-and-threads/) · [Meta 라벨 접근법](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/) · [changelog](https://developers.facebook.com/docs/instagram-platform/changelog) | 아래 1-1 |

### 1-1. AI 라벨 — 우리 파이프라인에서 메타가 자동 표시할 가능성
- 구조: AI 배경(+편집 실사) → HTML/CSS → Playwright Chromium 스크린샷 → PNG(→JPEG). 스크린샷은 원본 이미지의 C2PA·IPTC 메타데이터를 옮기지 않는다 → **메타데이터 경로 자동 라벨 가능성 낮음(대략 10% 미만, 추정)**.
- 남는 위험: ① 생성기가 픽셀에 심는 비가시 워터마크(Google SynthID 등)가 합성 후에도 일부 남을 수 있음 ② Meta 분류기. 둘 다 공개 근거가 없어 확률 산정 불가 [추정].
- 자동 라벨이 붙어도 페널티 공지는 없다(라벨은 표시일 뿐) [추정]. 세트 01(10/9 AI 없음)과 02~14(AI 배경)의 라벨 유무를 게시 후 앱에서 확인해 실측으로 교체.
- ⚠️ **규범 충돌 메모**: CLAUDE.md "기획서에서 온 고정 규칙"은 "AI 생성물 공개 라벨을 쓴다"이고, 대표 결정(2026-10-02)은 카드·캡션 AI 고지 문구 삭제. 문구 없이 규범을 맞추는 선택지로 API `is_ai_generated=true`(메타 "AI info" 라벨, 사진처럼 보이는 생성물은 Meta 정책상 자가 고지 대상)가 있다. 한국 AI 기본법(2026-01-22 시행)은 표시 의무 주체가 주로 AI 사업자(이용자 아님), 계도기간 1년 이상 [분석] [Stimson](https://www.stimson.org/2026/south-koreas-ai-basic-act-seeking-balance-between-industry-innovation-and-social-risk/). → **D6로 대표 결정 필요**(기본값 미적용).

### 1-2. 2026 기타 변화
- 게시 후 캐러셀 순서 변경 가능(2026-03, 추가는 불가) [분석] [Gulf News](https://gulfnews.com/technology/instagram-finally-allows-users-to-reorder-carousel-posts-everything-you-need-to-know-1.500484465) → 첫 24h 성과 보고 2장 교체 실험 가능.
- Mosseri 2026-07: "사진은 알고리즘상 불이익 없음, 영상이 추천을 더 받을 뿐" [분석] [Kontentino](https://www.kontentino.com/es/preguntas-y-respuestas/instagram-va-a-eliminar-las-fotos/).
- "Your Algorithm"(사용자 주제 조정) 릴스 2025-12 → 피드·탐색 테스트 2026-06 [분석] [TechCrunch 2026-06-27](https://techcrunch.com/2026/06/27/instagram-is-testing-more-ways-for-users-to-customize-your-algorithm) → 주제 일관성(한국 문화 트렌드)이 더 중요해짐 [추정].
- Instagram 유료 구독(2026-06, 상단 노출 포함 보도, 단일 출처) [분석] [fnnews](https://en.fnnews.com/news/202606020621223881) — 비용 상한상 대상 아님.

## 2. 게시 시각·빈도

| 자료 | 내용 | 근거 |
|---|---|---|
| 국내(소셜비즈 ~2,300계정 DM 자동화 로그, 2025-04~06) | 반응은 20시부터 상승, **22시 정점**. 일요일 최고, 금요일 최저 | [분석] [스마트투데이 2025-07-08](https://www.smarttoday.co.kr/ko-kr/articles/85166) |
| 국내(같은 데이터 2025 Q1) | 19시부터 상승, 22시 최다 | [분석] [스마트투데이](https://www.smarttoday.co.kr/ko-kr/articles/76958)(검색 요약) |
| 와이즈앱 2026-07 | 인스타 이용자 2,870만, 1인 월 21시간 27분(SNS 1위). 시간대 자료 없음 | [공식 데이터] [오픈애즈 2026-09-07](https://www.openads.co.kr/content/contentDetail?contsId=20361) |
| Metricool(2,436만 게시물) | 18~21시, 20시가 가장 꾸준. **캐러셀 일요일 19~21시**, 릴스는 자정 무렵 | [분석] [Metricool 2026-06-18](https://metricool.com/best-time-to-post-on-instagram) |
| Hootsuite / Sprout | 평일 오후~저녁 / 화·수 최고, 주말 최저(글로벌) | [분석] [Hootsuite 2026-07](https://blog.hootsuite.com/best-time-to-post-on-instagram) · [Sprout 2026-03](https://sproutsocial.com/insights/best-times-to-post-on-instagram/) |
| Buffer(10.2만 계정·210만 게시물) | 주 1~2회 대비 3~5회 도달 +12%, 6~9회 +18%, 10회+ +24%, 팔로워 성장률도 증가. 많이 올려도 게시물당 도달 감소 없음 | [분석] [Buffer 2025-08-13](https://buffer.com/library/how-often-to-post-on-instagram/) |
| Mosseri | "완벽한 간격은 없다, 유지할 수 있는 만큼." 자주 올려도 불이익 없다는 취지. "주 3~5회"는 공식 수치 아님 | [분석, 2차] [onlinemarketing.de 2025-08-24](https://onlinemarketing.de/social-media-marketing/instagrams-posting-tipp-frequenz-wie-lang-pause) |

- 국내 유료 리포트(오픈서베이·나스미디어·메조·DMC)의 시간대별 인스타 이용은 공개본에서 찾지 못함.
- **검증 결과**: 캐러셀 19:00 = 국내 상승 시작점 + Metricool 캐러셀 창과 일치 → **유지 타당**. 첫 1~2시간 반응이 20~22시 정점과 겹친다 [추정]. 릴스 21:00 = 타당하나 국내 정점 22시·글로벌 자정 경향 → **21 vs 22 2~4주 A/B 권장** [추정].
- **빈도**: 현 계획(캐러셀 매일 + 릴스 병행)은 근거상 해롭지 않고 성장엔 유리. 단 품질 유지가 조건. 권장 범위 = 캐러셀 주 5~7 + 릴스 주 2~4(합계 7~10) [추정]. 요일 가중: 일요일 최우선, 금요일 가장 약한 소재 [추정].

## 3. Threads 교차
- 규모: 국내 Threads MAU 648만(2025-10, 와이즈앱, +34%, 같은 시기 X 760만) [공식 데이터] [다음 2025-11-20](https://v.daum.net/v/3bSk2vLxgE?f=p). 2026-07 SNS 증가율 1위(+29.6%) [공식 데이터] [오픈애즈](https://www.openads.co.kr/content/contentDetail?contsId=20361) → 약 780~800만 추정 [추정]. 20대 37%·30대 25%(2025-07 모바일인덱스) [분석] [인사이트](https://www.insight.co.kr/news/515306).
- 사례: @ai.trend.kr("AI TREND KOREA") Threads 계정 존재만 확인(팔로워·형식 미확인) [공식] [threads.com/@ai.trend.kr](https://www.threads.com/@ai.trend.kr). 다른 국내 카드뉴스 계정의 교차 운영은 검증 자료 없음 → **대표가 앱에서 3~5개 계정 직접 확인 필요**.
- 규칙·효과:
  - 인스타→Threads 교차 공유(사진·캐러셀, 릴스 제외, 캡션 그대로·해시태그는 일반 텍스트) [분석] [PhoneArena](https://www.phonearena.com/news/meta-enables-cross-posting-from-facebook-and-instagram-to-threads_id161730)(검색 요약).
  - 교차 게시 자체의 패널티 공지 없음, 다만 대화형 피드와 결이 안 맞아 도달 낮다는 분석 [분석] [Kontentino](https://www.kontentino.com/q-and-a/common-questions-about-instagram-threads-facebook).
  - Mosseri: 원본 우대·참여 유도형 답글 하향, 링크 게시물 랭킹 개선(2025-06) [분석] [SMT 2025-06-08](https://www.socialmediatoday.com/news/meta-says-link-posts-ranked-properly-threads-reach/750126/).
  - 토픽 태그 게시물당 1개 [분석] [Android Central](https://www.androidcentral.com/apps-software/meta-threads-adds-hashtags).
  - → 자동 공유보다 **캐러셀 카피를 500자 이내 대화형 텍스트로 재작성 + 이미지 2~3장 + 토픽 태그 1 + 질문형 마무리**가 낫다 [추정]. 반말 문화 대비 존댓말 톤 유지는 차별점이 될 수도 [추정].
- API [공식] [Threads 게시 문서](https://developers.facebook.com/docs/threads/posts) · [create-posts](https://developers.facebook.com/docs/threads/create-posts):
  - 2단계(`/{user-id}/threads` → `/threads_publish`), 텍스트 500자, 이미지 JPEG·PNG 8MB, **캐러셀 2~20개**, `link_attachment`, `topic_tag` 파라미터.
  - 한도 24h: 게시 250(캐러셀=1), 답글 1,000. `threads_publishing_limit`로 확인.
  - 권한 `threads_basic`·`threads_content_publish`. **본인·테스터 계정은 앱 심사 없이 게시 가능** → 우리 계정 하나면 자동화 가능.
  - 네이티브 예약 없음 → 인스타와 같은 queue.json + 루틴 구조로 처리.
  - 새 환경변수 필요(이름만 docs/ENV.md에, 예: `THREADS_ACCESS_TOKEN`, `THREADS_USER_ID`) [추정].

## 4. 도구 연동 (Graph API v25.0, 2026-02-18 [공식] [Meta 블로그](https://developers.facebook.com/blog/post/2026/02/18/introducing-graph-api-v25-and-marketing-api-v25))

| 기능 | Graph API (자체 ig_publish.py) | 근거 |
|---|---|---|
| 게시 한도 | **24h 롤링 100건**, 캐러셀=1건(25·50건은 옛 정보). 컨테이너 24h 400개, 컨테이너 24h 후 만료 | [공식] [CP](https://developers.facebook.com/docs/instagram-platform/content-publishing/) · [REF](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media) |
| 캐러셀 장수 | API **최대 10장**(앱은 20). 첫 장 비율이 전체 기준 | [공식] CP |
| 이미지 | **JPEG만**, 8MB, 폭 320~1440, 비율 4:5~1.91:1 | [공식] REF |
| 예약 | **네이티브 예약 없음** → queue.json + 루틴(현 설계 맞음). Meta Business Suite·Metricool은 UI 예약 가능 | [공식, 부재] CP |
| alt text | `alt_text`(1000자) 2025-03-24 추가, 이미지만(릴스·스토리 불가). 캐러셀 자식 지원은 문서 불명 → 실테스트 | [공식] CP / [추정] |
| 협업 태그 | `collaborators` 최대 3명(피드·릴스·캐러셀) | [공식] REF |
| 유료 파트너십 라벨 | `is_paid_partnership` + `branded_content_sponsor_ids`(최대 2) 2026-04-22 추가. **Facebook Login 경로만** | [공식] [changelog](https://developers.facebook.com/docs/instagram-platform/changelog) · CP |
| AI 라벨 | `is_ai_generated` 2026-06-22 | [공식] changelog |
| 음악 | 릴스만(Audio API 2026-06-01), 캐러셀 불가 | [공식] changelog |
| 트라이얼 릴스 | `trial_params` 2025-12-03 | [공식] changelog |
| 사용자 태그·위치 | `user_tags`, `location_id` 지원 / 상품 태그는 문서끼리 상충 | [공식] REF·CP |

- **Metricool MCP**: 공식 원격 서버 `https://ai.metricool.com/mcp`(OAuth) [공식] [help](https://help.metricool.com/how-to-connect-metricools-mcp-eqp9h) · [Metricool 2026-08-27](https://metricool.com/connect-claude-to-instagram/). **무료 플랜에서도 MCP 사용 가능**(플랜 한도 적용) [공식] [limits](https://help.metricool.com/mcp-limits-and-plan-requirements-h72jg). 무료 = 브랜드 1, **예약 월 20건**, 분석 30일, 경쟁사 5 [공식] [pricing](https://metricool.com/pricing/). Starter $20/월(무제한 예약·분석 기간 무제한). 기능: 분석 조회, 예약 생성·관리, 최적 시각(`get_best_time_to_post` 등, 도구명은 미러 기준 [분석]). 불가: 인박스·댓글. UI는 캐러셀 10장 자동 게시·alt·첫 댓글·협업 5명·트라이얼 릴스·Threads 예약 지원, 유료 파트너십은 언급 없음 [공식] [help](https://help.metricool.com/schedule-and-post-on-instagram-6b6q5).
- **역할 분담 제안** [추정]:
  - **ig_publish.py = 유일한 게시 경로**(approved 게이트 보존). 추가할 것: PNG→JPEG 변환, 장별 `alt_text`, 협찬 시 `is_paid_partnership`(Facebook Login 토큰 필요 — 현 경로 확인), 게시 전 `content_publishing_limit` 확인, 10장 상한 검사.
  - **Metricool MCP(무료) = 읽기 전용**: 주간 분석 → `cardnews/reports/`, 경쟁 계정 5개 벤치마크, 최적 시각 데이터로 D4 재검토. 예약 기능은 비상용(월 20건)으로만, 그것도 approved PR 산출물만. 무료 비용 0원으로 월 5만원 상한 유지.
  - Threads: 자체 스크립트(`threads_publish.py`, 같은 게이트) 또는 Metricool 예약 중 택1 — D2 결정 후.
  - 미검증(실테스트 필요): 캐러셀 자식 `alt_text`, Metricool MCP 예약이 alt·협업 필드를 노출하는지.

## 5. 대표 결정 목록 (기본값 미적용 — 대표가 고를 때까지 현 계획 유지)
| # | 결정 | 선택지 | 리서처 추천(1줄) |
|---|---|---|---|
| D1 | 캐러셀:릴스 주간 비율 | 7:0 / 7:3 / 5:5 | **7:3** — 캐러셀은 저장·보내기(게이트), 릴스 3편은 비팔로워 유입(영상이 추천을 더 받음, Mosseri 2026-07). |
| D2 | Threads 교차 여부 | 안 함 / 자동 공유 / 재작성 텍스트판 | **재작성 텍스트판을 C1-1 2주차부터 주 3회 시험** — API 심사 불필요, 비용 0, 4주 후 프로필 유입으로 판단. |
| D3 | 해시태그 수 | 0 / 3 / 5 | **3개** — 공식상 도달 효과 미미, 주제 분류용으로 구체 태그 3개면 충분하고 캡션이 깔끔. |
| D4 | 게시 시각 | 유지(19/21) / 변경 | **캐러셀 19:00 유지, 릴스 21:00 vs 22:00 2주 A/B** — 국내 정점 22시 근거. |
| D5 | 트라이얼 릴스 | 사용 / 미사용 | **팔로워 1,000 도달 시 사용**(그 전엔 자격 없음 가능성 높음), 릴스 훅 A/B용. |
| D6(추가) | AI 표시 방식 | 표시 없음 / API `is_ai_generated` 라벨만 / 문구 복원 | **AI 배경 세트(02~14)는 `is_ai_generated` 라벨만** — 카드·캡션 문구 없이 CLAUDE.md 공개 라벨 규범과 Meta 자가 고지 정책을 맞춤. |

## 6. 자가 검증표
| 성공 기준 | 결과 | 비고 |
|---|---|---|
| 과제 1 알고리즘 10항목 모두 다룸 | ✅ | 1장 표 9행 + 1-1 AI 라벨 |
| 랭킹 가중치는 공식 언급만 | ✅ | 수치 가중치 미공개 명시, 매체 수치는 [분석] 표시 |
| 최근 6개월(2026-04~10) 자료 우선 | ✅ | 원본성 2026-04-30, 파트너십 API 2026-04-22, AI API 2026-06-22, Audio 2026-06-01, Metricool 2026-08~09, Mosseri 2026-09 등 |
| 과제 2 시각·빈도·19/21 검증 | ✅ | 국내 자료 1종(DM 로그 기반, 한계 표시) |
| 과제 3 Threads 사례·규칙·API | △ | API·규칙 ✅, 국내 교차 운영 사례는 @ai.trend.kr 존재만 확인 |
| 과제 4 한도·예약·alt·협업·파트너십·Metricool | ✅ | 캐러셀 자식 alt는 실테스트 필요 |
| 과제 5 D1~D5 추천 1줄 | ✅ | D6 추가 |
| 출처 URL·확인 날짜·추정 표시 | ✅ | 확인 날짜 2026-10-02 일괄, 403 원문은 "검색 요약" 표시 |
| 비밀값 미출력 | ✅ | 환경변수 이름만 |
| 첫 포스트 관련 차단 요소 발견 | ✅ | PNG→JPEG(§0-1) |
