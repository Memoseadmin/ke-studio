# 책가도 노트 시각 벤치마크 — 박물관·헤리티지 18계정 + 혼합 사례 6 + 3판 진단 + 4판 와이어프레임

작성 2026-10-02 · 리서처(디자인). 대표 지시(2026-10-02): "채널 성공 가능성을 높이는 벤치마크를 더. 지금은 너무 구리다."
대표의 3판 평가: "원화만으론 영양소 부족, AI 이미지·사진 결합 필요."
함께 볼 문서: `cardnews/docs/BENCHMARK.md` §2 C안(레이아웃 틀), `cardnews/main:cardnews/docs/DESIGN_SOURCES.md` §1·§2·§5, 디자인 시스템 `episodes/EP001/design/design-system.md` §8·§9(브랜치 `claude/admiring-clarke-beyyoi`).

## 0. 한 장 요약
| 질문 | 답 |
|---|---|
| 잘하는 계정은 뭐가 다른가 | ① **디테일과 전체를 오간다**(Rijksmuseum 3×3 디테일 표지, 대구간송 천원권→원화→디테일, 구글 Zoom 55→90%) ② **원화 위에 본문을 얹지 않는다**(리움·V&A·Rijks·뮷즈는 0) ③ **실물↔그림 비교**에서만 사진을 섞는다 ④ 출처는 **이미지 안 소자 + 캡션 블록 두 겹** ⑤ 반응 1위는 "고르게 하는 질문"·"일상 물건 연결"·"저장해 쓰는 실용물(달력·배경화면)" |
| 3판이 왜 빈약한가 | 원화 2점으로 8장을 채워 **같은 남색·노란 책더미가 6장 반복**. 사진 0·AI 0. 코드 그래픽은 **흰 종이 박스 4개가 그림을 덮는 같은 문법**. 본문 띠 7장이 같은 높이라 리듬이 없음. 본문 평균 약 30자 2줄로 정보 밀도가 낮음 (§3) |
| 4판 방향 | 장마다 **주인공 1개 + 조연 1개**. 역할 고정: 원화 = 표지·클라이맥스·비교 기준 / 사진 = 오늘의 실물·증거 / AI 플레이트 = 배경·여백 / 코드 = 숫자·서체·달력. 바탕·그레인은 렌더러가 공통으로 입힌다 (§2·§3) |
| AI 플레이트 톤 | 지금 접미사("flat editorial illustration, bold clean ink outlines")가 클립아트로 끌고 간다. **"광물안료·은은한 음영·하단 1/3 비움"** 쪽으로 바꾼다 (§4) |
| 대표 결정 | V1 이미지 비율 / V2 플레이트 스타일 / V3 출처 표기 (§5, 기본값 미적용) |

## 확인 방법과 한계 (먼저 읽기)
- **게시물 검증**: instagram.com은 로그인 벽이 있다. 그래서 계정마다 **프로필 공개 embed**(`instagram.com/{handle}/embed/`)에서 팔로워 수와 최근 게시물 약 6~12개를 받았다. 이어서 게시물 embed(`/p/{shortcode}/embed/captioned/`)의 contextJSON으로 **게시자 계정이 일치하는지** 확인했다. 아래 URL은 모두 일치를 확인한 것이다(2026-10-02).
- **✔ 직접 관찰**: 캐러셀 슬라이드를 스크래치패드에만 받아 표지·중간·마지막 장을 눈으로 봤다. 저장소에는 넣지 않았다(저작권). 이 문서에는 링크만 둔다.
- **반응 지표**: 저장 수는 공개되지 않는다. **좋아요(L)+댓글(C)을 대리 지표로** 썼다. 최근 게시물 안에서만 비교한 값이며 하루치 스냅샷이다 → 숫자는 모두 **(추정)**으로 본다.
- **팔로워**: 2026-10-02 embed 값. 바뀌므로 (추정).
- **핸들 정정**(지시문 예시와 다름): 국립민속박물관 = **@tnfmk**, 간송 = **@kansongart**(재단) + @kansongart.daegu, 리움 = **@leeummuseumofart**, 아모레퍼시픽미술관 = **@amorepacificmuseum**, 뮷즈 = **@muds_museumgoods**, 클리블랜드미술관 = **@clevelandmuseumofart**(@clevelandart는 다른 계정), 구글 = **@googleartsculture**, 스미소니언 = 한국·동아시아 관련성이 높은 **@natasianart**(국립아시아미술관) + 보조 @smithsonian.
- **혼합 사례(§2)**: 인스타 게시물은 검색으로 shortcode를 찾지 못했다. 그래서 공식 페이지·기사 URL로 대체했다(모두 HTTP 200 확인). 이미지를 직접 본 것은 사례 5(조선미녀)뿐이고, 나머지 시각 묘사는 기사 내용과 △ 추정이다.
- 요청은 15계정이었지만 국내 기관 6 + 해외 7 + 개인 작가 5 = **18계정**을 분석했다. 개인 작가 중 2명(⑰⑱)은 팔로워 6천 명 미만이라 문법 참고용으로만 쓴다.

## 1. 계정 분석 18 (국내 기관 6 · 해외 7 · 민화·동양화 작가 5)

열 설명: ①크롭 문법 ②타이포·그래픽 결합 ③사진·일러스트·AI 혼합 ④색·여백·띠 ⑤출처 표기 ⑥반응 높은 유형. 표시가 없으면 ✔ 관찰, △는 추정.

### 1-1. 국내 기관
| # | 계정(팔로워) | 공개 게시물 (L / C / 장) | ① 크롭 | ② 타이포·그래픽 | ③ 혼합 | ④ 색·여백·띠 | ⑤ 출처 표기 | ⑥ 반응 높은 유형 |
|---|---|---|---|---|---|---|---|---|
| 1 | 국립중앙박물관 @nationalmuseumofkorea (약 27.6만) | [Dd0YnhMAS9Y](https://www.instagram.com/p/Dd0YnhMAS9Y/) 14,599/193/7 · [Dd2qES-k3vv](https://www.instagram.com/p/Dd2qES-k3vv/) 2,520/13/10 · [Dd5v-UhDZ5A](https://www.instagram.com/p/Dd5v-UhDZ5A/) 857/5/5 | 진열 상태 사진 → 클로즈업 → 설명 패널. 마지막 장은 깨끗한 배경의 유물 단독컷 | 슬라이드엔 글자 거의 없음. 예외: 전시 포스터 〈우리들의 밥상〉 = **초대형 굵은 한글 제목 위에 풍속화 인물 누끼를 겹치고**, 좌우 여백에 세로 국·영 정보 | 참여자 사진 + 유물 나란히. AI 없음 | 크림 바탕, 갈색 단색 서체 | 캡션 끝 `📍전시품 정보 / 명칭 \| 시대 \| 기증(건희2082)`. 외부 사진은 이미지 안 하단 소자 © + 캡션 반복 | 참여형 이벤트 후속(일반 유물 소개의 약 17배) |
| 2 | 국립민속박물관 @tnfmk (약 3.7만) | [Dd5KNSzE6-h](https://www.instagram.com/p/Dd5KNSzE6-h/) 186/3/3 · [Dd8UqumFORE](https://www.instagram.com/p/Dd8UqumFORE/) 127/1/8 | 소장품(수저집 자수)을 일러스트로 재해석해 달력 배경화면. 마지막 장은 흰 바탕 원본 유물 단독 | 사진 위 01~07 번호 배지, 붓글씨풍 금색 + 굵은 고딕, 가는 구분선 + "대표 \|" 라벨, 우하단 ">>>" | **원본 유물 → 일러스트 재해석 → 기기 목업** | 검정 + 금색 포인트, 달력은 주홍 띠 | 유물명을 이미지 하단 중앙에 국/영 두 줄 | **저장해 쓰는 달력·배경화면**이 1위 |
| 3 | 간송미술문화재단 @kansongart (약 2.2만) + @kansongart.daegu (약 2.0만) | [Dd3UuNHEeFt](https://www.instagram.com/p/Dd3UuNHEeFt/)(대구) 740/7/7 · [DbUVT9wkr-a](https://www.instagram.com/p/DbUVT9wkr-a/) 507/11/3 · [DYoFN3MEj27](https://www.instagram.com/p/DYoFN3MEj27/) 429/3/6 | **천원권 → 지폐 확대 → 원화 전체(흰 여백 위) → 지폐·원화 위아래 비교 → 정자 속 이황 디테일.** 전체↔디테일 문법이 가장 뚜렷함 | 표지: 원화 + 하단 어두운 그라데이션 + 흰 고딕 제목 2줄 + 본문 4줄 | 흑백 아카이브 사진 + 현장 사진 + 실물 지폐 사진 | 넓은 흰 여백, 수묵 회색 | 원화 장 하단 소자 "《퇴우이선생진적첩》〈계상정거〉 정선, 조선 1746, 종이에 수묵, 보물, 삼성문화재단". 캡션 "소장품 정보" 블록 + 소장처 계정 태그 | **"천원에서 보던 그림이?" 일상 물건 연결 훅**이 1위 |
| 4 | 리움 @leeummuseumofart (약 22.1만) | [Ddp6eWGh50R](https://www.instagram.com/p/Ddp6eWGh50R/) 5,161/28/1 · [DdltNGpAae2](https://www.instagram.com/p/DdltNGpAae2/) 864/6/3 · [Dd1IpZkAWop](https://www.instagram.com/p/Dd1IpZkAWop/) 465/3/7 | 3:2·3:4 작품 사진, 원경 → 디테일 → 재료 매크로 | **작품 위 글자 0.** 행사 공지는 노랑·하늘 2색 그로테스크 포스터로 따로 | 사진만 | 검정·흰 여백 | 캡션 끝 밑줄 구분선 + `작가/제목/연도/재료/크기` 국·영 2블록 + 📷 사진가 태그 | 명절 인사 단일 사진(캐러셀의 6~10배) |
| 5 | 아모레퍼시픽미술관 @amorepacificmuseum (약 9.9만) | [DcSONIuE46w](https://www.instagram.com/p/DcSONIuE46w/) 947/6/1 · [Dc2V0-nErsQ](https://www.instagram.com/p/Dc2V0-nErsQ/) 483/6/1 | 설치 전경 풀블리드(최근엔 캐러셀 없음) | 얇은 기하 산세리프 대문자 + 하단 날짜 띠, 또는 **두꺼운 검정 프레임 제목 박스 2단 + 아래 작품("포스터 프레임")** | 사진만 | 무채색 타이포, 작품 색만 | △ 캡션 [전시 소개] 대괄호 라벨 | 사전예약 오픈 공지 |
| 6 | 뮷즈 @muds_museumgoods (약 7.2만) | [Dd0mXflj58q](https://www.instagram.com/p/Dd0mXflj58q/) 3,062/19/9 · [Dd70yMQD32h](https://www.instagram.com/p/Dd70yMQD32h/) 119/–/17 | 상품 = 단색 배경(버건디·코발트·회색) 스틸라이프. 유물은 흰 배경 누끼 | 상품 위 글자 0, 도록 표지를 이어 붙여 타이포 대신 | **유물 사진 + 도록 스캔 + 상품 연출 사진** | 한 장에 단색 배경 1, 여백 많음 | **이미지 좌상단 소자 "출처 : 국립광주박물관"을 매 장 반복**(가장 간결) | 아이돌 협업 압도적, 정보형 낮음 |

### 1-2. 해외 기관
| # | 계정(팔로워) | 공개 게시물 (L / C / 장) | ① 크롭 | ② 타이포·그래픽 | ③ 혼합 | ④ 색·여백·띠 | ⑤ 출처 표기 | ⑥ 반응 높은 유형 |
|---|---|---|---|---|---|---|---|---|
| 7 | The Met @metmuseum (약 473만) | [Ddy-_Qkl5Km](https://www.instagram.com/p/Ddy-_Qkl5Km/) 5,905/27/5 · [Dd9UwPdla7l](https://www.instagram.com/p/Dd9UwPdla7l/) 영상 11,048/151 · [DdrQPNNgnM4](https://www.instagram.com/p/DdrQPNNgnM4/) 영상 5,492/54 | 현장 사진 → 포스터 카드 → 현장 사진 **샌드위치**. 유물 컷아웃이 하단 프레임 밖으로 넘침 | 굵은 컨덴스드 산세리프 대문자, 크림·짙은 초록 2톤 교차 | 행사 사진 + 그래픽 카드, 보존처리는 영상 | 단색 핑크 바탕 + 듀오톤 초록 유물, 띠 없음 | 캡션 끝 `___` 뒤 "작가. 제목, 연대. 지역. 재질. 기증처, 소장번호. 전시실" | 이동·설치·보존처리 비하인드 영상 |
| 8 | 클리블랜드미술관 @clevelandmuseumofart (약 15.1만) | [Ddtrcf-IDjj](https://www.instagram.com/p/Ddtrcf-IDjj/) 1,361/4/6 · [Dd6oxH6OAJj](https://www.instagram.com/p/Dd6oxH6OAJj/) 영상 574/4 | 작품 단독 크롭 없이 **관람객이 작품 앞에 선 모습**·전시실 원경 | 이미지 위 글자 없음 | 행사 스냅·전시실 사진 | 고채도 무보정 | 캡션 "🌄: 제목, 연도. 작가(국적, 생몰년). 1965.233" | △ 전반적으로 낮음. 카드 디자인 벤치마크 가치 낮음 |
| 9 | Rijksmuseum @rijksmuseum (약 115만) | [Dd37yiXFPRd](https://www.instagram.com/p/Dd37yiXFPRd/) **15,537/351**/10 · [Dd1XAuAG8aC](https://www.instagram.com/p/Dd1XAuAG8aC/) 3,666/132/3 · [Dd9FaA9FI1a](https://www.instagram.com/p/Dd9FaA9FI1a/) 3,498/62/9 | **표지 = 3×3 디테일 그리드(귀걸이 9개), 2~10장 = 각 초상 전체.** 한 작품을 3구역으로 나눠 풀블리드. 전시장 전경 → 디테일 | 이미지 위 텍스트·로고·프레임 0 | 소장품 이미지 + 전시실 실물 사진(얕은 심도) | 작품 원색, 풀블리드, 여백 없음 | 캡션 "🖼️ 제목, 작가, 연도" 한 줄씩 + "👁️ id.rijksmuseum.nl/…" 영구 링크 | **"Which … catches your eye?" 고르게 하는 질문 + 디테일 비교 그리드** |
| 10 | V&A @vamuseum (약 213만) | [Ddy_bpoioyW](https://www.instagram.com/p/Ddy_bpoioyW/) 6,107/115/4 · [Dd9S60NG6ra](https://www.instagram.com/p/Dd9S60NG6ra/) 2,047/40/5 · [Dd6tzugNze4](https://www.instagram.com/p/Dd6tzugNze4/) 영상 10,210/80 | 한 장에 한 점. 표지만 극단 클로즈업 | 이미지 위 텍스트 0 | 회색·검정 그라데이션 배경 소장품 사진만 | 중성 배경, 오브젝트 색이 유일한 강조 | 캡션에 슬라이드 번호를 맞춰 "1. Shoes, pink satin…, 1958-1960." | **"Which pair would you wear?" 번호 투표형** |
| 11 | 스미소니언 국립아시아미술관 @natasianart (약 7.5만) + @smithsonian (약 120만) | [Ddti3rqEUpq](https://www.instagram.com/p/Ddti3rqEUpq/) 309/1/8(한국 작품 포함) · [Dd1RdZkl1iu](https://www.instagram.com/p/Dd1RdZkl1iu/) 143/2/3(고려청자) · [Dd6uJ03l4u6](https://www.instagram.com/p/Dd6uJ03l4u6/) 187/33/7 · [Dd1IsDSF4ty](https://www.instagram.com/p/Dd1IsDSF4ty/)(@smithsonian) 4,589/31/3 | 디테일 → 전체 → 다른 작품. 마지막 3장은 **족자 하나를 가로 파노라마로 분할**. **슬라이드 경계를 넘어 이어지는 심리스 캐러셀** | 연회색 바탕 휴머니스트 산세리프 2~4줄, 위치 핀 + "Gallery 13" 라벨 | 보도 사진 + 전시실 + 컷아웃 + 두루마리 크롭 콜라주 | **한지·비단 베이지, 연회색 단색면** | 캡션 풀 크레딧(작가·제목·연대·국가·재질·크기·소장·F번호) | 인물·이슈와 엮은 경로형 캐러셀(C33) |
| 12 | 대영박물관 @britishmuseum (약 257만) | [Dd8jkK3Arr2](https://www.instagram.com/p/Dd8jkK3Arr2/) 영상 2,547/30(**'Korea' 전시**) · [Dds37_PglUi](https://www.instagram.com/p/Dds37_PglUi/) 영상 3,551/121 · [Dd0mUE9Af9S](https://www.instagram.com/p/Dd0mUE9Af9S/) 영상 1,862/19 | **〈일월오봉도〉 디테일(소나무·파도) 단독 풀블리드 표지** → 책가도 노트에 가장 가까운 레퍼런스 | 초대형 흰 그로테스크 "Korea" + 가는 서브타이틀, 좌상단 세리프 로고 | 실사 재연 + 양피지 두루마리 일러스트 말풍선 | 작품의 군청·적색을 키컬러로 | **이미지 안 하단 소자 이탤릭 "Sun, Moon and Five Peaks (detail), © National Museum of Korea."** + 캡션 반복 | "On this day" 역사 재연 영상 |
| 13 | Google Arts & Culture @googleartsculture (약 61.5만) | [Dd1kp1sF2CP](https://www.instagram.com/p/Dd1kp1sF2CP/) 200/2/8 · [Dd3fe2SguRS](https://www.instagram.com/p/Dd3fe2SguRS/) 227/3/7 · [DdrHHudjDtW](https://www.instagram.com/p/DdrHHudjDtW/) 영상 512/24 | **"Look Closer" 표지 → Zoom 55%→70%→75%→90% 디테일 → 마지막 2장 전체** | 흰 Google Sans, **하단 중앙 반투명 알약 라벨 "Zoom 70%"**, 형광펜 띠 헤드라인, 원형 스티커 | 앱 스크린샷·폰 목업 + AI 기능 이미지(셀피 합성), "powered by conversational AI" 명시 | 다크(#111) + 작품 원색 | 캡션 이모지 목록 "작품명 / 🎨 작가 / 📅 연도 / 🏛️ @소장기관" | 실험 영상(캐러셀은 낮음) |

### 1-3. 민화·동양화 기반 개인 작가
| # | 계정(팔로워) | 공개 게시물 (L / C / 장) | ① 크롭 | ② 타이포·그래픽 | ③ 혼합 | ④ 색·여백·띠 | ⑤ 출처 표기 | ⑥ 반응 높은 유형 |
|---|---|---|---|---|---|---|---|---|
| 14 | 혜진(고양이 민화) @rockcobok (약 2.5만) | [DdWRiRcEt8S](https://www.instagram.com/p/DdWRiRcEt8S/) 724/4/5 · [Dd6TSx3kmBJ](https://www.instagram.com/p/Dd6TSx3kmBJ/) 481/3/3 | 한지 채색 원화 전체, 낙관 보이게 | 전시 포스터: 세로쓰기 붓글씨풍 명조 + 작은 세로 문구, 원화 아래 넓은 여백 | **실제 고양이 사진(폴라로이드) ↔ 원화 나란히** = 실물→그림 서사. 설치컷 | 한지 황토, 여백 | 캡션 첫 줄 "제목 / 29*34 / 한지에 채색 / 2026" | 명절 단일 그림, 개인 서사 캐러셀 |
| 15 | 한국화가 김현정 @hyunjung_artist (약 9.9만) | [DbSmS9Pknya](https://www.instagram.com/p/DbSmS9Pknya/) C6/5 · [DbAgB4DEmdx](https://www.instagram.com/p/DbAgB4DEmdx/) C3/4 (좋아요 숨김) | 드라마 세트에 걸린 원화 사진·스틸컷, 마지막 장 원화 단독 | **완전한 카드뉴스형**: 하단 어두운 그라데이션 + 굵은 고딕 2줄, 핵심어 살구색, 작품명 노란색, 표지 라벨 배지 | 드라마 스틸 + 폰 목업 + 이모티콘 그리드 | 반투명 어두운 오버레이 | 마지막 장 "작가, <제목>, Ø120 cm, 한지 위에 수묵과 담채, 콜라주" | **대중매체(드라마) 연결** |
| 16 | 동양화작가 윤이크 @yooniqueart (약 2.8만) | [Dcv5nApCf3_](https://www.instagram.com/p/Dcv5nApCf3_/) 312/5/4 · [DdaHaaiH202](https://www.instagram.com/p/DdaHaaiH202/) 150/1/7 | 수묵담채를 흰 배경 누끼로 4:5 위 2/3에 | **강의 캐러셀: 크림 바탕 + "01 재료·먹의 농담" 번호 라벨 + 굵은 고딕 제목 + 국문 본문 + 작은 영문, 우하단 이름 + 붉은 인장, 마지막 장 "저장 추천 / Save This" 알약 배지** | 작품만 | 크림·먹·붉은 인장 1 | 모든 장에 이름·인장 반복 | 글자 없는 작품 캐러셀 > 강의 공지 |
| 17 | 모던민화 서하나 @modernminhwa (약 5.7천, 소규모) | [DdT9zUSCeFE](https://www.instagram.com/p/DdT9zUSCeFE/) 55/–/3 · [Dd2umfVCdZx](https://www.instagram.com/p/Dd2umfVCdZx/) 24/–/7 | 브랜드 협업(궁중비책)용 민화 장면을 배경판으로, 동물을 구도마다 재배치 | 질문형 명조 대제목을 하늘 여백에, "ARTIST INTERVIEW" 라벨 + 검정 띠, 상품 장에 반투명 흰 패널 | **민화 배경 + 상품 실사 합성** | 분홍·연두 파스텔 | 리그램 배지 + 캡션 "아트워크 by" | 작품 단독 > 인터뷰 텍스트 |
| 18 | 김경희 달항아리 민화 @kim_kyonghee (약 5.6천, 소규모) | [DdelWX0PzOz](https://www.instagram.com/p/DdelWX0PzOz/) 141/2/1 · [DdmGgkajyu_](https://www.instagram.com/p/DdmGgkajyu_/) 60/–/3 | **전체(1:1) → 꽃 디테일 → 잎 디테일**, 디테일은 꽉 찬 블리드 | 글자 없음 | — | 금박·미색 | 캡션 《시리즈》 + 연월 | 단일 이미지 > 캐러셀 |

### 1-4. 18계정에서 뽑은 공통 규칙 (책가도 노트 적용형)
1. **줌 문법**: 표지는 기물 하나의 극단 디테일, 본문은 디테일 단계를 바꿔 가며, 마지막 장에서 병풍 전체(Rijks·구글·대영·간송·김경희 5곳 공통). 디테일 장에는 "3폭 상단 · 4배" 같은 **알약 라벨**을 작게(구글식).
2. **원화 위에 본문 0**: 본문은 띠·단색면에만(리움·V&A·Rijks·뮷즈·윤이크). 표지만 예외로, 원화 누끼와 큰 한글 제목을 겹친다(국중박 〈우리들의 밥상〉식). 핵심 디테일은 가리지 않는다.
3. **사진은 "실물 ↔ 그림" 비교 장에만**: 천원권↔〈계상정거〉(간송), 고양이 사진↔민화(혜진), 원본↔일러스트 재해석(민속박물관). 사진을 장식 배경으로 쓰지 않는다.
4. **저장을 부르는 장 1개**: 달력·배경화면(민속박물관 1위), "저장 추천" 알약 배지(윤이크), "어느 칸?" 고르게 하는 질문(Rijks C351·V&A C115).
5. **출처 두 겹**: 이미지 안 소자 한 줄(대영 "(detail), ©…", 뮷즈 "출처 : ○○") + 캡션 끝 구분선 블록(Met `___`, 국중박 `📍전시품 정보`, 리움 국·영 2블록). Met·Cleveland CC0는 소장번호·원본 URL까지.

## 2. "원화 + AI/신규 일러스트 + 실사 + 코드 그래픽" 혼합 사례 6
| # | 사례 | URL (HTTP 200, 2026-10-02) | 섞은 것 | 톤 통일 방법 | 구성 비율(추정) | 가져올 점 |
|---|---|---|---|---|---|---|
| 1 | Rijksmuseum "Operation Night Watch" AI 복원 띠(2021) | https://dutchnews.nl/2021/06/missing-bits-of-rembrandts-the-night-watch-are-recreated-by-ai · https://artreview.com/ai-restores-missing-figures-from-rembrandt-night-watch/ | 렘브란트 원화 + AI 생성 띠 + 고해상 스캔 + 과정 설명 그래픽 | 모사본 팔레트를 원화 팔레트로 학습 변환(**원화에서 뽑은 색 = LUT 역할**), 노화 균열 예측·추가(**질감**). 금속판으로 살짝 띄워 걸어 **경계는 보이게** | 원화 80~85 : AI 15~20 (면적) | AI 색은 원화에서 뽑고, 경계(테두리·라벨)는 남긴다 |
| 2 | ING × JWT "The Next Rembrandt"(2016) | https://www.lovethework.com/work-awards/entries/the-next-rembrandt-483542 | 원화 346점 분석 + ML 생성 초상 + 메이킹 사진 + 데이터 시각화 + 3D 프린트 | △ 데이터 그래픽을 어두운 배경 + 원화 갈색·금색으로, 산세리프 1벌 | 데이터 40 : 사진 30 : 원화 20 : 결과물 10 (러닝타임) | **코드 그래픽은 원화 색으로 칠해 "같은 종이 위 주석"처럼** |
| 3 | Coca-Cola "Masterpiece"(2023) | https://www.creativebloq.com/news/coca-cola-ad-masterpiece · https://news.designrush.com/blitzworks-new-coca-cola-campaign | 퍼블릭 도메인 명화 + 현대 작가 신작 + 실사 + VFX·AI 전환 | **반복 앵커 오브제(병) 하나**가 모든 장면을 관통, 장면마다 그 그림의 붓질로 다시 그림. △ 실사는 따뜻한 그레이딩 | 회화 60 : 실사 25 : CG·AI 15 | **8장 전체에 앵커 오브제 1개**(예: 같은 연적·붓)를 반복하면 매체가 바뀌어도 한 시리즈 |
| 4 | Gucci "Hallucination" × Ignasi Monreal(SS2018) | https://metalmagazine.eu/post/ignasi-monreal-x-gucci-building-a-hallucinogenic-world | 보스·반 에이크 구도를 재해석한 신규 디지털 페인팅 + 캠페인·상품 사진 + 벽화 | 일러스트레이터 한 명의 손맛, 원화 구도 차용, 팔레트 1개 | 신규 일러스트 80 : 사진 20 | AI 플레이트는 원화 **모사가 아니라 구도의 변주**로 |
| 5 | 조선미녀 "Small Happiness Calendar" 4월 ✔ 이미지 확인 | https://beautyofjoseon.com/blogs/news/small-happiness-calendar-letter_april | 책가도식 기물 일러스트 + 달력 그리드(코드형) + 세리프 타이포 + 같은 블로그 제품 사진 | **크림 단색 바탕 1개**, 일요일만 버밀리온, 반평면 채색에 은은한 음영(완전 플랫 아님), 사진 배경색을 일러스트 톤에 맞춤 | 일러스트 위 55 : 달력 아래 45 (관찰) | **우리 5장(달력)과 거의 같은 구조** — 위 기물, 아래 45% 데이터 |
| 6 | UNIQLO UT × Louvre (M/M Paris 2023 · Peter Saville 2021) | https://presse.louvre.fr/lancement-de-la-collection-uniqlo-x-louvre-par-br-mm-paris-1063000209347 · https://wallpaper.com/fashion/uniqlo-ut-collection-louvre-peter-saville | 소장품 이미지 조각 + 명문 기반 전용 서체 + 캐릭터 일러스트 + 캠페인 사진 | 이미지를 **정해진 모듈 마스크(글자·도형) 안에만** 가둠 | 원화 조각 30~40 : 타입 60 | 원화 크롭을 정해진 마스크(원·아치·사각) 2~3종으로만 자르면 출처가 달라도 한 체계 |
| 참고 | 아모레퍼시픽미술관 「조선민화전」(2025.3.27~6.29) / 설화수 컬처프로젝트 | https://www.apgroup.com/int/ko/news/2025-03-26-1.html | 민화 원화 + 현대 재해석(회화·오브제·가구·미디어아트) | △ 포스터·아이덴티티 세부는 확인 못 함 | — | 근거 약함 |

**우리가 가져올 규칙 3개**
1. **바탕·질감은 렌더러가 공통으로 입힌다(프롬프트에 맡기지 않는다).** 모든 장에 같은 한지 크림 바탕 + 그레인·종이 오버레이 1레이어(불투명도 고정)를 AI 플레이트·사진·코드 그래픽에 똑같이, 원화에는 약하게(디자인 시스템 §8-3 15%·§9-2 6%와 맞춤). 근거: 사례 1·5.
2. **색은 원화에서 뽑고, 원화는 거의 손대지 않는다.** 책가도 원화에서 팔레트·LUT 1개를 추출해 **AI 플레이트와 사진만** 그 LUT로 그레이딩. 코드 그래픽 색도 같은 팔레트에서만. 원화와 AI 사이엔 얇은 먹선 테두리로 경계를 드러낸다. 근거: 사례 1·2.
3. **장마다 주인공 1 + 역할 고정 + 앵커 오브제 1.** 원화 = 표지·클라이맥스·비교 기준, 사진 = 오늘의 실물·증거, AI = 배경·여백, 코드 = 숫자·서체·달력. 8장 내내 반복되는 기물 1개(예: 원화 속 붓통 누끼)를 장 모서리에 작게 둔다. 근거: 사례 2·3·6.

> ⚠ 충돌 메모: 혼합 사례 리서치와 구글 사례는 "AI 장에 공개 라벨"을 권했지만, 디자인 시스템 §9-5(대표 결정)는 **카드·캡션에 AI 표시를 넣지 않고 출처만**이다. 이 문서는 §9-5를 따른다. legal 재점검이 이미 열린 항목으로 남아 있다(§9-5).

## 3. 3판(`posts/2026-10-19/contact.png`) 진단 → 4판 개선안

### 3-1. 장별 진단 (contact.png 원본 1/2과 피드 폭 360px을 직접 보고 확인)
| 장 | 3판 구성 | 이미지 다양성 | 정보 밀도 | 시각 위계 | 리듬 | 무엇이 빈약한가 |
|---|---|---|---|---|---|---|
| 1 표지 | 책가도 책장 풀블리드 + 하단 제목 | 원화 1(Cleveland) | 2(설정줄·펀치줄) + 본문 2줄 | 펀치줄 청자색은 섬. 그림이 "윤동주·필사"와 무관 | — | 훅을 받칠 **증거 이미지가 없다**(책장=클립아트로 읽힘) |
| 2 판매 +692.8% | 원화 + 흰 차트 박스 덮음 | 원화 + 코드 | 3(숫자·막대 2) | 숫자 빨강이 강조색 청자 규칙(§9-6)과 다름. 차트 박스가 그림을 가림 | 1장과 같은 남색 책더미 | 서점·필사책 **실물 사진이 없다**. 360px에서 축 라벨 판독 불가 |
| 3 준비물은 셋 | 원화 붓통·도자기 | 원화만 | 1(본문만, 그래픽 0) | 평평 | 남색·노랑 반복 | 노트·펜·책 **오늘의 실물이 없다**. "셋"을 세어 볼 번호·라벨 없음 |
| 4 첫 줄은 밑줄에서 | 원화 + 원고지 박스 덮음 | 원화 + 코드 | 2 | 원고지 글자가 360px에서 안 읽힘 | 흰 박스 2번째 | 원고지가 그림 위 스티커. 밑줄 친 **실제 책 페이지가 없다** |
| 5 10분, 같은 시각 | 원화 시계 + 달력 박스 | 원화 + 코드 | 3 | 체크 21개가 너무 작음 | 유일하게 밝은 장(좋음) | 달력이 **저장할 만한 크기가 아님**(조선미녀식 위 55/아래 45 구조로 바꾸면 해결) |
| 6 정자로, 흘림으로 | 원화 책더미 | 원화만 | 1 | 평평 | 1·2·4장과 같은 책더미 | **내용과 그림의 불일치가 가장 큼**. 두 서체 대비를 보여 주는 그래픽이 없다 |
| 7 날짜와 책 제목 | 원화 화병 + 노트 박스 | 원화 + 코드 | 2 | 박스가 그림 중앙을 가림 | 흰 박스 4번째 | 2·4·5·7장이 같은 "흰 종이 박스" 문법 → 단조로움 |
| 8 마무리 | 병풍 전경 + 흰 카드 출처 | 원화 | 2(질문·출처) | 출처 소자뿐 | — | **저장 동기(배지·체크리스트)·다음 편 예고가 없다** |

**3줄 요약**
1. **이미지 다양성**: 8장 전부 원화(작품 2점)라 남색 바탕·노란 책더미가 6장 반복된다. 사진 0·AI 0이고, "오늘의 실물"(노트·펜·밑줄 친 책)이 한 장도 없다.
2. **정보 밀도·위계**: 본문이 평균 약 30자 2줄이다. 코드 그래픽은 흰 박스 4개가 그림을 덮는 같은 문법이라, 360px에서 숫자·원고지·달력이 읽히지 않는다.
3. **리듬**: 띠 높이·위치가 7장 동일하고 밝은 장이 1.5장뿐이다. 넘길 때 "다음 장이 다르다"는 신호가 없다.

### 3-2. 4판 8장 와이어프레임 (C 틀 유지: 3:4 1080x1440, 본문 장 위 62% 그림 / 아래 38% 띠는 기본값이고, 장에 따라 띠 색·높이를 바꿔 리듬을 만든다)
| 장 | 이미지 조합 (주인공 **굵게**) | 정보 요소 수 | 장식 | 3판 대비 개선 |
|---|---|---|---|---|
| 1 표지 | **원화 디테일 누끼**(붓통 또는 책갑, 4배) + AI 플레이트(한지 책상 빈 배경, 풀블리드) + 코드(초대형 제목) | 3: 설정줄 · 펀치줄(청자) · 알약 라벨 "책가도 2폭 · 4배" | 국중박 〈밥상〉식 누끼-제목 겹침, 앵커 오브제 첫 등장, 핸들 | 책장 클립아트 → 디테일 줌 + 큰 타이포. 실존 인물(윤동주)은 그리지 않는다(§6-1) |
| 2 판매 +692.8% | **코드**(초대형 숫자 + 막대 2 + 57→81권) + 사진(서점 필사책 매대, 듀오톤, 위 62% 배경) | 5: 숫자 · 막대 2 · 종수 · 출처 소자 | 숫자는 띠 위로 걸쳐 크게, 강조색 청자만 | 차트 박스가 그림 덮기 → 사진 위 큰 숫자 한 개 |
| 3 준비물은 셋 | **원화 붓통 누끼 ↔ 사진 노트·펜·책**(좌우 반반, "옛 문방 / 오늘 문방") + AI 플레이트 바탕 | 5: ①②③ 번호 라벨 3 · 본문 · 비교 캡션 | 먹선 2px 테두리로 원화/사진 경계, 번호 배지 | 실물 0 → 실물↔그림 비교(간송·혜진 문법) |
| 4 첫 줄은 밑줄에서 | **사진**(밑줄 친 책 페이지 클로즈업, 글자 안 읽히게 아웃포커스) + 코드(원고지 3칸을 크게, 한 줄만) | 3: 원고지 한 줄 · 본문 · 출처 소자 | 청자색 밑줄 한 획(코드) | 원고지 4줄 소자 → 한 줄 대형. 원화 쉬어 가는 장 |
| 5 10분, 같은 시각 | **원화 자명종 디테일**(위 55%, 크림 바탕) + 코드 달력(아래 45%, 실물 크기 체크칸) | 4: 시계 · 달력 · 본문 · "저장해서 쓰세요" | 밝은 크림 장(리듬 전환), 일요일 대신 오늘 칸만 청자 | 조선미녀 캘린더 구조. **저장용 장 1번** |
| 6 정자로, 흘림으로 | **코드**(같은 문장을 함렛 Black vs 붓글씨풍 서체로 위아래 대조) + AI 플레이트(수묵 번짐 배경) | 3: 정자 줄 · 흘림 줄 · 본문 | 띠 없이 전면 한지(리듬 전환 2) | 책더미 불일치 → 서체 자체가 그림 |
| 7 날짜와 책 제목 | **사진**(펼친 노트, 빈 칸) + 코드(날짜·제목 기입 예시를 노트 위에 손글씨풍으로) + 원화 소품(책갑 원형 마스크, 우상단 작게) | 4: 날짜 · 책 제목 · 본문 · 앵커 오브제 | 원형 마스크(UNIQLO식 모듈) | 흰 박스 반복 해소 |
| 8 오늘 옮길 한 줄 | **원화 병풍 전경**(위 55%, 가로 띠) + 코드(체크리스트 3줄 + "저장 추천" 알약 배지 + 다음 편 예고 1줄) + 출처 블록 | 6: 질문 · 체크 3 · 배지 · 다음 편 · 출처 | 얇은 청자 가로줄, 앵커 오브제 마지막 등장 | 출처만 있던 장 → **저장용 장 2번** + 전체 줌아웃으로 마무리 |

- **주인공 분포**: 원화 3(1·5·8) · 사진 2(4·7) · 코드 2(2·6) · 원화↔사진 비교 1(3). 같은 주인공 3연속 없음(§9-1 충족).
- **등장 횟수**: 원화 5장 · 사진 4장 · AI 플레이트 3장 · 코드 7장. **면적 비율(추정)은 원화 35 : AI 15 : 사진 25 : 코드 25.**
- **밝은 장**: 3판 1.5장 → 4판 3장(5·6·8). 어두운 띠 장과 번갈아 넘김 리듬을 만든다.
- **사진 조건**: 디자인 시스템 §9-2 그대로(CC0·CC BY·공공누리 1유형, 얼굴·로고·읽히는 글자 없음, 크롭·톤만).

## 4. AI 플레이트 톤 가이드 (ComfyUI)

### 4-1. 레퍼런스 11개 (참고 링크만, 이미지 복사·학습 안 함 · HTTP 200 확인 2026-10-02)
| # | URL | 왜 참고하나 (색·질감·조명·구도) | 계열 |
|---|---|---|---|
| 1 | https://www.clevelandart.org/art/2011.37 | 클리블랜드 책가도(CC0). 금빛 책·기물의 은은한 입체 음영 = **플랫이 아니다**의 기준 | 민화 플랫(원본) |
| 2 | https://www.metmuseum.org/art/collection/search/853896 | Met 책가도(CC0, DESIGN_SOURCES §5-2 #1. Met 웹은 429라 HTTP 확인 대신 API 판정 인용). 갈색 서가, 버밀리온 포인트, 바랜 비단 질감 | 민화 플랫(원본) |
| 3 | https://commons.wikimedia.org/wiki/Category:Chaekgeori | PD 책거리 묶음. 장르 안의 색 폭 확인용(SA 파일은 쓰지 않음, 참고만) | 민화 플랫(원본) |
| 4 | https://beautyofjoseon.com/blogs/news/small-happiness-calendar-letter_april | 크림 바탕 반평면 기물 정물 + 하단 45% 여백. **구도가 가장 비슷함** | 민화 플랫(현대) |
| 5 | https://www.koreatimes.co.kr/amp/lifestyle/koreanheritage/20260114/modern-minhwa-artist-paints-luck-everyday-hope-in-korean-folk-art | 현대 민화·책거리 변주의 평면 채색 팔레트 | 민화 플랫(현대) |
| 6 | https://www.thisiscolossal.com/2019/04/agreggations-by-kwang-young-chun/ | 전광영 〈집합〉. 고서 한지 섬유, 먹 글씨, 갈색 톤 | 한지 콜라주 |
| 7 | https://chennaiphotobiennale.foundation/biennale/artists/lim-soo-sik- | 임수식 〈책가도〉. 서가 사진을 한지에 바느질로 이어 붙인 역원근 구도 = **사진+한지+책가도 혼합의 정답에 가장 가까움** | 사진 합성(+한지) |
| 8 | https://the189.com/photography/in-the-pursuit-of-white-porcelain-vessels-photographed-by-bohnchang-koo/ | 구본창 〈Vessel〉. 부드러운 확산광, 크림·회백 톤, 넓은 빈 공간 | 사진 합성 |
| 9 | https://www.philamuseum.org/exhibitions/plain-beauty-korean-white-porcelainphotographs-by-bohnchang-koo | 백자 실물과 사진을 나란히 건 전시. 원본·사진 병치 방식 | 사진 합성 |
| 10 | https://www.koreanculture.org/press-releases/2019/7/9/immediate-release-kcsinkartpressrelease3a-edited-ver-1 | 김호득 등 현대 수묵 9인전. 먹 번짐과 한지 여백 | 수묵 |
| 11 | https://apollo-magazine.com/park-dae-sung-lacma-virtuous-ink/ | 박대성(LACMA). 한지 자체의 발광감을 흰색으로 활용 | 수묵 |
| (참고) | https://carat.im/en/prompt-gallery/korean-painting | AI 민화·수묵 갤러리. "muted natural pigments on rice paper" 계열 결과 | AI |
- Civitai·Lexica·OpenArt에서 책가도·한지 전용 갤러리나 LoRA는 찾지 못했다(LoRA는 어차피 쓰지 않는다, PROMPTS-v4 §0).

### 4-2. 현재 접미사(`plates/PROMPTS-v4.md` §0)의 문제
1. "flat editorial illustration" + "bold clean ink outlines"가 **벡터 클립아트 쪽으로 끈다.** 궁중 책가도는 광물안료에 은은한 명암과 서양식 투시가 있어서 플랫 결과가 원화 옆에서 약해 보인다.
2. **hex 코드(#3B2F2A 등)는 모델이 거의 해석하지 못한다.** 토큰만 쓴다. 색 이름 + "faded/muted"가 낫다.
3. "calm soft daylight"는 플랫 일러스트와 모순된다(플랫엔 빛이 없다).
4. **배경 플레이트라는 지시가 없다.** "하단 비움·저대비·주제 약화"가 빠져 있다.
5. 약 70토큰이라 SDXL CLIP 77토큰 한도에서 장별 주제가 잘릴 수 있다.
6. 질감("visible hanji fibres")은 시드마다 다르게 나온다 → 질감은 렌더러 공통 레이어로(§2 규칙 1).

### 4-3. 제안: 공통 접미사 (약 50단어)
```
ink and mineral pigments on aged hanji, Joseon court-painting atmosphere, gentle tonal shading with soft depth, muted palette of warm ink brown, celadon green, faded vermilion and cream paper, quiet scholar's study still life, soft diffused window daylight, generous empty space in lower third, low contrast, matte surface
```
**계열별 꼬리(V2 결정에 따라 1개만 붙인다)**
| 계열 | 꼬리 |
|---|---|
| 민화 플랫 | `flat mineral-pigment color fields, fine even ink contours, reverse-perspective shelves, symmetrical arrangement` |
| 수묵 | `monochrome ink wash with pale color washes, soft bleeding edges, mostly blank paper, single object` |
| 한지 콜라주 | `torn layered hanji pieces, visible mulberry fibres, deckled edges, faint paper-relief shadows, celadon and persimmon dyed paper` |
| 사진 합성 | `editorial still-life photograph, celadon and white porcelain on wooden scholar's table, natural window light from left, 50mm, shallow depth of field, hanji wall backdrop` |

**네거티브(SDXL용, PROMPTS-v4 네거티브에 추가)**: `glossy 3D render, plastic, neon, oversaturated, vector clip art, thick cartoon outlines, anime, calligraphy, pseudo-hanja, seal stamp, signature, gold sparkle, HDR, harsh shadows, cluttered lower area, picture frame`
- Z-Image-Turbo는 CFG 1이라 네거티브 효과가 거의 없다(추정). 그 경우 긍정 프롬프트 끝에 `No text, no logos, no people, empty lower third.`를 붙인다.
- 후처리 순서(렌더러, 모든 플레이트 동일): 원화 팔레트 LUT → 한지 multiply 15% → 그레인 6% → 하단 1/3 밝기 +5%(띠 대비 확보). 수치는 추정 → 4판 실측 후 교체.
- 반영 위치: `plates/PROMPTS-v4.md` 수정은 이 과제 범위 밖이다(다른 파일 수정 금지). 대표 결정 V2 뒤에 designer가 반영한다.

## 5. 대표 결정 목록 (기본값 미적용)
| # | 결정 | 선택지 | 리서처 추천 (1줄) |
|---|---|---|---|
| V1 | 4판 이미지 조합 비율(면적, 원화:AI:사진:코드) | ⓐ 50:10:20:20 원화 중심 ⓑ **35:15:25:25 균형** ⓒ 25:25:25:25 균등 ⓓ 직접 지정 | **ⓑ** — 원화를 표지·5장·8장 주인공으로 남겨 정체성을 지키고, 3판에 없던 "오늘의 실물" 사진을 4장에 넣는 최소 변화다 |
| V2 | AI 플레이트 스타일 | ⓐ 민화 플랫 ⓑ 수묵 ⓒ 한지 콜라주 ⓓ 사진 합성 | **ⓒ 한지 콜라주** — 종이 질감이 원화(비단·종이)와 사진(실물) 사이의 다리가 된다(임수식·전광영). 플랫은 원화 옆에서 약해 보였다(3판 평가) |
| V3 | 출처 표기 방식 | ⓐ 매 장 그림 우하단 소자 "이미지 제공 ・ 기관명" + 마지막 장 출처 줄 ⓑ 마지막 장에만 집중 | **ⓐ** — 18계정 중 출처를 표기하는 기관(대영·뮷즈·간송·민속)은 모두 이미지 안에 소자를 둔다. 마지막 장 출처 줄은 §8-4 필수라 어차피 남는다. 캡션 끝 구분선 블록도 추가 권장 |

## 6. 자가 검증
**성공 기준(작성 전)**: ① 15계정 이상 × 공개 URL 2개 이상, 게시자 일치 확인 ② 혼합 사례 5개 이상 + 통일 방법·비율·규칙 3 ③ 3판 장별 진단 + 4판 8장 와이어프레임 표 ④ 톤 레퍼런스 10개 + 공통 접미사 ⑤ V1~V3 + 추천 1줄씩 ⑥ 출처·확인일·추정 표시 ⑦ 이 파일 하나만 변경, 이미지 비커밋, 비밀값 0

| # | 기준 | 결과 | 근거 |
|---|---|---|---|
| 1 | 15계정 × URL 2+ | ✔ 18계정, 계정당 2~4개, 전부 게시자 일치 | §1 표. 한계: 대영박물관은 이 기간 캐러셀이 없어 영상 게시물. APMA는 단일 이미지만 |
| 2 | 혼합 사례 5+ | ✔ 6개 + 참고 1 | §2. 한계: 인스타 URL 대신 공식·기사 URL. 직접 이미지 확인은 1건 |
| 3 | 3판 진단 + 4판 8장 표 | ✔ | §3-1(contact.png 직접 확인), §3-2 |
| 4 | 톤 레퍼런스 10 + 접미사 | ✔ 11개 + 접미사 + 계열 꼬리 4 + 네거티브 | §4 |
| 5 | V1~V3 추천 | ✔ | §5, 기본값 미적용 |
| 6 | 출처·확인일·추정 | ✔ 확인일 2026-10-02, 팔로워·반응·비율은 (추정) | 본문 표기 |
| 7 | 변경 범위 | ✔ `cardnews/docs/BENCHMARK-visual.md` 1개만. 슬라이드는 스크래치패드에만 | git diff |

## 출처 (확인 2026-10-02)
- 인스타그램 게시물: §1 표의 링크(공개 embed로 게시자·좋아요·댓글·장 수 확인)
- 혼합 사례: §2 표의 링크
- 톤 레퍼런스: §4-1 표의 링크
- 내부: `cardnews/docs/BENCHMARK.md` §2, `cardnews/posts/2026-10-19/contact.png`·`cards.json`·`plates/PROMPTS-v4.md`, `cardnews/main:cardnews/docs/DESIGN_SOURCES.md` §1·§2·§5, `claude/admiring-clarke-beyyoi:episodes/EP001/design/design-system.md` §8·§9
