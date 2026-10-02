# EP001 장면별 이미지 프롬프트 (S01~S12)

직원: designer / 기준일: 2026-10-01 / 입력: `script.en.md` S01~S12 화면 메모, `research.md` §5 / 규칙: `design-system.md` v1.0
상태: **prompt-ready**, 이미지 미생성(생성 API 키 없음). 생성하면 장면별로 모델·날짜·시드를 이 파일 하단에 기록.

공통 원칙
- 모든 플레이트는 **글자 없는 그림**. 작품명·대사·숫자·출처·고지 문구는 편집에서 오버레이(Pretendard/Anton).
- 차트(S04·S09·S10)와 3칸 타이틀 카드(S02)는 AI로 그리지 않고 모션그래픽으로 만든다. 아래 프롬프트는 그 뒤에 깔 배경 플레이트.
- 16:9 원본은 1920x1080 이상(숏폼 후보는 3840x2160 권장). 숏폼 후보 장면(S03·S05·S06·S07·S08)은 9:16 네이티브 재생성 권장: 프롬프트의 "16:9, 1920x1080"을 "vertical 9:16, 1080x1920, main subject in the middle third"로 바꾼다.
- 9:16 크롭 메모의 좌표는 1080x1920 기준. 문구 안전 영역 x 60~940, y 260~1440(`design-system.md` §4).

공통 네거티브(모든 장면에 넣고, 장면별 추가분을 뒤에 붙인다)
```
text, letters, numbers, captions, subtitles, logos, brand names, trademarks, product packaging
graphics, printed labels, readable signage, real people, faces, celebrity likeness, copyrighted
characters, mascots, film or TV stills, posters, watermarks, UI elements
```

---

## S01 Hook (0:00~0:16)
요약: 밤의 작은 부엌, 가스레인지 위 냄비에서 김이 오르고 문가에 뒷모습 실루엣 둘. "라면 먹을래요?" 질문으로 연다.
```
A small Korean apartment kitchen at night, a plain yellow aluminum ramyeon pot steaming on a
two-burner gas stove, warm light from a single pendant lamp, a window with soft city lights.
In the doorway at the far left, two figures seen only from behind as flat dark featureless
silhouettes in generic everyday clothes, faces never visible, not resembling any actor. Pot
placed at about 62% of the frame width. Leave the lower third calm for a subtitle overlay.
Flat editorial illustration, bold clean ink outlines, warm limited palette of night navy
(#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA), subtle paper
grain, soft white steam, calm cinematic lighting. 16:9, 1920x1080. No text, no logos, no brand
packaging, no real people or faces.
```
Negative 추가: `profile view, recognizable hairstyles, couple embracing, romantic pose, film still recreation`
9:16 메모: 냄비 중심(x 62%)으로 608px 폭 크롭. 실루엣은 잘려도 됨(얼굴 없는 버전이 더 안전). 훅 문구 "라면 먹을래요?" / "Do you want to eat some ramyeon?"은 y 300~560.

## S02 Roadmap (0:16~0:45)
요약: 3칸 타이틀 카드(2001 / 2019 / Netflix, 글자만) 뒤 지도 위로 점선이 편의점·수출·40주년으로 뻗는다.
```
A simplified flat map plate of the Korean peninsula and surrounding sea on cream paper, no
labels and no borders drawn, with three dotted routes leading out to three small icons: a
generic corner convenience store with a blank awning, a container ship carrying plain unmarked
containers, and a small plain cake with lit candles. Generous empty space across the top
40% for animated title cards. Flat editorial illustration, bold clean ink outlines, warm
limited palette of night navy (#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream
paper (#F7F3EA), subtle paper grain, calm lighting. 16:9, 1920x1080. No text, no logos, no
brand packaging, no real people or faces.
```
Negative 추가: `place names, flags, country labels, store brand colors, streaming service logos, movie posters`
메모: 지도 윤곽은 AI 대신 Natural Earth(퍼블릭 도메인) 벡터로 그리는 것을 우선. "Netflix"는 텍스트로만, 로고 금지.
9:16 메모: 크롭하지 않고 재배치. 3칸 카드를 세로로 쌓기(y 300~1400), 지도는 반도 중심(x 50%) 크롭을 아래에 깐다.

## S03 Scene one: One Fine Spring Day (0:45~1:49)
요약: 봄 저녁 골목 → 현관 불빛 → 냄비. 2001년 대사가 "초대"의 뜻을 얻게 된 이야기. 인물 없음.
```
A quiet residential side street in a small Korean town in early spring at dusk, a modest
low-rise apartment building, a single warm porch light glowing above an entrance door left
slightly open, a few blossoming trees, an empty street with soft long shadows. Porch light at
about 55% of the frame width. Original composition, not based on any film scene. Flat
editorial illustration, bold clean ink outlines, warm limited palette of night navy (#1B1F2A),
chili red (#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA), subtle paper grain,
calm cinematic lighting. 16:9, 1920x1080. No text, no logos, no real people or faces.
```
Negative 추가: `bamboo forest, sound recording microphone, couple, actors, film still recreation`
메모: 냄비 클로즈업은 S01 플레이트 재사용. 작품명·대사·"Announced March 2026" 카드는 텍스트만(배우 사진 금지).
9:16 메모(숏폼 후보): 9:16 네이티브 재생성 권장(현관 불빛 위 3분의 1, 문 중앙). 크롭 시 중심 x 55%. 대사 자막 y 1150~1400, 작품명 y 300~420.

## S04 The shortcut theory (1:49~2:48)
요약: 1인당 79.2개(2024, 베트남 81개에 이은 2위), 주 1.5개. 익숙하니까 설명 없이 통하는 "약어"가 된다.
```
Overhead view of a simple wooden kitchen table: a blank paper week-planner sheet with seven
empty columns and no writing, one full bowl of ramyeon and one half-finished bowl beside it,
a pair of stainless steel chopsticks resting across the half bowl. Objects grouped in the
left 40%; the right 60% is plain table surface for animated bar charts. Flat editorial
illustration, bold clean ink outlines, warm limited palette of night navy (#1B1F2A), chili red
(#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA), subtle paper grain, soft white
steam, calm lighting. 16:9, 1920x1080. No text, no numbers, no logos, no real people or faces.
```
Negative 추가: `dates, numerals on the planner, charts drawn in the image, flags`
메모: 막대 "Vietnam 81 / South Korea 79.2 (2024)", "WINA, via Korea Times", "(79.2 ÷ 52)"는 모션그래픽.
9:16 메모: 그릇 묶음 중심(x 30%) 크롭을 하단(y 1000~1440)에, 막대는 세로 배치로 상단(y 300~900).

## S05 Scene two: Parasite (2:48~3:53)
요약: 무지 봉지 두 개가 한 그릇이 되는 짜파구리, 자막에서 "ram-don"이 태어남. 오스카 직후 GS25 판매 약 60% 증가(텍스트).
```
Two plain unprinted instant noodle packets, one kraft brown and one off-white, tilted toward
each other on the left and right thirds of the frame, above a white ceramic bowl in the lower
center filled with glossy dark black-bean-sauce noodles mixed with thick chewy noodles and a
few flecks of green onion, on a clean cream surface. Keep the lower 25% plain for a subtitle
card overlay. Flat editorial illustration, bold clean ink outlines, warm limited palette of
night navy (#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA),
subtle paper grain, soft white steam, calm lighting. 16:9, 1920x1080. No text, no logos, no
brand packaging, no real people or faces.
```
Negative 추가: `black packets, red or orange packets, steak or beef slices on top, luxury modern house interior, staircase, basement, film still recreation`
메모: "jjapaguri → ram-don" 타이핑, "ramyeon + udon = ram-don", GS25 수치·출처는 오버레이. 상표 표기는 글자로만.
9:16 메모(숏폼 후보): 9:16 네이티브 재생성 권장(봉지 두 개 위, 그릇 가운데). 16:9 중앙 크롭은 봉지가 잘림. 자막 카드 y 1150~1400.

## S06 Scene three: KPop Demon Hunters (3:53~5:01)
요약: 애니메이션 영화 초반의 컵라면 장면 → 한정 6개입 1,000세트, CU 외국인 결제 +185%(라면 +99%, 김밥 +231%).
```
Three plain white paper cups of instant noodles with lids peeled back and steam rising, lined
up on a simple neutral white-and-wood window counter of a small shop at night, warm city
lights softly blurred outside, a pair of chopsticks resting across the middle cup, and one
plain gimbap roll on a paper tray at the side. Flat editorial illustration, bold clean ink
outlines, warm limited palette of night navy (#1B1F2A), chili red (#C8102E), pot yellow
(#FFD23F) and cream paper (#F7F3EA), subtle paper grain, soft white steam, calm cinematic
lighting. 16:9, 1920x1080. No text, no logos, no brand packaging, no characters, no real people
or faces.
```
Negative 추가: `anime girls, idol performers, stage costumes, demons, tiger, magpie, folk-painting tiger motifs, purple or pink neon concert lighting, store brand colors, streaming service logos`
메모: "1,000 sets · pre-order Aug 28, 2025", CU 막대·출처는 모션그래픽. 그룹명은 공식 표기 확인 후 텍스트로만.
9:16 메모(숏폼 후보): 9:16 네이티브 재생성 권장("three cups in a staggered vertical arrangement"). 16:9 중앙 크롭은 컵 1개만 남음. 수치 카드 y 300~700.

## S07 Off script: Han River ramyeon (5:01~5:36)
요약: 대본 없는 장면. 한강 공원 편의점에서 산 라면을 즉석 조리기로 끓여 강가에서 먹는 체험.
```
A riverside park in Seoul at night, a wide calm river reflecting the lights of a long
illuminated bridge in the distance, a plain outdoor folding table in the foreground with a
paper bowl of steaming ramyeon, and beside it a generic unbranded stainless instant noodle
cooking machine (boxy, a hot plate and a water spout, no screen, no labels). Empty park, calm
mood. Flat editorial illustration, bold clean ink outlines, warm limited palette of night navy
(#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA), subtle paper
grain, soft white steam, calm cinematic lighting. 16:9, 1920x1080. No text, no logos, no brand
packaging, no real people or faces.
```
Negative 추가: `store signage, store brand colors, TV show set, camera crew, crowds`
메모: 예능 제목(I Live Alone, Running Man)은 텍스트로만. 실제 매장·방송 화면 금지.
9:16 메모(숏폼 후보): 9:16 네이티브 재생성 권장(다리 불빛 위 3분의 1, 조리기와 그릇 y 900~1440). 크롭 시 중심 x 45%(테이블).

## S08 The Ramyeon Library (5:36~6:08)
요약: 홍대 1호점(2023.12), 200종 이상, 즉석 조리기. 매출의 약 65~68%가 외국인 손님(2024 보도).
```
A floor-to-ceiling store wall of shelves packed with hundreds of plain unprinted instant
noodle packets and cups arranged in neat color blocks of muted pastel, kraft, cream, soft teal
and pale yellow, like a library of noodles, with a wooden library ladder leaning on the
shelves and a row of generic stainless instant cooking machines on a counter in front. Bright,
clean lighting, no people. Flat editorial illustration, bold clean ink outlines, warm limited
palette with pot yellow (#FFD23F) and cream paper (#F7F3EA) accents, subtle paper grain.
16:9, 1920x1080. No text, no logos, no brand packaging, no real people or faces.
```
Negative 추가: `red and black packaging, printed labels, price tags, shelf labels, store brand colors, purple and green store interior`
메모: "Hongdae · Dec 2023 · 200+ kinds", 원그래프 "~65–68% (2024 reports)"는 오버레이.
9:16 메모(숏폼 후보): 진열 벽은 어느 위치로 잘라도 성립. 중심 x 50% 크롭 가능, 고화질 원본(3840) 필요. 수치 카드 y 300~600, 원그래프 y 900~1400.

## S09 The bigger picture (6:08~6:48)
요약: 2025년 라면 수출 첫 15억 달러 돌파(약 +22%), 2026년 상반기 9억 3,539만 달러(+28%, 반기 최대). 인과는 주장하지 않음.
```
A calm wide view of a container port at dusk, stacks of plain unmarked shipping containers in
muted red, yellow and navy, a cargo ship leaving the harbor, and in the foreground a few plain
unprinted cardboard cartons on a pallet. The upper half is open evening sky for animated bar
charts. Flat editorial illustration, bold clean ink outlines, warm limited palette of night
navy (#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA), subtle
paper grain, calm lighting. 16:9, 1920x1080. No text, no logos, no brand packaging, no real
people or faces.
```
Negative 추가: `company names, ship names, flags, maps with borders, arrows, film reels or screens`
메모: 막대·출처("Korea Times / Asia Economy")는 모션그래픽. 영화→수출 인과 화살표 그리지 않음.
9:16 메모: 컨테이너 중심(x 50%) 크롭을 하단(y 1000~1440)에, 막대 2개는 상단 세로 배치(y 300~900).

## S10 Shin Ramyun at 40 (6:48~7:53)
요약: 1986년 10월 출시 → 2026년 10월 40주년. 소고기 장국에서 출발한 국물, 35년 1위, 약 425억 봉. 제품·패키지는 보여주지 않음.
```
A warm still life on a cream table: an earthenware bowl of homestyle Korean beef and radish
soup with green onion beside a plain yellow aluminum pot of noodles. Behind them, a long paper
ribbon timeline with four empty round markers stretches across the frame, ending at a small
plain cake with lit candles. Flat editorial illustration, bold clean ink outlines, warm limited
palette of night navy (#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream paper
(#F7F3EA), subtle paper grain, soft white steam, calm lighting. 16:9, 1920x1080. No text, no
numbers, no logos, no brand packaging, no real people or faces.
```
Negative 추가: `noodle packets, red and black packaging, large East Asian characters, product photography, factory branding, gaming expo booth, video game logos`
메모: 타임라인 "1986 → 1991 → 2025 → 2026", "42.5B packs", "100+ countries", "~40% overseas", "Gamescom 2026 · Cologne"은 전부 텍스트 오버레이. 로제 신제품 이미지 금지.
9:16 메모: 타임라인은 세로로 재배치(y 300~1200). 국그릇+냄비 중심(x 35%) 크롭을 하단(y 1000~1440).

## S11 Bring the scene home (affiliate) (7:53~9:08)
요약: 장면을 집에서 재현하는 최소 준비물 = 양은냄비 1개 + 라면 혼합 멀티팩 1상자. 구간 내내 하단 제휴 고지.
```
Clean catalog-style still life on cream paper: on the left, a plain yellow aluminum ramyeon pot
with its lid set slightly ajar, no embossing and no markings; on the right, an open plain
cardboard box filled with assorted plain unprinted noodle packets in muted colors. Honest,
simple, generous negative space, and the bottom 15% left completely plain for a fixed
disclosure bar. Flat editorial illustration, bold clean ink outlines, warm limited palette of
night navy (#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA),
subtle paper grain, calm lighting. 16:9, 1920x1080. No text, no logos, no brand packaging, no
real people or faces.
```
Negative 추가: `price tags, star ratings, badges, best or authentic labels, health or safety symbols, shopping UI, red and black packets, hands`
메모: 하단 고정 "Affiliate links · I may earn a commission"(marketer 지정 문구 그대로). 가격 표기 없음. 일러스트는 실제 링크 상품과 다를 수 있으니 상품 사진은 라이선스 확인 후에만 교체.
9:16 메모: 세로 재배치(냄비 위 y 300~800, 상자 아래 y 850~1300). 고지 바 y 1320~1420, 하단 UI(480px) 위.

## S12 Wrap-up and CTA (9:08~9:51)
요약: 세 장면 회상(초대 · ram-don · 컵라면) → 댓글 질문 → 엔드카드. 마지막 줄 AI 생성 고지.
```
Three round badge illustrations evenly spaced across the upper half of a cream paper
background: a steaming yellow pot with two pairs of chopsticks, two plain unprinted packets
joining into one bowl, and three plain paper cups with steam. A soft golden noodle line
connects the three badges. The lower half is a plain night navy band kept empty for end-screen
elements. Flat editorial illustration, bold clean ink outlines, warm limited palette of night
navy (#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA), subtle
paper grain, soft white steam. 16:9, 1920x1080. No text, no logos, no brand packaging, no
characters, no real people or faces.
```
Negative 추가: `subscribe buttons, play icons, platform logos, arrows, anime characters`
메모: "Links in the description", "AI-generated voice & images"는 텍스트. 하단 절반은 YouTube 최종 화면 요소 자리.
9:16 메모: 숏폼에서는 배지 3개를 세로로 쌓아(y 300~1400) 댓글 질문 카드로 사용 가능. 엔드카드 영역은 쓰지 않음.

---

## 생성 기록 (생성 후 채움)
| 장면 | 모델 | 날짜 | 시드 | 검수자 | 비고 |
|---|---|---|---|---|---|
