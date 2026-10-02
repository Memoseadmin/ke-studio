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
