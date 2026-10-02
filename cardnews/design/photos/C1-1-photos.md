# C1-1 실사 사진 후보 목록 (책가도 노트, 14세트)

- 작성: researcher · 2026-10-02 · 브랜치 `cardnews/c1-1-design` (커밋·푸시 안 함, 다운로드는 designer)
- 근거: 대표 결정(2026-10-02) 디자인 v2 = AI 민화 배경 + 실사 사진. COO 추가 지시: **세트 01(10/09)은 AI 없이 공개 원본 + 편집 실사만으로 만드는 프로토타입 → 최우선, 후보 5개 이상, 2차 가공 허용 라이선스만**.
- 입력: `cardnews/posts/2026-10-DD/cards.json`, `cardnews/posts/C1-1-plan.md` §1, `cardnews/docs/risk-C1-1.md` §1 5번 행.
- 기계용 목록: `cardnews/design/photos/C1-1-photos.json` (같은 내용, `modifiable`·`role` 필드 포함)

## 0. 성공 기준 (작업 시작 전에 적음)

| 기준 | 목표 |
|---|---|
| 라이선스 | 상업 이용 + 가공(크롭·톤 보정·질감 합성) 허용만: 공공누리 1유형, CC0, CC BY 2.0/3.0/4.0, 퍼블릭 도메인. BY-SA·NC·ND·공공누리 2~4·불명 0건 |
| 내용 | 알아볼 수 있는 얼굴 0, 상표·포장·간판 로고 0, 현대 미술·영화 스틸·포스터 0, 군사·정치 0 (크롭으로 제거해야 하는 것은 메모에 "크롭 필수") |
| 수량 | 세트당 1~3장 + 예비 1장, 세트 01은 5개 이상 |
| 검증 | 후보 전부 파일 페이지에서 라이선스 확인, 썸네일 육안 확인 |
| 링크 | 직접 내려받을 원본 URL(upload.wikimedia.org 또는 미술관 CDN) |

## 공통 메모 (designer)

- 플레이트 영역: 표지 936x410(약 2.28:1), 본문 936x408, 마지막 936x160 (`cardnews/design/template.md` §5). 해상도는 모두 가로 1000px 이상이라 크롭 여유가 있다.
- **크레딧은 카드에 한 줄**(아래 "크레딧" 열 그대로) + **캡션 출처 줄에 라이선스 URL**을 함께 적는다. CC BY 2.0/3.0은 라이선스 URI를 표시해야 하고, CC BY는 가공하면 "변경했음"을 밝혀야 해서 크레딧에 "크롭·보정"을 넣었다.
- 공공누리 1유형은 출처 표시만 하면 상업 이용과 변경이 모두 된다. 캡션에는 "○○(기관)이 공공누리 제1유형으로 개방한 저작물을 이용" 형식을 권장한다.
- 퍼블릭 도메인(PD)과 CC0는 법적으로 크레딧이 필요 없지만, 사실 확인을 위해 소장처를 적는다.
- 썸네일(500~960px)로 얼굴과 로고를 확인했다. **원본 해상도에서 얼굴은 designer가 한 번 더 확인**해야 한다(특히 "크롭 필수" 표시 항목).
- 여러 세트가 같은 사진을 후보로 쓰는 경우가 있다(메모에 "중복"으로 표시). 실제 게시에서는 한 세트에만 쓰는 것을 권장한다.
- 라이선스 약어: KOGL1 = 공공누리 제1유형, PD = 퍼블릭 도메인(Commons 템플릿 PD-South Korea + PD-1923).

---

## 1. ★ 세트 01 · 10/09 "올해 한글날이 '100돌'인 이유" (프로토타입, 후보 8)

| 장 | 역할 | 내용 | 파일 페이지 | 원본 직접 URL | 작가/기관 | 라이선스 | 크레딧(카드 한 줄) | 해상도 | 위험 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 메인 | 월인천강지곡 한글 금속활자판 **복제품**(1447년 원본 기준) | [Commons](https://commons.wikimedia.org/wiki/File:Worin_cheon-gang-ji-gok_movable_type_(replica),_1447_-_Korean_Culture_Museum,_Incheon_Airport,_Seoul,_South_Korea_-_DSC00793.JPG) | https://upload.wikimedia.org/wikipedia/commons/4/44/Worin_cheon-gang-ji-gok_movable_type_%28replica%29%2C_1447_-_Korean_Culture_Museum%2C_Incheon_Airport%2C_Seoul%2C_South_Korea_-_DSC00793.JPG | Daderot | CC0 1.0 | 사진: Daderot · CC0 | 4320x3240 | 인천공항 한국문화박물관에 전시된 복제품이라 카드에 "복제품"이라고 적는다. 파일 설명의 "원본은 도쿄 인쇄박물관"은 확인하지 못했다(미검증). 진열장 반사와 검은 테두리는 크롭. 얼굴·로고 없음 |
| 2 | 메인 | 훈민정음 해례본 예의 첫 장(國之語音… 新制二十八字) | [Commons](https://commons.wikimedia.org/wiki/File:Hunminjeongeum_Haerye_02.jpg) | https://upload.wikimedia.org/wikipedia/commons/1/16/Hunminjeongeum_Haerye_02.jpg | 조선 정부(1446) / 스캔: 규장각 GG43224 | PD | 훈민정음 해례본(1446) · 퍼블릭 도메인 · 이미지: 규장각 | 1920x1280 | 영인본(간송본) 스캔이고 발행 연도는 미검증. 도서관 소장 인장과 청구기호 스티커(316761)는 크롭. 규장각 이미지 이용 조건은 확인하지 못함(Commons 표기는 PD) |
| 3 | 메인 | 문자도·책거리 8폭 병풍(孝悌忠信禮義廉恥) | [Commons](https://commons.wikimedia.org/wiki/File:Anonymous_-_Munja-Chaekgeori_Screen_(Character-Books_Screen)_-_2017.6_-_Cleveland_Museum_of_Art.tiff) · [미술관](https://clevelandart.org/art/2017.6) | https://openaccess-cdn.clevelandart.org/2017.6/2017.6_print.jpg (원본 TIFF 16879x7907: https://upload.wikimedia.org/wikipedia/commons/c/c5/Anonymous_-_Munja-Chaekgeori_Screen_%28Character-Books_Screen%29_-_2017.6_-_Cleveland_Museum_of_Art.tiff) | 작자 미상 / 클리블랜드미술관 | CC0 1.0 (미술관 API: share_license_status CC0) | 문자도 병풍(20세기 초) · 클리블랜드미술관 · CC0 | 3400x1593 | 새·물고기 모티프는 있지만 호랑이·까치는 아님. Commons의 날짜 "1000"은 오기이고, 미술관 레코드는 "early 1900s". 10/11 예비와 중복 |
| 4 | 메인 | 훈민정음 해례본 표지("訓民正音") | [Commons](https://commons.wikimedia.org/wiki/File:Hunminjeongeum_Haerye_01_(front_cover).jpg) | https://upload.wikimedia.org/wikipedia/commons/0/04/Hunminjeongeum_Haerye_01_%28front_cover%29.jpg | 조선 정부 / 스캔: 규장각 | PD | 훈민정음 해례본 표지 · 퍼블릭 도메인 · 이미지: 규장각 | 1920x1280 | 오른쪽 아래 도서관 청구기호 라벨은 크롭. 10/22 3장과 중복 |
| 5 | 조건부 | 19세기 점자 쓰기 틀(스웨덴 1871년) | [Commons](https://commons.wikimedia.org/wiki/File:Writing_frame_for_the_blind,_Stockholm,_Sweden_Wellcome_L0059116.jpg) | https://upload.wikimedia.org/wikipedia/commons/e/ea/Writing_frame_for_the_blind%2C_Stockholm%2C_Sweden_Wellcome_L0059116.jpg | Wellcome Collection (Science Museum, London) | CC BY 4.0 | 사진: Wellcome Collection · CC BY 4.0 · 크롭 | 4256x2832 | **훈맹정음 유물이 아니다.** 쓴다면 카드에 "19세기 점자 쓰기 도구(스웨덴)"라고 밝히고, 아니면 5장은 사진 없이 둔다. 제조사 각인(C A Carlsson)이 작게 보이므로 크롭 권장 |
| 6 | 메인 | 경복궁 광화문 야경(2012) | [Commons](https://commons.wikimedia.org/wiki/File:경복궁_광화문_(2012).jpg) | https://upload.wikimedia.org/wikipedia/commons/6/68/%EA%B2%BD%EB%B3%B5%EA%B6%81_%EA%B4%91%ED%99%94%EB%AC%B8_%282012%29.jpg | 국가유산청(구 문화재청) | KOGL1 | 사진: 국가유산청 · 공공누리 1유형 | 4000x2385 | 문 앞에 원경 인물 몇 명(알아볼 수 없는 크기)과 차량 불빛 궤적. 2023년 월대 복원 이전 모습 |
| 6 | 예비 | 광화문·월대와 경복궁 전경(2023) | [Commons](https://commons.wikimedia.org/wiki/File:광화문_월대.jpg) | https://upload.wikimedia.org/wikipedia/commons/6/63/%EA%B4%91%ED%99%94%EB%AC%B8_%EC%9B%94%EB%8C%80.jpg | 서울관광아카이브 | KOGL1 | 사진: 서울관광아카이브 · 공공누리 1유형 | 6512x4341 | **크롭 필수**: 아래쪽 광장 군중과 노선 표시 버스가 보이므로 위쪽 약 60%(산·궁궐 지붕)만 쓴다. 10/21 예비와 중복 |
| 2·4 | 예비 | 훈민정음 언해본 첫 자음 면(ㄱ·ㅋ) | [Commons](https://commons.wikimedia.org/wiki/File:Hunminjeongeum_Eonhae_04.jpg) | https://upload.wikimedia.org/wikipedia/commons/f/f2/Hunminjeongeum_Eonhae_04.jpg | 조선 정부 / 이미지: 국립한글박물관 아카이브 | PD | 훈민정음 언해본(월인석보 권1, 1568년 간행) · 퍼블릭 도메인 · 이미지: 국립한글박물관 | 3442x2480 | 10/16 2장과 중복. 국립한글박물관 아카이브 페이지에서 이용 조건 문구를 찾지 못함(Commons 표기는 PD) |

- 세트 01에서 찾지 못한 것: **대한민국역사박물관 외관.** Commons 후보는 CC BY-SA이거나(불가), CC BY 4.0이어도 정부 상징 로고·기관 간판·"ITALY KOREA" 배너가 정면에 있어(Jjw 2024) 제외했다. **한글날 기념식·광화문 행사 사진**은 Korea.net 계열이 모두 CC BY-SA 2.0이거나 얼굴이 나와 제외했다. 훈맹정음 원본(1926) 이미지는 저작자 박두성이 1963년 사망해 보호기간이 남아 있어 찾지 않았다.

## 2. 10/10 "가을 궁중문화축전, 남은 이틀 궁궐 5곳"

| 장 | 역할 | 내용 | 파일 페이지 | 원본 직접 URL | 작가/기관 | 라이선스 | 크레딧 | 해상도 | 위험 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 메인 | 경복궁 근정전 일대 부감 | [Commons](https://commons.wikimedia.org/wiki/File:경복궁_근정전_근정전_전경(궁능유적본부)-min.jpg) | https://upload.wikimedia.org/wikipedia/commons/e/e6/%EA%B2%BD%EB%B3%B5%EA%B6%81_%EA%B7%BC%EC%A0%95%EC%A0%84_%EA%B7%BC%EC%A0%95%EC%A0%84_%EC%A0%84%EA%B2%BD%28%EA%B6%81%EB%8A%A5%EC%9C%A0%EC%A0%81%EB%B3%B8%EB%B6%80%29-min.jpg | 국가유산청 궁능유적본부 | KOGL1 | 사진: 국가유산청 궁능유적본부 · 공공누리 1유형 | 2000x1013 | 사람 없음. 비율 1.97:1이라 위아래만 조금 크롭 |
| 6 | 메인 | 창경궁 춘당지 가을(2012-11-15) | [Commons](https://commons.wikimedia.org/wiki/File:창경궁_춘당지_(2012).jpg) | https://upload.wikimedia.org/wikipedia/commons/6/61/%EC%B0%BD%EA%B2%BD%EA%B6%81_%EC%B6%98%EB%8B%B9%EC%A7%80_%282012%29.jpg | 국가유산청(구 문화재청) | KOGL1 | 사진: 국가유산청 · 공공누리 1유형 | 4000x1737 | 사람 없음(작은 배 1척). "물빛연화" 행사 장면이 아니므로 장소 사진으로만 쓴다 |
| 7 | 메인 | 창덕궁 일대 가을 부감(2012-11-16) | [Commons](https://commons.wikimedia.org/wiki/File:창덕궁_전경_(2012).jpg) | https://upload.wikimedia.org/wikipedia/commons/d/d4/%EC%B0%BD%EB%8D%95%EA%B6%81_%EC%A0%84%EA%B2%BD_%282012%29.jpg | 국가유산청(구 문화재청) | KOGL1 | 사진: 국가유산청 · 공공누리 1유형 | 4000x2283 | 원경 도로의 차량·버스와 아주 작은 행인. 버스 광고는 판독할 수 없는 크기. 궁역 중심으로 크롭 권장 |
| 3 | 예비 | 경복궁 경회루 야경 | [Commons](https://commons.wikimedia.org/wiki/File:경복궁_경회루_야경(궁능유적본부)-min.jpg) | https://upload.wikimedia.org/wikipedia/commons/7/72/%EA%B2%BD%EB%B3%B5%EA%B6%81_%EA%B2%BD%ED%9A%8C%EB%A3%A8_%EC%95%BC%EA%B2%BD%28%EA%B6%81%EB%8A%A5%EC%9C%A0%EC%A0%81%EB%B3%B8%EB%B6%80%29-min.jpg | 국가유산청 궁능유적본부 | KOGL1 | 사진: 국가유산청 궁능유적본부 · 공공누리 1유형 | 2000x961 | 사람 없음. "한복 연향" 행사 사진이 아니므로 장소 사진으로만 쓴다 |

## 3. 10/11 "호랑이 옆에 왜 까치가 있을까" (호랑이·까치 원본은 보류, 책가도 우선)

| 장 | 역할 | 내용 | 파일 페이지 | 원본 직접 URL | 작가/기관 | 라이선스 | 크레딧 | 해상도 | 위험 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 메인 | 이택균 책가도 10폭(19세기 후반) | [Commons](https://commons.wikimedia.org/wiki/File:Yi_Taek-gyun_-_Books_and_Scholars’_Accouterments_-_2011.37_-_Cleveland_Museum_of_Art.tif) · [미술관](https://clevelandart.org/art/2011.37) | https://openaccess-cdn.clevelandart.org/2011.37/2011.37_print.jpg (TIFF 11838x6670: https://openaccess-cdn.clevelandart.org/2011.37/2011.37_full.tif) | 이택균 / 클리블랜드미술관 | CC0 1.0 (미술관 API 확인) | 책가도(이택균) · 클리블랜드미술관 · CC0 | 3400x1915 | 호랑이·까치 없음. 계정 정체성(책가도)에 가장 가까운 원본 |
| 6 | 메인 | 책거리 10폭 병풍(20세기 초) | [Commons](https://commons.wikimedia.org/wiki/File:Books_and_Scholars'_Possessions_(Chaekgeori),_MET_2005.385.jpg) | https://upload.wikimedia.org/wikipedia/commons/9/96/Books_and_Scholars%27_Possessions_%28Chaekgeori%29%2C_MET_2005.385.jpg | 작자 미상 / 메트로폴리탄미술관 | CC0 1.0 | 책거리 병풍 · 메트로폴리탄미술관 · CC0 | 4000x1653 | **크롭 필수**: 아래쪽 컬러차트와 "Image copyright The Metropolitan Museum of Art" 문구 |
| 2 | 예비 | 문자도·책거리 병풍 | (세트 01의 3장과 같음) | https://openaccess-cdn.clevelandart.org/2017.6/2017.6_print.jpg | 클리블랜드미술관 | CC0 1.0 | 문자도 병풍 · 클리블랜드미술관 · CC0 | 3400x1593 | 10/09와 중복 |

## 4. 10/12 "2026 단풍 달력, 산별 절정 날짜"

| 장 | 역할 | 내용 | 파일 페이지 | 원본 직접 URL | 작가/기관 | 라이선스 | 크레딧 | 해상도 | 위험 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 메인 | 설악산 단풍 숲길(2016-10, 인제) | [Commons](https://commons.wikimedia.org/wiki/File:Way_Through_Autumn_Forest_(187194663).jpeg) | https://upload.wikimedia.org/wikipedia/commons/c/c9/Way_Through_Autumn_Forest_%28187194663%29.jpeg | Eirien | CC BY 3.0 | 사진: Eirien · CC BY 3.0 · 크롭·보정 | 2048x1361 | 사람 없음. 500px에서 가져온 파일(import-500px). 촬영지는 파일 설명과 좌표 기준 설악산 |
| 4 | 메인 | 내장산 능선 단풍 + 내장사(2013-10-31) | [Commons](https://commons.wikimedia.org/wiki/File:Najaengsan.JPG) | https://upload.wikimedia.org/wikipedia/commons/5/54/Najaengsan.JPG | Commons 사용자 "Café Bene" | CC0 1.0 | 사진: Café Bene(위키미디어 사용자) · CC0 | 4096x3072 | **크롭 필수**: 아래쪽 경내에 등산객이 많고 얼굴을 알아볼 수 있다. 위쪽 약 55%(능선·단풍·탑 끝)만 쓴다. 업로더 이름이 상호명과 같지만 사진에 로고는 없다 |
| 5 | 메인 | 지리산 능선 겹(2006-10-06) | [Commons](https://commons.wikimedia.org/wiki/File:Korea-Mountain-Jirisan-01.jpg) | https://upload.wikimedia.org/wikipedia/commons/7/73/Korea-Mountain-Jirisan-01.jpg | eimoberg | CC BY 2.0 (FlickreviewR 확인) | 사진: eimoberg · CC BY 2.0 · 크롭 | 2272x1704 | 사람 없음. 10월 초 사진이라 단풍이 적어 "능선" 용도 |
| 5 | 예비 | 지리산 바위 능선과 이른 단풍 | [Commons](https://commons.wikimedia.org/wiki/File:Korea-Mountain-Jirisan-08.jpg) | https://upload.wikimedia.org/wikipedia/commons/2/26/Korea-Mountain-Jirisan-08.jpg | eimoberg | CC BY 2.0 (FlickreviewR 확인) | 사진: eimoberg · CC BY 2.0 · 크롭 | 2272x1704 | 사람 없음 |

- 3장(오대산)은 **사진 없음.** Commons의 오대산·월정사 사진은 거의 모두 CC BY-SA이고, 공공누리 1유형 사진은 찾지 못했다.

## 5. 10/13 "빵을 샀는데 주인공은 책갈피" (상표 없는 일반 사물만)

| 장 | 역할 | 내용 | 파일 페이지 | 원본 직접 URL | 작가/기관 | 라이선스 | 크레딧 | 해상도 | 위험 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 메인 | 크림빵 단면(흰 배경, 포장 없음) | [Commons](https://commons.wikimedia.org/wiki/File:Cream_pan_003.jpg) | https://upload.wikimedia.org/wikipedia/commons/f/f3/Cream_pan_003.jpg | Ocdp | CC0 1.0 | 사진: Ocdp · CC0 | 5336x2412 | 일본식 크림빵이다. 협업빵 실물이 아니므로 "빵 예시"로만 쓴다. 상표·포장 없음 |
| 3 | 메인 | 책 옆면에 꽂힌 색 인덱스 탭 | [Commons](https://commons.wikimedia.org/wiki/File:Book_(35577498971).jpg) | https://upload.wikimedia.org/wikipedia/commons/9/9c/Book_%2835577498971%29.jpg | Dean Hochman | CC BY 2.0 (FlickreviewR 확인) | 사진: Dean Hochman · CC BY 2.0 · 크롭 | 4624x2763 | 로고·글자 없음. 10/17 예비와 중복 |
| 2 | 예비 | 사워도우 빵 단면 | [Commons](https://commons.wikimedia.org/wiki/File:Slices_of_sourdough_bread.jpg) | https://upload.wikimedia.org/wikipedia/commons/d/d5/Slices_of_sourdough_bread.jpg | Angel Ganev | CC BY 2.0 (FlickreviewR 확인) | 사진: Angel Ganev · CC BY 2.0 · 크롭 | 3436x3436 | 편의점 빵과 종류가 다름. 상표 없음 |

## 6. 10/14 "10월 남은 주말 3번 캘린더"

| 장 | 역할 | 내용 | 파일 페이지 | 원본 직접 URL | 작가/기관 | 라이선스 | 크레딧 | 해상도 | 위험 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 메인 | 설악산 계곡 단풍(2016-10) | [Commons](https://commons.wikimedia.org/wiki/File:Beautiful_Foliage_In_South_Korea_(187194125).jpeg) | https://upload.wikimedia.org/wikipedia/commons/8/89/Beautiful_Foliage_In_South_Korea_%28187194125%29.jpeg | Eirien | CC BY 3.0 | 사진: Eirien · CC BY 3.0 · 크롭·보정 | 2048x1361 | 사람 없음. 계곡 원경에 건물 지붕이 작게 보인다. Commons 분류는 Seoraksan |
| 1 | 메인 | 설악산 돌탑과 소나무 숲(2016-10) | [Commons](https://commons.wikimedia.org/wiki/File:Seoraksan_National_Park_(187188929).jpeg) | https://upload.wikimedia.org/wikipedia/commons/c/c8/Seoraksan_National_Park_%28187188929%29.jpeg | Eirien | CC BY 3.0 | 사진: Eirien · CC BY 3.0 · 크롭·보정 | 2048x1361 | 사람 없음. 표지에 쓰면 캡션에 "설악산"이라고 적는다 |
| 5 | 예비 | 내장산 능선 단풍 | (10/12의 4장과 같음) | https://upload.wikimedia.org/wikipedia/commons/5/54/Najaengsan.JPG | Café Bene | CC0 1.0 | 사진: Café Bene(위키미디어 사용자) · CC0 | 4096x3072 | 크롭 필수(군중). 10/12와 중복 |

- 2장(하늘공원 억새)과 3장(오대산)은 **사진 없음.** 하늘공원 억새는 CC BY-SA이거나 550px 저해상도뿐이다.

## 7. 10/15 "K-라면, 올해 수출 20억 달러 도전" (상표 없는 일반 음식만)

| 장 | 역할 | 내용 | 파일 페이지 | 원본 직접 URL | 작가/기관 | 라이선스 | 크레딧 | 해상도 | 위험 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 메인 | 포장 없는 즉석면 블록 | [Commons](https://commons.wikimedia.org/wiki/File:Typical_instant_noodles.jpg) | https://upload.wikimedia.org/wikipedia/commons/d/da/Typical_instant_noodles.jpg | Ninosan | CC0 1.0 | 사진: Ninosan · CC0 | 1842x1382 | 포장·로고·사람 없음 |
| 6 | 메인 | 그릇에 담긴 라면(2020, 한국) | [Commons](https://commons.wikimedia.org/wiki/File:20200804_033546_Ramyeon_IMG_8515.jpg) | https://upload.wikimedia.org/wikipedia/commons/5/58/20200804_033546_Ramyeon_IMG_8515.jpg | 최광모 | CC0 1.0 | 사진: 최광모 · CC0 | 4032x3024 | 로고·사람 없음 |
| 6 | 예비 | 해물라면(식당 상차림) | [Commons](https://commons.wikimedia.org/wiki/File:Haemul-ramyeon.jpg) | https://upload.wikimedia.org/wikipedia/commons/f/fb/Haemul-ramyeon.jpg | lazy fri13th | CC BY 2.0 (FlickreviewR 확인) | 사진: lazy fri13th · CC BY 2.0 · 크롭 | 4032x3024 | 왼쪽 위에 집게나 손 일부가 보일 수 있어 크롭 |

## 8. 10/16 "사라진 한글 네 글자" (EP002)

| 장 | 역할 | 내용 | 파일 페이지 | 원본 직접 URL | 작가/기관 | 라이선스 | 크레딧 | 해상도 | 위험 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 메인 | 훈민정음 언해본 첫 자음 면(ㄱ·ㅋ) | [Commons](https://commons.wikimedia.org/wiki/File:Hunminjeongeum_Eonhae_04.jpg) | https://upload.wikimedia.org/wikipedia/commons/f/f2/Hunminjeongeum_Eonhae_04.jpg | 조선 정부 / 국립한글박물관 아카이브 | PD | 훈민정음 언해본(1568년 간행) · 퍼블릭 도메인 · 이미지: 국립한글박물관 | 3442x2480 | 10/09 예비와 중복 |
| 3 | 메인 | 언해본 아래아(ㆍ) 설명 면 | [Commons](https://commons.wikimedia.org/wiki/File:Hunminjeongeum_Eonhae_10.jpg) | https://upload.wikimedia.org/wikipedia/commons/5/58/Hunminjeongeum_Eonhae_10.jpg | 조선 정부 / 국립한글박물관 아카이브 | PD | 훈민정음 언해본 · 퍼블릭 도메인 · 이미지: 국립한글박물관 | 3425x2475 | 오른쪽 첫 줄이 "ㆍ눈 如呑ㄷ字中聲". 사람·로고 없음 |
| 5 | 메인 | 언해본 옛이응(ㆁ) 설명 면 | [Commons](https://commons.wikimedia.org/wiki/File:Hunminjeongeum_Eonhae_05.jpg) | https://upload.wikimedia.org/wikipedia/commons/a/a9/Hunminjeongeum_Eonhae_05.jpg | 조선 정부 / 국립한글박물관 아카이브 | PD | 훈민정음 언해본 · 퍼블릭 도메인 · 이미지: 국립한글박물관 | 3471x2480 | 오른쪽 첫 줄이 "ㆁ눈 牙音이니 如業字". 사람·로고 없음 |
| 3 | 예비 | 언해본 여린히읗(ㆆ) 설명 면 | [Commons](https://commons.wikimedia.org/wiki/File:Hunminjeongeum_Eonhae_08.jpg) | https://upload.wikimedia.org/wikipedia/commons/4/4b/Hunminjeongeum_Eonhae_08.jpg | 조선 정부 / 국립한글박물관 아카이브 | PD | 훈민정음 언해본 · 퍼블릭 도메인 · 이미지: 국립한글박물관 | 3425x2480 | 반시옷(ㅿ) 면은 Commons에서 찾지 못했다 |

## 9. 10/17 "편의점 협업 상품, 흐름 3 + 체크 5" (상표 없는 일반 사물만)

| 장 | 역할 | 내용 | 파일 페이지 | 원본 직접 URL | 작가/기관 | 라이선스 | 크레딧 | 해상도 | 위험 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 메인 | 책상 위 펼친 책과 끈 책갈피 | [Commons](https://commons.wikimedia.org/wiki/File:Open_book_1_(Unsplash).jpg) | https://upload.wikimedia.org/wikipedia/commons/d/d6/Open_book_1_%28Unsplash%29.jpg | Alina Daniker | CC0 1.0 (Unsplash 2017-06-05 이전 게시분) | 사진: Alina Daniker · CC0 | 4938x3292 | 글자 판독 불가, 로고 없음. 파일 페이지에 색수차 보정 권장 표시. 10/19 예비와 중복 |
| 2 | 예비 | 색 인덱스 탭 책 | (10/13의 3장과 같음) | https://upload.wikimedia.org/wikipedia/commons/9/9c/Book_%2835577498971%29.jpg | Dean Hochman | CC BY 2.0 | 사진: Dean Hochman · CC BY 2.0 · 크롭 | 4624x2763 | 10/13과 중복 |

- 3장(스포츠 카드)·6장(비교표)은 **사진 없음.** 상품·포장 사진이라 규칙상 제외했다.

## 10. 10/18 "품절된 키링, 원래는 나라의 도장"

| 장 | 역할 | 내용 | 파일 페이지 | 원본 직접 URL | 작가/기관 | 라이선스 | 크레딧 | 해상도 | 위험 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 메인 | 영빈 이씨 인장(거북 손잡이·붉은 술) | [Commons](https://commons.wikimedia.org/wiki/File:Royal_Seal_of_Lady_Yi,_Yeongbin_01.jpg) | https://upload.wikimedia.org/wikipedia/commons/1/19/Royal_Seal_of_Lady_Yi%2C_Yeongbin_01.jpg | 국립중앙박물관 | KOGL1 | 사진: 국립중앙박물관 · 공공누리 1유형 | 3000x2000 | **국새가 아니라 왕실 인장**이므로 카드에 유물 이름을 적는다. 키캡의 원형처럼 보이게 배치하지 않는다. 플랜 §2-10에 따라 손잡이 모양(거북)은 본문에서 언급하지 않는다 |
| 3 | 메인 | 색동저고리(20세기 중반, 호놀룰루미술관 소장) | [Commons](https://commons.wikimedia.org/wiki/File:Girl's_Blouse,_Korea,_mid-20th_century,_Honolulu_Museum_of_Art,_13783.1a.jpg) | https://upload.wikimedia.org/wikipedia/commons/5/50/Girl%27s_Blouse%2C_Korea%2C_mid-20th_century%2C_Honolulu_Museum_of_Art%2C_13783.1a.jpg | Hiart | CC0 1.0 | 사진: Hiart · CC0 | 3140x1152 | 진열장 테두리가 보인다. 굿즈 "색동공기"가 아니므로 "색동 예시"로만 쓴다. 가로가 길어 플레이트에 잘 맞는다 |
| 4 | 메인 | 국립중앙박물관 외관(거울못 너머) | [Commons](https://commons.wikimedia.org/wiki/File:National_Museum_of_Korea,_Seoul_(2)_(40236586235).jpg) | https://upload.wikimedia.org/wikipedia/commons/2/24/National_Museum_of_Korea%2C_Seoul_%282%29_%2840236586235%29.jpg | Richard Mortel | CC BY 2.0 (FlickreviewR 확인) | 사진: Richard Mortel · CC BY 2.0 · 크롭 | 6000x4000 | 건물만 보이고 사람 없음. 2005년 현대 건축물이라 저작권법 제35조 2항(공개장소 건축물) 이용 범위를 legal이 확인하는 것을 권장. 10/21과 중복 |
| 2 | 예비 | 명성황후 옥인(거북 손잡이) | [Commons](https://commons.wikimedia.org/wiki/File:Seal_of_the_Empress_Myeongseong_01.jpg) | https://upload.wikimedia.org/wikipedia/commons/3/3a/Seal_of_the_Empress_Myeongseong_01.jpg | 국립중앙박물관 | KOGL1 (Commons 표기) | 사진: 국립중앙박물관 · 공공누리 1유형 | 3000x2000 | **파일 메타데이터에 "All Rights Reserved" 문구가 있어 KOGL1 표기와 충돌한다.** e뮤지엄 원 페이지에서 공공누리 유형을 다시 확인하기 전까지는 예비로만 둔다. 국새 아님 |

## 11. 10/19 "필사 입문 체크리스트 5단계"

| 장 | 역할 | 내용 | 파일 페이지 | 원본 직접 URL | 작가/기관 | 라이선스 | 크레딧 | 해상도 | 위험 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 메인 | 노트에 펜으로 쓰는 손 | [Commons](https://commons.wikimedia.org/wiki/File:Pen-writing-notes-studying.jpg) | https://upload.wikimedia.org/wikipedia/commons/5/59/Pen-writing-notes-studying.jpg | Tookapic (Pexels) | CC0 1.0 (2025-02-08 리뷰 확인) | 사진: Tookapic · CC0 | 4752x3168 | 손만 보이고 얼굴은 없음. 필기 판독 불가, 펜에 로고 없음. visual 메모의 "손 없음"과 다르므로 designer가 판단 |
| 3 | 메인 | 조선 벼루·문진·벼루함·촛대(진열장) | [Commons](https://commons.wikimedia.org/wiki/File:Inkstone,_Paperweight,_Inkstone_case,_Candlestick.jpg) | https://upload.wikimedia.org/wikipedia/commons/1/1e/Inkstone%2C_Paperweight%2C_Inkstone_case%2C_Candlestick.jpg | Commons 사용자 "고려" | CC BY 4.0 | 사진: 위키미디어 사용자 고려 · CC BY 4.0 · 크롭·보정 | 9248x6936 | 유리 반사와 유물 설명판 글자가 보이므로 크롭. 소장 박물관은 파일 페이지에 없음(미검증) |
| 6 | 메인 | 서예 10폭 병풍 뒷면(19세기 후반, 초서) | [미술관](https://clevelandart.org/art/1998.286.b) | https://openaccess-cdn.clevelandart.org/1998.286.b/1998.286.b_print.jpg | 작자 미상 / 클리블랜드미술관 | CC0 1.0 (미술관 API 확인) | 서예 병풍 · 클리블랜드미술관 · CC0 | 3400x1262 | 정자·흘림을 대비하는 4단계 카드용. 사람·로고 없음 |
| 2 | 예비 | 펼친 책과 끈 책갈피 | (10/17의 2장과 같음) | https://upload.wikimedia.org/wikipedia/commons/d/d6/Open_book_1_%28Unsplash%29.jpg | Alina Daniker | CC0 1.0 | 사진: Alina Daniker · CC0 | 4938x3292 | 10/17과 중복 |

## 12. 10/20 "라면이 영화 소품이 된 이유" (EP001, 상표 없는 일반 음식만)

| 장 | 역할 | 내용 | 파일 페이지 | 원본 직접 URL | 작가/기관 | 라이선스 | 크레딧 | 해상도 | 위험 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 메인 | 양은냄비 라면과 김치 | [Commons](https://commons.wikimedia.org/wiki/File:Ramyeon_and_kimchi.jpg) | https://upload.wikimedia.org/wikipedia/commons/3/38/Ramyeon_and_kimchi.jpg | Hyeon-Jeong Suk | CC BY 2.0 (FlickreviewR 확인) | 사진: Hyeon-Jeong Suk · CC BY 2.0 · 크롭 | 1280x1920 | 상표 없음. 세로 사진이라 냄비 중심으로 1280x560 정도 가로 크롭 |
| 2 | 메인 | 흰 그릇의 미역국 라면 | [Commons](https://commons.wikimedia.org/wiki/File:Miyeok-guk-ramyeon.jpg) | https://upload.wikimedia.org/wikipedia/commons/0/05/Miyeok-guk-ramyeon.jpg | lazy fri13th | CC BY 2.0 (FlickreviewR 확인) | 사진: lazy fri13th · CC BY 2.0 · 크롭 | 4032x3024 | 로고·사람 없음 |
| 6 | 예비 | 냄비 속 매운 라면과 포크 | [Commons](https://commons.wikimedia.org/wiki/File:A_spicy_ramyeon.jpg) | https://upload.wikimedia.org/wikipedia/commons/e/e0/A_spicy_ramyeon.jpg | BrithnyBiong | CC BY 4.0 | 사진: BrithnyBiong · CC BY 4.0 · 크롭 | 1536x2048 | 2026-04-05에 올라온 신규 "자작" 파일이라 저작자 본인 여부는 미검증. 예비로만 둔다 |

## 13. 10/21 "10월 넷째 주 전시 체크리스트" (건물 외관만)

| 장 | 역할 | 내용 | 파일 페이지 | 원본 직접 URL | 작가/기관 | 라이선스 | 크레딧 | 해상도 | 위험 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 메인 | 국립중앙박물관 외관(거울못 너머) | (10/18의 4장과 같음) | https://upload.wikimedia.org/wikipedia/commons/2/24/National_Museum_of_Korea%2C_Seoul_%282%29_%2840236586235%29.jpg | Richard Mortel | CC BY 2.0 | 사진: Richard Mortel · CC BY 2.0 · 크롭 | 6000x4000 | 건물만, 사람 없음. 현대 건축물이라 legal 확인 권장. 10/18과 중복 |
| 4 | 메인 | 국립현대미술관 서울관 마당과 종친부 처마 | [Commons](https://commons.wikimedia.org/wiki/File:MMCA_Seoul_2016.jpg) | https://upload.wikimedia.org/wikipedia/commons/3/30/MMCA_Seoul_2016.jpg | jens kuu | CC BY 2.0 (Flickr 원본 페이지에서 직접 확인) | 사진: jens kuu · CC BY 2.0 · 크롭 | 4272x2856 | 원경 행인 2명(뒷모습)과 관람객 1명이 작게 보인다. 작품·로고·배너는 안 보인다. 2013년 현대 건축물이라 legal 확인 권장. Commons 첫 업로드 때는 BY-SA로 적혀 있었지만 Flickr 원본과 FlickreviewR 모두 CC BY 2.0 |
| 5 | 예비 | 광화문·월대와 경복궁 전경 | (세트 01의 6장 예비와 같음) | https://upload.wikimedia.org/wikipedia/commons/6/63/%EA%B4%91%ED%99%94%EB%AC%B8_%EC%9B%94%EB%8C%80.jpg | 서울관광아카이브 | KOGL1 | 사진: 서울관광아카이브 · 공공누리 1유형 | 6512x4341 | 크롭 필수(군중·버스). "광화문 일대"로만 쓰고 역사박물관 건물이라고 하지 않는다. 10/09와 중복 |

- 3장(과천관)과 5장(대한민국역사박물관 외관)은 **사진 없음.** 과천관은 허용 라이선스 사진을 찾지 못했다. 역사박물관은 BY-SA이거나 로고·배너가 있었다. 서울관 정면(서울연구원 CC BY 4.0)은 MMCA 로고 기둥과 전시 배너(작품 이미지)가 있어 제외했다.

## 14. 10/22 "해외 23만 명이 배우는 한국어, 퀴즈 3"

| 장 | 역할 | 내용 | 파일 페이지 | 원본 직접 URL | 작가/기관 | 라이선스 | 크레딧 | 해상도 | 위험 메모 |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 메인 | 해례본 예의 자음 면(ㅋ·ㆁ·ㄷ·ㅌ·ㄴ·ㅂ·ㅍ·ㅁ·ㅈ·ㅊ) | [Commons](https://commons.wikimedia.org/wiki/File:Hunminjeongeum_Haerye_03.jpg) | https://upload.wikimedia.org/wikipedia/commons/6/67/Hunminjeongeum_Haerye_03.jpg | 조선 정부 / 스캔: 규장각 | PD | 훈민정음 해례본(1446) · 퍼블릭 도메인 · 이미지: 규장각 | 1920x1280 | 아래쪽의 흐린 청구기호 숫자는 크롭 |
| 3 | 메인 | 해례본 표지("訓民正音") | (세트 01의 4장과 같음) | https://upload.wikimedia.org/wikipedia/commons/0/04/Hunminjeongeum_Haerye_01_%28front_cover%29.jpg | 조선 정부 / 규장각 | PD | 훈민정음 해례본 표지 · 퍼블릭 도메인 · 이미지: 규장각 | 1920x1280 | 라벨 크롭. 10/09와 중복 |
| 6 | 예비 | 19세기 점자 쓰기 틀(스웨덴) | (세트 01의 5장과 같음) | https://upload.wikimedia.org/wikipedia/commons/e/ea/Writing_frame_for_the_blind%2C_Stockholm%2C_Sweden_Wellcome_L0059116.jpg | Wellcome Collection | CC BY 4.0 | 사진: Wellcome Collection · CC BY 4.0 · 크롭 | 4256x2832 | 훈맹정음 유물이 아니다. 쓰면 "스웨덴 1871년"이라고 밝힌다 |

- 1장(세계지도)·2장(세종학당 타임라인)은 **사진 없음.** 세종학당 간판·기관 로고와 교재 표지 저작권 때문에 찾지 않았다.

---

## 15. 검토했지만 뺀 후보 (재검색 방지용)

| 후보 | 이유 |
|---|---|
| Gyeongbokgung(palace) Geunjeongjeon(hall).jpg (Brady Bellini, CC0) | 아래쪽 계단의 군중 얼굴. 궁능유적본부 공공누리 사진으로 대체 |
| Book Mark.jpg (CC0) | 책갈피에 "kteb FROSH" 로고 |
| Writing with a fountain pen (Unsplash, CC0) | 펜촉에 브랜드 각인 일부가 보임 |
| Desk-laptop-notebook-pen (CC0) | 노트북 키보드 로고, 형광펜 바코드, 휴대폰 |
| Braille numbers 111.jpg (CC0) | 객실 번호판이라 주제와 맞지 않음 |
| 20240413 National Museum of Korean Contemporary History.jpg (CC BY 4.0) | 정부 상징 로고, 기관 간판, 배너 |
| MMCA Seoul.jpg (서울연구원, CC BY 4.0) | MMCA 로고 기둥, 전시 배너(작품) |
| National Museum of Korea, Seoul (1) (CC BY 2.0) | 실내 홀(외관 아님), 석조 유물·안내판·관람객 |
| 오대산·하늘공원 억새·내장산 다수, 경복궁 근정전 다수, Korea.net 한글날 행사 사진 | CC BY-SA(불가 라이선스) |
| Crust and crumb.jpg (CC BY 4.0) | 남의 사진을 바탕으로 한 파생물이고 글자 주석 가능성 |
| 한글날 기념식 (1954).jpg (KOGL1) | 697px 저해상도, 인물 |
| 포토코리아(phoko.visitkorea.or.kr) | 검색 페이지 HTTP 403 (접근 불가) |
| e뮤지엄(emuseum.go.kr) | 검색 HTTP 500 (접근 불가). 국립중앙박물관 사진은 Commons의 KOGL1 사본으로 대체 |

## 16. 자가 검증 (성공 기준 대비)

고유 사진은 42장이고, JSON에는 세트별 중복 사용을 포함해 51행이 있다.

| 기준 | 결과 | 판정 |
|---|---|---|
| 불가 라이선스(BY-SA·NC·ND·공공누리 2~4·불명) | 0/42. 분포(중복 없이): PD 7 · CC0 12 · KOGL1 8 · CC BY 2.0 9 · CC BY 3.0 3 · CC BY 4.0 3 | 통과 |
| 2차 가공 허용(`modifiable: true`) | 42/42 | 통과 |
| 알아볼 수 있는 얼굴 | 원본에 얼굴이 들어 있는 것 1장(Najaengsan), 군중 원경 2장(광화문 월대, 창덕궁 전경). 셋 다 메모에 크롭 지시를 적었고, 지시대로 크롭하면 0 | 조건부 통과 (크롭 필수) |
| 상표·포장·간판 로고 | 0. MET 하단 저작권 문구는 크롭 필수 1건, 도서관 청구기호 라벨은 크롭 3건 | 조건부 통과 |
| 현대 미술 작품·스틸·포스터·군사·정치 | 0 | 통과 |
| 라이선스를 파일 페이지에서 직접 확인 | Commons 파일 페이지 41/42 (97.6%). 나머지 1장(클리블랜드 1998.286.b)은 미술관 공식 오픈액세스 API에서 CC0을 직접 확인. 42/42 모두 Commons API 메타데이터와 교차 확인했고, Flickr 원본 페이지도 1건(MMCA) 확인 | 통과 |
| 썸네일 육안 확인 | 42/42 (500~960px). 원본 해상도의 얼굴 재확인은 designer 몫 | 통과 |
| 직접 다운로드 URL | 42/42 ("수동 다운로드 필요" 0건) | 통과 |
| 해상도(가로 1000px 이상) | 42/42 (가장 작은 것: Ramyeon and kimchi 1280px 폭, 세로 사진) | 통과 |
| 수량 | 14/14 세트에 최소 1장. 세트 01은 8개(메인 6 + 예비 2). 10/17은 1장 + 예비 1장. "사진 없음(AI 배경만)" 세트는 0이고, 카드 단위로 사진이 없는 곳은 각 세트 표 아래에 적었다 | 통과 |

### 확인이 필요한 점
1. **명성황후 인장**은 메타데이터의 "All Rights Reserved"가 KOGL1과 충돌한다. e뮤지엄에서 다시 확인하기 전까지는 예비로만 둔다.
2. **현대 건축물 외관**(국립중앙박물관 2005, 국립현대미술관 서울관 2013)은 저작권법 제35조 2항의 상업적 카드뉴스 이용 범위를 legal이 확인해야 한다.
3. **규장각·국립한글박물관 스캔 이미지**는 원 제공처의 이용 조건 문구를 확인하지 못했다. Commons 표기는 PD-South Korea + PD-1923이다.
4. **점자 쓰기 틀(스웨덴)**은 훈맹정음 유물이 아니므로, 출처를 밝혀 쓸지 사진 없이 둘지 대표나 designer가 정해야 한다.
5. **A spicy ramyeon**(2026-04 신규 업로드)은 저작자 진위를 검증하지 못했다.
