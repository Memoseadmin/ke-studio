# 세트 11 "필사 입문" 4판 — AI 플레이트 프롬프트 팩 (집 PC ComfyUI용)

> **v4.1 변경 이력(2026-10-02, 대표 결정 V1·V2 반영)**: V2 AI 플레이트 스타일 = ⓒ 한지 콜라주(찢은 한지 결·겹침·먹 번짐·낮은 채도) — §0 스타일 꼬리 문자열만 교체, 프롬프트 ID·시드·저장 경로·절차는 그대로.
> V1 면적 비율 원화:AI:사진:코드 = 35:15:25:25 — 플레이트는 "바탕"만. 꼬리에 `background plate only, subject small or absent, wide empty negative space, empty lower third` 추가, 네거티브에 BENCHMARK-visual §4-3 SDXL 항목 추가.
> v4 원 스타일 문자열(기록용, 사용 안 함): `flat editorial illustration in Korean minhwa folk-painting manner, bold clean ink outlines, warm limited palette of ink brown (#3B2F2A), celadon green (#7FA99B), muted vermilion (#B5523B) and hanji cream paper (#F3ECDD), visible hanji mulberry paper fibres, subtle paper grain, calm soft daylight, generous empty space, quiet still-life mood`

> 2026-10-02 designer. 대표 결정: 집 PC(ComfyUI)에서 AI 플레이트를 먼저 만든 뒤 4판 렌더. 작업 순서는 `plates/README-homepc.md`.
> **플레이트 = 배경만.** 사물(책·붓·시계)은 CC0 원화 크롭, 글자·숫자·원고지·달력·막대는 코드 그래픽이 맡는다. 플레이트에는 글자·인물·로고가 0이어야 한다.
> **1장(윤동주)은 AI로 인물을 그리지 않는다**(디자인 시스템 §6-1 실존 인물 금지). 1장 플레이트는 사진·원화를 얹을 **빈 배경**만 만든다.

## 0. 공통 규칙

**크기** (카드 3:4 1080x1440, design-system §9-6 C 틀)

| 용도 | 최종 영역 | 생성 크기(64배수, 비율 맞춤) | 후처리 |
|---|---|---|---|
| 본문 2~7장 그림 영역(위 62%) | 1080x893 | **1536x1280** (1.2:1) | 1080x900으로 축소 → 위·아래 균등 크롭 893 |
| 표지 1장 풀블리드 | 1080x1440 | **1152x1536** (3:4) | 1080x1440으로 축소 |
| 마지막 8장 그림 영역(위 55%) | 1080x792 | **1536x1128** (≈1.36:1) | 1080x793 축소 → 792 크롭 |

**스타일 꼬리 문자열** (v4.1 · 대표 결정 V2 ⓒ 한지 콜라주. §5 공통 문자열 구조를 따르되 hex 코드는 모델이 해석 못 해 색 이름만 씀(BENCHMARK-visual §4-2). 실존 작가 이름은 넣지 않는다):
```
torn layered hanji collage, overlapping mulberry paper pieces with deckled edges and visible fibres, faint paper-relief shadows, soft ink bleed, low-saturation palette of cream, warm ink brown, celadon and faded persimmon dyed paper, matte, background plate only, subject small or absent, wide empty negative space, empty lower third
```

**네거티브** (§5 "항상 포함" 원문 그대로 + §6·§10 추가분 + v4.1 BENCHMARK-visual §4-3 SDXL 추가분):
```
text, letters, numbers, captions, logos, brand names, trademarks, product packaging graphics, printed labels, readable signage, real people, faces, celebrity likeness, copyrighted characters, mascots, film or TV stills, posters, watermarks, UI elements, human figures, hands, silhouettes of people, calligraphy, hanja characters, seal stamps, signatures, tigers, magpies, red cross on white, flags, photorealistic, 3d render, glossy, copy of an existing painting, plastic, neon, oversaturated, vector clip art, thick cartoon outlines, anime, pseudo-hanja, gold sparkle, HDR, harsh shadows, cluttered lower area, picture frame
```
- 네거티브 칸이 약한 모델(Z-Image-Turbo는 CFG 1이라 네거티브 효과가 거의 없음 — 추정)은 프롬프트 끝에 §5 문장을 그대로 붙인다: `No text, no logos, no brand packaging, no real people or faces.` 그 뒤에 v4.1 바탕 지시 `Empty lower third, subject small or absent.`를 한 줄 더 붙인다.

**모델·설정 권장** (`docs/LOCAL_GPU_PROMPT.md`: 상업 사용 허용 체크포인트만, 모델명은 GEN.json 필수)

| 1순위 | 2순위(대체) |
|---|---|
| Z-Image-Turbo (Tongyi-MAI, Apache-2.0) — 3판 `plates/prompts.json`과 같은 모델 · steps 8 · CFG 1.0 · sampler euler · scheduler simple | SDXL base 1.0 (CreativeML Open RAIL++-M) · steps 30 · CFG 6.0 · dpmpp_2m karras |

- ComfyUI에서 Z-Image 노드를 못 쓰면 2순위로. LoRA는 쓰지 않는다(라이선스 확인 부담·화풍 복제 위험).
- **시드**: 3판 규칙 그대로 `seed = MMDD*1000 + card*10 + variant` (세트 날짜 10/19). 프롬프트마다 기본 시드 + 3개(+1·+2·+3) = **4장 생성 → 사람이 1장 고름**. 고른 시드를 GEN.json `picked`에 기록.
- 파일명: `plates/v4/P{장 2자리}{변형 a|b}-s{시드}.png` (예 `plates/v4/P02a-s1019020.png`). 원본 PNG는 그대로 커밋(영상·오디오가 아니므로 허용). 편집·크롭은 클라우드 세션이 한다.

**생성 후 사람 검수 체크(1장이라도 걸리면 다른 시드)**: 글자·숫자처럼 보이는 획 0 / 사람·손·얼굴 0 / 로고·상표 0 / 호랑이·까치 0 / 특정 원화를 그대로 베낀 구도 아님 / 아래쪽 30%가 비어 있어 원화·코드 그래픽을 얹을 자리 있음 / (v4.1) 벡터 클립아트·플랫 일러스트처럼 보이지 않고 종이 결이 보임 / 주제 사물이 화면의 1/4을 넘지 않음.

---

## 1. 장별 프롬프트 (10개)

### P01a — 1장 표지 · 별 헤는 밤의 빈 하늘 (윤동주 사진·원화 뒤 배경)
- 콘셉트: 「서시」·「별 헤는 밤」을 떠올리게 하는 별 뜬 남색 밤하늘과 한지 지평선. 인물·건물 없음. 가운데에 사진 액자 자리를 비운다.
- 프롬프트: `Empty night sky full of small scattered stars above a low horizon of soft rolling hills, gentle wind lines drawn as thin ink curves, the centre of the image left open and calm as negative space, no buildings, no people. ` + 스타일 꼬리 + `, deep indigo night variant of the palette`
- 크기 1152x1536 · 시드 1019010~013 · 용도: 풀블리드 배경. 윤동주 사진(PHOTOS-yun.md)은 한지 매트 액자로 가운데 위에 얹고, 원화가 대신이면 책가도 한 폭을 액자에.
- ⚠ 사진을 플레이트에 "합성"하지 않는다(사진 픽셀 불변, 액자로 겹쳐 놓기만). §9-2 내용 변형 금지와 같은 취지.

### P01b — 1장 표지 대안 · 빈 서안(書案) 위 한지 벽
- 콘셉트: 사진 대신 원화를 쓸 때 쓰는 차분한 배경. 비어 있는 낮은 서안, 뒤는 한지 바른 벽, 창살 그림자 한 줄.
- 프롬프트: `A plain hanji papered wall with a single soft lattice-window shadow falling diagonally, a low empty wooden writing table at the bottom edge, nothing on the table, wide empty upper area. ` + 스타일 꼬리
- 크기 1152x1536 · 시드 1019014~017 · 용도: 풀블리드 배경(하단 40% 그라데이션이 서안 위를 덮는다).

### P02a — 2장 판매 +692.8% · 끝없이 이어지는 빈 책장
- 콘셉트: 서점 매대 실사 대신 "책이 많이 팔렸다"를 민화 책장 리듬으로. 책등은 무지(글자 없음).
- 프롬프트: `Rows of plain cloth-bound book spines with no titles stacked on simple wooden shelves, receding into soft depth, repeating rhythm, left half denser and right half lighter to leave room for a chart. ` + 스타일 꼬리
- 크기 1536x1280 · 시드 1019020~023 · 용도: 배경. 막대 그래프(1 : 7.928)는 코드, 원화 책갑 크롭은 왼쪽 패널.

### P03a — 3장 준비물은 셋 · 빈 책상 윗면(탑뷰)
- 콘셉트: 노트·펜·책 세 원화 크롭을 올려 둘 "자리". 3판 진단(자리가 먼저) 그대로.
- 프롬프트: `Top-down view of an empty low wooden desk surface covered with a sheet of hanji, faint wood grain at the edges, soft morning light from the upper left, completely empty surface. ` + 스타일 꼬리
- 크기 1536x1280 · 시드 1019030~033 · 용도: 배경. 원화 크롭 3개(붓 필통·책갑·연적)는 찢김 테두리 패널로 위에.

### P04a — 4장 첫 줄은 밑줄에서 · 펼친 빈 책
- 콘셉트: 펼친 책 두 쪽, 글자 대신 빈 지면. 원고지·밑줄·「서시」 넉 줄은 코드가 얹는다.
- 프롬프트: `An open old Korean thread-bound book lying flat, both pages blank cream paper with no writing, soft page curl and gentle shadow in the gutter, seen slightly from above. ` + 스타일 꼬리
- 크기 1536x1280 · 시드 1019040~043 · 용도: 배경(코드 원고지 쪽지 아래 깔림).

### P04b — 4장 대안 · 책 더미 옆 빈 원고 자리
- 프롬프트: `A small stack of plain closed books on the left, a large empty sheet of cream paper on the right with no grid and no writing, quiet still life on a wooden floor. ` + 스타일 꼬리
- 크기 1536x1280 · 시드 1019044~047 · 용도: P04a가 글자처럼 보이는 획을 계속 만들면 이것으로.

### P05a — 5장 10분, 같은 시각 · 창살 사이 아침 햇살
- 콘셉트: "같은 시각"을 매일 같은 각도로 드는 햇살로. 시계는 Met 원화 자명종 크롭이 맡는다.
- 프롬프트: `Morning sunlight slanting through a traditional Korean lattice window onto a wooden maru floor, long geometric light pattern, warm and quiet, nothing else in the room. ` + 스타일 꼬리
- 크기 1536x1280 · 시드 1019050~053 · 용도: 배경. 오른쪽에 코드 달력(1~18일 체크), 왼쪽에 자명종 원화.

### P06a — 6장 정자로, 흘림으로 · 먹이 번지는 벼루 주변 결
- 콘셉트: 서체 두 가지를 흉내 내지 않고(가짜 손글씨 금지, 3판 브리프) 먹의 농담만. 정자·흘림 견본은 코드 서체로.
- 프롬프트: `Abstract ink wash texture spreading on hanji, one area of crisp dense black ink and one area of soft diluted grey ink flowing outward, no strokes that resemble characters, minimal composition. ` + 스타일 꼬리
- 크기 1536x1280 · 시드 1019060~063 · 용도: 배경(원화 벼루 크롭 + 코드 견본 두 줄).
- ⚠ 이 장이 글자 닮은 획이 가장 잘 나오는 위험 장. 4장 중 획이 글자처럼 읽히면 전부 폐기.

### P07a — 7장 날짜와 책 제목 · 문갑 칸에 꽂힌 무지 노트
- 콘셉트: 노트가 쌓여 "나만의 문장집"이 되는 장면. 표지는 무지.
- 프롬프트: `A row of plain notebooks with blank kraft covers standing upright in a wooden stationery cabinet compartment, slightly uneven heights, one notebook pulled out a little, no labels. ` + 스타일 꼬리
- 크기 1536x1280 · 시드 1019070~073 · 용도: 배경(코드 기록 칸 두 줄 + Met 문갑 원화).

### P08a — 8장 오늘 옮길 한 줄은 · 저녁 한지 창
- 콘셉트: 끝맺음. 1장 밤하늘과 이어지는 해 질 녘 창. 원화 전경을 쓰면 생략 가능(선택).
- 프롬프트: `A hanji paper window glowing with soft dusk light, faint first stars visible through a slightly open lattice panel, calm closing mood, wide empty lower area. ` + 스타일 꼬리
- 크기 1536x1128 · 시드 1019080~083 · 용도: 선택 배경. 원화 전경(클리블랜드 7폭)이 1순위.

---

## 2. 요약

| 장 | 프롬프트 | 생성 크기 | 시드 | 장수 |
|---|---|---|---|---|
| 1 | P01a · P01b | 1152x1536 | 1019010~017 | 8 |
| 2 | P02a | 1536x1280 | 1019020~023 | 4 |
| 3 | P03a | 1536x1280 | 1019030~033 | 4 |
| 4 | P04a · P04b | 1536x1280 | 1019040~047 | 8 |
| 5 | P05a | 1536x1280 | 1019050~053 | 4 |
| 6 | P06a | 1536x1280 | 1019060~063 | 4 |
| 7 | P07a | 1536x1280 | 1019070~073 | 4 |
| 8 | P08a (선택) | 1536x1128 | 1019080~083 | 4 |
| 합계 | **10개** | | | **40장** |

- 출처 줄: AI 플레이트는 출처 줄(§8-4)에 넣지 않는다(§9-5: 카드·캡션 AI 라벨 없음). 생성 기록은 `plates/GEN-v4.json`에만 남긴다. ⚠ legal 열린 항목(§9-5): 플레이트가 실제로 카드에 들어가면 "사진·원화는 AI 생성물이 아님" 전제가 바뀌므로 4판 PR 전에 legal-reviewer 재점검 필요.
