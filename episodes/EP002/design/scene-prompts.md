# EP002 장면별 이미지 프롬프트 (S01~S13)

직원: designer / 기준일: 2026-10-01 / 입력: `script.en.md` 메타 표("화면 원칙"·"숏폼 후보") + S01~S13 화면·텍스트·장면 메모 / 규칙: `/episodes/EP001/design/design-system.md` v1.0(채널 공통, 참조만)
상태: **prompt-ready**, 이미지 미생성(생성 API 키 없음). 생성하면 장면별로 모델·날짜·시드·라이선스를 이 파일 하단 표에 기록.

공통 원칙
- 모든 플레이트는 **글자 없는 그림**. 연도·자모·이름·인용·고지 문구는 전부 편집 프로그램 텍스트 오버레이(EN Anton/Pretendard, KR Black Han Sans/Pretendard). 아래 각 장면의 "텍스트 오버레이" 목록이 그 전부다.
- **자모는 전 편의 핵심 비주얼**이지만 AI 이미지 안에 그리지 않는다. 자모 격자(S04·S12), 획 그리기(S09·S13), 타이포 모션(S07·S08)은 모션그래픽 레이어로 만들고, 아래 프롬프트는 그 뒤에 깔 **배경 플레이트**다. 현행 24자 = 흰색(#FFFFFF), 폐지 4자 = 회색(#7C838F) 고정.
- 폐지 4자 유니코드(검증값): ㆁ U+3181, ㅿ U+317F, ㆆ U+3186, ㆍ U+318D. 대본 S04 메모의 "ㆁ(U+318D) ㆆ(U+318E)"는 오기이므로 이 값을 쓴다. 목업 VM 폰트 WenQuanYi Zen Hei(GPL-2+embedding exception)는 4자 모두 지원. 최종본 KR 폰트(Black Han Sans/Pretendard)는 이 4자 지원 여부를 설치 후 확인하고, 미지원이면 Noto Sans KR(OFL) 등 OFL 폰트로 그 4자만 대체.
- 역사 인물(세종·최만리·연산군·주시경·전형필·정인지)은 **얼굴 없는 뒷모습 실루엣 또는 손만**. 세종 표준영정·광화문 동상·드라마/영화 배우를 연상시키는 의상·구도 금지. 작품명은 텍스트 카드만.
- 벽서(S01·S06)·상소문(S05)·공문서(S07·S08)·해례본(S03·S10) 위의 글자는 **읽히지 않는 흐림**. 사료에 원문이 없는 벽서는 어떤 문장도 생성하지 않는다. 해례본 실물 사진은 라이선스 확인 전 사용 금지(자체 일러스트).
- 지도(S05·S10)는 퍼블릭 도메인 Natural Earth 윤곽을 모션그래픽으로 얹는다. AI 플레이트에는 지도 윤곽을 그리지 않는다(국경·영역 오류 방지). 한일·한중 비교나 우열을 암시하는 배치 금지. 국기·정치 상징 금지.
- 16:9 원본은 1920x1080 이상. **숏폼 후보 장면(S01·S04·S05·S06·S10·S12)은 9:16 네이티브로 따로 생성**: 프롬프트 끝의 "16:9, 1920x1080"을 "vertical 9:16, 1080x1920, main subject in the middle third, calm upper and lower thirds"로 바꾼다. 9:16 메모 좌표는 1080x1920 기준, 문구 안전 영역 x 60~940, y 260~1440(design-system §4).
- 스타일 문자열(모든 프롬프트 끝): `flat editorial illustration, bold clean ink outlines, warm limited palette of night navy (#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA), subtle paper grain, calm cinematic lighting`
- 네거티브 입력란이 없는 생성기(Gemini 등)는 본문 끝에 `No text, no letters, no logos, no real people or faces.`를 그대로 넣는다.

공통 네거티브(모든 장면에 넣고, 장면별 추가분을 뒤에 붙인다)
```
text, letters, numbers, calligraphy strokes that form readable words, captions, subtitles, logos,
brand names, trademarks, product packaging graphics, printed labels, readable signage, maps with
borders, flags, real people, faces, portraits, royal portrait painting, bronze statue, celebrity
likeness, actors, copyrighted characters, mascots, film or TV stills, posters, watermarks, UI elements
```

---

## S01 Hook (0:00~0:14)
요약: 1504년 여름, 수도의 어두운 돌담에 붙은 익명의 종이 3장. 글자는 읽히지 않는다. 인물 없음.
```
A dark stone wall of a 15th-century Korean walled city at dusk, large rounded stones with deep
ink outlines, a narrow dirt lane below. Three plain sheets of cream hanji paper are pasted on
the wall at slightly different angles, one corner curling. The sheets carry only soft, out-of-
focus vertical ink marks that cannot be read, like a blurred memory of writing. A single warm
lantern glow from the upper right, the rest of the frame in deep night navy. Sheets sit in the
right 55% of the frame; the left 45% stays calm and dark for a headline. No people, no
silhouettes. Flat editorial illustration, bold clean ink outlines, warm limited palette of
night navy (#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA),
subtle paper grain, calm cinematic lighting. 16:9, 1920x1080. No text, no letters, no logos,
no real people or faces.
```
Negative 추가: `readable Korean letters, readable Chinese characters, legible handwriting, crowd, guards, torches held by people, blood, weapons`
텍스트 오버레이: `1504` 한 줄만(Anton, 흰색, 좌상단 안전 영역).
모션 메모: 종이 3장이 0.5초 간격으로 차례로 "붙는" 페이드인. 글자 흐림은 유지(샤픈 금지). 효과음 과장 없음.
9:16 메모: 종이 3장을 중앙 1:1(y 420~1500)에 세로로 재배치해 네이티브 생성. "1504"는 y 300~400. 숏폼 1번(S01+S06) 첫 컷.

## S02 Roadmap (0:14~0:52)
요약: 가로 타임라인 1446→1504→1894→1926→2026, 점이 하나씩 켜짐. 배경에 흐린 자모 패턴(모션 레이어).
```
An abstract wide background plate for a timeline: a long horizontal band of cream paper
stretched across the middle of a deep night navy frame, like an unrolled scroll, with a faint
warm glow along its length. Soft, out-of-focus geometric circle and stroke shapes drift in the
background at very low contrast, suggesting letterforms without being any readable script.
No dots, no markers and no labels on the band; those will be animated later. Flat editorial
illustration, bold clean ink outlines, warm limited palette of night navy (#1B1F2A), chili red
(#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA), subtle paper grain, calm cinematic
lighting. 16:9, 1920x1080. No text, no letters, no logos, no real people or faces.
```
Negative 추가: `clock, calendar grid, arrows, ruler marks, numbers`
텍스트 오버레이: `1446 · 1504 · 1894 · 1926 · 2026`(점 5개 위, Anton) / `580 years · 100th Hangul Day`(하단, Pretendard).
모션 메모: 점 5개가 red로 켜지며 라벨이 아래서 올라옴. 자모 24자가 배경에서 흰색 저대비로 천천히 떠다님(모션 레이어, 폰트 라이선스 확인). 상품 예고 구간에는 어떤 상품 그림도 없음.
9:16 메모: 타임라인을 세로로 세워 y 420~1500에 배치(1446 위, 2026 아래). 숏폼 비후보.

## S03 Why a king invents an alphabet (0:52~2:04)
요약: 15세기 서재, 책상 위 종이와 붓. 왕은 뒷모습 실루엣. 책 표지 모양 카드·드라마/영화 제목은 텍스트 카드만.
```
A quiet 15th-century Korean palace study at night, seen from behind: a low wooden desk with
blank sheets of cream paper, an ink stone, a single brush resting on a brush holder, a small
oil lamp with a warm flame. A seated figure in a plain dark robe is shown only from behind as
a flat featureless silhouette, no face, no profile, no crown, no portrait resemblance, the
head slightly bowed over the desk. Latticed window with soft moonlight behind. The desk and
paper in the lower right, the figure on the left third. Flat editorial illustration, bold
clean ink outlines, warm limited palette of night navy (#1B1F2A), chili red (#C8102E), pot
yellow (#FFD23F) and cream paper (#F7F3EA), subtle paper grain, calm cinematic lighting.
16:9, 1920x1080. No text, no letters, no logos, no real people or faces.
```
Negative 추가: `face, profile, beard, crown, dragon robe, throne, royal portrait, statue, actor, TV drama set, film still, hanging scroll with characters, readable writing on the paper`
텍스트 오버레이: `1443 · 28 letters` → `1446 · Hunminjeongeum` → 책 표지 카드(ke-paper 사각형)에 한글 `훈민정음`(Black Han Sans) → 인용 카드 `"a morning ... ten days" — the Haerye says`(Pretendard, 화자 특정 없음) → 텍스트 카드 `Tree with Deep Roots (SBS, 2011) · The King's Letters (2019)`(스틸·포스터·배우 이미지 없음).
모션 메모: 붓이 종이 위로 내려오는 느린 줌(인물은 실루엣 유지). 책 표지 카드는 플레이트 위에 그린 단색 사각형. 작품명 카드는 2초, 글자만.
9:16 메모: 책상·종이·붓만 중앙 1:1에 두고 실루엣은 프레임 밖으로. 숏폼 비후보.

## S04 Twenty-eight letters, twenty-four today (2:04~2:40)
요약: 검은 배경에 28자 격자(획 순서 모션). 현행 24자 흰색, 폐지 4자 회색으로 뒤늦게 켜졌다 흐려짐. 숏폼 "사라진 네 글자" 원본.
```
A minimal dark background plate for an animated letter grid: deep night navy field with a very
subtle 7 by 4 grid of faint rounded rectangles, like empty tiles on a quiet board, centred in
the frame with generous margins. A soft vignette, slightly lighter at the centre. No letters,
no symbols, no numbers inside the tiles; they will be animated later. Flat editorial
illustration, bold clean ink outlines, warm limited palette of night navy (#1B1F2A), chili red
(#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA), subtle paper grain, calm cinematic
lighting. 16:9, 1920x1080. No text, no letters, no logos, no real people or faces.
```
Negative 추가: `keyboard, keycaps, scrabble tiles, chess board, periodic table, calculator`
텍스트 오버레이: 자모 28자(모션 레이어: 흰 24 + 회색 4 `ㆁ ㅿ ㆆ ㆍ`) / `17 consonants + 11 vowels = 28` → `today: 24` → 회색 4자 옆 `no longer used`.
모션 메모: 자모 한 글자씩 획 순서대로 그려짐(스트로크 리빌, 0.25초/자). 24자 먼저, 4자는 1초 늦게 회색으로 켜진 뒤 60% 불투명도로 흐려짐(사라지지 않고 남음, S12 복귀용). 격자 배치는 `make_thumbs.py`의 `JAMO_28` 순서와 동일.
9:16 메모: 격자를 4열 7행으로 재배열해 y 420~1500에 배치. 훅 문구 `4 letters vanished` y 300~400. 숏폼 3번(S04+S12) 첫 컷.

## S05 1444: "Only barbarians have their own script" (2:40~3:40)
요약: 두루마리 상소문(글자 흐림). 지도 위 몽골·여진·일본·티베트 영역 표시와 일반화한 문자 아이콘(모션 레이어). 인물 얼굴 없음.
```
A long scroll of cream paper partly unrolled across a dark wooden table, lit from one side,
its surface covered with soft out-of-focus vertical ink columns that cannot be read. Beside it
an ink stone and a brush. Behind the table, a plain dark backdrop with a faint warm glow in the
upper half, left empty for an animated map layer. No figures, no hands. Scroll in the lower
third, running from lower left to the right. Flat editorial illustration, bold clean ink
outlines, warm limited palette of night navy (#1B1F2A), chili red (#C8102E), pot yellow
(#FFD23F) and cream paper (#F7F3EA), subtle paper grain, calm cinematic lighting. 16:9,
1920x1080. No text, no letters, no logos, no real people or faces.
```
Negative 추가: `readable Chinese characters, legible script, map, borders, flags, soldiers, horses, weapons, ethnic costume, caricature`
텍스트 오버레이: `1444 · petition` → `"Mongols · Jurchens · Japanese · Tibetans"`(따옴표 유지: 상소문 표현 인용) → `"only barbarians"`(따옴표 유지).
모션 메모: 상단 빈 영역에 Natural Earth 기반 동아시아 윤곽(퍼블릭 도메인, 국경 없음)이 저대비로 등장, 네 영역이 같은 색·같은 크기 톤으로 차례로 하이라이트(우열 암시 없음). 각 영역 위 문자 아이콘은 특정 문자를 베끼지 않은 **일반화한 획 3~4개**. 현대 지도 표기·국기 금지.
9:16 메모: 두루마리를 하단(y 1100~1450), 지도 레이어를 중앙(y 420~1100)에. 숏폼 2번(S05) 단독 컷. 네이티브 생성 권장.

## S06 1504: The ban (3:40~4:42)
요약: S01 돌담·벽서로 복귀 → 종이가 찢겨 떨어짐 → 3단어 지워짐 → 달력 페이지 위 자모 재등장. 왕은 실루엣.
```
Plate A (same wall as S01, daytime): the same dark stone wall of a Korean walled city under
a flat grey-blue daylight, three pasted sheets of cream paper with unreadable soft ink marks,
one sheet already torn and hanging by a corner, a few paper scraps on the ground. No people.
Plate B: a single page of an old Korean almanac style calendar, a tall sheet of cream paper
with an empty ruled grid of thin ink lines and no characters, lying on a dark wooden table,
warm lamp light from the left. Both 16:9. Flat editorial illustration, bold clean ink
outlines, warm limited palette of night navy (#1B1F2A), chili red (#C8102E), pot yellow
(#FFD23F) and cream paper (#F7F3EA), subtle paper grain, calm cinematic lighting. 16:9,
1920x1080. No text, no letters, no logos, no real people or faces.
```
Negative 추가: `readable letters, legible handwriting, crowd, soldiers, executioner, sword, blood, fire, throne room, king portrait, actor`
텍스트 오버레이: `July 19, 1504` → `no learning · no teaching · no using`(세 구가 차례로 red 취소선으로 지워짐) → `December 1504 · calendar in Hangul` → `about 5 months`. 처벌 조항(참수 등)은 자막에 넣지 않음.
모션 메모: Plate A에서 종이가 찢겨 떨어지는 모션(마스크 애니메이션, 2초) → 3단어 등장·삭제 → Plate B로 크로스페이드, 빈 달력 격자 위에 자모가 흰색으로 다시 그려짐(스트로크 리빌). 왕(연산군)이 필요하면 Plate A 왼쪽에 뒷모습 실루엣 레이어만, 얼굴·표정 없음. 인물 평가(폭군 등) 비주얼 금지.
9:16 메모: Plate A 종이 3장을 중앙에, 삭제 3단어는 y 300~420에. 숏폼 1번(S01+S06) 두 번째 컷. 네이티브 생성 권장.

## S07 Surviving as "vernacular writing" (4:42~5:26)
요약: 상단은 한자가 빽빽한 공문서(실제 문장 아님), 하단은 한글 편지·불경 두루마리. 두 층 분리 구도. 인물은 실루엣.
```
A split composition in one frame. Upper half: a formal dark lacquered desk in a dim official
hall, with stacked documents of cream paper whose surfaces show dense, soft, out-of-focus
square-shaped ink marks that cannot be read, cold blue-grey light. Lower half: a warm humble
room with a low table, a short folded letter on cream paper and a small unrolled Buddhist
style scroll, both carrying only soft unreadable round and straight ink marks, warm yellow
lamp light. A thin horizontal band of night navy divides the two halves. At the far left of
the lower half, one seated figure seen only from behind as a flat featureless silhouette in a
plain robe, face never visible. Flat editorial illustration, bold clean ink outlines, warm
limited palette of night navy (#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream
paper (#F7F3EA), subtle paper grain, calm cinematic lighting. 16:9, 1920x1080. No text, no
letters, no logos, no real people or faces.
```
Negative 추가: `readable Chinese characters, readable Korean letters, Buddha statue, temple roof, monk face, woman face, portrait`
텍스트 오버레이: `언문 · eonmun · 'vernacular writing'` / `court: Chinese characters ↑` / `everyday life: Hangul ↓`.
모션 메모: 상·하 두 층이 각각 다른 속도로 느리게 패닝(상단 좌→우, 하단 우→좌). 문해율 숫자 어떤 것도 오버레이 금지.
9:16 메모: 상·하 분할이 세로 포맷에 그대로 맞음(상단 y 260~960, 하단 y 960~1440). 숏폼 비후보.

## S08 1894: "National script" (5:26~5:58)
요약: 공문서 위에 한글 먼저, 한자가 작게 뒤따르는 레이아웃 전환. "언문"이 "국문"으로 바뀌는 타이포 모션(모션 레이어).
```
A single large official document of cream paper lying flat on a dark desk, photographed from
straight above, with a red wax seal mark in one corner that is a plain round shape with no
characters. The paper surface is clean and empty except for faint ruled lines, ready for
animated type. Daylight from the left, long soft shadows, a brush and ink stone at the edge
of the frame. Flat editorial illustration, bold clean ink outlines, warm limited palette of
night navy (#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA),
subtle paper grain, calm cinematic lighting. 16:9, 1920x1080. No text, no letters, no logos,
no real people or faces.
```
Negative 추가: `readable seal characters, national emblem, flag, coat of arms, government logo, signature`
텍스트 오버레이: `November 1894` → `국문 · gungmun · 'national script'` → `1446 → 1894: 448 years`. 공문서 본문은 자모 24자를 무작위 배열한 **읽히지 않는 더미 열**(모션 레이어)로만 채운다. 실제 칙령 문장 생성 금지.
모션 메모: S07의 `언문` 텍스트가 `국문`으로 모프(0.8초). 더미 열이 한자 모양 자리에서 한글 자리로 재배열되고 한자 자리는 작게 축소. 정치 배경(외세·전쟁) 비주얼 없음.
9:16 메모: 문서를 세로로 세워 중앙 1:1에. 숏폼 비후보.

## S09 A new name and a first holiday (5:58~6:34)
요약: "한글" 두 글자 획 순서 그리기와 "한 = great / 글 = letters" 분해. "가 갸 거 겨" 어린이 글씨체 등장. 전부 모션 레이어.
```
A warm, bright background plate: a sheet of cream paper filling the frame, lit softly from
the upper left, with a few plain wooden pencils and one brush resting along the bottom edge,
and a small empty wooden desk corner visible at lower right. Gentle paper grain, very light
yellow glow at the centre, nothing drawn on the paper. Flat editorial illustration, bold clean
ink outlines, warm limited palette of night navy (#1B1F2A), chili red (#C8102E), pot yellow
(#FFD23F) and cream paper (#F7F3EA), subtle paper grain, calm cinematic lighting. 16:9,
1920x1080. No text, no letters, no logos, no real people or faces.
```
Negative 추가: `school logo, flag, children, hands, faces, classroom photo, branded pencils`
텍스트 오버레이: `around 1912 · 한글` → `한 great + 글 letters` → `1926 · 가갸날 Gagya Day` → `→ 한글날 Hangul Day`. `가 갸 거 겨`는 둥근 손글씨풍 OFL 폰트(설치 후 라이선스 확인)로 작게.
모션 메모: `한글` 두 글자 스트로크 리빌(ink, 1.5초) → 두 글자가 좌우로 벌어지며 영문 뜻이 아래 등장 → `가 갸 거 겨` 네 음절이 한 글자씩 톡톡 등장. 식민기 관련 비주얼 없음(F11 보류). 주시경 초상 없음.
9:16 메모: 종이 플레이트가 세로에 맞음. `한글`은 y 600~900, 분해 라벨 y 950~1100. 숏폼 비후보.

## S10 The lost manual and the date on the calendar (6:34~7:32)
요약: 지도에서 안동 점등 → 오래된 책이 열림(자체 일러스트) → 책 마지막 장에서 "구월 상순" 텍스트가 달력 "10월 9일" 칸으로 이동. 숏폼 2개 후보 원본.
```
Plate A: a dark wooden table with a single old bound book, closed, its cover of worn kraft
brown paper with no title and no markings, a loose thread binding on the spine, lit by one
warm lamp, a dark attic-like room behind; the book sits in the right half. Plate B: the same
book now open, two cream pages with only soft out-of-focus ink columns that cannot be read, a
modern wall calendar page of plain white paper with an empty grid pinned on the wall behind
and to the right, its single highlighted cell left blank. Both 16:9, same lighting. Flat
editorial illustration, bold clean ink outlines, warm limited palette of night navy
(#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA), subtle paper
grain, calm cinematic lighting. 16:9, 1920x1080. No text, no letters, no logos, no real
people or faces.
```
Negative 추가: `photograph of a real museum manuscript, museum display case, museum logo, UNESCO emblem, national treasure plaque, readable characters, hands, collector portrait`
텍스트 오버레이: `1940 · Andong` → `National Treasure No. 70 (1962)` → `UNESCO Memory of the World (1997)`(엠블럼 없이 글자만) → `9th lunar month, first ten days → October 9` → `fixed since 1946`. 책 마지막 장 위에 한글 `구월 상순`(Black Han Sans)이 떠올라 달력 칸으로 이동.
모션 메모: Plate A 위에 Natural Earth 한반도 윤곽(퍼블릭 도메인, 국경선 없이 남부 윤곽만) 저대비 레이어, 안동 위치에 red 점 하나 → Plate A→B 크로스페이드(책 열림) → `구월 상순` 텍스트가 책에서 달력 빈 칸으로 날아가 `9`로 바뀌고 red 링 1개. 전형필·정인지 초상 없음. 환산 방식 세부 자막 없음.
9:16 메모: 책을 하단(y 900~1450), 달력을 상단(y 420~900)에 세로 배치. 숏폼 4번(1940 발견)·5번(10/9가 된 이유) 공용 컷. 네이티브 생성 권장.

## S11 The holiday that came and went, and 2026 (7:32~8:30)
요약: 달력 아이콘 10/9 켜짐(1949)→꺼짐(1991)→켜짐(2013) → 광화문광장 풍경(동상 비포함, 바닥·현수막·군중 실루엣만) → 러닝 코스 지도 모션.
```
A wide public plaza in a modern Korean city in the morning, seen from a high angle: long
granite paving, a shallow water channel, rows of plain blank banners on poles with no
lettering, a few plain white event tents, and small groups of people shown only as tiny flat
featureless silhouettes seen from above and behind, no faces. Low hills and modern buildings
in the far background, no statue, no palace gate, no landmark architecture reproduced in
detail, no flags. Soft autumn light. Flat editorial illustration, bold clean ink outlines,
warm limited palette of night navy (#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and
cream paper (#F7F3EA), subtle paper grain, calm cinematic lighting. 16:9, 1920x1080. No text,
no letters, no logos, no real people or faces.
```
Negative 추가: `statue, bronze king, Gwanghwamun gate, palace roof detail, national flag, political banner, sponsor logos, race bibs with numbers, faces, close-up people`
텍스트 오버레이: `public holiday 1949 → dropped 1991 → restored 2013` → `2026: 580th · 100th · 100th (Braille)` → `Oct 9 · Gwanghwamun Square` → `Hangeul Run · 10.9 km`. 전시명은 넣지 않음.
모션 메모: 달력 아이콘(단색 모션 그래픽) `10/9` 켜짐·꺼짐·켜짐 각 0.6초 → 광장 플레이트 → 광장 위에 러닝 코스 선(단순 폐곡선, 실제 지도 아님)이 그려지며 `10.9 km`. 10/9 이후 업로드면 자막 시제 과거형.
9:16 메모: 광장을 중앙 1:1, 달력 아이콘·연도는 상단 y 300~420. 숏폼 비후보.

## S12 Try the twenty-four yourself (affiliate) (8:30~9:41)
요약: S04 격자 재등장 → 회색 4자 사라지고 24자만 남음 → 책상 위 무지 워크북과 붓펜 일러스트 → 손이 "한글"을 쓰는 클로즈업(손만). 상품 사진 없음.
```
Plate A: a bright desk scene from a three-quarter angle: a plain closed workbook with a blank
cream cover, no title, no logo, no printed pattern, a slightly thicker spiral binding on the
left, and three plain brush pens with unmarked dark barrels and no caps branding, laid beside
it on a light wooden desk, soft daylight from a window at the left, a small ceramic cup
holding two more pens. Plate B: close-up of the same desk, a sheet of cream practice paper
with faint ruled squares and no writing on it, one hand holding a plain brush pen poised above
the paper, shown from the wrist down only, no face, no body, no jewellery, generic skin tone,
no sleeve pattern. Both 16:9. Flat editorial illustration, bold clean ink outlines, warm
limited palette of night navy (#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream
paper (#F7F3EA), subtle paper grain, calm cinematic lighting. 16:9, 1920x1080. No text, no
letters, no logos, no real people or faces.
```
Negative 추가: `brand name on pen, product label, barcode, price tag, book cover art, publisher logo, printed title, face, arm above the wrist, watch, nail polish, shopping cart, Amazon smile logo`
텍스트 오버레이: 구간 전체 하단 고정 바 `Affiliate links · this channel earns a commission`(Pretendard 40px 이상, 문구 한 글자도 변경 금지) / 상단 `24 letters` → `workbook · brush pen set`. 가격 없음. "authentic / best / traditional" 같은 수식 없음. Plate B 종이 위에 `한글` 두 글자가 스트로크 리빌로 그려짐(모션 레이어, 손 움직임과 동기).
모션 메모: S04 격자 재등장(동일 좌표) → 회색 4자가 0.8초간 페이드아웃 → 24자가 모여 작아지며 Plate A로 전환 → Plate B 클로즈업. 효능·학습 보장 문구 금지. marketing.md가 Amazon Associates로 확정하면 고지 바 문장은 marketer 지정 그대로 추가.
9:16 메모: 격자 4열 7행 → 워크북·붓펜을 중앙 1:1에, 고지 바는 y 1300~1400(안전 영역 안). 숏폼 3번(S04+S12) 두 번째 컷. 네이티브 생성 권장.

## S13 Wrap-up and CTA (9:41~10:36)
요약: S02 타임라인 회상 → 24자 자모가 "한글" 두 글자로 모이는 모션 → 엔드카드. 전부 모션 레이어 위주.
```
A calm closing background plate: deep night navy field with a soft warm glow rising from the
lower centre like a lamp just out of frame, faint paper grain, a thin horizontal band of cream
paper near the top third echoing an unrolled scroll, and nothing else. Generous empty space
in the lower half for end screen elements. Flat editorial illustration, bold clean ink
outlines, warm limited palette of night navy (#1B1F2A), chili red (#C8102E), pot yellow
(#FFD23F) and cream paper (#F7F3EA), subtle paper grain, calm cinematic lighting. 16:9,
1920x1080. No text, no letters, no logos, no real people or faces.
```
Negative 추가: `play button, subscribe button, bell icon, YouTube UI, social media icons, QR code`
텍스트 오버레이: `Links in the description` / `580 years · 100th Hangul Day` / 마지막 줄 `AI-generated voice & images · human-written, fact-checked script`(한 글자도 변경 금지).
모션 메모: 상단 띠에 S02 타임라인 5점 회상(1446→2026, 각 0.3초) → 24자 자모가 화면 중앙으로 모여 `한글` 두 글자로 합쳐짐(모프, 2초) → 하단 절반은 YouTube 최종 화면 요소 자리로 비움. 댓글 질문 카드는 글자 쓰기 질문(구매 유도 아님).
9:16 메모: 숏폼에서는 `한글` 합체 모션만 중앙 1:1에 쓰고 엔드카드 영역은 쓰지 않음. 숏폼 비후보.

---

## 숏폼 5개 컷 매핑(script.en.md 메타 "숏폼 후보" 기준)
| 숏폼 | 원본 장면 | 첫 1초 훅 문구(4단어 이하) | 네이티브 9:16 생성 |
|---|---|---|---|
| 1 | S01 + S06 | `Three sheets. One ban.` | S01·S06 Plate A |
| 2 | S05 | `"Only barbarians…"` | S05 |
| 3 | S04 + S12 | `4 letters vanished` | S04(격자 배경)·S12 Plate A |
| 4 | S10 | `Lost, then found: 1940` (대본은 "for centuries"만 말하므로 햇수 숫자 금지) | S10 Plate A·B |
| 5 | S10 | `Why October 9?` | S10 Plate B |

---

## 생성 기록 (생성 후 채움)
| 장면 | 플레이트 | 모델 | 날짜 | 시드 | 해상도 | 라이선스/이용약관 확인 | 검수자 | 비고 |
|---|---|---|---|---|---|---|---|---|
| S01 | - | | | | | | | |
| S02 | - | | | | | | | |
| S03 | - | | | | | | | |
| S04 | - | | | | | | | |
| S05 | - | | | | | | | |
| S06 | A / B | | | | | | | |
| S07 | - | | | | | | | |
| S08 | - | | | | | | | |
| S09 | - | | | | | | | |
| S10 | A / B | | | | | | | |
| S11 | - | | | | | | | |
| S12 | A / B | | | | | | | |
| S13 | - | | | | | | | |
