# 유튜브 론칭 실행 계획 — 영상·썸네일·채널명·마케팅·채널 설정 (바로 시작용)

작성 2026-10-02 · 리서처 세션(research/youtube-launch) · 대표 지시(2026-10-02): "유튜브 계획안을 더 디테일하게 — 영상(실사·모션그래픽), 썸네일, 채널 이름, 마케팅 수단, 유튜브 설정까지 조사해서 바로 시작할 수 있게."
전제 문서: `docs/PLAN.md`(수익·게이트), `docs/GROWTH_STRATEGY.md`(90일 플레이북 [G#]), `docs/TOOLING_OPENSOURCE.md`(OSS-③ [O#]), `docs/TOOLING_TTS_IMAGE.md` §C·§D, `episodes/EP001/design/design-system.md`(v1.0), `cardnews/docs/DESIGN_SOURCES.md` §5(원화 31점).
현재 상태: EP001·EP002 대본·검수 승인, EP003 대본 완료. 업로드 0건(키 UNSET), 채널 미개설, 채널명은 가칭 "Korea Explained".

> **표기 규칙**
> - `[Y#]` = 맨 아래 출처 번호. **확인 날짜는 전부 2026-10-02.**
> - (스니펫) = 검색 요약만 확인. 미확인 = 근거를 찾지 못함.
> - 금액·소요시간·구독 수는 전부 **추정**이며, 실측값이 생기면 교체한다. 1 USD ≈ 1,400원.
> - **"대표 결정" 칸이 ●인 항목은 기본값을 적용하지 않았다.** §7 목록을 COO가 대표에게 그대로 묻는다.
> - 이 세션에서는 아무것도 설치·등록·업로드하지 않았다. 웹 조사와 `curl` 상태 코드 조회만 했다.

---

## 0. 결론 먼저 (8줄)
1. **채널명 "Korea Explained"는 선점·혼잡 상태다.** 핸들 @koreaexplained는 이미 있고(HTTP 200), 동명 채널이 8곳 이상이며, koreaexplained.com은 2025-12에 등록된 동명 블로그다 [Y60][Y61]. **추천은 "Korea, Annotated"(@KoreaAnnotated)**: 핸들 404, .com 미등록이고, "원전에 주석을 단다"는 뜻이 원화 아카이브 세계관과 맞는다 [Y60][Y61]. ● 대표 결정 N1.
2. **제작 방식은 "원화 아카이브 × 코드 모션그래픽"을 추천한다.** 구성은 퍼블릭 도메인 민화 원화(CC0·공공누리 1유형)의 크롭·패닝, Remotion 템플릿 12종(한지·한글 획·지도·연표·인용·엔드스크린 등), Gemini TTS다. AI 이미지는 원화가 없는 장면의 보조 플레이트로만 쓴다(카드뉴스 1안과 같은 세계관). ● N2~N4.
3. 실사는 **공공누리 1유형·CC0·Pexels만** 쓰고, 대표가 직접 찍는 얼굴 없는 B-roll로 보강한다(장비 약 23~35만원, 일회성, 선택). CC BY-SA·공공누리 2~4유형·e영상역사관은 쓰지 않는다 [Y34][Y41].
4. **썸네일 규칙 3줄**:
   ① 텍스트 3~4단어, 흰색 대문자 + 먹선 외곽선(교육 분야 중앙값 4단어) [Y64].
   ② 원화 디테일 1개를 화면 40%로 크게 잘라 "얼굴" 대신 초점으로 쓴다(교육 분야 얼굴 비율 57%라 얼굴 없이도 불리하지 않음) [Y64].
   ③ 한지 찢김 테두리와 붉은 낙관을 매 편 같은 자리에 둔다(시그니처). 3안을 만들어 Test & Compare(승자 = 시청시간)로 고른다 [Y11].
5. **마케팅 상위 3**:
   ① 숏폼 하루 1개 + "관련 영상" 연결 + TikTok·Reels에는 워터마크 없는 원본을 직접 올리고 **AI 라벨을 켠다**(두 플랫폼 모두 AI 음성 라벨 대상) [Y16][Y73][Y75].
   ② YouTube Collaborations로 같은 규모 한국 소재 채널과 공동 태그 [Y77].
   ③ 링크 없는 Q&A 참여(r/koreatravel 등) + Koreabridge 피드 등록 [Y68][Y72].
   r/korea·r/travel·r/solotravel은 자기 링크 금지(Restricted)이고, Waygook.org는 카지노 사이트로 바뀌어 금지다 [Y67][Y71].
6. **개설 당일 체크리스트는 42항목(§5)이다.** 핵심 3가지:
   - **전화 + 신분증 인증(Advanced 기능)**: 없으면 설명란 제휴 링크가 클릭되지 않고, 맞춤 썸네일·고정 댓글·A/B 테스트도 쓸 수 없다 [Y10].
   - **OAuth 동의 화면 "In production" 전환**: Testing이면 리프레시 토큰이 7일 만에 만료된다 [Y28].
   - **API 감사 신청**: 통과 전까지 API 업로드는 전부 비공개로 잠긴다 [Y26][Y27].
7. 첫 4주에는 **감사 통과 전이라 대표가 Studio에서 수동 업로드**하고, 세션은 업로드 패키지(MP4·SRT·썸네일 3·설명란)를 만든다. 월 비용은 약 0.5~1.5만원으로 상한 20만원의 7% 이하다(추정, §6).
8. **2027-02-01부터 YPP 신규 문턱이 시청 8,000시간 또는 숏폼 2,000만 뷰로 오른다** [Y19]. 1월 말 안에 4,000시간을 채우기는 어렵다(추정). 그래서 수익 순서는 제휴 → 팬 펀딩 → YPP다(GROWTH §9와 같음).

---

## 1. 채널 포지셔닝·이름

### 1-A. "Korea Explained" 점검
| 항목 | 결과 | 출처 |
|---|---|---|
| 핸들 @koreaexplained | **선점**(HTTP 200, 구독 1명, 추정) | [Y60] |
| 동명 YT 채널 | @koreaexplainedofficial 164 · @koreaexplained1 59 · @koreaexplaineden 19 · @KoreaExplainedGlobal 10 · @korea.explained26 10 · @KoreaExplained2025 9 등 8곳 이상(추정). 한국어 채널 "韓풀이 (Korea Explained)" @KorExplained 1.97K | [Y60] |
| koreaexplained.com | **선점**: 2025-12-27 등록, 블로그 "Korea, Explained"(Explainers·Culture·Politics, 뉴스레터) | [Y61] |
| 유사 브랜드 | KOREA EXPOSÉ("Internet's No.1 Explainer for All Things Korean", 스니펫), "DPRK Explained" | [Y60] |
| 상표(USPTO·KIPRIS·WIPO) | 자동 조회 실패(403·JS 화면) → **미확인**. 조회 방법은 §1-C | [Y62] |
| 검색성 | "korea explained"는 일반 구문이라 기사·숏폼·동명 채널과 경쟁한다. 브랜드 검색어로 쓰기 어렵다(판단) | [Y60] |

### 1-B. 대안 5안 (0 = 현행 유지)
| # | 이름 / 핸들 | 뜻·세계관 적합 | YT 핸들 | .com | 장점 | 단점 | 대표 결정 |
|---|---|---|---|---|---|---|---|
| 0 | Korea Explained / (핸들 변형 필요) | 직관적 | **선점** | 선점 | 뜻이 바로 통함 | 구별 불가, 상표화 어려움, 핸들을 @KoreaExplainedHQ 같은 변형으로 써야 함 | ● |
| **1 (추천)** | **Korea, Annotated** / @KoreaAnnotated | 원전(원화·사료)에 주석을 단다 → "원화 아카이브"·"책가도 노트"(서가·노트)와 같은 축 | 404 (@AnnotatedKorea도 404) | 미등록(RDAP 404) | 고유함. "explained"의 뜻 유지. 화면 문법(원화 위 주석 콜아웃)과 이름이 일치 | 쉼표가 핸들에서 빠짐, 약간 학술적 | ● |
| 2 | Chaekgado Notes / @ChaekgadoNotes | "책가도 노트" 영문판, 단일 브랜드 | 404 (@chaekgado는 선점) | 미등록 | 인스타와 1:1 브랜드 | 외국인이 철자·발음을 어려워해 검색 유입이 거의 없음 | ● |
| 3 | Hanji Archive / @HanjiArchive | 한지 + 아카이브 | 404 | 미확인 | 비주얼과 바로 연결 | 공예·종이 채널로 오해받을 수 있음 | ● |
| 4 | Korea in the Margins / @KoreaInTheMargins | 역사의 여백 + 고문서 난외 주석 | 404 | 미등록 | 서사형 콘셉트가 분명함 | 길고, "marginal"의 부정적 뉘앙스 | ● |
| 5 | The Minhwa Files / @TheMinhwaFiles | 민화로 푸는 사건 파일 | 404 | 미확인 | 미스터리·시리즈 느낌 | "minhwa" 인지도가 낮고 범위가 좁게 들림 | ● |

- 브랜드 관계(추천안): 채널명은 "Korea, Annotated", 채널 소개 끝에 "A Chaekgado Note studio channel"을 붙인다. 숏폼·카드뉴스 공통 시그니처는 붉은 낙관과 한지 테두리다. 검색 유입은 1번 이름이, 브랜드 연결은 2번 이름이 맡는다.
- 검색 보완: 이름과 상관없이 **채널 핸들 아래 첫 줄 소개에 "Korean history & culture, explained from the original art"** 를 넣어 "korea explained" 검색어를 소개문으로 흡수한다(판단).

### 1-C. 이름·핸들·상표 확인 방법 (실제 등록은 대표)
| 대상 | 방법 | 비고 |
|---|---|---|
| YT 핸들 | `curl -o /dev/null -w "%{http_code}" -L https://www.youtube.com/@핸들` → 404면 공개 채널 없음. 최종 확인은 Studio → 맞춤설정 → 핸들 입력란 | 404가 등록 가능을 보장하지는 않음(예약·숨김 가능) [Y60]. 핸들은 3~30자, `_ - . ·` 사용 가능(맨 앞·맨 뒤 제외), 14일에 2회까지 변경 [Y3][Y4] |
| 다른 SNS | namecheckr.com · namechk.com에서 IG·TikTok·X·Threads 동시 조회 | 이번엔 미실행(미확인) |
| 도메인 | `curl https://rdap.verisign.com/com/v1/domain/<이름>.com` → 404면 미등록 | 구매 시 연 약 2만원(추정) |
| 상표 | USPTO tmsearch: Wordmark "KOREA ANNOTATED"·"KOREA * ANNOTATED", 류 041·009·035, Live만. KIPRIS: 상표명 영문·한글 음역, 41·9·35류. WIPO Global Brand DB: Nice 41 | 등록 출원은 이번 범위 밖. 출원 여부는 대표 결정(N12) [Y62] |

### 1-D. 벤치마크 10개 채널 (구독은 YT 반올림 표시값, 추정, 2026-10-02)
| 채널 | 구독 / 영상 수 | 업로드 주기 | 길이 | 썸네일 패턴 | 수익 모델(about 링크 기준) |
|---|---|---|---|---|---|
| Kings and Generals | 4.2M / 2.2K | 주 3~4 | 18~23분 | 회화풍 전투·지도, 2~5단어 세리프 흰·금, **찢어진 종이 테두리**, 얼굴 없음, 우상단 로고 | 광고·Patreon·머치 |
| Simple History | 5.11M / 1.3K | 주 1~2 | 9~12분 | 플랫 카툰, 텍스트 0~3단어, 중앙 피사체 1 | Patreon·머치·저자 책(Amazon) |
| History Matters | 1.92M / 396 | 월 1~2 | 8~9.5분 | **질문형 5~8단어**, 막대 인형, 단색 배경 | Patreon |
| OverSimplified | 9.65M / 33 | 연 1 안팎 | 21~49분 | 시리즈명 1~3단어 + 워드마크, 카툰 얼굴 | Patreon·자체 머치 |
| Asianometry | 965K / 725 | 주 2~3 | 15~30분 | 사물 사진 + 녹색 띠 위 흰 대문자 3~6단어, 얼굴 없음 | Patreon |
| fern | 5.54M / 141 | 주 1 안팎 | 25~35분 | 어두운 시네마틱, 텍스트 0~2단어(빨강) | 매니지먼트 소속, 그 외 미확인 |
| The Frog Outside the Well (한국사) | 214K / 428 | 주 1 안팎 | 8~22분 | 교수 얼굴 + 큰 텍스트 3~8단어 + 고문서 배경 | Amazon 링크·GoFundMe |
| Loonytricky (조선사) | 39.3K / 238 | 2~3개월에 1 | 8~15분 | 회화풍(AI로 보임) 인물 우측 + 큰 흰 제목 1~3단어 | Buy Me a Coffee·머치 |
| Asian Boss (한국 사회) | 4.17M / 1.9K | 주 0.7 | 40~54분 | 진행자 얼굴 + 지도·국기 + 2~4단어 | 광고, 그 외 미확인 |
| 韓풀이 (Korea Explained, 동명) | 1.97K / 53 | 불규칙 | 2~21분 | 텍스트 과다, 스타일 혼재 | 미확인 |

- 출처: 각 채널 @페이지 [Y63]. 업로드 주기·길이는 최근 약 14편으로 계산했다. 스폰서 계약은 설명란을 보지 않아 전부 미확인이다.
- 시사점(판단):
  - 얼굴 없는 상위 채널 6/10이 **단일 비주얼 언어 + 고정 로고 위치 + 시리즈 통일감**을 갖고 있다.
  - Patreon·머치가 기본이다. 이는 PLAN의 멤버십(③) 경로와 같다.
  - 한국 특화 영어 채널 중 일러스트·원화 기반 상위 채널은 Loonytricky 정도로, 경쟁이 얕다.

---

## 2. 영상 제작 방식 — 원화 아카이브 × 코드 모션그래픽 하이브리드

### 2-A. 화면 소스 우선순위와 라이선스 (상업 유튜브 기준)
| 순위 | 소스 | 상업 | 변경 | 출처 표기 | 주의 | 출처 |
|---|---|---|---|---|---|---|
| 1 | **민화 원화**: Met·Cleveland CC0 (DESIGN_SOURCES §5-2의 18점) | O | O | 의무 없음, "Image: The Met, CC0" 감사 표기 권장 | 박물관이 보증하는 것처럼 보이는 배치 금지. **호랑이·산신 모티프 2점은 금지** | [Y83] |
| 1 | 민화 원화: e뮤지엄 **공공누리 1유형** (11점) | O | O | **필수**(아래 문구) | 같은 장르라도 소장처마다 유형이 다르므로 항목 단위로 확인 | [Y34][Y83] |
| 2 | 포토코리아(주소 **phoko.visitkorea.or.kr**로 변경) | **1유형 사진만** | 1유형만 | 필수: "ⓒ Korea Tourism Organization PhotoKorea-[촬영자]" | 1~4유형이 섞여 있음. 마크가 없으면 개별 허락 필요. 영상 제공 범위 미확인 | [Y35] |
| 2 | 국가유산포털·e뮤지엄 사진 | 자료별 표시 유형 | 유형별 | 필수 | 포털 전체 정책 문구 미확인 → 자료마다 확인 | [Y34] |
| 3 | Pexels | O | O | 불필요 | 식별 가능 인물의 부정적 묘사·보증처럼 보이는 사용 금지 | [Y36] |
| 3 | Pixabay | O | O | 불필요 | **상표·로고가 식별되는 소재는 상업 이용 금지**. 인물은 릴리스 확인 권고 | [Y37] |
| 3 | Unsplash | O | O | 권장 | 무수정 판매 금지 | [Y38] |
| 4 | NASA | O(미국 내 저작권 없음 원칙) | O | 권장 | 휘장·로고 금지, 보증 암시 금지 | [Y40] |
| 4 | NARA(미 국립기록관리청) | O(연방 저작물 PD) | O | 불필요 | 기증자 제한 소장품 확인 | [Y42] |
| 4 | Prelinger(archive.org) | PD 항목만 | O | 불필요 | 약 65%만 PD → 항목별 확인 | [Y44] |
| ✕ | Wikimedia **CC BY-SA** | — | — | — | 동일조건 조항이 영상 전체로 번질 위험 → 사용 안 함. PD·CC0 파일만 개별 사용 | [Y41] |
| ✕ | 공공누리 2·3·4유형 | — | — | — | 2·4는 상업 불가, 3·4는 변경 불가 | [Y34] |
| ✕ | e영상역사관(KTV·대한뉴스) | 불명 | 불명 | — | 이용조건 비공개 → 허락 전 사용 금지 | [Y44] |
| ✕ | Coverr | O | — | — | AI 학습 금지 조항 있음. 대체재가 있어 제외(판단) | [Y39] |
| ✕ | 미 의회도서관(LoC) | 자동 허용 아님 | — | — | 저작권 판단이 이용자 책임 → 개별 검토 없이는 제외 | [Y43] |

- 공공누리 1유형 표기 공식 문구(설명란 "Image credits" 블록에 영문 병기) [Y34]:
  `본 저작물은 '기관명'에서 'OO년' 작성하여 공공누리 제1유형으로 개방한 '저작물명(작성자:OOO)'을 이용하였으며, 해당 저작물은 '기관명, 홈페이지 주소'에서 무료로 다운받으실 수 있습니다.`
- YouTube **재사용 콘텐츠** 기준: 다른 출처 영상을 실질적 해설·변형 없이 쓰면 수익화 불가다. 아카이브 소재 위에 고유 내레이션·서사·주석을 얹으면 허용 범위로 본다 [Y33].

### 2-B. 민화·책가도 원화를 유튜브 장면에 쓰는 규칙 (DESIGN_SOURCES §5 → 영상판)
| # | 규칙 | 근거 |
|---|---|---|
| R1 | 쓸 수 있는 원화는 Met·Cleveland CC0와 e뮤지엄 1유형뿐이다. 장면 JSON에 `asset_id`(목록 번호 1~29)·소장처·라이선스를 기록한다 | [Y83] |
| R2 | 금지 모티프(호랑이·산신, 목록 30·31)와 저작권 캐릭터 연상 요소는 쓰지 않는다(design-system §6.3) | [Y83] |
| R3 | 허용 가공: 크롭·패닝(Ken Burns)·마스킹·색 보정(LUT 통일)·한지 그레인 합성·주석 콜아웃 오버레이. **원화 위에 AI로 덧그리기(인페인팅)는 하지 않는다** → 원화와 생성물의 경계를 지킨다 | 판단 |
| R4 | 원화를 AI 생성물로 표시하지 않고, AI 생성물을 원화처럼 보이게 하지도 않는다. 장면 캡션에 "Original: [작품명], [소장처]"를 3초 동안 표시한다 | 판단 |
| R5 | 설명란 "Image credits" 블록에 장면별 원화 목록을 쓴다(1유형은 공식 문구, CC0는 감사 표기) | [Y34] |
| R6 | 박물관 로고·이름을 썸네일에 쓰지 않는다(보증 암시 금지) | [Y83] |
| R7 | 원화 고해상도 원본은 저장소에 커밋하지 않는다(용량). `setup.sh`에서 받거나 대표 PC에 보관하고, 저장소에는 썸네일 크기와 출처 목록만 둔다 | CLAUDE.md |

### 2-C. 대표 직접 촬영(선택) — 얼굴 없는 B-roll
| 품목 | 용도 | 가격(추정) |
|---|---|---|
| 기존 스마트폰(4K30 이상) | 본 촬영 | 0 |
| 3축 짐벌(Osmo Mobile급) | 걸으면서 찍는 B-roll | 15~20만 |
| 가변 ND 클립 | 주간 셔터 확보 | 3~6만 |
| 미니 삼각대 | 타임랩스 | 2~4만 |
| 보조배터리·저장공간 | — | 3~5만 |
| **합계(무선마이크 제외)** | 일회성. 월 상한과 별도로 대표 승인 필요 | **약 23~35만** |

**촬영 리스트(첫 3편용, 사람 얼굴이 나오지 않는 구도)**
- EP002: 광화문 광장 바닥 한글 자모·한글날 현수막 원경, 붓·한지 손 클로즈업
- EP001: 양은냄비 끓는 물·김 클로즈업(무지 냄비), 한강 편의점 외관 원경(간판 식별 불가 구도)
- EP003: 배추 절이기 손, 김장 매트·대야(무지), 시장 배추 더미

**촬영 규칙**
| 항목 | 규칙 | 출처 |
|---|---|---|
| 궁궐·왕릉 | 수익 채널은 **"일반 상업용, 모델 없음" 동영상으로 무료 신청**(촬영일 60일~5일 전, 국가유산청 e-minwon). 모델이 있으면 4시간 60만원. 작품당 기관별 월 3일까지. **드론은 공익 목적 외 불허** | [Y45] |
| 드론 | 서울은 공항 반경 9.3km·광화문 반경 3.7km 이내와 고도 150m 이상 금지. 드론원스톱 신고 필수 → **도심 드론 촬영은 하지 않는다** | [Y46] |
| 지하철 | 상업 촬영은 서울영상위원회 경유 신청(스니펫), 개인 소규모 기준 미확인 → 찍지 않는다 | (스니펫) |
| 초상권 | 기준은 유명 여부가 아니라 **식별 가능성**이다. 지나가는 인물도 흐림 처리하고, 얼굴이 나오지 않는 구도를 우선한다 | (스니펫, 법률 원문 아님) |

### 2-D. 모션그래픽 도구 비교 → 추천 1
| 도구 | 라이선스 | 학습 곡선 | GPU PC 활용 | JSON 자동화 | 템플릿 재사용 | 판정 | 출처 |
|---|---|---|---|---|---|---|---|
| **Remotion** | 개인·직원 3명 이하 무료(상업 포함), 그 이상은 회사 라이선스 | 중(React) | 낮음(Chromium 렌더, **클라우드 CPU VM에서 헤드리스 렌더**) | **강함**: props·JSON → 렌더 | 강함 | **추천** | [Y53] |
| HyperFrames | Apache-2.0 | 낮음~중(HTML/CSS) | 낮음 | 강함(data 속성) | 강함 | 대안(2026 신생, 안정성 미확인) | [Y55] |
| Motion Canvas | MIT | 중 | 낮음 | 가능 | 중 | 헤드리스 렌더 미확인 → 자동화에 부적합 | [Y56] |
| Blender Grease Pencil | Blender는 GPL, **결과물은 사용자 소유** | 높음 | **높음**(CUDA·OptiX) | Python + `-b` 백그라운드 렌더 | 중 | 붓 터치 손애니메이션이 필요할 때만 대표 PC에서 쓰는 보조 도구 | [Y57] |
| DaVinci Resolve 무료 | 무료(UHD 60p까지) | 중 | 단일 GPU. H.264/265 하드웨어 인코딩은 Studio 기능으로 명시 | 무료판 외부 스크립팅 제한(추정) | Fusion 템플릿 | 대표 PC의 **최종 확인·수동 미세 편집용** | [Y58] |
| Natron | GPLv2 | 높음 | CPU 위주 | Python | 중 | 유지보수 위험 → 제외 | [Y59] |

- **추천: Remotion.** 이유 4가지:
  - 클라우드 세션 VM에서 사람 손 없이 장면 JSON → 렌더가 된다.
  - 같은 HTML/React 자산을 카드뉴스 릴스와 공유한다(DESIGN_SOURCES §3).
  - 1인 회사 무료다.
  - 한글 획 리빌은 `@remotion/paths`의 `evolvePath()`(strokeDasharray·offset 반환)로 공식 지원된다 [Y54]. 한글 폰트는 `@remotion/fonts` `loadFont`로 로컬 OFL 폰트를 넣는다(CJK 명시 문서는 미확인, Chromium 렌더라 동작 추정) [Y54].
- ● 대표 결정 N3(Remotion vs HyperFrames).

### 2-E. 첫 3편 Remotion 템플릿 목록 (재사용 단위)
| ID | 템플릿 | 내용 | EP001 | EP002 | EP003 | 제작(추정) |
|---|---|---|---|---|---|---|
| T01 | HanjiBG | 한지 섬유 질감 루프 + 그레인(multiply 8~12%) + 비네트. 모든 장면의 바닥 | ✓ | ✓ | ✓ | 0.5일 |
| T02 | ArchivePan | 원화 크롭 Ken Burns + "Original: 작품·소장처" 캡션 3초 | ✓ | ✓ | ✓ | 0.5일 |
| T03 | Annotate | 원화 위 **주석 콜아웃**(가는 먹선 + 라벨 카드). 채널명 "Annotated"의 시그니처 문법 | ✓ | ✓ | ✓ | 0.5일 |
| T04 | HangulStroke | 자모 중심선 JSON → `evolvePath` 획 리빌 + 붓 질감 마스크. 현행 24자는 흰색, 폐지 4자는 회색 | — | ✓ | △(김장 한글 라벨) | 1~2일(자모 30개 경로 제작 포함, [O58] 대신 자체 제작) |
| T05 | MapKR | Natural Earth(PD) 한반도·세계 지도, 점·선 애니메이션 | △(수출) | △(안동) | ✓(강원·기온선) | 0.5일 |
| T06 | Timeline | 가로 연표, 연도 카운터, 사건 핀 | ✓(2001→2026) | ✓(1443→2026) | ✓(13세기→1995) | 0.5일 |
| T07 | QuoteCard | 사료·대사 인용 카드(마루부리·Noto Serif KR, 영어 번역 병기) + 출처 줄 | ✓ | ✓(최만리 상소) | ✓(이규보) | 0.3일 |
| T08 | StatCard | 숫자 강조(4℃·0℃, 28→24, 40주년) | ✓ | ✓ | ✓ | 0.3일 |
| T09 | ChapterCard | 챕터 제목 2초 + 낙관 | ✓ | ✓ | ✓ | 0.2일 |
| T10 | AffiliateBar | 제휴 고지 바(상품 구간 내내 고정) + 무지 상품 카드 | ✓ | ✓ | ✓ | 0.3일 |
| T11 | EndScreen | 20초: 영상 2칸 + 구독 원 자리(엔드스크린 요소 4개 이하, 마지막 5~20초) + AI 고지 소형 표기 | ✓ | ✓ | ✓ | 0.3일 |
| T12 | ShortFrame | 9:16 안전영역(design-system §4) + 훅 4단어 + 자막 | ✓ | ✓ | ✓ | 0.5일 |

- 합계는 약 5~7일(에이전트 작업, 추정)이다. 이후 편당 신규 템플릿은 0~1개다. 엔드스크린 요소 규칙은 [Y13].

### 2-F. 음성·음악·효과음
| 구분 | 소스 | 조건 | Content ID 위험 | 쓰임 | 출처 |
|---|---|---|---|---|---|
| 음성 1순위 | Gemini Flash TTS **유료 티어** | 결과물 소유권을 주장하지 않음. 유료 티어 입력은 제품 개선에 쓰지 않음. 3.8 Flash TTS 출력 $9/1M 토큰(**2027-01-01부터 $18**) | — | 내레이션. 편당 약 100~300원(추정) | [Y52] |
| 음성 백업 | Kokoro-82M | Apache-2.0, 로컬 실행. **대표 GPU PC에서 실시간보다 빠름(추정)** | — | 키 장애 시·블라인드 A/B | [Y51] |
| 음악 1순위 | YouTube 오디오 보관함 | CC 트랙은 설명란 표기 필수. **타 플랫폼 사용 조건은 공식 문구 미확인 → 롱폼 전용** | 낮음 | 롱폼 BGM | [Y47] |
| 음악(숏폼 교차 게시) | incompetech(CC BY 4.0) / FMA **CC0·CC BY만** | 표기: `"Track" Kevin MacLeod (incompetech.com) Licensed under CC BY 4.0`. **NC 트랙 금지** | 낮음~중(이의제기로 해제) | TikTok·Reels 겸용 | [Y48][Y50] |
| 음악(보류) | Pixabay Music | 일부 작곡가가 Content ID에 등록 | **중** | 쓰지 않음 | [Y37] |
| 효과음 | Freesound **CC0·CC BY만** | NC·Sampling+ 제외 | 낮음 | 붓 소리·종이 넘김 | [Y49] |
| ✕ | AI 생성 음악 | YouTube 공개 대상 목록에 들어 있음 | — | 쓰지 않음(라벨 부담) | [Y32] |

### 2-G. AI 생성물 공개 — YouTube "변형·합성 콘텐츠" 설정
| 질문 | 답 | 출처 |
|---|---|---|
| 무엇을 반드시 공개하나 | 실존 인물이 하지 않은 언행처럼 보이는 것, 실제 사건·장소 영상의 변경, 일어나지 않은 장면의 **사실적** 생성, AI 생성 음악, 타인 목소리 복제 | [Y32] |
| 공개 불필요 | 비현실적·애니메이션 콘텐츠, 색보정·필터, 대본·썸네일·인포그래픽 제작 보조, 자막, 업스케일, 본인 목소리 복제 보이스오버 | [Y32] |
| 일반 TTS 내레이션 | **공식 문서에 명시 없음**(2차 출처는 "불필요"로 해석) | 미확인 |
| 표시 위치·제재 | 사실적 콘텐츠는 플레이어 위, 그 밖에는 펼친 설명란에 표시된다. 계속 누락하면 YouTube가 라벨을 붙이거나 삭제·YPP 정지를 할 수 있다. 공개 자체로 수익화가 제한되지는 않는다 | [Y32] |
| **우리 적용(판단)** | 원화 + 코드 모션 + TTS만 쓴 편은 법적 의무가 없지만, CLAUDE.md "AI 생성물 공개 라벨"을 지키기 위해 ① 영상 내 낭독·자막 고지(대본에 이미 있음) ② 설명란 둘째 줄 고지는 그대로 한다. YouTube 체크박스는 **사실적 AI 플레이트·AI 영상 훅을 한 장이라도 쓴 편에서 켠다** | ● N5 |
| 비진정성 정책 | 2025-07-15 개명. "일반적·독창성 없는 템플릿 AI 콘텐츠", 서사 없는 이미지 슬라이드쇼는 금지. 회차마다 서사가 다른 시리즈는 허용. 2026-07 개정 3유형은 2차 출처만 확인 | [Y33] |

### 2-H. 편집 파이프라인 (대본 → 업로드)
| 단계 | 담당 | 도구 | 실행 위치 | 시간(추정) | 비용(추정) |
|---|---|---|---|---|---|
| 1 대본 EN/KR | writer | 기존 | 클라우드 | 에이전트 | 0 |
| 2 장면 JSON(장면 유형·asset_id·템플릿 ID·자막) | producer + designer | `ffmpeg-assemble` JSON 확장(`template`, `asset_id` 필드 = 스킬 수정 제안, 대표 승인 후) | 클라우드 | 에이전트 30분 | 0 |
| 3 원화 선택·크롭 지정 | designer → **사람 검수 20분** | DESIGN_SOURCES 목록 | 클라우드 | 20분(사람) | 0 |
| 4 보조 플레이트(원화 없는 장면만) | producer | Z-Image Turbo(fal) **또는 대표 PC 로컬 생성** | 클라우드 / 대표 PC | 편당 0~6장 | 0~50원 |
| 5 내레이션 | producer | Gemini TTS(Kokoro 백업), 발음 사전 | 클라우드 | 10분 | 100~300원 |
| 6 모션 렌더 | producer | Remotion, 장면 단위 알파 클립 | 클라우드 CPU VM | 10분 영상 기준 20~60분(1080p, 실시간 0.3~1배, 추정) | 0 |
| 7 합성·loudnorm·자막 번인 | producer | ffmpeg-assemble | 클라우드 | 10분 | 0 |
| 8 자막 .srt(EN, 선택 KR) | producer | TTS 장면 길이 기반 타이밍(필요 시 whisper.cpp 정렬) | 클라우드 | 5분 | 0 |
| 9 숏폼 5개 | producer | shorts-cut + T12 | 클라우드 | 30분 | 0 |
| 10 썸네일 3안 | designer | HTML/CSS → Playwright Chromium(§3) | 클라우드 | 5분 + 모바일 검수 | 0 |
| 11 검수 PR | COO | 검수 시트 ①~⑧ | GitHub | 대표 10~20분 | 0 |
| 12 업로드 | publisher / **감사 전에는 대표** | 감사 전: MP4를 R2 비공개 링크로 넘기고 대표가 Studio 업로드. 감사 후: API `videos.insert`(private) → 승인 후 공개 | 클라우드 / 대표 | 대표 20분(감사 전) | R2 무료 범위(추정) |
| 13 Studio 전용 작업 | **대표** | 엔드스크린·A/B 테스트·Collaborations·고정 댓글(API로 못 하는 항목은 Studio에서) | 대표 PC·폰 | 15분 | 0 |

- **역할 분담**:
  - 클라우드 VM: 1~12단계 자동화. 렌더는 VM에서 바로 업로드·R2로 넘기고, 영상은 커밋하지 않는다.
  - 대표 GPU PC(선택):
    - ⓐ 보조 플레이트·자체 LoRA를 로컬로 생성 → fal 비용 0, 결과 PNG만 커밋
    - ⓑ Blender GP 붓 애니메이션
    - ⓒ Resolve 최종 확인
    - ⓓ OAuth 토큰 1회 발급(`scripts/youtube_auth.py`)
    - ⓔ Studio 전용 작업
- **편당 합계(추정)**: 에이전트 약 3~4시간, 대표 약 1.5시간(검수 PR + 업로드 + Studio). 금액은 약 100~400원이다. 주 5.5시간 예산(GROWTH §8) 안에 든다.

---

## 3. 썸네일

### 3-A. 상위 채널 패턴 (데이터)
| 근거 | 수치 | 출처 |
|---|---|---|
| Thumbnail Bench 2026(10만+ 구독 채널 1,043개, 11,223장) | 얼굴 71%(**교육 57%**). 텍스트 있음 77%, **중앙값 4단어**(1~2단어 22%, 3~4단어 32%, 7+ 27%). 흰 글씨 68%, 대문자 62%, 외곽선·그림자 73%, 따뜻한 강조색 56%. 텍스트 없는 썸네일은 소형 19% vs 2M+ 채널 32% | [Y64](원문 미열람, 보도 기준) |
| vidIQ 2026-07(돌파 영상 500개) | 얼굴 69%, 텍스트 중앙값 5단어 | [Y65](스니펫) |
| 1of10(2025, 30만 편) | 얼굴 효과는 분야별 차이가 크고, 전체로는 비슷함 | [Y66] |
| 벤치마크 10개 직접 관찰 | 0~5단어, 얼굴 없는 채널 6/10, 피사체 1개 + 고정 로고 위치 + 시리즈 통일감 | [Y63] |

### 3-B. 우리 디자인 시스템으로 만드는 템플릿 3종 (design-system v1.0 + 원화 아카이브 → v1.1 제안, 대표 승인 필요)
| 템플릿 | 구도 | 텍스트 | 색 | 쓰는 편(예) |
|---|---|---|---|---|
| **TH-A 원화 디테일** | 원화 1점을 크게 크롭(화면 40~50%, 오른쪽). 왼쪽 45%에 텍스트 | 3~4단어 질문·사실("WHY 1504?") | 한지 paper 배경 + ink 텍스트 + ke-red 낙관 | 역사 서사형(EP002) |
| **TH-B 거대 글자·숫자** | 한글 자모 또는 숫자 1개가 화면 60% ("ㆍ", "28→24", "4℃") | 2~3단어 보조 | night 배경 + ke-yellow 숫자 | 한글·데이터 각도(EP002 썸2·EP003) |
| **TH-C 사물 + 지도·연표 조각** | 단일 사물(무지 냄비·배추) 30~50% + 원화 조각 배경 | 3~4단어 | paper 또는 night 1색 + 강조 1색 | 구매 의도형(EP001) |

**공통 규칙**
- 시그니처: 한지 찢김 테두리(좌측 또는 하단) + 붉은 낙관(좌상단 고정, 채널 이니셜). 기존 노란 시그니처 바는 v1.1에서 낙관으로 대체할지 ● N6에서 정한다.
- 서체: EN은 Anton(대문자, 흰색/ink + ink 6px 외곽선). 한글이 들어가면 함렛 Black(카드뉴스 세트 B)을 써서 세계관을 맞춘다.
- 금지: 그림자·3D 글자, 빨간 화살표, "SECRET/BANNED" 낚시 문구, 실존 인물, 로고(design-system §6).
- 사양: 1920×1080 JPG(sRGB) **2MB 이하**로 낸다. 모바일 업로드 상한이 2MB이고, 공식 권장은 3840×2160, 최소 폭 640px이다 [Y6]. 저장소 커밋은 500KB 이하 축소본만 한다. **우하단 재생시간 배지 자리(240×100)는 비운다.**

### 3-C. Test & Compare 사용법
| 항목 | 내용 | 출처 |
|---|---|---|
| 조건 | 데스크톱 Studio, **Advanced 기능 필요**. 숏폼·프리미어·아동용·연령 제한·비공개 영상은 불가 | [Y11] |
| 변형 | 제목·썸네일 최대 3안(조합 가능) | [Y11] |
| 승자 | **시청시간 점유율** 기준(CTR 아님). 결과는 Winner / Performed same / Inconclusive | [Y11] |
| 기간 | 보통 2주 이내 | [Y11] |
| 절차 | Studio → 콘텐츠 → 영상 → 썸네일 아래 "A/B Testing" → 3안 업로드 → 결과는 Analytics. **테스트 중 제목·썸네일을 바꾸면 자동 중단** | [Y11] |
| 우리 운영 | 매 편 제목 1안 고정 + TH 3안 비교(검수 시트 ④의 3안 그대로). 결과를 `episodes/EPxxx/publish.log`에 기록하고, 3편 누적 후 템플릿 우선순위를 정한다 | 판단 |

### 3-D. 모바일 가독성 체크리스트 (designer 자동 + 사람 육안)
1. 320×180(피드)·168×94(사이드바) 축소본에서 텍스트를 판독할 수 있다.
2. 텍스트 대비 4.5:1 이상(design-system §1 금지 조합 0).
3. 텍스트·초점 오브젝트가 사방 64px 안전영역 안에 있다.
4. 우하단 배지 자리가 비어 있다.
5. 낙관·한지 테두리가 정해진 위치에 있다.
6. 초점은 1개(피사체 2개 이상 금지).
7. 제목을 그대로 반복하지 않고 보완한다.
8. 실존 인물·로고·글자 생성 이미지 0.
9. 원화 출처가 설명란 credits에 있다.
10. 다크모드 배경(검정)에서 테두리가 묻히지 않는다.

- 제작 도구: **HTML/CSS → Playwright Chromium**(VM 실측 1.1초/장, 한글 셰이핑·keep-all 정상, DESIGN_SOURCES §3). 기존 `make_thumbs.py`(Pillow)는 목업용으로 남긴다.

---

## 4. 마케팅 수단 (론칭 전후 90일)

### 4-A. 수단별 판정 (효과 근거 / 비용 / 주당 시간, 모두 추정)
| 수단 | 규칙 요지 | 효과 근거 | 비용 | 주당 | 판정 | 출처 |
|---|---|---|---|---|---|---|
| **YT 숏폼 1일 1개 + 관련 영상 링크** | Studio → 숏폼 → Related video | 공식 기능, 전환 데이터 없음 | 0 | 포함 | **상위 1** | [Y16][G18] |
| **TikTok·Reels·FB Reels 원본 직접 업로드** | 타 앱 워터마크 = 추천 제외. **AI 음성 사용 시 TikTok AIGC 라벨·Meta AI 라벨 필수**(일러스트만이면 Meta 불필요, 우리는 AI 음성이라 필요) | 공식 규칙, 효과 데이터 없음 | 0 | 2~3h | **상위 1** | [Y73][Y74][Y75] |
| **YouTube Collaborations** | 롱폼·숏폼에 공동 크리에이터 태그. 인원은 공식 문서 기준 최대 10명(출시 보도·스니펫은 5명 → 업로드 화면에서 확인). 수익은 게시 채널 몫 | 공식 기능 + 2018 논문(7,942채널, 협업 영상 인기 증가) | 0 | 2h | **상위 2** | [Y77][Y80] |
| 콜라보 섭외 명단 | 문체부 K-인플루언서(2025년 YouTuber 1,303명 위촉)·Korea.net 명예기자 중 구독 1천~3만 영어 채널 | 의견 | 0 | 0.5h | 상위 2 보조 | [Y81] |
| **Reddit 링크 없는 Q&A** | r/koreatravel(22.9만, 규칙 미확인)·r/seoul(9.4만, video 플레어 규칙 확인 필요)에서 답변만 | 의견 | 0 | 1h | **상위 3** | [Y68] |
| Koreabridge 피드 등록 | 한국 관련이면 누구나 publisher 등록, YT 피드 게시 허용 | 없음 | 0 | 0.2h | 상위 3 보조 | [Y72] |
| YouTube Posts(커뮤니티) | 구독 하한 없음, Advanced 필요, 투표·퀴즈 | 공식 기능 | 0 | 0.5h | 채택 | [Y10] |
| IG 자매 계정(책가도 노트) | Collab 게시물(최대 5명, 공식 미확인), 프로필 링크 5개, Trial Reels | 공식 기능. **한국어 독자라 영어 채널과 겹침이 적음(추정)** | 0 | 0.5h | 월 1회 교차 소개만 | [Y73] |
| X·Threads | X 링크 감점: GROWTH [G39]는 "있음"이었으나 2026-07-29 머스크가 "1년 넘게 안 함"이라고 답함 → **상충, 미확인**. 안전하게 링크는 답글에 둔다 | 의견 | 0 | 0.5h | 선택 | [Y76] |
| FB 그룹·Discord(Expats in Korea 10만+, KoreaTravel Discord 4.3천) | 규칙 미확인 → 가입 후 About 확인 | 없음 | 0 | 1h | 보류 | [Y69] |
| 뉴스레터(beehiiv 무료 2,500명) | 반증 사례: 오픈 18,326 → 구독 +26 | 의견(약함) | 0 | 1~2h | **90일 후 재검토** | [Y79][G47] |

### 4-B. 하지 말 것
| 행위 | 이유 | 출처 |
|---|---|---|
| r/videos·r/history 링크, r/Korean(AI 금지), **r/korea·r/travel·r/solotravel 자기 링크**(Restricted) | 차단·채널 연쇄 차단 | [G36][Y67] |
| TripAdvisor 포럼 자기 홍보 | 금지 | [Y70](스니펫) |
| **Waygook.org** 링크 | 도메인이 카지노 리뷰 사이트로 바뀜 → 평판 위험 | [Y71] |
| Lonely Planet Thorn Tree | 2021 폐쇄 | (스니펫) |
| sub4sub·조회 구매·참여 품앗이(pod) | 가짜 참여 정책 → 삭제·해지 | [Y82] |
| 대형 채널 댓글에 "check out my channel" 반복, 낚시 메타데이터 | 스팸 정책 | [Y22] |
| 워터마크 남은 숏폼 재업로드, AI 라벨 누락(TikTok·Meta) | 추천 제외·제재 | [Y73][Y75] |
| Quora 제휴 링크 | 금지 | [G45] |

- 주간 시간 합계(채택 수단만): 약 4.7~6.2시간 → GROWTH §8의 "외부 유입 1h + 콜라보 0.5h + 커뮤니티 1h"를 넘는다. **TikTok·Reels 교차 게시는 퍼블리셔 자동화(수동 패키지)로 사람 시간을 0.5h로 줄여야** 예산(주 5.5h) 안에 든다(추정). ● N9.

---

## 5. 유튜브 채널 설정 체크리스트 — 개설 당일 그대로 (42항목)

**[대표]** = 대표가 직접. **[세션]** = 자식 세션이 준비물을 만든다. 순서대로 진행한다.

### 5-A. 계정·채널 (1~8)
| # | 할 일 | 담당 | 세부 | 출처 |
|---|---|---|---|---|
| 1 | 전용 Google 계정 준비(2단계 인증 켜기) | 대표 | YPP 요건에 2단계 인증이 포함됨 | [Y18] |
| 2 | 채널 만들기 → **브랜드 계정** | 대표 | YouTube → 채널 목록 → Create a new channel → 이름·핸들·사진 | [Y1] |
| 3 | 채널명·핸들 입력(N1 결정값) | 대표 | 이름·핸들 각각 14일에 2회까지만 변경 가능 → 결정 후 입력 | [Y4] |
| 4 | **전화번호 인증**(Intermediate) | 대표 | 15분 넘는 영상, 맞춤 썸네일 | [Y10] |
| 5 | **신분증 또는 영상 인증**(Advanced) | 대표 | 설명란·게시물 **클릭 가능한 링크**, 고정 댓글, 챕터, A/B 테스트, 수익화 신청. 활성화까지 최대 48시간 | [Y10] |
| 6 | 권한: 채널 권한(Channel permissions)으로 관리자 추가(필요 시) | 대표 | 역할 Owner·Manager·Editor 등. **채널 권한은 API를 지원하지 않음 → API OAuth는 Owner 계정으로** | [Y2] |
| 7 | 시청자층: Settings → Channel → Advanced → Audience = **"아니요, 아동용이 아님"** | 대표 | 아동용이면 엔드스크린·카드·A/B 테스트가 꺼짐 | [Y9] |
| 8 | 채널 국가 = 대한민국, 키워드(10개 내외) | 대표 | 키워드 목록은 세션이 준비 | 판단 |

### 5-B. 브랜딩 (9~16)
| # | 할 일 | 담당 | 규격 | 출처 |
|---|---|---|---|---|
| 9 | 프로필 사진 | 세션 제작 → 대표 업로드 | JPG/PNG, 98×98로 표시(800×800으로 제작, 권장 크기는 미확인), 파일 상한 15MB 표기. 붉은 낙관 + 한지 | [Y5] |
| 10 | 배너 | 세션 → 대표 | 최소 2048×1152, 권장 2560×1440, **안전영역 1235×338**, 6MB 이하, 테두리·그림자 금지 | [Y5] |
| 11 | 워터마크(구독 버튼) | 세션 → 대표 | 최소 150×150 정사각, 1MB 미만, "마지막 15초" | [Y5] |
| 12 | 채널 소개문(EN) | 세션 | 첫 줄에 검색어("Korean history & culture, explained from the original art"), 주기("one deep-dive a week"), AI 음성·원화 출처 정책 1줄, 제휴 고지 1줄. 길이 한도는 미확인 | 판단 |
| 13 | 링크 섹션 | 대표 | 최대 14개. 링크 허브 1 + 인스타 + TikTok | [Y4] |
| 14 | 문의 이메일(비즈니스) | 대표 | 협찬 문의용. 공식 Help 미확인 | 미확인 |
| 15 | 채널 홈 레이아웃: 추천 섹션 = 시리즈 재생목록 2개 | 대표 | EP 3편 이후 | 판단 |
| 16 | 채널 트레일러 | 보류 | 첫 3편 후 60초 하이라이트(비구독자 노출, 비공식 출처) | 미확인 |

### 5-C. 업로드 기본값 — Studio → Settings → Upload defaults (17~28)
| # | 항목 | 값(추천) | 비고 / 출처 |
|---|---|---|---|
| 17 | 공개 범위 | **비공개(Private)** | 승인(approved) 전 공개 금지 규칙과 일치 [Y8] |
| 18 | 제목 템플릿 | 비움 | 매 편 marketer 제목 |
| 19 | 설명 템플릿 | 1행 제휴 고지(**"commission"**) → 2행 AI 고지 → 링크 → 본문 → Chapters → Sources → Image credits | §5-E [Y7] |
| 20 | 태그 | 채널 공통 5개 | — |
| 21 | 카테고리 | ● N7: **Education**(추천) vs Travel & Events | 공식 권장 문구 없음(미확인) |
| 22 | 라이선스 | 표준 YouTube 라이선스 | CC BY로 하면 원화 credits 체계와 혼동(판단) |
| 23 | 언어 | 제목·설명 언어 = 영어, 영상 언어 = 영어 | — |
| 24 | 자막 인증 | "해당 없음/미국 TV 미방영" | [Y7] |
| 25 | 댓글 | 켜기, "부적절할 수 있는 댓글 검토 보류" | — |
| 26 | 고급: 퍼가기 허용 O, 구독 피드 게시 O, 숏폼 리믹스 O, 자동 챕터 **끔**(직접 챕터 입력) | — | [Y15] |
| 27 | 변경·합성 콘텐츠 | 영상마다 지정(N5) | [Y32] |
| 28 | **주의** | 업로드 기본값은 **브라우저 업로드에만 적용**된다. API 업로드에 적용되는지는 미확인 → publisher는 모든 필드를 API 요청에 직접 넣는다(`status.selfDeclaredMadeForKids=false`, `snippet.categoryId`, `defaultLanguage`, `status.license`, `status.containsSyntheticMedia`. 필드명은 실행 전 문서로 재확인) | [Y8][Y26] |

### 5-D. 재생목록·시리즈·영상 요소 (29~34)
| # | 할 일 | 세부 | 출처 |
|---|---|---|---|
| 29 | 재생목록 3개 만들기 | ① "Korea's Calendar"(EP003~) ② "Hangul & Words"(EP002~) ③ "Korea on Screen"(EP001~, 드라마·영화 속 한국) | 판단, GROWTH §9 시리즈 2개 + 1 |
| 30 | 시리즈 지정 | 재생목록 설정 → "Set as official series"(인증 계정, 영상당 시리즈 1개) | [Y12](스니펫) |
| 31 | 엔드스크린 | 영상 25초 이상, 마지막 5~20초, 요소 4개 이하 → T11에 맞춤. **API로 설정 불가 → 대표가 Studio에서** | [Y13] |
| 32 | 카드 | 영상당 최대 5개. 외부 링크 카드는 YPP 회원만 → 지금은 영상·재생목록 카드만 | [Y14] |
| 33 | 챕터 | 00:00 시작, 3개 이상, 각 10초 이상(설명란 Chapters) | [Y15] |
| 34 | 고정 댓글 | 출처 노트·다음 편 예고. Advanced 필요, 영상당 1개 | 스니펫 |

### 5-E. 정책·저작권·고지 (35~38)
| # | 할 일 | 세부 | 출처 |
|---|---|---|---|
| 35 | 업로드 중 "Checks"(저작권·광고 적합성) 완료 확인 후 게시 | 대부분 1시간 안에 판정. 자가 인증은 YPP 회원 대상 | [Y17] |
| 36 | 제휴 고지 | 설명란 **첫 줄**: "Disclosure: Some links below are affiliate links. I may earn a commission at no extra cost to you." + Amazon 필수 문구. **영상 안 구두 고지 유지**(FTC: 설명란만으로는 부족) | [Y23] |
| 37 | "유료 프로모션 포함" 체크 | 대상은 스폰서십·보증. **순수 제휴 링크가 대상인지는 공식 미확인** → 협찬 편은 반드시 체크, 제휴만 있는 편은 legal-reviewer 판단(● N8) | [Y21] |
| 38 | 공정위 추천·보증 심사지침(2024-12-01 시행) | 문자 매체는 "제목 또는 첫 부분", 구매 링크 사후 수수료도 경제적 이해관계 → 설명란 첫 줄 규칙과 일치. **공정위 원문 URL 미확인(로펌 뉴스레터만)** | [Y24] |

### 5-F. 수익화 준비 (39~40)
| # | 할 일 | 세부 | 출처 |
|---|---|---|---|
| 39 | YPP 요건 숙지 | 현재: 구독 1,000 + 12개월 4,000시간 또는 90일 숏폼 1,000만, 2단계 인증, Advanced, AdSense 1개, 활성 경고 없음. **2027-02-01부터 신규 신청 8,000시간 또는 숏폼 2,000만.** 기존 회원은 2027-01-31까지 새 약관 수락. 팬 펀딩 문턱(500 구독 + 3,000시간 등)은 "unchanged"(수치는 2차 출처) | [Y18][Y19] |
| 40 | AdSense for YouTube | 요건 달성 시 Studio → 수익 창출 → AdSense START로 연결. **미국 세금 정보(W-8BEN, 개인)는 매년 12/10까지 제출. 미제출 시 최대 24% 원천징수.** 한미 조세조약 세율은 미확인 → 세무 확인(PLAN 대표 결정 4와 연결) | [Y20] |

### 5-G. YouTube Data API 업로드 권한 (41) — 대표 단계만 분리
| 단계 | 담당 | 할 일 | 출처 |
|---|---|---|---|
| 41-1 | 대표 | **Owner 계정**으로 GCP 프로젝트 → YouTube Data API v3 사용 설정 | [Y26] |
| 41-2 | 대표 | OAuth 동의 화면: 사용자 유형 **External**, 범위 `youtube.upload`(민감) + `youtube.readonly` + `yt-analytics.readonly`(기존 `scripts/youtube_auth.py`와 같음) | [Y28] |
| 41-3 | 대표 | **게시 상태를 "In production"으로 전환**. Testing 상태면 리프레시 토큰이 **7일 후 만료**된다(기존 스크립트 주석은 "테스트 사용자"를 전제 → 수정 제안). 앱 미검증이면 경고 화면이 뜨고 사용자 100명 제한이 걸리지만, 1인 사용에는 지장 없다(판단) | [Y28] |
| 41-4 | 대표 | OAuth 클라이언트(데스크톱 앱) JSON → 대표 PC에서 `python3 scripts/youtube_auth.py client_secret.json` → 계정 선택 화면에서 **브랜드 채널** 선택 → 출력된 3개 값을 클라우드 환경변수에(`YOUTUBE_CLIENT_ID`·`YOUTUBE_CLIENT_SECRET`·`YOUTUBE_REFRESH_TOKEN`, docs/ENV.md) | 저장소 스크립트 |
| 41-5 | 대표 | **API 감사(audit) 신청**: support.google.com/youtube/contact/yt_api_form. 2020-07-28 이후 만든 미검증 프로젝트의 `videos.insert`는 **비공개로 잠긴다.** 통과 전까지는 수동 업로드(§6). 심사 기간은 미확인 | [Y26][Y27] |
| 41-6 | 세션 | 쿼터: `videos.insert`는 2025-12-04부터 약 100단위로 인하, 2026-06-01부터 **별도 버킷(하루 100회)**. 그 밖에는 하루 10,000단위(thumbnails.set 50, captions.insert 400, videos.update 50). 주 1편 + 숏폼 7은 여유 | [Y25] |
| 41-7 | 세션 | 순서: `videos.insert`(private) → `thumbnails.set`(2026-09-14부터 50MB) → `captions.insert` → approved 확인 → `videos.update`로 공개·예약. 리프레시 토큰은 6개월 미사용 시 만료 | [Y25][Y29][Y28] |

### 5-H. 분석 지표 설정 (42)
| 지표 | 위치 | 기록 주기 | 출처 |
|---|---|---|---|
| 노출수·노출 CTR | Analytics → 콘텐츠(썸네일이 1초 넘게 50% 이상 보일 때 1회) | 주 1회 | [Y30] |
| 주요 순간(Intro = 30초 잔존율, Spikes·Dips) | 영상 분석 → 참여도(60초 이상·100뷰 이상, 1~2일 지연) | 편마다 | [Y30] |
| 트래픽 소스(검색·추천·숏폼) | 도달 범위 | 주 1회 | GROWTH §10 |
| 구독/1천 뷰, 숏폼 engaged views | 고급 모드 | 주 1회 | GROWTH §10 |
| A/B 결과 | Analytics(Test & Compare) | 편마다 | [Y11] |
| **Inspiration 탭은 2026-08부터 단계적 종료** → Research/Ask Studio 사용 | — | — | [Y31] |

- 기록처는 `reports/weekly-YYYY-WW.md`(analyst)이고, 체크포인트 수치는 GROWTH §10을 그대로 쓴다.

---

## 6. 첫 4주 실행 캘린더 (2026-10-05 월 ~ 11-01 일)

- **선행 조건**:
  - ⓐ N1(이름)·N2(제작 방식) 결정
  - ⓑ 채널 개설 + 전화·신분증 인증
  - ⓒ `GEMINI_API_KEY`(유료 티어), 필요 시 `FAL_KEY`
  - ⓓ Amazon 트래킹 ID(제휴 링크)
  - ⓔ OAuth 프로덕션 전환 + 감사 신청
- ⓔ가 늦어도 수동 업로드로 진행할 수 있다.
- 업로드 순서의 시의성 근거: EP002 = 한글날 10/9. EP001 = 신라면 40주년 "this month"라 **10월 공개 필수**(대본 타이밍 메모). EP003 = 김장철. EP004 = 빼빼로데이(11/11, GROWTH W4).

| 주 | 롱폼(주 1편 상한) | 숏폼 | 대표 할 일 | 자식 세션 할 일 | 선행 조건 |
|---|---|---|---|---|---|
| **W0** 10/2~10/4 | — | — | §7 결정 N1~N13 답변. 키 입력 | 이 문서 검수 PR. 프로필·배너·워터마크 시안(designer) | — |
| **W1** 10/5~10/11 | **EP002 한글** (● N10: ⓐ 10/9 공개 / ⓑ 10/13~14 공개 + 시제 수정) | EP002 파생 5(10/9~) | §5 1~16 개설·인증(1일), 업로드 기본값 17~28, OAuth 41-1~5, EP002 검수 PR 승인 → **Studio 수동 업로드 + 엔드스크린·A/B** | Remotion 템플릿 T01~T04·T07~T12 우선 제작 → EP002 렌더(원화 + 자모 리빌) → 썸네일 3안 → 업로드 패키지(R2 비공개 링크) | 키·채널 |
| **W2** 10/12~10/18 | **EP001 라면** (10/15 공개, 10월 필수) | EP001 파생 5 + (GROWTH D1에 따라) 독립 2 | 검수 PR 승인·업로드, 첫 Posts(자기소개 + 다음 주제 투표), Reddit 답변 1h | T05·T06 마무리, EP001 렌더, EP004 리서치 시작(빼빼로), TikTok·Reels 수동 패키지 | Amazon 트래킹 ID |
| **W3** 10/19~10/25 | **EP003 김장** (10/22 공개) | EP003 파생 5 | 업로드, 콜라보 후보 20곳 명단 검토, Koreabridge 등록 | EP003 렌더, EP004 대본, analyst 첫 주간 리포트(CTR·30초 잔존율) | Klook 제휴 ID |
| **W4** 10/26~11/1 | **EP004 빼빼로데이**(11/1 공개 목표) | EP004 파생 5 | 업로드, 콜라보 제안 5곳(0원), **30일 리뷰**(A/B 결과 3편) | 30일 리뷰 리포트, 템플릿 우선순위 갱신, API 감사 통과 시 publisher 자동 업로드 전환 | 감사 결과 |

**월 비용 (상한 20만원 대비, 추정)**
| 항목 | 월 | 비고 |
|---|---|---|
| Gemini TTS(유료 티어) | 약 1,000~2,000원 | 2027-01부터 단가 2배 |
| 보조 플레이트(fal Z-Image, 원화 없는 장면만) | 0~1,000원 | 대표 PC 로컬 생성이면 0 |
| Remotion·Playwright·ffmpeg·오디오 보관함·Freesound | 0 | 1인 무료·OSS |
| Cloudflare R2(업로드 패키지 전달) | 0(무료 범위 추정) | 기존 계정 |
| 도메인(선택, N12) | 약 1,700원/월(연 약 2만원) | — |
| 숏폼 훅 LTX(선택) | 0~5,600원 | OSS-③ 선택 항목 |
| **월 합계** | **약 0.3~1.1만원** | **상한의 6% 이하** |
| 일회성(선택) | 촬영 장비 23~35만원, 자체 LoRA 0.3~1.3만원, 상표 출원(미산정) | 대표 별도 승인(N4·N11·N12) |

---

## 7. 대표 결정 목록 (기본값 미적용 — COO가 그대로 질문)
| # | 결정 | 선택지 | 추천 | 근거 |
|---|---|---|---|---|
| N1 | 채널명·핸들 | ⓪ Korea Explained(핸들 변형) ① **Korea, Annotated** ② Chaekgado Notes ③ Hanji Archive ④ Korea in the Margins ⑤ The Minhwa Files | ① | 현 이름은 핸들·도메인 선점, 동명 8곳 이상 [Y60][Y61]. ①은 핸들·도메인이 비어 있고 원화 주석 문법과 일치. 상표는 미확인 |
| N2 | 비주얼 제작 방식 | ⓐ **원화 아카이브 × 코드 모션(AI 플레이트는 보조)** ⓑ OSS-③ 원안(AI 민화 플레이트 중심 + 코드 모션) ⓒ 생성 이미지 슬라이드(상용안) | ⓐ | 카드뉴스 1안과 같은 세계관, 생성 비중 최소 → 비진정성·고증 리스크 최저 [Y33][O§2]. 첫 샘플은 EP002 S01로 ⓐ·ⓑ A/B 비교 가능 |
| N3 | 모션 도구 | ⓐ **Remotion** ⓑ HyperFrames | ⓐ | 성숙도, JSON 렌더, 획 리빌 공식 API [Y53][Y54] |
| N4 | 대표 직접 촬영·장비 | ⓐ 촬영 안 함(원화·아카이브만) ⓑ **폰 + 짐벌 최소 키트(약 23~35만원, 일회성)** ⓒ 폰만(0원) | ⓒ로 시작해 W4 리뷰 후 ⓑ | 첫 3편은 원화로 충분(판단). 궁궐 촬영은 무료 신청 필요 [Y45] |
| N5 | YouTube "변형·합성 콘텐츠" 체크 | ⓐ 사실적 AI 플레이트·AI 영상이 들어간 편만 켬 ⓑ AI 음성을 쓰므로 매 편 켬 ⓒ 끔(설명란·영상 고지만) | ⓐ | 공식 기준은 사실적 콘텐츠. 일반 TTS는 명시 없음 [Y32]. 설명란·영상 고지는 어느 안이든 유지(CLAUDE.md) |
| N6 | 썸네일 시그니처 | ⓐ **붉은 낙관 + 한지 테두리(v1.1)** ⓑ 기존 노란 바 유지 ⓒ 둘 다 | ⓐ | 원화 세계관 일치, K&G 종이 테두리 사례 [Y63]. design-system 버전업은 대표 승인 사항 |
| N7 | 기본 카테고리 | ⓐ **Education** ⓑ Travel & Events | ⓐ | 서사형 60~70% 비중. 공식 권장 없음(미확인) |
| N8 | 제휴만 있는 편의 "유료 프로모션" 체크 | ⓐ 체크 안 함(설명란·구두 고지로) ⓑ 매 편 체크 | legal-reviewer 판정 후 결정 | 공식 문서는 스폰서십·보증만 명시 [Y21] |
| N9 | 숏폼 교차 게시 범위 | ⓐ **YT + TikTok + IG Reels(영어 신규 IG 계정)** ⓑ YT + 자매 IG(책가도 노트)만 ⓒ YT만 | ⓐ(자동 패키지 전제) | 자매 계정은 한국어 독자라 겹침이 적음(추정). 시간 예산 §4 |
| N10 | EP002 공개일 | ⓐ 10/9 한글날 당일(W1에 개설·인증·템플릿 최소 세트 완료가 조건) ⓑ 10/13~14(대본 S11 시제 "hosted"로 수정) | 키·채널이 10/5까지 준비되면 ⓐ, 아니면 ⓑ | 날짜 훅 [G40]. 대본 타이밍 메모 |
| N11 | 자체 LoRA·로컬 생성 | ⓐ 안 함(원화 + fal 소량) ⓑ 대표 PC 로컬(ComfyUI 등)로 보조 플레이트·LoRA | ⓐ로 시작 | ⓐ 채택 시 생성 필요량이 작음 |
| N12 | 도메인·상표 | ⓐ .com만 구매(연 약 2만원) ⓑ .com + 상표 출원(KIPRIS·USPTO) ⓒ 둘 다 안 함 | ⓐ(이름 확정 후 즉시) | 동명 선점 사례 [Y61] |
| N13 | API 업로드 전환 | ⓐ **OAuth 프로덕션 전환 + 감사 신청(W1)**, 통과 전 수동 ⓑ 계속 수동 업로드 | ⓐ | 미감사 업로드는 비공개로 잠김 [Y26]. Testing 토큰 7일 만료 [Y28] |

- 참고(보고, 결정 아님):
  - GROWTH의 D1~D3(숏폼 개수·커뮤니티 범위·콜라보)는 그 문서의 결정 대기 항목 그대로다.
  - Collaborations 인원(5 vs 10)과 X 링크 감점은 출처끼리 상충한다 → 실제 화면에서 확인한다.
  - `scripts/youtube_auth.py` 주석의 "테스트 사용자" 전제는 41-3에 맞게 고칠 것을 제안한다(이번 범위 밖).

---

## 8. 자가 검증
**성공 기준(작업 시작 시 설정)**:
- ① 지시 7개 범위를 모두 다룬다.
- ② 정책·요건 행에 공식 URL과 확인 날짜를 단다.
- ③ 수치·단가에 추정 표기를 한다.
- ④ 대표 결정 항목에 기본값을 적용하지 않는다.
- ⑤ 금지 사항 위반 0.
- ⑥ 400행 안팎, 표 중심.

| 기준 | 결과 | 판정 |
|---|---|---|
| 범위 1~7 | §1 이름·벤치마크 10 / §2 실사·모션·원화·오디오·AI 라벨·파이프라인 / §3 썸네일 / §4 마케팅 / §5 체크리스트 42 / §6 4주 캘린더·비용 / §7 결정 13 | 통과 |
| 출처 수 | Y1~Y83 신규 83개(+ 기존 문서 G·O 참조) | 통과 |
| 공식 문서 확인 비율 | 정책·요건 행(§2-A·2-G·§5 전체·§4 규칙) 중 공식 1차 출처 직접 확인 약 80%. 나머지는 (스니펫)·미확인·2차로 표기(공정위 원문, Reddit 규칙, TikTok 가이드, 팬 펀딩 수치, 채널 소개 길이 등) | 부분 통과(미확인 항목 명시) |
| 추정 표기 | 구독 수·가격·시간·비용 전부 "추정" 또는 표 머리에 명시 | 통과 |
| 대표 결정 기본값 | N1~N13 모두 "추천"만 표기, 캘린더의 해당 칸에 ●·N번호 표시 | 통과 |
| 금지 사항 | `.env`·비밀값 열람 0. 설치·등록·업로드 0. 건강·금융·법률 주제 0. 실존 인물·로고 사용 제안 0. Amazon 오프라인 링크 0 | 통과 |
| 분량 | 약 400행(커밋 시 `wc -l`로 확인) | 통과 |
| 한계 | 상표 DB·타 SNS 핸들·Reddit 원문 규칙·FB 그룹 규칙은 접근 차단으로 미확인. YT 핸들 404는 등록 가능 보장 아님 | 공개 |

---

## 출처 (확인 날짜 전부 2026-10-02)
- **YouTube Help·블로그**:
  - Y1 support.google.com/youtube/answer/1646861 · Y2 …/9481328 · Y3 …/11585688 · Y4 …/2657964
  - Y5 …/10456525 · Y6 …/72431 · Y7 …/57404 · Y8 …/2660027 · Y9 …/9527654 · Y10 …/9890437
  - Y11 …/16391400 · …/13861714 · Y12 …/6084043(스니펫) · Y13 …/6388789 · Y14 …/6140493
  - Y15 …/9884579 · Y16 …/14075157(스니펫) · Y17 …/7561938 · Y18 …/72851
  - Y19 blog.youtube/news-and-events/youtube-partner-program-updates-2027-new-opportunities-earn/
  - Y20 …/10391362 · Y21 …/154235 · Y22 …/2801973 · Y30 …/9314415 · …/9314486(스니펫) · Y31 …/15575509
  - Y32 …/14328491 · Y33 …/1311392 · Y47 …/3376882 · Y77 …/16554898 · Y78 …/10623810(스니펫) · Y82 …/3399767
- **YouTube API·Google 인증**:
  - Y25 developers.google.com/youtube/v3/revision_history · …/determine_quota_cost
  - Y26 …/youtube/v3/docs/videos/insert
  - Y27 …/youtube/v3/guides/quota_and_compliance_audits · support.google.com/youtube/contact/yt_api_form
  - Y28 developers.google.com/identity/protocols/oauth2 · support.google.com/cloud/answer/7454865(스니펫)
  - Y29 …/youtube/v3/docs/thumbnails/set
- **고지·법규**:
  - Y23 ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
  - Y24 shinkim.com/kor/media/newsletter/2613 · ajunews.com/view/20251202085042877(2차, 공정위 원문 미확인)
  - Y45 royal.khs.go.kr/afile/fileDownload/l7Amn(궁·능 관람 등에 관한 규정, 2026-02-05 개정)
  - Y46 news.seoul.go.kr/safe/archives/518080 · drone.onestop.go.kr
- **소재 라이선스**:
  - Y34 kogl.or.kr/info/licenseType1.do · mcst.go.kr/kor/s_open/kogl/koglType.jsp(스니펫)
  - Y35 phoko.visitkorea.or.kr · Y36 pexels.com/license · Y37 pixabay.com/service/license-summary/ · pixabay.com/service/faq/
  - Y38 unsplash.com/license · Y39 coverr.co/license · Y40 nasa.gov/nasa-brand-center/images-and-media/
  - Y41 commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia
  - Y42 archives.gov/global-pages/privacy.html · Y43 loc.gov/legal/
  - Y44 archive.org/details/prelinger(본문 미렌더, 2차 확인) · ehistory.go.kr(이용조건 미공개)
  - Y48 freemusicarchive.org/faq · Y49 freesound.org/help/faq/
  - Y50 incompetech.com/music/royalty-free/licenses/
  - Y83 cardnews/docs/DESIGN_SOURCES.md §5(origin/cardnews/main, Met·Cleveland·e뮤지엄 31점 원문 확인 기록)
- **TTS·도구**:
  - Y51 huggingface.co/hexgrad/Kokoro-82M · Y52 ai.google.dev/gemini-api/docs/pricing · ai.google.dev/gemini-api/terms
  - Y53 github.com/remotion-dev/remotion/blob/main/LICENSE.md
  - Y54 remotion.dev/docs/fonts · remotion.dev/docs/paths/evolve-path(스니펫)
  - Y55 github.com/heygen-com/hyperframes · Y56 github.com/motion-canvas/motion-canvas
  - Y57 blender.org/about/license/ · developer.blender.org/docs/release_notes/5.0/grease_pencil/(스니펫)
  - Y58 blackmagicdesign.com/products/davinciresolve/studio · Y59 github.com/NatronGitHub/Natron
- **이름·벤치마크·썸네일**:
  - Y60 youtube.com/@koreaexplained · youtube.com/results?search_query=korea+explained&sp=EgIQAg%253D%253D · youtube.com/@KorExplained
  - Y61 koreaexplained.com · rdap.verisign.com/com/v1/domain/koreaexplained.com
  - Y62 tmsearch.uspto.gov · kipris.or.kr · branddb.wipo.int
  - Y63 youtube.com/@KingsandGenerals · @Simplehistory · @HistoryMatters · @OverSimplified · @Asianometry · @fern-tv · @TheFrogOutsidetheWell · @loonytricky · @AsianBoss · @KorExplained
  - Y64 netinfluencer.com/?p=53558(원문 thumbnailbench.com/resources/youtube-thumbnail-study-2026 미열람)
  - Y65 vidiq.com/research/youtube-thumbnail-study/(403, 스니펫)
  - Y66 searchenginejournal.com/do-faces-help-youtube-thumbnails-heres-what-the-data-says/563944/
- **마케팅**:
  - Y67 replyhey.com/subreddits/korea · /travel · /solotravel(3자 집계, Reddit 원문 접근 차단)
  - Y68 gummysearch.com/r/koreatravel/ · /seoul/ · /Living_in_Korea/ · /hanguk/ · /AskAKorean/ · /kpop/ · /KoreanFood/
  - Y69 seoulstart.com/directory/communities · discordbotlist.com/servers/koreatravel-discord-1305766449360670741(스니펫)
  - Y70 tripadvisor.com.au/Trust-llmsjBtituuk(스니펫) · Y71 waygook.org · Y72 koreabridge.net/about
  - Y73 petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/ · storyboard18.com(Reels 3분, 스니펫) · searchengineland.com/instagram-now-allows-up-to-5-links-in-bio-395742(스니펫)
  - Y74 meta.com/help/artificial-intelligence/1783222608822690/
  - Y75 newsroom.tiktok.com/en-us/partnering-with-our-industry-to-advance-ai-transparency-and-literacy(스니펫)
  - Y76 ppc.land/x-drops-year-old-link-penalty-musk-tells-zuckerberg-on-platform/
  - Y79 creatorexperiments.substack.com/p/should-you-use-your-substack-to-grow · Y80 arxiv.org/abs/1805.01887
  - Y81 koreatimes.co.kr/amp/lifestyle/people-events/20250429/korea-appoints-2800-global-content-creators-to-promote-culture-tourism
- **기존 문서 참조**:
  - [G#] = docs/GROWTH_STRATEGY.md 출처 목록
  - [O#] = docs/TOOLING_OPENSOURCE.md 출처 목록
