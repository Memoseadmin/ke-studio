# 유튜브 채널명 조사 — "Korea" 없는 이름 (리서처·네이밍, 2026-10-02)

> 전제: 대표 결정(2026-10-02). 채널명에 "Korea / Korean / K-"를 쓰지 않는다. Korea Explained는 핸들·도메인이 선점됐고 동명 채널이 8곳 이상이라 폐기([YOUTUBE_LAUNCH_PLAN §1-A](YOUTUBE_LAUNCH_PLAN.md)). 이전 추천안 "Korea, Annotated"도 같은 이유로 제외.
> 기준: 채널 정체성(외국인 대상 한국 문화·역사·여행·음식 설명, 서사형 60~70%, 시각 = 퍼블릭 도메인 민화 원화 × 코드 모션그래픽, 자매 인스타 "책가도 노트")과 cardnews DESIGN_SOURCES §8 1안 "원화 아카이브"(박물관 도록 톤, 한지 오프화이트, 붉은 낙관).
> 모든 실측은 2026-10-02 이 세션 VM에서 실행. 수치·판정은 추정이며 최종 확인은 대표가 등록 화면에서 한다.

## 0. 결론 (5줄)
- 후보 15개를 만들어 YouTube 핸들 34개, 도메인 24개×3(.com·.co·.kr)을 실측하고 동명 검색 9회를 했다.
- **추천 1위 = Hanji Archive (@HanjiArchive)**. 핸들 404, hanjiarchive.com·.co·.kr 모두 RDAP 404(미등록). "원화 아카이브" 시각 방향과 이름이 그대로 일치한다.
- 2위 Ink & Hanji, 3위 Joseon Annotated, 4위 The Minhwa Files, 5위 The Folding Screen.
- 탈락: Tiger & Magpie(국내 차 브랜드 Magpie&Tiger와 충돌), Morning Calm 계열(대한항공 기내지 "Morning Calm"과 충돌), Red Seal·Scholar's Shelf(.com 선점).
- 확인 못 한 것: 상표(USPTO·KIPRIS·WIPO), IG·TikTok·X 핸들, .kr 외국인 등록 자격, 404 핸들의 실제 예약 여부.

## 1. 후보 15개
발음 난이도는 영어권 화자 기준(하=바로 읽음, 중=한 번 들으면 됨, 상=철자·발음이 막힘), 판단.

| # | 이름 | 뜻·세계관 | 발음 | 브랜드 확장성 (시리즈·굿즈·도메인) | 한국 채널임을 알리는 태그라인 예시 |
|---|---|---|---|---|---|
| 1 | **Hanji Archive** | 한지(닥나무 종이) + 아카이브. 원화를 한지 위에 모아 둔 서고 | 하~중 (HAHN-jee) | 시리즈 "Archive No.01~", 굿즈 한지 엽서·노트, hanjiarchive.com | *Korea's stories, pulled from the archive.* |
| 2 | **Ink & Hanji** | 먹과 한지. 쓰는 사람(먹)과 기록(한지) | 하~중 | 시리즈 "Ink Notes", 굿즈 먹 스탬프, inkandhanji.com | *Korean history & culture, in ink on paper.* |
| 3 | **Joseon Annotated** | 조선 원전에 주석을 단다. 이전 추천 "Korea, Annotated"의 주석 문법 유지 | 중 (JOE-sun) | 시리즈 "Annotated: ___", joseonannotated.com | *Korea, from Joseon to K-drama, annotated.* |
| 4 | **The Minhwa Files** | 민화로 푸는 사건 파일. 미스터리·시리즈감 | 중 (MIN-hwa) | 시리즈 "File 001", minhwafiles.com | *Korean folk paintings that explain Korea.* |
| 5 | **The Folding Screen** | 병풍. 한 편 = 병풍 한 폭(Panel) | 하 | 시리즈 "Panel 1~10", thefoldingscreen.com | *One panel of Korea at a time.* |
| 6 | Chaekgado Notes | "책가도 노트" 영문판, 인스타와 1:1 | 상 (CHECK-gah-doh) | 인스타와 통합 브랜드, chaekgadonotes.com | *Notes from a Korean bookshelf painting.* |
| 7 | Minhwa Notes | 민화 노트 | 중 | 인스타 "책가도 노트"와 "Notes" 공유 | *Korea, read through its folk art.* |
| 8 | Hanji Notes | 한지 노트 | 하~중 | 노트 굿즈와 직결 | *Short notes on Korea, on hanji.* |
| 9 | Tiger & Magpie | 까치호랑이(작호도). 민화 대표 도상, 마스코트화 쉬움 | 하 | 마스코트 굿즈 최강 | *Korea's favorite folk painting, explaining Korea.* |
| 10 | Morning Calm Notes | "고요한 아침의 나라" 별칭 | 하 | morningcalmnotes.com | *Notes from the Land of the Morning Calm (Korea).* |
| 11 | Red Seal Notes | 붉은 낙관 | 하 | 낙관 = 로고 | *Stamped, sourced, Korean.* |
| 12 | Brush & Seal | 붓과 낙관 | 하 | 붓글씨 굿즈 | *Korean culture, signed and sealed.* |
| 13 | Seal & Screen | 낙관과 병풍 | 하 | 두 상징 조합 | *Korea, framed in folk art.* |
| 14 | Inkstone Notes | 벼루 노트 | 하 | 문방사우 시리즈 | *A Korean scholar's desk, explained.* |
| 15 | Peninsula, Annotated | 반도에 주석 | 하 | — | *The Korean peninsula, annotated.* |

## 2. 가용성 실측

### 2-A. YouTube 핸들 (`curl -o /dev/null -w "%{http_code}" -L https://www.youtube.com/@핸들`)
대조군: @koreaexplained 200, @mkbhd 200 → 방법 정상. 404 = 공개 채널 없음(예약·숨김 가능성은 남음).

| 핸들 | 결과 | 핸들 | 결과 |
|---|---|---|---|
| @HanjiArchive | **404** | @MagpieAndTiger | 200 (Magpie&Tiger 맥파이앤타이거, 구독 5.22K, 영상 112) |
| @InkAndHanji / @HanjiAndInk | **404 / 404** | @MagpieTiger | 200 (한국어 채널, 구독 3.75K) |
| @JoseonAnnotated | **404** | @TigerAndMagpie | 404 |
| @TheMinhwaFiles / @MinhwaFiles | **404 / 404** | @MorningCalmNotes / @MorningCalmAnnotated | 404 / 404 |
| @TheFoldingScreen | **404** | @FoldingScreen | 200 (무관 채널, 구독 32) |
| @FoldingScreenNotes | 404 | @RedSealNotes | 404 |
| @ChaekgadoNotes | 404 | @TheRedSeal | 200 (구독 521) |
| @MinhwaNotes / @HanjiNotes | 404 / 404 | @ScholarsShelf / @TheScholarsShelf | 404 / 200 |
| @BrushAndSeal | 404 | @InkstoneNotes | 404 |
| @SealAndScreen / @ScreenAndSeal | 404 / 404 | @PeninsulaAnnotated / @ThePeninsulaAnnotated | 404 / 404 |
| @HanjiHours / @TenScreens / @TheInkSeal | 404 / 404 / 404 | @MinhwaMuseum | 200 (한국민화뮤지엄, 구독 2.36K) |

### 2-B. 도메인 (RDAP, 404 = 미등록)
- 조회처: .com = `rdap.verisign.com/com/v1/domain/`, .co = `rdap.registry.co/co/domain/`, .kr = `rdap.nic.or.kr/domain/` (IANA RDAP bootstrap에서 확인).
- 대조군: google.com 200, google.co 200, google.kr 200 / 임의 문자열 .co·.kr 404 → 방법 정상.

| 도메인 기본형 | .com | .co | .kr |
|---|---|---|---|
| hanjiarchive | **미등록** | 미등록 | 미등록 |
| inkandhanji / hanjiandink | 미등록 / 미등록 | 미등록 | 미등록 |
| joseonannotated | 미등록 | 미등록 | 미등록 |
| minhwafiles / theminhwafiles | 미등록 / 미등록 | 미등록 | 미등록 |
| thefoldingscreen | 미등록 | 미등록 | 미등록 |
| chaekgadonotes / chaekgado | 미등록 / 미등록 | 미등록 | 미등록 |
| minhwanotes · hanjinotes · brushandseal · sealandscreen · inkstonenotes · morningcalmnotes · peninsulaannotated | 모두 미등록 | 미등록 | 미등록 |
| tigerandmagpie / magpieandtiger | **등록됨 / 등록됨** | 미등록 | 미등록 |
| redsealnotes | **등록됨** | 미등록 | 미등록 |
| scholarsshelf | **등록됨** | 미등록 | 미등록 |

- 가격은 이번에 조회하지 않았다(.com 연 약 2만원, 추정, §1-C 기존 값). .kr은 국내 주소·사업자 요건이 있을 수 있어 등록 자격 **미확인**.

### 2-C. 다른 SNS 핸들 (방법만, 미실행 = 미확인)
- namecheckr.com 또는 namechk.com에 핸들을 넣어 Instagram·TikTok·X·Threads 동시 조회.
- 직접 확인: `instagram.com/<핸들>`, `tiktok.com/@<핸들>`, `x.com/<핸들>`은 로그인 벽·봇 차단으로 HTTP 코드가 신뢰되지 않는다 → 앱의 프로필 편집 화면에서 입력해 본다.
- 인스타는 이미 "책가도 노트" 계정이 있으므로 채널명 확정 후 표시 이름만 맞출지는 대표 결정.

### 2-D. 동명 채널·브랜드·앱·책 검색 (WebSearch 2026-10-02)
| 이름 | 충돌 | 판정 |
|---|---|---|
| Hanji Archive | 서울 북촌 "한지가헌(Hanji House)" 지하 자료실을 영문 기사에서 "hanji archive"로 소개 [S1][S2] | 낮음. 고유명사가 아닌 설명어. 오히려 "한지 = 한국" 연상을 강화. 채널·앱·책 동명 없음 |
| Ink & Hanji | 동명 없음. "Hanji Notes"는 한지 노트 상품명으로 다수 쓰임 [S3] | 낮음 |
| Joseon Annotated | 동명 없음 [S4] | 낮음. 단 범위가 조선으로 좁게 들림 |
| The Minhwa Files | 동명 없음 [S4] | 낮음 |
| The Folding Screen | 1999년 동명 책(Lund Humphries), 일본 병풍 튜토리얼, Eames 가구 [S5] | 중. 일반어라 검색 선점이 어렵고 일본 byōbu 연상 |
| Tiger & Magpie | 국내 차 브랜드 Magpie&Tiger(YT 5.22K), 워싱턴DC 한식당 "Magpie and the Tiger"(2022, 폐업 후 팝업) [S6], .com 선점 | **높음 → 탈락** |
| Morning Calm 계열 | 대한항공 기내지 "Morning Calm"(1977~, 2024 WTA 수상) [S7] | **높음 → 탈락**(상표·혼동) |
| Inkstone / Brush & Seal / Red Seal | 중국 서예 용품(Inkston 등) 결과가 상위 [S8] | 중. 중국 문화로 오인 |
| Seal & Screen | 산업용 실(seal)·샤워 스크린 결과가 상위 [S9] | 중. 검색 노이즈 |
| Red Seal | 캐나다 기술 자격 "Red Seal"이 강한 일반 명칭(판단) + .com 선점 | 높음 → 탈락 |

### 2-E. 상표 (자동 조회 불가 → 전부 **미확인**)
- USPTO: tmsearch.uspto.gov → Wordmark "HANJI ARCHIVE", "HANJI*" / Nice 041(교육·엔터테인먼트), 009(영상), 035 / Live만.
- KIPRIS(kipris.or.kr): 상표명 영문 + 한글 음역("한지아카이브"), 41·9·35·16류.
- WIPO Global Brand Database: Brand = "HANJI ARCHIVE", Nice 41.
- "Hanji" 자체는 보통명사(한지)라 단독 등록은 어렵고, 결합 상표로 판단될 것(판단, 변리사 확인 필요).

## 3. 상위 5 추천 순위
5점 척도(5 = 가장 좋음). 검색 노출 = 이름 그대로 검색했을 때 1위를 차지할 가능성, 고유성 = 동명·혼동 없음, 세계관 = 원화 아카이브·책가도 노트와의 일치, 발음 = 영어권 화자 기준, 확장성 = 시리즈·굿즈·도메인. 전부 판단(추정).

| 순위 | 이름 | 검색 노출 | 고유성 | 세계관 | 발음 | 확장성 | 합계 | 핸들 / .com |
|---|---|---|---|---|---|---|---|---|
| **1** | **Hanji Archive** | 4 | 4 | 5 | 4 | 5 | **22** | 404 / 미등록 |
| 2 | Ink & Hanji | 4 | 5 | 4 | 4 | 4 | 21 | 404 / 미등록 |
| 3 | Joseon Annotated | 4 | 5 | 4 | 3 | 3 | 19 | 404 / 미등록 |
| 4 | The Minhwa Files | 4 | 5 | 4 | 3 | 3 | 19 | 404 / 미등록 |
| 5 | The Folding Screen | 2 | 2 | 4 | 5 | 4 | 17 | 404 / 미등록 |

근거:
1. **Hanji Archive** — 시각 방향 1안 "원화 아카이브"와 이름이 같은 말이다. "hanji"는 한국 고유 단어 중 외국인 인지도가 비교적 높고 두 음절이라 읽기 쉽다. "Archive"는 시리즈 번호(Archive No.07), 출처 노트 멤버십(③ 수익 경로의 "대본·출처 노트")과 바로 이어진다. 약점: 공예·종이 채널로 오해할 수 있음 → 태그라인과 첫 줄 소개로 보완.
2. **Ink & Hanji** — 가장 고유하고 부드럽다. 약점: 앰퍼샌드가 핸들에서 "And"로 바뀌고, 무엇을 다루는지 덜 명확하다.
3. **Joseon Annotated** — "Joseon"이 한국을 가장 강하게 알린다(K-드라마 사극 시청자에게 익숙, 판단). 약점: 현대 음식·여행 주제와 범위가 어긋난다.
4. **The Minhwa Files** — 시리즈·미스터리감이 좋다. 약점: "minhwa" 인지도가 낮다.
5. **The Folding Screen** — 발음이 가장 쉽고 "한 편 = 병풍 한 폭" 구조가 깔끔하다. 약점: 일반어라 검색을 선점하기 어렵고 일본 병풍과 혼동된다.

### 1위 로고 워드마크 방향 (1줄)
한지 오프화이트 바탕에 먹색 세리프 대문자 "HANJI ARCHIVE"(자간 넓게, 박물관 도록 표제 톤)를 쓰고, 오른쪽 끝에 붉은 정사각 낙관 "韓紙"(또는 "한지")를 찍는다. 원형 프로필은 낙관만 쓴다.

### 브랜드 관계 (1위 기준 제안)
- 채널 소개 첫 줄: *Korean history & culture, explained from the original art.* → "korea explained" 검색어를 소개문으로 흡수(기존 §1-B 방식 유지).
- 소개 끝: *A Chaekgado Notes studio.* → 인스타 "책가도 노트"와 연결.

## 4. 대표 결정 목록 (기본값 미적용 — COO가 그대로 질문)
| # | 항목 | 선택지 | 리서처 의견 | 비고 |
|---|---|---|---|---|
| C1 | 최종 채널명 | ① Hanji Archive ② Ink & Hanji ③ Joseon Annotated ④ The Minhwa Files ⑤ The Folding Screen ⑥ 기타 | ① | 상표 미확인 |
| C2 | 핸들 표기 | ⓐ @HanjiArchive ⓑ @hanjiarchive ⓒ @hanji.archive ⓓ @Hanji_Archive | ⓐ | 핸들은 대소문자 구분 없음, 표시만 달라짐(추정). 구분점·밑줄은 구두 전달 시 오류 위험 |
| C3 | 태그라인 | ⓐ *Korea's stories, pulled from the archive.* ⓑ *Korean history & culture, explained from the original art.* ⓒ 직접 작성 | ⓑ (검색어 포함) | 태그라인에는 Korea 사용 가능 |
| C4 | 도메인 구매 | ⓐ .com만 ⓑ .com + .co ⓒ .com + .kr ⓓ 구매 안 함 | — | 가격·.kr 자격 미확인. 이름 확정 직후 선점 여부만 결정 |
| C5 | 상표 조회·출원 | ⓐ 조회만(대표 직접) ⓑ 조회 + 출원 ⓒ 안 함 | — | 기존 N12와 통합 가능 |
| C6 | 인스타 표시 이름 통일 | ⓐ "책가도 노트" 유지 ⓑ 채널명으로 통일 ⓒ 병기 | — | |

## 5. 자가 검증
| 성공 기준 | 결과 |
|---|---|
| 후보 12개 이상, Korea/Korean/K- 미포함 | O 15개 (태그라인에만 Korea 사용) |
| 후보별 뜻·발음·확장성·태그라인 | O §1 |
| YT 핸들 실측 + 대조군 | O 34개, 대조군 2개 |
| .com·.co·.kr 실측 + 대조군 | O 24개×3, 대조군 각 1개 |
| IG·TikTok·X 방법 | O 방법만, 미실행 |
| 동명 검색 | O 9회 |
| 상표 방법 | O 방법만, 미확인 |
| 상위 5 표·근거·워드마크 | O §3 |
| 대표 결정 목록(기본값 미적용) | O §4 |

## 출처 (확인 날짜 전부 2026-10-02)
- [S1] https://kculture.or.kr/cms/content/view/717
- [S2] https://thesoulofseoul.net/a-love-letter-to-korean-paper-exploring-hanji-house-in-bukchon-hanok-village/
- [S3] https://www.presentandcorrect.com/products/hanji-notebook
- [S4] https://www.davisart.com/blogs/curators-corner/korean-folk-art-chaekgado/ (검색 결과 중 동명 없음 확인용)
- [S5] https://www.deslegte.com/the-folding-screen-102451/ · https://learning.culturalheritage.org/products/the-japanese-folding-screen-a-tutorial-video-by-yoshiyuki-nishio
- [S6] https://dcist.com/story/22/01/31/magpie-and-the-tiger-opens-petworth · https://www.washingtonian.com/2023/06/09/their-restaurant-closed-too-soon-you-have-to-try-their-pop-ups
- [S7] https://www.imm-international.com/?p=14742
- [S8] https://www.inkston.com/shop/inks/seal-paste/red-seal-paste/
- [S9] https://www.aesseal.com/en/node/1152
- YouTube 핸들: https://www.youtube.com/@<핸들> (curl HTTP 코드, 200 페이지는 og:title·구독 수 추출)
- RDAP: https://data.iana.org/rdap/dns.json · https://rdap.verisign.com/com/v1/ · https://rdap.registry.co/co/ · https://rdap.nic.or.kr/

## 6. 2차 탐색 — 쉬운 영어 일반어 조합 (2026-10-02)

> 대표 피드백(2026-10-02): 1차 상위 5 전부 보류. 방향 = 한국어 단어(hanji·minhwa·joseon) 없이 영어권 화자가 바로 읽고 뜻을 짐작하는 일반어 조합. "Korea/Korean/K-"는 이름에 금지, 태그라인엔 허용.
> 규칙: **YouTube 핸들 404 + .com 미등록 둘 다** 충족한 후보만 상위에 올림. 실측은 전부 2026-10-02 이 세션 VM, 방법은 §2와 동일. 모든 수치·판정은 추정이며 최종 확인은 대표가 등록 화면에서 한다.

### 6-0. 결론 (5줄)
- 후보 24개(+변형)를 만들어 YouTube 핸들 105개(대조군 3개 포함), 도메인 40개×3(.com·.co·.kr)을 실측하고 동명 검색 7회를 했다.
- **추천 1위 = Plate & Caption (@PlateAndCaption)**. 핸들 404, plateandcaption.com·.co·.kr 미등록. 도록의 "도판(plate) + 설명(caption)" = 원화 + 해설이라는 채널 형식 그 자체이고, plate(접시)가 음식 편까지 덮는다.
- 2위 The Painted Map, 3위 The Annotated Map, 4위 Ten Panels, 5위 Ink Almanac.
- 일반어라 예상대로 선점이 많았다: Margin Notes·Paper Lantern·Second Look·Story Screen·Folded Map·Footnote Lab 등 핸들 200 → 탈락.
- 확인 못 한 것: 상표(USPTO·KIPRIS·WIPO), IG·TikTok·X 핸들, 404 핸들의 실제 예약 여부, .kr 등록 자격(§2-B와 같음).

### 6-1. 후보 24개
발음 난이도 = 영어권 화자 기준(하=바로 읽음, 중=한 번 들으면 됨), 판단. 세계관 = 원화 아카이브(박물관 도록 톤)·책가도 노트와의 연결.

| # | 이름 | 뜻 | 세계관 연결 | 발음 | 태그라인 예시 (Korea 허용) |
|---|---|---|---|---|---|
| 1 | **Plate & Caption** | 도판과 그 아래 설명문 | 도록 한 장 = 원화(plate) + 해설(caption). plate = 음식 접시 이중 의미 | 하 | *Korea, one plate and one caption at a time.* |
| 2 | **The Painted Map** | 그려진 지도 | 민화·고지도 위에서 여행·역사를 짚는다 | 하 | *Korea's history and places, on a painted map.* |
| 3 | **The Annotated Map** | 주석 달린 지도 | 1차 "Annotated" 문법 유지 + 지도(여행) | 하 | *Korea, explained on an annotated map.* |
| 4 | **Ten Panels** | 열 폭 | 병풍 10폭. 한 편 = 한 폭, 10편 = 한 시즌 | 하 | *Korean stories told across ten folding-screen panels.* |
| 5 | **Ink Almanac** | 먹으로 쓴 연감 | 절기·명절·음식 달력형 서사, 기록물 톤 | 하~중 (AWL-muh-nak) | *A Korean year, written in ink.* |
| 6 | The Long Scroll | 긴 두루마리 | 연속 서사·시리즈 | 하 | *Korea's story, one long scroll.* |
| 7 | Margin & Ink | 여백과 먹 | 여백에 단 메모 = 주석 | 하 | *Notes in the margins of Korean history.* |
| 8 | Fold & Footnote | 접힘과 각주 | 병풍 접힘 + 출처 각주 | 하 | *Korean culture, folded open and footnoted.* |
| 9 | The Almanac Room | 연감 방 | 서가·자료실 은유 | 하~중 | *Every season of Korea, in one room.* |
| 10 | Catalogue Notes | 도록 노트 | 도록 + 인스타 "책가도 노트"의 Notes | 하 | *Museum-style notes on Korea.* |
| 11 | Paper Window Notes | 창호지 창 노트 | 창으로 들여다본 한국 | 하 | *A paper window into Korea.* |
| 12 | The Explaining Room | 설명하는 방 | "explained" 계열 설명 동사 | 하 | *Where Korea gets explained.* |
| 13 | Ink Catalogue | 먹 도록 | 도록 톤 | 하 | *A catalogue of Korea, in ink.* |
| 14 | The Captioned Map | 캡션 달린 지도 | 1·2 혼합 | 하 | *Korea, mapped and captioned.* |
| 15 | Gallery Notes (The) | 전시실 노트 | 박물관 톤 | 하 | *Gallery notes on Korean culture.* |
| 16 | Shelf & Story | 서가와 이야기 | 책가도(서가) | 하 | *Stories from a Korean bookshelf.* |
| 17 | Open Shelf Notes | 열린 서가 노트 | 책가도 | 하 | *An open shelf of Korean stories.* |
| 18 | Margin Notes | 여백 메모 | 주석 | 하 | — |
| 19 | Paper Lantern | 종이 등 | 등불·축제 | 하 | — |
| 20 | Footnote Atlas | 각주 지도첩 | 출처 + 지도 | 하 | — |
| 21 | The Second Look | 다시 보기 | 설명 행위 | 하 | — |
| 22 | Story Screen | 이야기 병풍 | 병풍(screen) | 하 | — |
| 23 | The Folded Map | 접힌 지도 | 지도 | 하 | — |
| 24 | Ink Explained / Explained in Ink | 먹으로 설명 | "explained" 동사 | 하 | — |

(18~24는 아래 실측에서 핸들 또는 .com 선점으로 탈락. 태그라인 생략.)

### 6-2. YouTube 핸들 실측 (`curl -s -o /dev/null -w "%{http_code}" -L https://www.youtube.com/@핸들`)
대조군: @koreaexplained 200, @mkbhd 200, @zzqxnotachannel123 404 → 방법 정상. 404 = 공개 채널 없음(예약·숨김 가능성 남음). 200 채널의 내용은 이번엔 열어 보지 않음(선점 사실만 사용).

| 후보 | 404 (비어 있음) | 200 (선점) |
|---|---|---|
| Plate & Caption | **@PlateAndCaption, @PlateCaption, @ThePlateAndCaption, @PlateAndCaptionNotes, @PlateAndCaptionStudio** | — (@PlateNotes·@ThePlateNotes·@PlateLab·@PlateRoom 200, @ThePlateRoom 404) |
| The Painted Map | **@ThePaintedMap, @PaintedMap, @PaintedMapNotes, @PaintedMapLab, @PaintedMapFiles, @ThePaintedMapFiles** | — (@PaintedAtlas 200, @ThePaintedAtlas 404) |
| The Annotated Map | **@TheAnnotatedMap, @AnnotatedMap** | — |
| Ten Panels | **@TenPanels, @TheTenPanels, @TenPanelsNotes, @TenPanelsStudio, @TenPanelsLab, @TenPanelsFiles** | — |
| Ink Almanac | **@InkAlmanac, @TheInkAlmanac, @InkAlmanacNotes, @InkAlmanacLab, @InkAlmanacFiles, @AlmanacOfInk** | — |
| The Long Scroll | @TheLongScroll, @LongScroll | @OpenScroll, @TheOpenScroll, @ScrollNotes |
| Margin & Ink | @MarginAndInk | @InkAndMargin, @MarginNotes, @TheMarginNotes, @MarginNotesStudio, @MarginLab, @MarginAtlas, @TheMarginAtlas, @MapAndMargin |
| Fold & Footnote | @FoldAndFootnote | @FootnoteFiles, @TheFootnoteFiles, @TheFootnote, @Footnoted, @FootnoteLab, @FootnoteAtlas (@TheFootnoteAtlas 404) |
| Almanac | @TheAlmanacRoom, @AlmanacNotes | — |
| Catalogue | @CatalogueNotes, @InkCatalogue, @TheInkCatalogue | — |
| Paper Window | @PaperWindowNotes | @PaperWindow, @ThePaperWindow |
| Explaining | @TheExplainingRoom | @ExplainedInInk, @InkExplained |
| Captioned Map | @TheCaptionedMap, @TheFootnotedMap, @CaptionNotes | @TheCaptioned, @TheCaptionRoom |
| Gallery / Shelf | @TheGalleryNotes, @ShelfAndStory, @OpenShelfNotes | @GalleryNotes, @TheOpenShelf, @StoryShelf, @TheStoryShelf, @ShelfNotes, @TheLongShelf |
| 기타 | @TheInkfold, @FoldedMapNotes, @TheUnfoldedMap, @PaperAndPlate, @InkAndPlate | @Inkfold, @PaperLantern, @ThePaperLantern, @Paperlight, @ThePaperlight, @SlowLantern, @QuietInk, @TheQuietInk, @SecondLook, @TheSecondLook, @StoryScreen, @TheStoryScreen, @TheThreshold, @ThresholdNotes, @FoldedMap, @TheFoldedMap, @UnfoldedMap, @LanternNotes |

### 6-3. 도메인 실측 (RDAP, 404 = 미등록, 200 = 등록됨)
조회처 §2-B와 동일. 대조군: google.com·.co·.kr 200, zzqxnotadomain917.com·.co·.kr 404 → 방법 정상.

| 도메인 기본형 | .com | .co | .kr |
|---|---|---|---|
| plateandcaption / platecaption | **미등록 / 미등록** | 미등록 / 미등록 | 미등록 / 미등록 |
| thepaintedmap / paintedmap / paintedmapnotes | **미등록** / 등록됨 / 미등록 | 미등록 ×3 | 미등록 ×3 |
| theannotatedmap / annotatedmap | **미등록 / 미등록** | 미등록 | 미등록 |
| tenpanels / thetenpanels / tenpanelsnotes | **미등록** ×3 | 미등록 | 미등록 |
| inkalmanac / theinkalmanac / almanacofink | **미등록** ×3 | 미등록 | 미등록 |
| thelongscroll / longscroll | 미등록 / 등록됨 | 미등록 | 미등록 |
| marginandink · foldandfootnote · thealmanacroom · almanacnotes · cataloguenotes · inkcatalogue · paperwindownotes · thecaptionedmap · thefootnotedmap · thefootnoteatlas · footnoteatlas · thegallerynotes · openshelfnotes · foldedmapnotes · theinkfold | 모두 미등록 | 미등록 | 미등록 |
| theexplainingroom | 미등록 | **등록됨** | 미등록 |
| paperwindow · shelfandstory · captionnotes · theplateroom · theunfoldedmap · paperandplate · inkandplate · thepaintedatlas | 모두 등록됨 | 미등록 | 미등록 |
| inkfold | 등록됨 | 등록됨 | 미등록 |

**핸들 404 + .com 미등록 동시 충족(상위 후보군)**: Plate & Caption, The Painted Map, The Annotated Map, Ten Panels, Ink Almanac, The Long Scroll(the- 형만), Margin & Ink, Fold & Footnote, The Almanac Room, Almanac Notes, Catalogue Notes, Ink Catalogue, Paper Window Notes, The Captioned Map, The Gallery Notes, Open Shelf Notes. 탈락: 핸들 선점 = Margin Notes·Paper Lantern·Second Look·Story Screen·Folded Map·Footnote Atlas(무관사형)·Explained in Ink 등, .com 선점 = Shelf & Story·Paper Window·Caption Notes, .co 선점 = The Explaining Room(감점).

### 6-4. 동명 채널·브랜드·앱·책 검색 (WebSearch 2026-10-02)
| 이름 | 결과 | 판정 |
|---|---|---|
| Plate & Caption | 동명 브랜드·팟캐스트·책·앱 없음. "Caption"(팟캐스트 검색 스타트업), "Palate"(AI 팟캐스트 앱) 등 유사어만 [T1] | 낮음 |
| The Painted Map | Cambridge UP 학술서 *The Mapping of Power in Renaissance Italy*(2014)의 서론 장 제목 "The Painted Map" [T2], Goodreads에 관련 도서 항목 1건(제목 미확인) [T3] | 중~낮음. 채널·앱 동명 없음, 검색 1위 선점은 다소 어려움(추정) |
| The Annotated Map | 동명 없음. 지도 유튜버 Map Men의 책 *This Way Up*이 상위 [T4] | 낮음. 단 "annotated map"은 일반 명사구라 검색 노이즈 큼 |
| Ten Panels | 동명 없음. 만화 "Panels" 팟캐스트·잡지가 상위 [T5] | 낮음. 만화 채널로 오인 가능 |
| Ink Almanac / Margin & Ink / Fold & Footnote / The Long Scroll | 앞의 셋은 동명 없음 [T6]. "The Long Scroll"은 둔황 출토 초기 선(禪) 문헌의 영어 통칭 [T7] | Long Scroll = 중(중국·선불교 연상) → 상위 제외 |

### 6-5. 상위 5 추천 순위
5점 척도(5 = 가장 좋음), 항목 정의는 §3과 같음. 전부 판단(추정). 1차 후보와 겹치지 않음.

| 순위 | 이름 | 검색 노출 | 고유성 | 세계관 | 발음 | 확장성 | 합계 | 핸들 / .com |
|---|---|---|---|---|---|---|---|---|
| **1** | **Plate & Caption** | 4 | 5 | 5 | 5 | 4 | **23** | @PlateAndCaption 404 / plateandcaption.com 미등록 |
| 2 | The Painted Map | 3 | 3 | 5 | 5 | 5 | 21 | @ThePaintedMap 404 / thepaintedmap.com 미등록 |
| 3 | The Annotated Map | 3 | 4 | 4 | 5 | 4 | 20 | @TheAnnotatedMap 404 / theannotatedmap.com 미등록 |
| 4 | Ten Panels | 3 | 4 | 4 | 5 | 3 | 19 | @TenPanels 404 / tenpanels.com 미등록 |
| 5 | Ink Almanac | 4 | 4 | 4 | 4 | 3 | 19 | @InkAlmanac 404 / inkalmanac.com 미등록 |

근거 (각 3줄):
1. **Plate & Caption**
   - 박물관 도록의 기본 단위(도판 + 캡션)가 곧 우리 영상 문법(퍼블릭 도메인 원화 + 해설 모션그래픽)이다.
   - plate는 "음식 접시"로도 읽혀 음식·구매 의도형 편(30~40%)까지 이름 하나로 덮는다.
   - 핸들 변형 5종·도메인 3종 전부 비어 있고 동명 없음. 약점: 앰퍼샌드가 핸들에서 "And"로 바뀐다(구두 전달 시 "plate and caption").
2. **The Painted Map**
   - 민화·고지도 원화 위에 장소·역사를 짚는 여행·역사 편과 잘 맞고 단어가 가장 쉽다.
   - 시리즈("Map 01 · Gyeongju") 확장이 자연스럽다. paintedmap.com은 선점이라 the- 형 사용.
   - 약점: 학술서 장 제목·도서 1건과 겹쳐 검색 1위 선점이 상대적으로 어렵다(추정).
3. **The Annotated Map**
   - 이전 추천 "Korea, Annotated"의 주석 문법을 Korea 없이 잇는다. 핸들·.com 모두 the-/무관사형 둘 다 비어 있다.
   - "설명 채널"이라는 정체가 이름에서 바로 드러난다.
   - 약점: 일반 명사구라 검색 노이즈가 크고, 민화 시각 톤과의 연결은 2위보다 약하다.
4. **Ten Panels**
   - 병풍 10폭 = 시즌 10편 구조로 기획이 바로 선다. 두 단어 모두 초급 영어.
   - 핸들 변형 6종·도메인 전부 비어 있다.
   - 약점: 숫자가 고정돼 시즌 외 단발 편·숏폼과 어긋나고, 만화(panel) 채널로 오인될 수 있다.
5. **Ink Almanac**
   - 절기·명절·제철 음식처럼 "달력으로 읽는 한국" 서사에 강하고, 먹 = 원화 톤.
   - 두 단어 조합이 드물어 검색 선점이 쉬워 보인다(추정). 변형 전부 비어 있다.
   - 약점: almanac 발음·뜻이 비원어민 시청자에게 한 단계 어렵고, 범위가 계절물로 좁게 들린다.

차순위(상위 5 밖, 핸들·.com 모두 비어 있음): Margin & Ink, Fold & Footnote, Catalogue Notes, The Captioned Map, Paper Window Notes.

#### 1위 워드마크 방향 (1줄)
한지 오프화이트 바탕에 먹색 세리프 대문자 "PLATE & CAPTION"(넓은 자간, 도록 표제 톤)을 쓰고 앰퍼샌드만 붉은 낙관색 정사각 도장 안에 넣으며, 아래에 도록 캡션처럼 작은 이탤릭 "Pl. 01 — Korea, explained"를 붙인다(원형 프로필 = 붉은 "&" 낙관).

### 6-6. 대표 결정 목록 갱신 (기본값 미적용 — COO가 그대로 질문, §4를 대체하지 않고 2차 기준으로 다시 씀)
| # | 항목 | 선택지 | 리서처 의견 | 비고 |
|---|---|---|---|---|
| C1 | 최종 채널명 | ① Plate & Caption ② The Painted Map ③ The Annotated Map ④ Ten Panels ⑤ Ink Almanac ⑥ 차순위·1차 후보 중 선택 ⑦ 3차 탐색 | ① | 상표 미확인 |
| C2 | 핸들 표기 | ⓐ @PlateAndCaption ⓑ @PlateCaption ⓒ @ThePlateAndCaption | ⓐ (이름 그대로 읽힘) | 셋 다 404. 대소문자는 표시만 달라짐(추정). 미사용 변형은 예약 여부 결정 필요 |
| C3 | 태그라인 | ⓐ *Korea, one plate and one caption at a time.* ⓑ *Korean history & culture, explained from the original art.* ⓒ 직접 작성 | ⓑ (검색어 "korea explained" 흡수) | 태그라인에는 Korea 허용 |
| C4 | 도메인 구매 | ⓐ .com만 ⓑ .com + .co ⓒ .com + .kr ⓓ 구매 안 함 | — | 가격 미조회, .kr 자격 미확인 |
| C5 | 상표 조회·출원 | ⓐ 조회만(대표 직접) ⓑ 조회 + 출원 ⓒ 안 함 | — | 일반어 조합이라 식별력 판단은 변리사 확인 필요(판단) |
| C6 | 인스타 표시 이름 | ⓐ "책가도 노트" 유지 ⓑ 채널명으로 통일 ⓒ 병기 | — | |
| C7 (신규) | 앰퍼샌드 사용 | ⓐ 표시명 "Plate & Caption" ⓑ "Plate and Caption" | — | 1위 선택 시에만. 핸들은 어느 쪽이든 PlateAndCaption |

### 6-7. 자가 검증
| 성공 기준 | 결과 |
|---|---|
| 후보 20개 이상, 1~2단어 영어 일반어, 한국어 단어·Korea/Korean/K- 미포함 | O 24개(이름엔 미포함, 태그라인에만 Korea) |
| 후보별 뜻·세계관·발음·태그라인 | O §6-1 (선점 탈락 7개는 태그라인 생략) |
| YT 핸들 실측 + 대조군 + 변형(The·Notes·Files·Lab 등) | O 105개(대조군 3개 포함) |
| .com·.co·.kr RDAP + 대조군 | O 40개×3, 대조군 2개 |
| 동명 검색 | O 7회 |
| 상위 5 = 핸들 404 + .com 미등록만 | O §6-5 |
| 상위 5 표·근거 3줄·워드마크, 1차와 미중복 | O |
| 대표 결정 목록(기본값 미적용) | O §6-6 |
| 1차 내용 보존 | O §0~5·출처 수정 없음 |

### 6-8. 출처 (확인 날짜 전부 2026-10-02)
- [T1] https://techcouver.com/2020/11/27/vancouver-startup-caption-creates-google-for-podcasts/ · https://apps.apple.com/us/app/id6479173263
- [T2] https://resolve.cambridge.org/core/books/abs/mapping-of-power-in-renaissance-italy/introduction-the-painted-map/096A9E988657658BEB25D07421EA439E
- [T3] https://www.goodreads.com/book/show/243034482 (검색 결과에 노출, 제목 직접 미확인)
- [T4] https://www.rizzolibookstore.com/product/map-men-debut-book-original
- [T5] https://bookriot.com/introducing-oh-comics-the-panels-podcast · https://www.comic-salon.de/en/panels-0
- [T6] https://theinkwellpodcast.substack.com · https://podcasts.apple.com/us/podcast/ink-peat/id1462594194 (동명 없음 확인용)
- [T7] https://forum.treeleaf.org/forum/treeleaf/treeleaf-community-topics-about-zen-practice/541037-the-long-scroll
- YouTube 핸들: https://www.youtube.com/@<핸들> (curl HTTP 코드)
- RDAP: https://rdap.verisign.com/com/v1/ · https://rdap.registry.co/co/ · https://rdap.nic.or.kr/
