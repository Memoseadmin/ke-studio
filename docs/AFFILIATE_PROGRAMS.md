# 제휴 프로그램 등록부 (대표 가입용)

작성 2026-10-02 · 담당 marketer · 대표 결정 "제휴할 수 있는 건 다 넣어 두고 필요할 때 꺼내 쓴다" 반영.
채널: Korea Explained(EN, 시청자 미국·EU·동남아) + 한국어 인스타 카드뉴스(한국 독자). 금지 품목: 건강·금융·법률·도박·주류(링크·상품 선정 시 제외).
모든 수치는 2026-10-02 WebSearch 확인치. 공식 페이지가 아닌 2차 출처만 있으면 `(2차)`, 못 찾으면 `미확인`. 가입 직전 반드시 공식 약관으로 재확인하고 실측값으로 바꿀 것.

## 성공 기준(작성 전 선언)
1. 후보 전부 + 추가 발견을 표에 넣고 11개 항목(시장·URL·수수료·쿠키·지급·유지·고지·링크규칙·서브ID·변수·우선순위)을 채우거나 미확인 표시 2. "지금 가입 / 첫 업로드 직전 / 필요 시" 분리 3. 대표→COO 전달 값 목록 4. 링크 허브 1안(맨 위 고지) 5. 150행 이내.

## A. 영어권(Korea Explained)
| 프로그램 | 시장 | 가입 URL·조건 | 수수료·쿠키 | 지급 조건 | 유지 조건 | 고지·링크 규칙 | 서브ID | 변수 | 우선순위 |
|---|---|---|---|---|---|---|---|---|---|
| Amazon Associates(US) | 미국. CA·UK·DE·FR·IT·ES는 US 계정 1개의 store ID로 함께 정산(OneLink) | affiliate-program.amazon.com. 채널 URL 제출, 가입 즉시 링크 가능 | 카테고리별 1~20%(대부분 2~5%). 쿠키 24h, 장바구니 담기면 90일 | 직접입금·기프트카드 $10 / 수표 $100. 발생 월말 +60일. 해외 계좌 가능(미확인: 한국 은행 직접입금 여부) | **가입 후 180일 내 적격 판매 3건 없으면 계정 종료**(재가입 가능) | 필수 문구 "As an Amazon Associate I earn from qualifying purchases." 이메일·PDF·eBook·인쇄물·구두 등 오프라인 사용 금지(옵트인 이메일만 예외). 가격 직접 표기 금지 | 트래킹 ID 최대 100개(ID 자체가 서브ID 역할: `ke-ep001-20`) | `AMAZON_ASSOCIATE_TAG`(비밀 아님) | **첫 업로드 직전** |
| Klook Affiliate | 글로벌(미국·EU·동남아·KR 동일 계정) | affiliate.klook.com 직접 또는 Involve Asia·Ecomobi 경유. 승인 2~5일 | 카테고리별 2~20%(투어·호텔 6.5%, 어트랙션 5%, eSIM 20%; 기본 2~5%+보너스 표기도 있음)(2차). 쿠키 30일(호텔·렌터카 7일) | 최소 $50(2차). PayPal·은행이체. 월 정산(검증 T+1, 지급은 그 뒤 최대 90일) | 미확인(비활성 종료 조항 못 찾음) | 일반 FTC/공정위 고지. 주류 투어 상품 제외(우리 규칙) | `aid` + 캠페인 파라미터(`aff_adid`/`aff_ext`, 미확인) | `KLOOK_AFFILIATE_ID`(비밀 아님) | 지금 가입 |
| Trip.com Affiliate | 글로벌 | trip.com/partners 직접(또는 CJ·FlexOffers·Travelpayouts) | 호텔 ~7%, 항공 ~5%, 기차 건당 ~$1.5(2차, 네트워크별 상이). 쿠키 30일 | 직접 프로그램 최소 지급 없음(2차). PayPal·은행·Payoneer, 월 1회 | 미확인 | 일반 고지 | `allianceid`+`sid`, 서브ID 지원 미확인 | `TRIP_AFFILIATE_ID`(비밀 아님) | 지금 가입 |
| Agoda Partners | 글로벌(동남아 강함) | partners.agoda.com. 웹사이트/채널 URL 심사 | 숙박 완료 기준 4%(1~50건)→4.5%→5%, 최대 7%. 쿠키 24h/세션(30일 표기도 있어 상충, 공식 재확인) | **최소 $200**, SWIFT 은행이체. 체크아웃 +30일 후 청구 가능, 150일 내 미청구 시 소멸 | 미확인 | 일반 고지 | `cid` + `tag` 파라미터(미확인) | `AGODA_CID`(비밀 아님) | 지금 가입(승인 보류 가능) |
| Booking.com(CJ·Awin) | 글로벌 | 직접 프로그램 종료(2025). CJ 또는 Awin에서 신청. 18세+, 공개 채널, 승인 3~5일 | 숙박 4%, 렌터카 6%, 어트랙션 4%(CJ). **세션 기반 트래킹(쿠키 없음)** | 네트워크 기준(CJ $50 / Awin $20) | 네트워크 기준 | 일반 고지 | CJ `sid` / Awin `clickref` | `BOOKING_AID`(비밀 아님) | 지금 가입 |
| Airalo(eSIM) | 글로벌 | impact.com에서 Airalo 신청 | 8~12%(네트워크별)(2차). 쿠키 30일 | Impact 기준: 최소 $10, PayPal·은행 | 미확인 | 일반 고지 | Impact `subId1~3` | `AIRALO_IMPACT_ID`(비밀 아님) | 지금 가입 |
| YesStyle | 글로벌(K-뷰티·패션) | Awin(머천트 63156) 또는 ShareASale·Commission Factory | Awin 신규 10%/기존 5%, SAS 10%, 최대 15%. 쿠키 30일 | 네트워크 기준 | 미확인 | 일반 고지 | Awin `clickref` / SAS `afftrack` | `YESSTYLE_AFFILIATE_ID`(비밀 아님) | 지금 가입 |
| Olive Young Global | 150+국(**미국 거주 운영자는 2026-05-29부터 Rakuten US로 이관**; 한국 거주 운영자는 글로벌 프로그램) | global.oliveyoung.com/influencer/main | 최대 13%(판매액 구간별). 쿠키 30일. 건강·웰니스 상품은 우리 규칙상 제외 | PayPal, 포인트 $20 이상 월 1회 출금, 익월 10일 처리. 포인트 2년 유효 | 미확인 | 일반 고지 | 미확인 | `OLIVEYOUNG_AFFILIATE_ID`(비밀 아님) | 지금 가입 |
| KKday | 글로벌(동남아·대만 강함) | FlexOffers·Involve Asia·Ecomobi 경유(직접 포털 미확인) | 기본 ~5%, 프로모션 시 SIM/WiFi 9.6%·투어 6.4%·숙박 4%(2차). 쿠키 30일 | 네트워크 기준 | 미확인 | 일반 고지 | 네트워크 서브ID | `KKDAY_AFFILIATE_ID` | 지금 가입 |
| GetYourGuide | 글로벌(EU 강함) | partner.getyourguide.com | 8%(협상 시 10~12%). 쿠키 31일 | 최소 $50, 매월 5영업일 | 미확인 | 일반 고지 | `partner_id` + `cmp` | `GYG_PARTNER_ID` | 지금 가입 |
| Viator | 글로벌(미국 강함) | viator.com/affiliate 직접 또는 Awin(US 11018) | 8%(상위 12%; Awin 일부 지역 4%). 쿠키 30일. 여행일 경과 후 확정 | 미확인($50 표기 2차 미확정) | 미확인 | 일반 고지 | `pid`+`mcid`+`campaign` | `VIATOR_PID` | 지금 가입 |
| Coupang Global | 해당 없음 | 쿠팡은 한국·대만만 운영, 영어권 제휴 프로그램 없음(YouTube Shopping 제휴는 KR 한정) | - | - | - | - | - | - | 필요 시(해당 없음) |
| Gmarket Global | 미확인 | 직접 프로그램 못 찾음. 링크프라이스 머천트 여부 확인 필요 | 미확인 | 미확인 | 미확인 | - | - | - | 필요 시 |

## B. 한국어(인스타 카드뉴스)
| 프로그램 | 가입 URL·조건 | 수수료·쿠키 | 지급 조건 | 유지 조건 | 고지·링크 규칙 | 서브ID | 변수 | 우선순위 |
|---|---|---|---|---|---|---|---|---|
| 쿠팡파트너스 | partners.coupang.com. 만 19세+, 쿠팡 계정, 채널 URL·본인 계좌·신분증. 가입 즉시 "임시 승인"으로 링크 생성 가능 | 기본 3%(카테고리별 상이, 2차 표기 1~8%). **쿠키 24h** | **1만원 이상** 월 정산, **익익월 15일** 지급. 사업소득 3.3% 원천징수(미확인) | **누적 판매 15만원 달성 후 채널 검토 → 최종 승인**. 최종 승인 전 지급 제한 가능. 임시승인 유효기간 미확인 | 공정위 문구(지정 문구) **"이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."**(2차, 가입 후 도움말 원문 재확인). 콘텐츠 시작 지점·설명란 최상단, 접힘·작은 글씨 금지. 가격 임의 표기 금지 | `subId` 파라미터 지원 | `COUPANG_PARTNERS_ID`(비밀 아님) · API 쓸 때만 `COUPANG_PARTNERS_ACCESS_KEY`/`SECRET_KEY`(비밀) | **첫 업로드 직전**(카드뉴스 첫 게시 직전) |
| 네이버 쇼핑 커넥트 | 2025-07-23 정식 출시. 네이버 블로그·인스타·유튜브 채널 등록. 자격·심사 기준 미확인 | 셀러가 수수료율·조건 결정(상품마다 다름) | 미확인 | 미확인 | 일반 공정위 고지 | 미확인 | `NAVER_CONNECT_ID` | 지금 가입(심사 통과 시) |
| 알리익스프레스 어필리에이트 | portals.aliexpress.com | 3~9%. **쿠키 3일**. 확정까지 60일 | **최소 $16**, 국제 은행이체, 건당 수수료 $15 | 미확인 | 일반 고지 | 트래킹 ID 다중 생성 | `ALIEXPRESS_TRACKING_ID` | 필요 시(수수료 $15 때문에 묶음 출금) |
| 링크프라이스 | linkprice.com → 인플루언서 가입, CPS/CPA 선택. 브랜드 다수(G마켓·11번가·야놀자 등 머천트 포함 여부 미확인) | 머천트별 상이 | 미확인(최소 지급·주기) | 미확인 | 일반 고지 | `a_id` + 커스텀 파라미터(미확인) | `LINKPRICE_AFFILIATE_ID` | 지금 가입 |
| 텐핑 | tenping.kr. 캠페인 선택형(CPC·CPA·CPS) | 캠페인별 | 미확인(최소 출금·수수료) | 미확인 | 일반 고지 | 미확인 | `TENPING_ID` | 필요 시 |
| 11번가·지마켓 직접 제휴 | 자체 어필리에이트 프로그램 못 찾음 → 링크프라이스 경유 확인 | - | - | - | - | - | - | 필요 시 |
| 야놀자·여기어때 | 직접 프로그램 없음. 모멘트스튜디오 '세시간전' 또는 링크프라이스 경유 CPS(2차) | 미확인 | 미확인 | 미확인 | 일반 고지 | 미확인 | - | 필요 시 |
| 클룩 KR | A의 Klook 글로벌 계정 하나로 KR 링크 생성(원화 지급 여부 미확인) | A와 동일 | A와 동일 | - | - | - | 공용 | 지금 가입(A와 함께) |

## C. 네트워크(한 계정으로 브랜드 다수)
| 네트워크 | 최소 지급·수단 | 유지 조건 | 서브ID | 브랜드 예(관광·항공·숙박·뷰티) | 변수 |
|---|---|---|---|---|---|
| Impact | $10, PayPal·은행(다통화) | 미확인 | `subId1~3` | Airalo. Korean Air(미주→아시아 1.6%, 쿠키 10일, **현재 모집 종료**) | `IMPACT_PUBLISHER_ID` |
| CJ Affiliate | $50, 직접입금·Payoneer | 장기 무실적 비활성화 가능(미확인) | `sid` | Booking.com, Trip.com(일부 지역) | `CJ_PUBLISHER_ID` |
| Awin | $20/€20/£20, 은행·Payoneer·PayPal | 미확인 | `clickref` | Booking.com, Viator(US·CA·EU), YesStyle | `AWIN_PUBLISHER_ID` |
| ShareASale(Awin 소유) | $50, 수표·ACH·Payoneer | 미확인 | `afftrack` | YesStyle | `SHAREASALE_AFFILIATE_ID` |
| Partnerize | £20/$30/€30 월 단위 | 미확인 | `pubref` | 입점 브랜드 미확인(여행·항공 다수 표기, 개별 확인 필요) | `PARTNERIZE_PUBLISHER_ID` |
| Rakuten Advertising | 미확인 | 미확인 | `u1` | Olive Young US(미국 거주 운영자용) | 필요 시 |
| Involve Asia·Ecomobi·FlexOffers | 미확인 | 미확인 | 네트워크별 | Klook·KKday·Olive Young Global(동남아 중계) | 필요 시 |
한국관광공사·롯데면세점·아시아나 제휴 프로그램은 못 찾음(미확인). 모든 네트워크 ID는 링크에 노출되므로 비밀 아님.

## 결론 1. 가입 시점
- **지금 가입(가입만으로 불이익 없음)**: Klook, Trip.com, Agoda, Booking.com(CJ/Awin), Airalo(Impact), YesStyle(Awin), Olive Young Global, KKday, GetYourGuide, Viator, 네이버 쇼핑 커넥트, 링크프라이스, 네트워크 계정 5개(Impact·CJ·Awin·ShareASale·Partnerize).
- **첫 업로드 직전 가입(유지 조건 있음)**: Amazon Associates(180일 내 3건 판매 없으면 종료) → EP001 업로드 1주 전. 쿠팡파트너스(누적 15만원 전엔 최종승인·지급 제한) → 카드뉴스 첫 게시 1주 전.
- **필요 시**: 알리익스프레스(출금 수수료 $15), 텐핑, Gmarket Global, 11번가·지마켓, 야놀자·여기어때(경유 경로 확인 후), Rakuten(미국 거주 전환 시).
- 유지 조건이 확인된 프로그램: Amazon(180일·3건), 쿠팡(15만원 최종승인), Agoda(150일 미청구 소멸), Olive Young(포인트 2년), CJ(장기 무실적, 미확인).

## 결론 2. 대표가 가입 후 COO에게 전달할 값
| 변수 | 비밀 여부 | 비고 |
|---|---|---|
| `AMAZON_ASSOCIATE_TAG` | 비밀 아님, 채팅 전달 가능 | 기본 트래킹 ID. 영상별 ID(`ke-ep001-20`)는 COO가 대시보드에서 추가 요청 |
| `COUPANG_PARTNERS_ID` | 비밀 아님 | 링크의 파트너 식별자. `subId`는 COO가 `ke-EPxxx-<상품>`로 붙임 |
| `COUPANG_PARTNERS_ACCESS_KEY` / `COUPANG_PARTNERS_SECRET_KEY` | **비밀** | 딥링크 API 자동화 시에만. 클라우드 환경변수에 직접 입력, 채팅 금지 |
| `KLOOK_AFFILIATE_ID`, `TRIP_AFFILIATE_ID`, `AGODA_CID`, `BOOKING_AID`, `GYG_PARTNER_ID`, `VIATOR_PID`, `KKDAY_AFFILIATE_ID`, `OLIVEYOUNG_AFFILIATE_ID`, `YESSTYLE_AFFILIATE_ID`, `AIRALO_IMPACT_ID`, `ALIEXPRESS_TRACKING_ID`, `NAVER_CONNECT_ID`, `LINKPRICE_AFFILIATE_ID`, `TENPING_ID` | 비밀 아님 | 전부 URL에 노출되는 값 |
| `IMPACT_PUBLISHER_ID`, `CJ_PUBLISHER_ID`, `AWIN_PUBLISHER_ID`, `SHAREASALE_AFFILIATE_ID`, `PARTNERIZE_PUBLISHER_ID` | 비밀 아님 | 네트워크 로그인 비밀번호·API 토큰은 전달하지 않음 |
| 각 프로그램 승인 상태·날짜 | - | "승인 / 심사 중 / 반려" 한 줄씩. Amazon·쿠팡은 가입일 기록(180일·15만원 카운트 기준) |
위 변수 이름은 공급자 확정 후 `docs/ENV.md` 표에 COO가 추가(이 문서는 ENV.md를 수정하지 않음).

## 결론 3. 링크 허브(프로필 링크) 구성 1안
도구: 무료 링크 허브(Linktree 등) 또는 GitHub Pages 정적 페이지 1장. EN·KR 각 1개. 모든 링크 서브ID `ke-hub-<상품>`.
```
[맨 위 고정 고지]
EN: Disclosure: Some links below are affiliate links. I may earn a commission at no extra cost to you.
    As an Amazon Associate I earn from qualifying purchases.
KR: 이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.
1. 최신 에피소드(YouTube)                      ← 비제휴, 맨 위
2. 이번 편 상품 3개(에피소드 바뀔 때 교체)      ← Amazon / Klook / Airalo
3. 한국 여행 준비: eSIM(Airalo) · 투어(Klook) · 숙소(Agoda 또는 Booking)
4. K-뷰티·식품: YesStyle · Olive Young Global
5. (KR 허브) 카드뉴스 소개 상품(쿠팡) · 네이버 쇼핑 커넥트 링크
6. 채널 멤버십·대본 노트 안내(멤버십 개시 후)
```
규칙: Amazon 링크는 허브(웹)에는 가능, 이메일·PDF엔 금지. 허브 자체에 "AI 생성 음성·이미지 사용" 한 줄 추가. 건강·금융·법률·도박·주류 상품 링크 금지.

## 자가 검증
| 기준 | 결과 |
|---|---|
| 후보 전부 + 추가 발견 수록 | 통과: A 13 · B 8 · C 7 = 28행(추가: Rakuten, Involve Asia·Ecomobi·FlexOffers, 세시간전) |
| 11개 항목 채움 또는 미확인 표시 | 통과: 미확인 항목 모두 명시(아래 목록) |
| 지금/직전/필요 시 분리 | 통과(결론 1) |
| 전달 값 목록·비밀 여부 | 통과(결론 2, 비밀은 쿠팡 API 키 2개만) |
| 링크 허브 1안·맨 위 고지 | 통과(결론 3) |
| 150행 이내·한국어·git 미사용·비밀키 파일 미접근 | 통과 |
| 미확인(가입 시 공식 페이지로 확인) | 쿠팡 지정 문구 원문·임시승인 기간·원천징수, Klook 최소 지급·서브ID, Trip.com 서브ID, Agoda 쿠키(24h vs 30일)·tag, Olive Young 서브ID, Viator 최소 지급, 네이버 커넥트 자격·지급, 링크프라이스·텐핑 지급 조건, 11번가·지마켓·Gmarket Global·야놀자·여기어때 경유 경로, CJ 비활성 규정, Partnerize 브랜드, 한국 은행 Amazon 직접입금 |

## 출처(확인 2026-10-02)
Amazon: affiliate-program.amazon.com/help/operating/compare · unilink.us/blog/amazon-associates-guide-2026 · conductatlas.com(Operating Agreement 고지·오프라인 금지) · geniuslink.com/blog/amazon-associates-earn-globally-initiative · affiliate-program.amazon.com/help/node/topic/G84KVZ7BTNXHF4UH
쿠팡: choicemon.com/coupang-partners-signup-guide · jab-guyver.co.kr/3067, /3699 · calcnara.com/guides/coupang-partners-guide · foxcg.com/coupang-partners-instagram · adsensefarm.kr(공정위 문구)
Klook: involve.asia/?p=36792 · ecomobi.com/ecomobi/klook-affiliate-program-review · uppromote.com/affiliate-directory/klook · kyodonewsprwire.jp/release/202607162696(KTO MoU)
Trip.com: sg.trip.com/ask/questions/trip.com-affiliate-program.html · uppromote.com/affiliate-directory/trip-com · flexoffers.com(trip-com-apac)
Agoda: track360.io/blog/agoda-affiliate-program-operator-teardown-2026 · uppromote.com/affiliate-directory/agoda · partnerhub.agoda.com(Bank Transfer)
Booking.com: track360.io/blog/booking-com-affiliate-partner-program-operator-teardown-2026 · netinfluencer.com(Awin 이관) · makeinfluence.com/en/academy/booking-coms-affiliate-program
Airalo: travelpayouts.com/en/offers/airalo-partner-program · flexoffers.com/affiliate-programs/airalo-affiliate-program · linkclicky.com/affiliate-program/airalo
YesStyle: ui.awin.com/merchant-profile/63156 · uppromote.com/affiliate-directory/yesstyle · commissionfactory.com(59459)
Olive Young: global.oliveyoung.com/influencer/main · help.global.oliveyoung.com/hc/en-au/articles/16665087814927 · help.us.oliveyoung.com/hc/en-us/articles/57704134295961 · app.involve.asia/directory/olive-young-global-affiliate-program
KKday: ecomobi.com/?p=52792 · flexoffers.com/affiliate-programs/kkday-affiliate-program · involve.asia/?p=58561
GetYourGuide: petraontheway.com/en/review-getyourguide-affiliate-program · affilimate.io/programs/getyourguide-affiliate-program
Viator: ui.awin.com/merchant-profile/11018 · track360.io/blog/best-travel-affiliate-programs-2026-operator-rate-card-benchmark
Coupang Global: kedglobal.com/newsView/ked202406050016 · en.wikipedia.org/wiki/Coupang
네이버: navercorp.com/media/pressReleasesDetail?seq=32355 · inews24.com/view/1830058 · heraldk.com/article/2025072218190389988
알리: uppromote.com/affiliate-directory/aliexpress · strackr.com/blog/aliexpress-affiliate-program · diggitymarketing.com/best-affiliate-programs/aliexpress
링크프라이스·텐핑·야놀자: tilnote.io/pages/6aa038168a847deea1859f0d · k-calc.com/events/tenping-side-income-marketing · newsspace.kr/news/article.html?no=4830(세시간전)
네트워크: help.impact.com(How Do Partners Get Paid) · success.awin.com/articles/en_US/Knowledge/What-are-the-payment-thresholds · uppromote.com/affiliate-program-directory/cj · unilink.us/blog/shareasale-guide-2026 · help.creator.expediagroup.com/hc/en-us/articles/15185855539223(Partnerize 임계) · flexoffers.com/affiliate-programs/korean-air-affiliate-program · affi.io/m/korean-air
