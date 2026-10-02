# 프로필 사진 v4 — AI 생성 프롬프트 3안 (2026-10-02, designer)

대표 결정(2026-10-02): v3 A/B/C(원화 크롭+낙관) 보류. "원화를 바탕으로 한 프로필 사진은 프롬프트를 짜서 자식 세션에서 이미지 생성. 책가도 관련 이름으로 붓글씨 같은 것도 되고."
근거 규칙: design-system v1.1 §5(공통 문자열)·§6(금지)·§8(원화)·§10(호랑이·까치 AI 금지)·§9-5(카드·캡션에 AI 라벨 없이 출처만, 생성 기록은 저장소 내부).

## 0. 공통

| 항목 | 값 |
|---|---|
| 크기 | 1024x1024(정사각). 업로드 전 1080x1080으로 업스케일 |
| 원형 크롭 안전 영역 | 핵심 요소는 **중앙 지름 80%(약 820px) 원 안**. 바깥 20%는 한지 바탕만 |
| 권장 모델 | 1순위 `flux-2-pro`(muapi, docs/OPEN_GENERATIVE_AI_SETUP.md §5 목록) · 2순위 `imagen4` · 3순위 `gpt-image-2`. 같은 프롬프트·시드로 1장씩 |
| 명령(예) | `~/.venvs/muapi/bin/muapi image generate "<프롬프트>" --model flux-2-pro --download render/avatar-v4/` (render/는 커밋 제외. 채택본만 `cardnews/profile/`로 복사) |
| 기록 | 모델·날짜·프롬프트·네거티브·시드·비용(응답 JSON) → `cardnews/profile/avatar-v4-GEN.json` |
| 팔레트 | 먹 #111111 · 한지 #F7F3EA · 낙관 red #C8102E 1점만. 채도 낮게(§8-3 v1.2 톤) |

**공통 스타일 꼬리**(프롬프트 끝): `Korean traditional ink painting on hanji mulberry paper, warm cream paper (#F7F3EA) with visible fibers and subtle grain, sumi ink black (#111111), restrained muted palette, one small square red seal stamp (#C8102E) with no legible characters, generous empty margin around the subject, centered composition inside the inner 80% circle, flat even lighting, no frame`

**공통 네거티브**(§5 + 이번 추가): `text, letters, numbers, captions, calligraphy characters, Hangul, Chinese characters, readable writing, logos, brand names, trademarks, watermarks, signatures, real people, faces, hands, figures, celebrity likeness, tiger, magpie, birds, animals, copyrighted characters, mascots, film or TV stills, posters, UI elements, photorealistic, 3D render, glossy, neon, gradient background, border, vignette, cropped subject at edge`
- 네거티브 입력란이 없는 모델은 본문 끝에 `No text, no letters, no logos, no people or faces, no tiger, no magpie, no watermark.`

---

## ① 책장 한 칸 (미니멀 일러스트)
- **콘셉트 1줄**: 책가도 책장 한 칸을 먹선으로 다시 그린 미니멀 정물 — 쌓인 책·벼루·붓, 낙관 하나.
- **프롬프트(EN)**: `A minimalist reinterpretation of a single compartment of a Korean chaekgado scholar's bookshelf screen: a small stack of three thread-bound books with plain blank covers, an ink stone, and one brush resting on a brush rest, drawn with confident sumi ink line and light dry-brush wash, muted indigo and ochre accents at low saturation, the shelf compartment drawn as a simple open square frame of thin ink lines,` + 공통 스타일 꼬리
- **네거티브**: 공통 네거티브 + `cluttered shelf, many objects, clock, vase with decoration text, book titles, spine labels`
- **권장**: flux-2-pro 1024x1024, 시드 고정(예: 20261002)
- **설명(KR)**: 원화의 "칸 + 문방 기물" 문법만 빌리고 그림은 새로 그린다(원화 복제 아님). 책 표지·등에 글자가 생기기 쉬워 "blank covers, no spine labels"를 반복. 110px에서 책 더미 실루엣 + 붉은 점 하나로 읽히게 물건 수를 3개로 제한.

## ② 붓글씨가 주인공 (2단 구조: AI 바탕 + 코드 글자)
- **콘셉트 1줄**: 먹 번짐 붓글씨 "책가도"(또는 "노트")가 주인공 — 글자는 코드로 합성, AI는 한지·먹 번짐 바탕만.
- **왜 2단**: 생성 모델은 한글을 깨뜨린다(획 누락·가짜 글자). 그래서 AI에는 **글자 없는** 바탕(한지 질감 + 가장자리 먹 번짐 + 빈 중앙)만 요청하고, 글자·낙관은 `cardnews/design/render_avatar_v4.py`(OFL 붓 서체 + 코드 낙관)로 위에 얹는다.
- **1단 프롬프트(EN, 바탕만)**: `An empty sheet of handmade Korean hanji paper photographed flat from above, warm cream tone with long visible mulberry fibers and soft uneven grain, a few faint pale ink wash blooms and tiny ink speckles near the lower left edge only, the center area completely blank and clean for later lettering, absolutely no writing,` + 공통 스타일 꼬리에서 `one small square red seal stamp ... no legible characters,` 구절은 **빼고**(낙관도 코드로 얹음)
- **네거티브**: 공통 네거티브 + `seal, stamp, red marks, brush strokes forming characters, objects`
- **2단(코드)**: AI 바탕을 `paper_bg()` 대신 입력으로 받아 `ink_layer()`(Nanum Brush Script / East Sea Dokdo, OFL) + `seal_layer()` 합성. 현재 폴백은 절차적 한지 바탕으로 같은 2단계를 이미 수행(아래 폴백 결과).
- **권장**: flux-2-pro 또는 imagen4 1024x1024. 바탕은 글자가 없어 모델 간 차이가 작으므로 저가 모델로도 충분(추정).
- **설명(KR)**: 글자 정확도 100%를 코드가 보장. 생성물 안에 글자가 하나라도 보이면(가짜 획 포함) 그 장은 버린다.

## ③ 병풍 전경 아이콘 (격자 책장 + 사물 실루엣)
- **콘셉트 1줄**: 책가도 병풍 전경을 3x3 격자 책장 아이콘으로 단순화 — 칸마다 사물 실루엣 하나, 낙관 하나.
- **프롬프트(EN)**: `A simplified flat icon of a Korean chaekgado folding screen seen from the front: a 3 by 3 grid of open shelf compartments drawn with thick ink lines, each compartment holding one simple silhouette — stacked books, a round vase, a brush holder with brushes, a scroll, a small bowl, a teapot, more stacked books, a fan, a potted flower — silhouettes in ink black and muted indigo, ochre and celadon at low saturation, slight reverse perspective typical of chaekgado, bold readable shapes at small size,` + 공통 스타일 꼬리
- **네거티브**: 공통 네거티브 + `realistic shading, tiny details, more than nine compartments, decorative patterns with characters, clock face`
- **권장**: flux-2-pro 1024x1024. 아이콘형은 gpt-image-2가 선을 깔끔하게 낼 가능성(추정) → 2순위로 비교.
- **설명(KR)**: 110px에서 "격자 + 점들"로 읽혀 계정명 '책가도'와 가장 직접 연결. 칸이 많으면 뭉개지므로 3x3 상한.

---

## 생성 기록 (2026-10-02)
| 안 | 시도 | 결과 |
|---|---|---|
| ①②③ | `MUAPI_API_KEY` / `FAL_KEY` / `IMAGE_API_KEY` 확인 | **전부 UNSET → 생성 0장, 비용 0** |
| 폴백 | `render_avatar_v4.py` 코드 렌더 붓글씨 3안(②의 2단 구조 중 코드 단계) | `avatar-v4-A/B/C.png` · `contact-profile-v4.png`, PROFILE.md §13 |

키가 생기면: 위 명령으로 ①③은 그대로 1장씩, ②는 1단 바탕 생성 후 `render_avatar_v4.py`에 바탕 입력 옵션을 붙여 합성 → `avatar-v4-GEN.json`에 모델·프롬프트·시드·비용 기록. 카드·캡션에는 AI 라벨을 넣지 않는다(§9-5).
