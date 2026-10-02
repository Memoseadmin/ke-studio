# 책가도 노트 카드뉴스 디자인 소스 리서치 (v3 준비)

> 2026-10-02 리서처(디자인 소싱). 대표 지시: "품질이 너무 낮다. 무료·오픈소스로 세계 수준까지."
> 범위: 웹 조사 + VM 실측(서체 20종 cmap·셰이핑, Chromium 렌더 1회). **아무것도 설치·업로드하지 않았다.**
> 표기: 금액은 모두 **추정**(2026-10-02 조회, 1 USD ≈ 1,400원). 라이선스는 원문 페이지를 직접 보고 "원문"으로 적었고, 검색 요약이나 2차 출처에만 의존한 것은 "[2차]", 확인하지 못한 것은 "미확인"으로 적었다. 확인일은 별도 표기가 없으면 모두 2026-10-02.

## 0. 한 장 요약
| 질문 | 답 |
|---|---|
| 왜 낮아 보이나 | ① **중국어 대체 서체**(WenQuanYi + 가짜 볼드)로 렌더됨 ② 내용과 무관한 책장 클립아트가 반복됨 ③ 본문 아래 빈 띠가 의도 없이 남음 ④ 위계와 그리드가 없음 ⑤ 옛한글이 낱자로 깨짐 (§1) |
| 렌더러 | **HTML/CSS → Playwright Chromium**(VM에 이미 설치돼 있고 실측 통과). Pillow는 폐기 (§3) |
| 서체 | 세트 B **함렛 Black + 마루부리 + Black Han Sans**, 옛한글은 Noto Serif KR이 대체 (§4) |
| 그림 | 퍼블릭 도메인 원화(Met·Cleveland CC0 + e뮤지엄 공공누리 1유형) **31점 확보**. 원화 디테일 크롭 + 코드 그래픽 + (선택) 자체 LoRA (§5·§6) |
| v3 추천 | **1안 "원화 아카이브"**: AI 생성 0, 유료 API 0, 10/9 전에 시작 가능. AI 플레이트는 C1-2부터 보조로 시험 (§8) |
| 월 비용 | 1안 0원 / 2안 약 1만원 / 3안 약 2~3만원 (추정) |

## 1. 현재 카드 진단 (`posts/2026-10-09/contact.png`, `2026-10-16/card-03.png`를 직접 열어 확인)
| # | 증상 | 근거 | 영향 |
|---|---|---|---|
| 1 | 서체가 중국어 고딕 대체본이고 가짜 볼드 | `RENDER.json`: head·body = `wqy-zenhei.ttc`, `fake_bold: True`. Black Han Sans·Pretendard 미설치 | 한글 속공간이 뭉개지고 본문 자간이 듬성함. "싸 보임"의 1순위 원인 |
| 2 | 모티프가 내용과 무관하고 반복됨 | 10/9 세트 2·6장이 같은 책장 격자, 10/16 "사라진 넷"(옛한글)에도 책장 격자 | 그림이 정보를 주지 않는 장식(클립아트)으로 읽힘 |
| 3 | 빈 띠가 의도 없이 남음 | 10/16-3장 본문 끝(y≈470)~플레이트(y=760) 사이 약 290px 공백. 10/9-4장은 화면 60%가 빔 | 여백이 아니라 "덜 채운 화면"으로 보임 |
| 4 | 위계가 평평함 | 본문 44px : 제목 88px = 2:1. 라벨·핸들·장번호가 모두 비슷한 무게 | 시선의 첫 지점이 없음 |
| 5 | 옛한글이 깨짐 | ㆁ ㅿ ㆆ ㆍ가 호환자모 낱자로 찍히고 ㆍ는 점으로 떠 있음 | 바로 이 주제(훈민정음)에서 신뢰도가 떨어짐 |
| 6 | 질감이 거의 보이지 않음 | 한지 결 9%에 포스터라이즈까지 걸려 300px에서 소멸 | 평면 PPT처럼 보임 |
| 7 | 마지막 장이 비어 있음 | 출처 텍스트만 있고 시각 요소가 없음 | 저장·공유 동기가 약함 |

## 2. 벤치마크 15곳 — 원리만 추출 (모사 금지)
> 계정 존재는 기관 공식 사이트의 IG 링크로 확인했다. instagram.com은 로그인 벽 때문에 **피드를 직접 보지 못했다**. 그래서 "왜 고급인가" 칸은 전부 **추정(유형별 편집 관행을 일반화)**이다. 대표가 폰으로 보고 실측 메모로 교체해야 한다.

| # | 계정 | 유형 | 왜 고급인가 (추정) |
|---|---|---|---|
| 1 | 국립중앙박물관 @nationalmuseumofkorea | 박물관 | 유물 단독 배치 + 넓은 여백, 명조 제목 + 고딕 캡션 2단 |
| 2 | 국립한글박물관 @hangeul_m | 박물관 | 큰 한글 1~2자 vs 작은 설명의 극단적 크기 대비, 2~3색 |
| 3 | 국가유산청 @chlove_u | 정부 | 고정 표지 틀 반복(일관성 참고용) |
| 4 | 서울역사박물관 @seoulmuse | 박물관 | 고지도·아카이브 대형 사용, 연도 숫자를 디스플레이 크기로 |
| 5 | 서울공예박물관 @seoulmuseumofcraftart | 박물관 | 공예 디테일 클로즈업, 산세리프 1종, 오프화이트 |
| 6 | 매거진B @magazine.b | 매거진 | 1브랜드=1시리즈, 고정 로고타입 위치, 저채도 통일 |
| 7 | 일상의실천 @hello_ep | 스튜디오 | 강한 그리드, 화면 끝까지 차는 큰 글자, 1~2색 |
| 8 | 뉴닉 @newneek.official | 미디어 | 카드뉴스 서사 구조의 기준점(훅→결론) |
| 9 | The Met @metmuseum | 박물관 | 원본 100% 또는 디테일만 확대, 글자는 캡션으로 |
| 10 | Rijksmuseum @rijksmuseum | 박물관 | 균열이 보일 만큼 디테일 확대, 작은 산세리프 + 큰 여백 |
| 11 | Cooper Hewitt @cooperhewitt | 디자인박물관 | 자체 서체, 흰 배경 누끼, 표본 도판식 일정 배치 |
| 12 | Public Domain Review @publicdomainrev | 아카이브 | 종이 노화·얼룩 보존 + 세리프 제목. **우리 톤에 가장 가까움** |
| 13 | Pentagram @pentagramdesign | 스튜디오 | 전체→디테일→적용 순서, 매 장 같은 마진 |
| 14 | It's Nice That @itsnicethat | 매거진 | 고정 표지 템플릿에 작품만 교체, 큰 산세리프 + 작은 크레딧 |
| 15 | Kinfolk @kinfolk | 매거진 | 자연광·저채도 사진, 얇은 세리프 + 넓은 행간 |

예비: 도쿄국립박물관 @tnm_ir_en(병풍 소장품 비교용). 제외: 프로파간다·Monocle·Atlas Obscura(공식 출처 확인 실패 또는 차단).

**옮겨 올 원칙 9개 (1080×1350, 수치는 추정)**
1. 제목:본문 크기 ≥ 3:1(표지 ≥ 5:1). 크기 단계는 3단까지. 예: 제목 104 / 본문 34 / 캡션 24px
2. 바깥 여백 ≥ 8%(88px), 위아래는 더 넓게(≥ 104px). 모든 장 동일
3. 6단 그리드 + 기준선 8px. 텍스트 시작점은 시리즈 전체에서 2곳까지
4. 서체 2계열·굵기 2단계. 본문 행간 160~170%, 제목 120~128%. 제목 자간 -2~-3%, 캡션 +3~5%
5. 색: 바탕 1 + 잉크 1 + 포인트 1. 포인트 면적 ≤ 10%. 순백 대신 한지 오프화이트
6. 질감은 5~12%로 깔되 글자 위에는 올리지 않음. 원화의 노화 흔적은 지우지 않음
7. 한 장에 이미지 1개. 전체 → 2~4배 디테일 순서. 보정 프리셋 1개로 통일
8. 표지 단어 ≤ 7개, 본문 ≤ 2~3문장(60~90자). 화면 40% 이상 비움
9. 장번호·계정명은 고정 모서리. 표지 틀 1개를 정하고 내용만 바꿈. 마지막 장은 출처 + 다음 편 예고

## 3. 렌더 파이프라인 — 추천: HTML/CSS → Playwright Chromium
**VM 실측(2026-10-02):** 노드 Playwright 1.56.1 + `/opt/pw-browsers/chromium-1194`로 1080×1350 PNG 1장을 약 1.1초에 렌더. Noto Serif CJK KR을 `@font-face`로 불러서 아래가 모두 정상 동작했다(결과 이미지 육안 확인).
- `word-break: keep-all`, `text-wrap: balance`, `letter-spacing: -0.02em`
- `writing-mode: vertical-rl`(낫표 회전 정상)
- 옛한글 ᄒᆞᆫ·ᅀᅡ·ᅌᅩᆼ이 한 음절로 합성됨

| 도구 | 라이선스 | CPU VM | 한글 셰이핑·옛한글 | 세로쓰기 | 줄바꿈·자간 | 판정 |
|---|---|---|---|---|---|---|
| **Playwright + Chromium** | Apache-2.0 | 설치돼 있음 | O(실측) | O(실측) | keep-all·balance·자간 O | **1순위** |
| Pillow 12 + raqm | HPND | pip 휠에 raqm·HarfBuzz 포함 | O(실측) | `ttb` 실행만 확인 | 직접 구현해야 함 | 대비책 |
| Pango/HarfBuzz | LGPL | 라이브러리는 있으나 `gi` 바인딩 깨짐 | O | 까다로움 | keep-all 없음 | 비추천 |
| Satori | MPL-2.0 | O(WASM) | O | **X** | O | 세로쓰기 불가로 탈락 |
| resvg / CairoSVG | Apache / LGPL | O | 부분 / 약함 | 미검증 | 수동 | 탈락 |
| skia-python | BSD-3 | O | O | 수동 | 수동 | 비효율 |
| Puppeteer | Apache-2.0 | O | =Chromium | =Chromium | =Chromium | Playwright와 중복 |
| Remotion | 직원 3명 이하 무료 | O | =Chromium | O | O | **릴스용**(같은 HTML 재사용) |
| HyperFrames | Apache-2.0 | O(Node 22 + FFmpeg) | =Chromium | O | O | 릴스 대안. 정지 PNG 출력은 미확인 |
| Penpot | MPL-2.0 | Docker 전체 스택 필요 | — | — | — | 플러그인은 편집기 UI 안에서만. 자동화용으로 무거움 |

- **마이그레이션 난이도: 중하**(약 1~2일, 추정).
  - `render_cards.py`의 좌표 코드를 HTML 템플릿 3종(표지·본문·마지막)과 CSS 토큰 1개로 옮긴다.
  - 렌더 스크립트는 약 20줄. `cards.json` 형식은 그대로 쓴다.
  - 서체는 `scripts/setup.sh`에서 받아 오고 저장소에는 커밋하지 않는다.
- **릴스 확장:** 같은 HTML을 Remotion 컴포지션에 넣으면 정지 카드와 영상이 한 디자인 언어를 쓰게 된다.

## 4. 무료 한글 서체 (VM에서 20종 실측)
- 실측 방법: fontTools로 cmap·GSUB를 보고, uharfbuzz로 `ᄒᆞᆫ ᄀᆞᆯ ᄋᆞᆷ`을 셰이핑했다. 3음절이 3글리프로 합쳐지면 정상이다.
- 호환자모 = ㅿ U+317F · ㆁ U+3181 · ㆆ U+3186 · ㆍ U+318D. 첫가끝 = U+1100 계열 + ljmo/vjmo/tjmo.

| 서체 | 용도 | 라이선스(원문) | 호환자모 | 첫가끝 조합 | 굵기 | 민화·한지 톤 |
|---|---|---|---|---|---|---|
| 송명 Song Myung | 제목 | OFL 원문 | 4/4 | X | 1 | 고서 활자 느낌이 가장 강함. 2,350자뿐 |
| 함렛 Hahmlet | 제목 | OFL 원문 | 4/4 | X | 가변 100~900 | Black으로 쓰면 목판 제목 느낌. GF 빌드 2,788자 |
| 마루부리 MaruBuri | 제목·본문 | 네이버 글꼴(OFL) 원문 | **0/4** | X | 5 | 붓맛 있는 현대 명조. 11,172자 |
| 고운바탕 | 본문 | OFL 원문 | 4/4 | X | 2 | 손글씨 기운. 민화와 궁합 |
| Noto Serif KR / 본명조 | 본문·제목·옛한글 | OFL 원문 | 4/4 | **O(실측)** | 7 | 정갈함. 옛한글 대체 1순위 |
| 나눔명조 옛한글 | 옛한글 인용 | 네이버(OFL) 원문 | 4/4 | **O(실측)**, PUA 5,299 | 1 | 훈민정음 인용에 최적 |
| Noto Sans KR | 정보·캡션 | OFL 원문 | 4/4 | **O(실측)** | 9 | 중립 |
| 나눔손글씨 붓 | 강조 | 네이버(OFL) 원문 | 4/4 | X | 1 | 붓글씨 포인트 |
| Black Han Sans | 강조(숫자·낙관) | OFL 원문 | 0/4 | X | 1 | 2,581자뿐. 제목 전용으로 쓰면 무거움 |
| 페이퍼로지 | 강조(태그) | OFL(제작사 페이지 + name 테이블) | 1/4 | X | 9 | 깔끔하지만 전통 톤은 약함 |
| Pretendard | 정보 본문 | OFL 원문 | 1/4 | X | 9 | 현대적 대비용 |
| KoPub World 바탕/돋움 | 본문 | KoPub 라이선스 원문(판매만 금지) | 미측정 | 미측정 | 3 | 무난 |
| 함초롬 | — | **미확인**(독점 글꼴로 분류한 사례 있음) | — | — | — | **제외**. 대체재 있음 |

- **핵심:** 옛한글을 제대로 조합하는 무료 서체는 **나눔명조 옛한글 · 나눔바른고딕 옛한글 · Noto Serif KR(본명조) · Noto Sans KR** 네 종뿐이다(실측). 나머지는 같은 문자열이 빈 네모로 깨진다. → CSS `font-family` 대체 순서의 마지막에 반드시 넣는다.
- **GF 배포본 주의:** 송명·함렛·Black Han Sans는 2,3xx~2,7xx자뿐이라 드문 음절이 빠진다. `carousel-qa` 3번 항목(글리프 누락 0)으로 검사한다.
- **라이선스:** OFL·네이버·KoPub 모두 글꼴 단독 판매만 금지하고, 이미지 게시는 허용한다. 네이버 원문에는 "사용 이미지를 나눔 프로모션에 활용할 수 있다"는 조항이 있다(원하지 않으면 요청 가능).

**추천 3세트**
| 세트 | 제목 | 본문 | 강조 | 옛한글 대체 | 무드 |
|---|---|---|---|---|---|
| A 민화 서책 | 송명 | 고운바탕 | 나눔손글씨 붓 | 나눔명조 옛한글 | 고서·서책, 가장 전통적 |
| **B 한지 모던 (추천)** | 함렛 Black/Bold | 마루부리 Regular | Black Han Sans(붉은 낙관 박스 안 숫자) | Noto Serif KR | 목판 제목 + 현대 명조. 고급스러우면서 읽힘 |
| C 정보·구매 의도형 | Noto Serif KR Black | Pretendard | 페이퍼로지 ExtraBold | Noto Sans KR | 협찬·리스트형 게시물용 |

## 5. 질감·문양·색·원화 소스 (상업 + 2차 가공 가능만)
**5-1. 텍스처·문양·색**
| 소스 | 라이선스(원문 인용 요지) | 상업 | 가공 | 출처표시 | 쓰임 |
|---|---|---|---|---|---|
| ambientCG docs.ambientcg.com/license | CC0 "even for commercial purposes"(원문) | O | O | 불필요 | 종이·섬유 결 |
| Poly Haven polyhaven.com/license | CC0 "do not need to give credit"(원문) | O | O | 불필요 | 종이·나무 결 |
| Unsplash / Pexels | 상업·수정 허용, 원본 그대로 판매 금지(원문) | O | O | 불필요 | 실사 사진(인물·로고 없는 컷만) |
| **문화포털 전통문양** culture.go.kr/tradition | 공공누리 출처표시 조건 = 1유형(원문) | O | O | **필수**: "본 저작물은 '문화포털'에서 서비스 되는 전통문양을 활용하였습니다" | 단청·창살·구름 문양 벡터 |
| 공공누리 1유형 kogl.or.kr/info/licenseType1.do | 영리 이용·2차 저작물 가능, 출처 표시 의무(원문) | O | O | 필수 | 공통 기준 |
| 공유마당 gongu.copyright.or.kr | 만료·CC0·BY·공공누리가 섞여 있음 | 항목별 | 항목별 | 항목별 | 만료·CC0·1유형만 사용 |
| 오방색·KS A 0011 색이름 | 색 값 자체는 저작권 대상 아님 | O | O | 불필요 | 팔레트(표준 문서는 복제하지 않음) |
| 자체 한지 스캔 | 우리 소유 | O | O | — | **가장 확실한 질감**. 한지 3종 구입·스캔(약 1만원, 추정) |

**제외 (사유):**
- textures.com·rawpixel: 원문 미확인(403·빈 페이지)
- 서울색 자료: 공공누리 4유형, 상업·변경 불가
- 디자인진흥원 전통문양 PDF: 이용조건 미확인
- Wikimedia SA 파일: 결과물까지 같은 라이선스가 전염됨
- 국가유산청 문양 DB: 찾지 못함

**5-2. 퍼블릭 도메인 민화 원본 31점 (금지 모티프 2점 포함)**
- Met은 공식 API의 `isPublicDomain=True`로 확인했다(웹페이지는 429).
- Cleveland는 API와 작품 페이지의 CC0 표기로 확인했다.
- e뮤지엄은 상세페이지의 공공누리 유형 표기를 직접 확인했다.

| # | 장르 | 제목 | 소장 | URL | 라이선스 |
|---|---|---|---|---|---|
| 1 | 책가도 | Books and Scholarly Accoutrements | Met | metmuseum.org/art/collection/search/853896 | CC0 |
| 2 | 책거리 | Books and Scholars' Possessions (10폭) | Met | …/search/73134 | CC0 |
| 3 | 화조도 | Birds and Flowers (8폭) | Met | …/search/853895 | CC0 |
| 4 | 화조도 | Birds and Flowers (10폭) | Met | …/search/44760 | CC0 |
| 5 | 화조 자수 | Birds and Flowers (10폭) | Met | …/search/918072 | CC0 |
| 6 | 모란도 | Butterflies and Peonies | Met | …/search/45063 | CC0 |
| 7 | 기명절지 | Still life with bronze vessels… (1894) | Met | …/search/646996 | CC0 |
| 8 | 화조·책거리 | Birds, Animals, and Still-lifes | Met | …/search/929265 | CC0 |
| 9 | 화조 | Golden Rooster and Hen | Met | …/search/40073 | CC0 |
| 10 | 어변성룡 | Dragon and carp | Met | …/search/853892 | CC0 |
| 11 | 문자도·책거리 | Munja-Chaekgeori Screen | Cleveland | clevelandart.org/art/2017.6 | CC0(원문) |
| 12 | 책가도 | Books and Scholars' Accoutrements | Cleveland | …/art/2011.37 | CC0 |
| 13 | 화조도 | Birds and Flowers | Cleveland | …/art/1991.80 | CC0 |
| 14 | 모란도 | Peonies | Cleveland | …/art/2022.59 | CC0 |
| 15 | 모란도 | Peonies and Rocks | Cleveland | …/art/2022.60 | CC0 |
| 16 | 화조 | Lotuses, Insects, and Birds | Cleveland | …/art/1985.18 | CC0 |
| 17 | 문자 | Set of Four Painted Characters | Cleveland | …/art/1998.119 | CC0. 'Tiger' 패널은 제외 |
| 18 | 백화 | Painting of One Hundred Themes | Cleveland | …/art/1998.286 | CC0 |
| 19 | 책가도 | 책가도 6곡병(건희 4123) | 국립중앙박물관 | emuseum.go.kr/detail?relicId=PS0100100102400412300000 | 공공누리 1유형 |
| 20 | 책가도 | 책가도 | 국립중앙박물관 | …relicId=PS0100100102400412100000 | 1유형 |
| 21 | 책가도 | 책가도 병풍 | 국립중앙박물관 | …relicId=PS0100100102400405500000 | 1유형 |
| 22 | 모란도 | 봉황모란도 | 국립중앙박물관 | …relicId=PS0100100102400410200000 | 1유형 |
| 23 | 모란도 | 모란도 | 국립중앙박물관 | …relicId=PS0100100101601043500000 | 1유형 |
| 24 | 십장생도 | 십장생도 10폭병풍 | 국립중앙박물관 | …relicId=PS0100100102400405300000 | 1유형 |
| 25 | 일월오봉도 | 일월오봉도 | 국립중앙박물관 | …relicId=PS0100100100101161500000 | 1유형 |
| 26 | 일월오봉도 | 일월오봉도(8886×3487px) | 국립고궁박물관 | …relicId=PS0100201100700000100001 | 1유형 |
| 27 | 문자도 | 문자도 8폭 | 천안박물관 | …relicId=PS0100309800100149000000 | 1유형 |
| 28 | 화조도 | 화조도 10폭 병풍 | 천안박물관 | …relicId=PS0100309800100114900000 | 1유형 |
| 29 | 모란도 | 괴석모란도 8폭(13485×8990px) | 천안박물관 | …relicId=PS0100309800100148800000 | 1유형 |
| 30 | ~~산신·호랑이~~ | Mountain god with tiger | Met | …/search/853891 | CC0, **금지 모티프** |
| 31 | ~~호랑이~~ | Tiger Family | Cleveland | …/art/1997.148 | CC0, **금지 모티프** |

- **e뮤지엄에서 제외한 소장처:** 영남대박물관(4유형), 남가람박물관(2유형), 영천역사박물관(3유형), 울산박물관(4유형). 같은 장르라도 소장처마다 유형이 다르므로 **항목 단위로 확인**한다.
- **미확인:** Smithsonian NMAA(API 한도 초과), Brooklyn, LACMA, 국립민속박물관 아카이브.

**용도별 판정**
| 출처 | (a) 레퍼런스 | (b) LoRA 학습 | (c) 가공 후 배경 | 조건 |
|---|---|---|---|---|
| Met·Cleveland CC0 | O | O | O | 표기 의무 없음. "Image: The Met, CC0" 같은 감사 표기 권장. 박물관이 상품을 보증하는 것처럼 보이는 배치 금지 |
| 공공누리 1유형 | O | O(학습 목록에 출처 기록) | O | 마지막 장 출처 줄에 기관명·작품명·"공공누리 제1유형" 표기 필수 |
| 공공누리 AI유형(국립중앙박물관 신설) | O | O(출처 생략 가능) | 함께 붙은 유형을 따름 | 원본과 유사한 산출물 방지 조치, 학습데이터 재판매 금지 (museum.go.kr/MUSEUM/contents/M3304000000.do) |
| 2·3·4유형, NC·ND·SA | 참고만 | X | X | — |

## 6. AI 이미지 생성 (2안·3안에서만 사용)
| 모델 | 가중치 라이선스 | 한국 상업 | fal 단가(추정) | LoRA 학습(추정) | 판정 |
|---|---|---|---|---|---|
| **Z-Image Turbo 6B** | Apache-2.0(원문, HF) | O | $0.005/MP, LoRA 사용 시 $0.0085/MP | z-image-trainer $2.26/1000스텝 | **기본** |
| Z-Image base | Apache-2.0 | O | $0.01/MP | 같은 트레이너 | 네거티브 프롬프트가 꼭 필요할 때 |
| FLUX.2 klein 4B | Apache-2.0(원문) | O | $0.005/MP | $5/1000스텝 [2차] | 멀티 참조 편집으로 세트 일관성 유지 |
| Qwen-Image-2512 / Edit-2511 | Apache-2.0 | O | $0.02 / $0.03 per MP | $0.95/1000스텝 | 승인 플레이트 변주용 |
| HiDream-I1 | MIT + Llama 3.1 조건 | 조건부 | $0.05/MP | — | 비쌈 |
| SD3.5 | 매출 $1M 이하 무료 | 조건부 | — | — | 구세대 |
| FLUX.2 dev · klein 9B · Ideogram 4 · Qwen-Image-2.1 | 비상업 / Research [2차] | **X** | — | — | 제외 |
| HunyuanImage 3.0 | "DOES NOT APPLY IN … SOUTH KOREA"(원문) | **X** | — | — | 제외 |

**fal 외 실행 경로 (1줄씩)**
| 경로 | 단가(추정) | 설치 난이도 | 비고 |
|---|---|---|---|
| Replicate | Z-Image Turbo 1MP 이하 $0.005/장 | 낮음(API) | 상업 OK 모델만 |
| RunPod 시간제 | RTX 4090 커뮤니티 약 $0.34/시간, 초 단위 과금 [2차] | 중(ComfyUI 템플릿) | 월 2시간이면 약 1천원. LoRA 학습도 가능 |
| Hugging Face | PRO $9/월에 ZeroGPU 40분/일 [2차] | 중(Space 필요) | 고정비라 소량 사용엔 비쌈 |
| 대표 개인 GPU PC + ComfyUI | 전기료만(0원에 가까움) | 중상(VRAM 12GB+ 권장, 추정) | 결과 PNG를 수동으로 올려야 함. 자동화 불가 |

- **한국 소재 품질:** 공개 벤치마크는 없다. 연구(CuRe arXiv 2506.08071, ICCVW 2025 "Lost in Translation")는 한복이 기모노·한푸와 섞이는 오류를 보고한다. Z-Image·Qwen은 "Korean folk painting"을 공필화 쪽으로, "seal"을 한자 낙관으로 그릴 위험이 있다(추정). → 네거티브 프롬프트 + LoRA + S0 A/B 실측으로 대응한다.
- **공개 민화 LoRA:** 모두 제외.
  - gagong Traditional-Korean-Painting(SDXL, OpenRAIL-M): 데이터 권리 불명
  - Hanbok_LoRA(SD1.5 애니): 화풍 부적합
  - flux-lora-korea-palace: 기반 모델이 dev 비상업
  - Civitai: 민화 LoRA 검색 결과 없음

**STYLE / NEGATIVE (고정 v1)**
- STYLE: `flat Korean minhwa folk painting, gouache mineral pigments on aged hanji mulberry paper, visible paper fibers, bold flat color fields with thin even ink outlines, naive decorative reverse perspective, muted obangsaek palette (cinnabar red, ochre yellow, celadon green, ink black, cream paper), generous empty paper space, matte, no gradients`
- NEG: `text, letters, calligraphy, hanzi, hangul, seal stamp, signature, watermark, logo, brand, person, human figure, face, hands, celebrity, cartoon or anime character, mascot, tiger, magpie, Chinese gongbi, Japanese ukiyo-e, photorealistic, 3d render, glossy, lens blur, gradient sky`
- Turbo는 증류 모델이라 네거티브가 약하게 듣는다(추정). 금지 요소는 긍정 표현("empty paper")과 사후 검수로 막는다.

**프롬프트 템플릿 10개** (모두 `{STYLE}`를 앞에 붙임)
| # | 용도 | 비율 | 프롬프트 |
|---|---|---|---|
| C1 | 표지 | 4:5 | `chaekgado bookshelf screen, stacked bound books, celadon vase with peony, brush pot, symmetrical, upper 40% plain empty hanji for title` |
| C2 | 표지 | 4:5 | `single large stylized {peony|lotus|persimmon branch} rising from bottom edge, oversized decorative leaves, top half empty paper` |
| B1 | 본문 | 4:5 | `small isolated {pomegranate|lotus pod|ink stone and brush|celadon jar}, centered lower third, 70% empty hanji` |
| B2 | 본문 | 4:5 | `border of cloud scrolls and peony scrolls along left and bottom edges only, interior plain paper` |
| B3 | 본문 | 4:5 | `pine, crane, deer, turtle, lingzhi, cloud and rock as a low horizon band in bottom 25%, rest empty paper` |
| L1 | 마지막 | 4:5 | `night variant on dark indigo paper, full moon disc, five peaks silhouette, pine trees, wheat-colored outlines, center empty dark field` |
| L2 | 마지막 | 4:5 | `closed bound book with knotted cord and folded fan on kraft paper, bottom-right corner, large empty area` |
| P1 | 사진 합성 | 936×410(2배로 생성) | `ornamental frame of peony and cloud scrolls around a flat solid FF00FF rectangle filling center 60%` (마젠타 = 사진 마스크) |
| P2 | 사진 합성 | 플레이트 | `wide hanji border with torn deckled inner edge, duotone kraft and ink, center flat solid FF00FF` |
| P3 | 사진 합성 | 4:5 | `minhwa lotus leaves and butterflies only along right third, left two-thirds plain cream paper reserved for photograph` |

**14세트 일관성 레시피**
1. STYLE·NEG는 버전을 붙여 고정한다. 세트 사이에 바꾸는 것은 `{motif}` 하나뿐이다.
2. 시드: 세트 기준값은 날짜 8자리, 장 n은 기준+n, 후보는 +100/+200. 채택한 시드·모델·LoRA 해시를 `plates/PLATES.json`에 기록한다.
3. 1세트에서 승인한 마스터 플레이트 2장을 klein 4B 멀티 참조(또는 Qwen-Edit)에 넣고 "same style, new motif"로 변주한다.
4. 사후 처리(CPU): 8색 팔레트 최근접 매핑(디더 없음) → 6~8단계 포스터라이즈 → **자체 한지 스캔** multiply 8~12% → 단색 그레인 σ 3~4.
5. 검수: tesseract로 글자 혼입 검사, 마스크 영역이 비었는지 확인, 세트 평균 색차 검사.

**LoRA 학습 계획 (일회성 총 $15 이하, 추정)**
| 단계 | 내용 | 비용(추정) |
|---|---|---|
| S0 | 같은 프롬프트 10개로 Turbo·Qwen-2512·klein 4B를 LoRA 없이 A/B | 약 $0.5 |
| S1 | §5-2의 책가도·화조·모란·십장생·일월오봉 원화에서 디테일 크롭 30~40장(1024px). 문자도·글자·낙관·호랑이 영역 제외. 캡션은 `kemnhw style, <대상>`. 1,500·2,500스텝 2회 | 약 $9 |
| S2 | 승인된 자체 플레이트 5~10장을 섞어 재학습 | 약 $5 |
| 평가 | 프롬프트 10 × 시드 3 그리드를 대표가 승인. 글자 혼입 0%, 공필화·일본풍 오인율(3인 블라인드), LoRA 스케일 0.6/0.8/1.0 비교, 원본과 너무 닮은 출력(LPIPS)은 폐기 | — |

## 7. GitHub 스킬·도구 (이미 설치된 canvas-design, gemini-carousel, graphic-designer, image, design-critique, design-system, theme-factory, accessibility-review와 겹치지 않는 것만)
| 후보 | 저장소 @ SHA (`git ls-remote` HEAD) | ★·최근 커밋(조회값) | 라이선스 | 더해 주는 것 | 우리 규칙과 충돌 |
|---|---|---|---|---|---|
| **frontend-design** | anthropics/skills @ `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4` · `skills/frontend-design/` | 179k · 2026-09-29 | Apache-2.0(폴더 LICENSE.txt) | HTML/CSS 미적 방향과 "템플릿 같은 기본값 회피" 지침. HTML 렌더러와 직결 | 없음 |
| **webapp-testing** | 같은 SHA · `skills/webapp-testing/` | 같음 | Apache-2.0 | Playwright 스크린샷·검증 스크립트. `carousel-qa` 자동화 바탕 | 없음 |
| **taste-skill** | Leonxlnx/taste-skill @ `ce26fc25c0e5e8cab638f883de62d9a86ee5e45b` · `skills/taste-skill/` | 91.8k · 2026-09-26 | MIT | "AI 티 나는 결과물" 회피 미감 규칙 | `imagegen-*` 계열은 외부 API 전제라 복사하지 않음 |
| ui-ux-pro-max | nextlevelbuilder/ui-ux-pro-max-skill @ `09170eec67eefd46a7ae85de61b40c194020f997` · `.claude/skills/ui-ux-pro-max/` | 132k · 2026-09-27 | MIT | 서체·색 조합 CSV와 로컬 검색 스크립트 | 같은 저장소의 `design-system`은 이름이 겹치므로 이 폴더만 복사. 데이터의 실존 브랜드 사례는 참고로만 |
| (도구) color.js | color-js/color.js(npm) | 2.3k | MIT | WCAG 2.1 대비 + APCA + OKLCH 계산 | 없음. `setup.sh`에서 npm으로 설치 |

- **제외:**
  - brand-guidelines: 실존 기업 브랜드를 다룸
  - apca-w3: All Rights Reserved + W3 전용 라이선스
  - HyperFrames 스킬: 공식 설치가 플러그인 방식이라 클라우드 세션에서 로드 불가. 릴스 단계에서 폴더 복사만 재검토
  - 캐러셀 생성기 저장소들: ★0~2, 일부는 유료 API 전제
  - awesome 목록 2종: LICENSE 파일 없음, 탐색용으로만
- 설치는 skill-installer가 **복사 방식**으로 하고(내용 무수정), `docs/SKILLS.md`에 출처·SHA·라이선스를 기록한다. 대표 승인 후 진행.
- **우리 전용 스킬 초안 3개**(`cardnews-art-director`, `minhwa-plate-prompting`, `carousel-qa`)는 **부록 A**에 SKILL.md 전문으로 실었다.

## 8. v3 시각 방향 3안
| 항목 | **1안 원화 아카이브 (추천)** | 2안 민화 플레이트 | 3안 하이브리드 콜라주 |
|---|---|---|---|
| 무드 | Public Domain Review × 박물관 도록. 진짜 조선 민화 디테일을 크게 보여 주고, 글은 고서 판면처럼 정돈 | 자체 LoRA로 만든 플랫 민화 일러스트. 그림책처럼 통일된 시리즈 | 실사 사진 + 민화 프레임·문양. 잡지 콜라주 |
| 타이포 | 세트 B(함렛 / 마루부리 / Black Han Sans 낙관) | 세트 A(송명 / 고운바탕 / 붓) | 세트 C(Noto Serif Black / Pretendard / 페이퍼로지) |
| 색 | 원화 고유색 + 한지 오프화이트 + ke-red 포인트 1 | 토큰 8색으로 팔레트 매핑 | 사진 듀오톤(ink + kraft) + ke-red |
| 질감 | 자체 한지 스캔 multiply 8% + 원화의 노화 흔적 보존 | 한지 스캔 + 그레인 | 종이 찢김 테두리(코드 마스크) |
| 이미지 | §5-2 원화 크롭(전체 → 2~4배 디테일), 실사 사진은 CC0·1유형만 | AI 플레이트(§6 템플릿) | Unsplash·Pexels·1유형 사진 + P1~P3 플레이트 |
| 릴스 | 같은 HTML을 Remotion에 넣어 원화 패닝·줌, 글자는 획 리빌, Kokoro CPU TTS 또는 무음 + 자막 | 플레이트 Ken Burns + 코드 모션 | 사진 컷 편집 + 프레임 애니메이션 |
| 월 비용(추정) | **0원**(한지 스캔 1회 약 1만원) | 약 1만원 + LoRA 1회 약 2만원 | 약 2~3만원 |
| 난이도 | 중하(렌더러 교체 + 원화 크롭 작업) | 중상(LoRA·검수 부담) | 중(사진 권리 확인이 매번 필요) |
| AI 티 위험 | **매우 낮음**(실물 유물) | 중(LoRA 품질에 좌우) | 중하 |
| 라이선스 위험 | 낮음(CC0·1유형, 출처 줄 필수) | 낮음(Apache 모델 + 자체 데이터) | 중(사진 속 인물·로고·건물 권리) |
| 호스팅 GPU 없이 가능 | **O**(CPU VM만으로 완결) | X(fal·RunPod·개인 PC 중 하나 필요) | 부분 O(P 플레이트를 빼면 O) |
| 차별성 | 원본 유물 = 남이 못 만드는 신뢰. 박물관 계정급 톤 | 고유 화풍이 생기지만 AI 계정이 많음 | 범용적 |

**1안이 "AI 0 · 유료 API 0"으로 세계 수준이 가능한가 → 가능하다고 판단한다(추정, 샘플로 검증 필요).** 근거와 처리법:
1. **원본:** Met 책가도(853896)·책거리 10폭(73134), Cleveland 책가도(2011.37)·문자도책거리(2017.6), 국립중앙박물관 책가도 3점·십장생·일월오봉, 천안박물관 괴석모란도(13485×8990px). 고해상도라 4배 크롭에도 1080px 이상이 나온다.
2. **크롭 문법:** 표지 = 병풍 한 폭 전체(세로 4:5와 잘 맞음). 본문 = 사물 디테일 2~4배(책갑·도자기·모란 꽃잎). 마지막 = 원화 전경을 축소한 띠.
3. **톤 처리(Pillow·CSS, CPU):** 레벨 보정으로 누런 변색을 살짝만 줄임 → 채도 -10% → 전 세트 같은 LUT 1개 → 자체 한지 스캔 multiply 8%. 원화의 균열과 얼룩은 보존한다.
4. **코드 그래픽:** 문화포털 전통문양(1유형) 벡터로 단청 띠·창살 프레임을 만들고, CSS로 낙관 박스·장번호·세로쓰기 캡션을 그린다.
5. **출처 줄:** 마지막 장에 "그림: 국립중앙박물관 〈책가도〉 공공누리 제1유형 · The Met CC0"를 고정한다. 출처 표시 의무와 신뢰감을 동시에 얻는다.
6. **AI 고지:** 1안에는 생성 이미지가 없으므로 캡션 고지를 "초안은 AI 도움, 사실 확인은 사람"으로 줄일 수 있다(PLAN 문구 변경은 대표 결정).
7. **한계:** 원화 31점은 반복 위험이 있다. 하루 1개 기준으로 약 2~3주마다 같은 작품이 돌아온다. → 디테일 부위를 바꾸고, Smithsonian·국립민속박물관 1유형 항목을 추가 조사하며, 2안 플레이트를 보조로 섞는다.

**릴스 무료 경로 확인:** 컷 구성은 Remotion(1인 무료) 또는 HyperFrames(Apache)로 원화 패닝·한글 획 리빌을 만들고, FFmpeg로 합성·자막 번인을 한다. 음성은 Kokoro(Apache, CPU, 이전 조사 Elo 1063)를 쓰거나 음성 없이 자막 + 무료 음원(YouTube 오디오 라이브러리 등)으로 간다. 이 경로라면 **유료 API 없이 VM 안에서 닫힌다**(추정, 미실행). 음색 품질은 상용보다 낮으므로 "자막 + 음악" 포맷을 기본으로 권한다.

**실행 순서 (월 5만원 안)**
| 시점 | 할 일 | 비용(추정) |
|---|---|---|
| 10/3~10/8(10/9 전) | ① `setup.sh`에 서체(세트 B + Noto Serif/Sans KR + 나눔명조 옛한글) 추가 ② HTML 렌더러 v3로 10/9 세트만 재렌더 ③ 원화 3점(국립중앙박물관 책가도, Met 853896, Cleveland 2011.37) 크롭 적용 ④ `carousel-qa`로 검수 → PR | 0원 |
| 10/9~10/22(C1-1 나머지) | 남은 13세트를 1안으로 순차 재렌더. 한지 3종 구입·스캔 | 약 1만원 |
| C1-2 | 스킬 4개 복사 설치, 2안 S0 A/B(약 700원) → 대표가 보고 LoRA 여부 결정 | 약 1천원 |
| C1-3~ | LoRA S1·S2(약 2만원), 1안 + 2안 보조 혼합, 릴스 Remotion 템플릿 | 월 1만원 이하 |

**대표 결정 필요:**
① v3 = 1안 채택 여부
② 10/9 첫 게시를 v3로 다시 만들지(일정 위험 있음), 아니면 현 v2로 게시하고 10/10부터 교체할지
③ 서체 세트 B 확정
④ 스킬 4개 복사 설치
⑤ LoRA 학습비(약 2만원) 지출
⑥ 디자인 시스템에 4:5·원화 사용 규칙 추가
⑦ 1안 게시물의 AI 고지 문구 조정

## 9. 자가 검증
| 기준 | 결과 |
|---|---|
| 벤치마크 10~15곳(한국 5+ · 해외 5+) | 15곳(한국 8 · 해외 7). 계정 존재는 공식 사이트로 확인, 피드 분석은 추정 표기 |
| 렌더 파이프라인 비교 + 추천 1 | 10종 비교, Chromium 실측 통과(옛한글·세로쓰기·keep-all) |
| 서체 제목·본문·강조 각 3 + 옛한글 표기 + 세트 3 | 13종 표기(실측 20종), 세트 3 |
| 질감·문양·색 소스 | 8종 채택, 5종 제외(사유 기재) |
| 퍼블릭 도메인 원화 20점 이상 | 31점(사용 가능 29 + 금지 모티프 2) |
| 모델 비교·프롬프트 10·일관성·LoRA·fal 외 경로 | 12모델, 프롬프트 10, 레시피 5단계, LoRA 3단계, 대안 경로 4 |
| 스킬 후보 5 이내 + 자체 초안 3 | 4 + 도구 1, 초안 3(부록 A) |
| v3 3안 + 추천 + 실행 순서 + "호스팅 GPU 없이" 열 | 충족 |
| 출처 수 | 고유 URL 약 70개 |
| 라이선스 원문 확인 비율 | 채택 항목 기준 약 85%. 나머지는 [2차]·미확인으로 표기(RunPod·HF·Replicate 일부 단가, klein 트레이너 단가, Qwen 2.1 라이선스) |
| 추정치 표기 | 모든 금액·벤치마크 분석·일정에 "추정" 표기 |
| 금지 사항 위반 | 0: 실존 인물·로고·IP·작가 모사 전제 제안 없음. 호랑이·까치는 목록에서 표시 후 제외. NC·ND·SA 제외. 설치·업로드·비밀값 접근 없음 |

## 출처 (확인일 2026-10-02)
- **렌더:**
  - github.com/microsoft/playwright · python-pillow/Pillow · HOST-Oman/libraqm · GNOME/pango
  - vercel/satori(README Typography) · linebender/resvg · Kozea/CairoSVG · skia-python/skia-python
  - remotion-dev/remotion/blob/main/LICENSE.md · heygen-com/hyperframes · penpot/penpot
- **서체:**
  - hangeul.naver.com/font(나눔·마루부리 저작권 안내)
  - github.com/google/fonts/tree/main/ofl · notofonts/noto-cjk · adobe-fonts/source-han-serif
  - orioncactus/pretendard · freesentation.blog/paperlogyfont
  - github.com/adrinerDP/font-kopubworld(LICENSE.md) · sandollcloud.com/free-font/15810
- **질감·원화:**
  - docs.ambientcg.com/license · polyhaven.com/license · unsplash.com/license · pexels.com/license
  - culture.go.kr/tradition/traditionalUseDesignView.do?seq=3456 · kogl.or.kr/info/licenseType1.do · gongu.copyright.or.kr
  - emuseum.go.kr/copyright · museum.go.kr/MUSEUM/contents/M3304000000.do
  - metmuseum.org Open Access API · clevelandart.org/open-access
  - news.seoul.go.kr/culture/?p=521810(서울색, 제외 근거)
- **AI 모델:**
  - fal.ai/models/fal-ai/z-image/turbo · …/z-image/turbo/lora · …/z-image/base · …/z-image-trainer
  - huggingface.co/Tongyi-MAI/Z-Image · black-forest-labs/FLUX.2-klein-4B · FLUX.2-klein-9B · fal.ai/models/fal-ai/flux-2/klein/4b
  - fal.ai/models/fal-ai/qwen-image-2512 · qwen-image-edit-2511 · huggingface.co/HiDream-ai/HiDream-I1-Full
  - huggingface.co/tencent/HunyuanImage-3.0/blob/main/LICENSE · stability.ai/community-license-agreement · replicate.com/prunaai/z-image-turbo
  - arxiv.org/pdf/2506.08071 · openaccess.thecvf.com(ICCVW 2025 Lost in Translation) · huggingface.co/gagong/Traditional-Korean-Painting-Model-v2.0
  - [2차] invideo.io/blog/open-source-image-models-licenses · llmreference.com/model/qwen-image-2.1 · hivenet.com/post/runpod-pricing-complete-guide-to-gpu-cloud-costs · eesel.ai/en/blog/hugging-face-pricing
- **스킬:**
  - github.com/anthropics/skills · Leonxlnx/taste-skill · nextlevelbuilder/ui-ux-pro-max-skill
  - color-js/color.js · Myndex/apca-w3/blob/master/LICENSE.md(제외 근거)
- **벤치마크(존재 확인용):**
  - museum.go.kr/CHILD/contents/snsGuideCHILD.do · hangeul.go.kr · heritage.go.kr · mediahub.seoul.go.kr/staticpage/sns.do
  - magazine-b.com · everyday-practice.com · rijksmuseum.nl · cooperhewitt.org · publicdomainreview.org
  - pentagram.com · itsnicethat.com · kinfolk.com · tnm.jp

## 부록 A. 우리 전용 스킬 초안 3개 (SKILL.md 전문, 설치는 대표 승인 후 `.claude/skills/`에)

### A-1. `.claude/skills/cardnews-art-director/SKILL.md`
```markdown
---
name: cardnews-art-director
description: 책가도 노트 카드뉴스(1080x1350, 7장)의 아트 디렉터. cards.json 브리프를 받아 장별 시각 설계(레이아웃·위계·플레이트/사진 역할)를 쓰고, 렌더 후 원본·360px 축소본을 보고 검수 판정을 낸다. 새 게시물 설계, 디자인 반려 재작업, 시리즈 일관성 점검 때 쓴다.
---
# cardnews-art-director
## 입력
- `cardnews/posts/<날짜>/cards.json`(장별 headline·body·visual·type), 디자인 토큰(`template.md` §2~3), v3 방향 문서(`cardnews/docs/DESIGN_SOURCES.md` §8).
## 절차
1. **한 장 한 메시지**: 장마다 "독자가 이 장에서 가져갈 한 문장"을 15자 안으로 적는다. 못 적으면 장을 합치거나 나눈다.
2. **장 역할 지정**: 표지(훅) / 전개 / 근거(숫자·사진) / 전환 / 정리 / CTA·출처. 7장 중 같은 레이아웃은 연속 3장 이상 금지.
3. **위계 3단 고정**: 제목:본문 크기 비율 ≥ 2.2:1, 3단(제목·본문·캡션) 외 크기 금지. 한 장 강조색 1개.
4. **그리드**: 12열 × 기준선 8px, 바깥 여백 ≥ 88px(8%). 제목은 좌측 정렬 기본, 중앙 정렬은 표지·CTA만.
5. **이미지 역할 선택**(장마다 하나): A 민화 플레이트(AI, 글자 없음) / B 실사 사진(라이선스 기록 필수) / C 공공 원본 디테일 크롭(PD·공공누리1) / D 이미지 없음(타이포만). 같은 게시물에 A·B·C 중 최대 2종.
6. **브리프 표 출력**: | 장 | 역할 | 한 문장 | 레이아웃 | 이미지 역할·프롬프트 ID 또는 사진 출처 | 강조색 |.
7. 렌더 후 `carousel-qa` 체크리스트를 돌리고, 원본+contact를 **직접 열어** 아래 기준으로 판정한다.
## 검수 기준 (하나라도 X면 반려)
- 360px 축소에서 표지 제목 3초 안에 읽힘 / 장마다 시선 첫 지점이 제목 / 빈 영역이 의도된 여백인지(30% 이상 빈 띠가 무의미하게 남으면 X)
- 이미지가 그 장 내용과 직접 관련 / 같은 모티프가 한 게시물에서 2회 이상 반복되지 않음
- 시리즈 고정 요소(로고 라벨 위치·장 번호·여백·서체)가 지난 게시물과 같음
## 금지
실존 인물 얼굴·브랜드 로고·IP 캐릭터·특정 작가 화풍 모사 지시, 호랑이·까치 모티프(디자인 시스템 금지), 이미지 안 글자, 과장 문구, em dash.
## 출력
`cardnews/posts/<날짜>/ART_BRIEF.md`(설계 표 + 판정 표). 판정은 통과/반려 + 반려 장 번호와 고칠 점 1줄씩.
```

### A-2. `.claude/skills/minhwa-plate-prompting/SKILL.md`
```markdown
---
name: minhwa-plate-prompting
description: 책가도 노트·Korea Explained용 민화 플랫 × 한지 배경 플레이트(글자 없는 이미지) 프롬프트를 모델별로 만들고, 시드·스타일 문자열·팔레트 후처리로 시리즈 일관성을 유지한다. 플레이트 생성 전, LoRA 학습 데이터 준비 때 쓴다.
---
# minhwa-plate-prompting
## 고정값
- STYLE·NEGATIVE: `cardnews/docs/DESIGN_SOURCES.md` §6 "STYLE / NEGATIVE (고정 v1)" 문자열을 그대로 쓴다. 바꿀 때는 v2로 올리고 대표 승인.
- 팔레트(후처리 매핑): #F7F3EA #111111 #C8102E #FFD23F #1B1F2A #C9A877 #6FA89B #F2D49B
## 절차
1. 브리프의 이미지 역할 A/C만 처리. 장마다 `PLATE_ID = <날짜>-<장>-<v>`.
2. 모델 선택: 기본 Z-Image Turbo(Apache-2.0) + 자체 LoRA(학습 후). 대안 Qwen-Image(Apache-2.0). 라이선스가 비상업·지역 배제인 모델(FLUX.2 dev, Hunyuan 계열 등)은 쓰지 않는다.
3. 프롬프트 = `[주제 1문장: 소재·구도·빈 공간 위치] + STYLE + [비율]`. 빈 공간 위치는 텍스트 자리와 맞춘다(예: "empty upper 40%").
4. 시드: 게시물마다 기준 시드 1개(날짜 숫자 8자리)를 정하고 장 n은 +n, 후보는 +100/+200. 3안 생성 → 1안 채택, 시드·모델·LoRA 버전을 `plates/PLATES.json`에 기록.
5. 후처리(코드): 팔레트 8색 최근접 매핑(디더 없음) → 한지 결 레이어 multiply 8~12% → 가장자리 비네트 없음.
6. 검사: 이미지 안 글자·얼굴·로고·호랑이·까치 0(육안 + 의심 시 재생성). 실패 3회면 역할 D(타이포만)로 바꾼다.
## 금지
실존 작가명·"in the style of <작가>" 금지, 박물관 원본을 img2img로 그대로 덮어 쓰기 금지(참고·학습만, 라이선스 기록 필수), 생성물을 실제 유물인 것처럼 설명 금지(캡션 AI 고지 유지).
## 출력
`cardnews/posts/<날짜>/plates/PLATES.json` + 썸네일(커밋 가능 크기). 원본 고해상도는 렌더 입력으로만.
```

### A-3. `.claude/skills/carousel-qa/SKILL.md`
```markdown
---
name: carousel-qa
description: 인스타 캐러셀(1080x1350) 렌더 결과를 게시 전에 자동·육안으로 검수한다. 원본과 360px 피드 크기에서 글자 잘림·대비·안전 영역·서체 대체·AI 표시·출처 줄을 체크리스트로 판정한다. 렌더 직후, PR 생성 직전에 쓴다.
---
# carousel-qa
## 자동 체크 (스크립트로 판정, 결과를 표로)
| # | 항목 | 기준 |
|---|---|---|
| 1 | 규격 | 1080x1350 sRGB PNG, 장 수 = cards.json |
| 2 | 서체 | RENDER.json 글꼴이 지정 서체와 일치. 폴백(WenQuanYi·DejaVu 등)·가짜 볼드 = 실패 |
| 3 | 글리프 누락 | 모든 문자가 지정 서체 cmap에 있음(두부 □ 0). 옛한글은 조합형 지모 + ljmo/vjmo/tjmo 서체만 |
| 4 | 잘림·넘침 | 텍스트 박스 bbox가 안전 영역(사방 88px) 안. 줄 수 상한(제목 2, 본문 3) |
| 5 | 대비 | 글자 대비 WCAG ≥ 4.5:1(제목 36px↑은 ≥ 3:1). 사진·플레이트 위 글자는 뒤 픽셀 실측 |
| 6 | 축소 판독 | 360x450 축소본에서 제목 x-height ≥ 9px, 본문 ≥ 5px |
| 7 | 1:1 크롭 | 표지 제목이 y 135~1215 안 |
| 8 | 고지 | 마지막 장 출처 1줄 + AI 표시 문구 + 핸들. 캡션 끝 AI 고지, 협찬이면 첫 줄 "#광고" |
| 9 | 금지 문자 | em dash, MOCKUP 표기(게시본), 과장 단어 목록 |
| 10 | 용량 | 장당 ≤ 8MB, 업로드 전 미리보기 1회 |
## 육안 체크 (원본 + contact 시트를 직접 열어서)
- 행 끝 한 글자 고아·조사 분리, 제목 줄바꿈이 의미 단위인가(word-break: keep-all 결과)
- 자간·행간: 제목 자간 -2~-4%, 본문 행간 1.5~1.7, 본문 한 줄 18~24자
- 이미지 안 글자·얼굴·로고·호랑이·까치 0, 사진 라이선스 기록과 출처 줄 일치
- 7장 연속 넘김 리듬(같은 레이아웃 3연속 없음), 지난 게시물과 고정 요소 일치
## 출력
`cardnews/posts/<날짜>/QA.md`: 항목별 통과/실패 표 + 실패 장 썸네일 경로. 실패 1개라도 있으면 PR 생성 금지.
```
