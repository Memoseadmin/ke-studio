# 크리에이티브 에이전트 리서치 — 벤치마크·설계 패턴·직원 로스터 (설치 없음)

갱신: 2026-10-02 · 작성: 리서처 겸 CD 자식 세션 · 브랜치 `research/creative-agents`
범위: 리서치 + 설계안만. `.claude/agents/`·`.claude/skills/`는 건드리지 않았다. 초안은 `docs/agents-draft/`.
관련: `cardnews/docs/BENCHMARK-visual.md`(박물관 18계정, cardnews/c1-1-design) · `episodes/EP001/design/design-system.md` §8·§9 · `docs/TOOLING_OPENSOURCE.md` §3

## 0. 요약 10줄
1. 반려 3건(2판 "AI 생성물", bio v4 "AI틱", 프로필 v4 낙관·바탕)의 공통 원인 = **만든 사람이 스스로 채점**했고, **"무엇을 닮을지" 기준 이미지가 없었다**.
2. Anthropic 실험도 같은 결론: 생성자가 자기 결과를 평가하면 "평범해도 자신 있게 칭찬"한다 → **생성자와 비평가를 분리**해야 한다 [P1].
3. 취향은 프롬프트 한 줄이 아니라 **레퍼런스 보드 + 루브릭 + 비교 생성(best-of-N) + 독립 비평**의 공정으로 만든다 [P1·P2·P4].
4. 현 디자인 인력은 `designer` 1명(썸네일·프롬프트)과 `producer`(렌더)뿐 — 사진 배치·타이포·모션·편집 리듬을 맡은 사람이 없다.
5. 제안 로스터 **8명**: 크리에이티브 디렉터(비평·반려) · 아트디렉터 · 포토에디터 · 일러스트레이터 · 타이포그래퍼 · 모션 디자이너 · 영상 편집자 · 썸네일 디자이너.
6. "작가 투입"은 **실존 작가 모사 금지 → 원칙 기반 페르소나**(민화 화원의 규칙·한지 콜라주 원리 등)로 구현한다.
7. 벤치마크 16곳(유튜브 모션 6·숏폼/에디토리얼 6·한국 스튜디오/기관 4)에서 공통 문법 5개: **줌 문법, 한 화면 한 주인공, 종이·실물 질감, 편집 리듬의 변주, 출처의 시각화**.
8. 루브릭 30항(사진 배치 10·타이포 10·모션 10)을 CD가 매 판 채점, 7/10 미만 항목이 있으면 반려.
9. 파일럿: 세트 11 4판 + 릴스 1편을 새 체계로 — 바뀌는 점은 "브리프→3안 비교→독립 비평→1회 수정" 공정. 추가 비용 ≈ 0원(구독·집 PC), 시간 +2~3시간(추정).
10. 대표 결정 10건(A1~A10, 기본값 미적용). 설치는 승인 뒤 별도 세션.

## 1. 세계 수준 벤치마크 16 (기존 BENCHMARK-visual 18계정과 겹치지 않게 골랐다)
확인 수준: 공개 채널·2차 분석 자료 기준. 이 세션에서 프레임 단위 시청은 하지 못했다(추정 E1).

| # | 채널 (유형) | 레이아웃 | 타이포 | 사진·그림 배치 | 컬러 | 모션 | 편집 리듬 | 책가도 노트에 가져올 것 |
|---|---|---|---|---|---|---|---|---|
| 1 | Kurzgesagt (YT 모션) [B1] | 화면 중앙 1주인공, 배경은 단계적 흐림 | 둥근 산세리프, 화면 글자 최소 | 벡터 일러스트만, 사진 0 | 고채도 보색 대비, 장면별 팔레트 | **무한 줌**(디테일↔전체) | 설명 1문장 = 장면 1개 | 원화 디테일→병풍 전체 줌을 릴스 기본 문법으로 |
| 2 | Vox (YT 설명형) [B2] | 종이·문서 콜라주 위 하이라이트 | 굵은 산세리프 + 형광펜 강조 | 실사 사진을 **오려 붙이기**, 문서 확대 | 크라프트·형광 노랑 포인트 | **12fps 스터터**로 손맛 | 주장→증거(문서) 교차 | 출처 문서를 "증거 장"으로 클로즈업 |
| 3 | Johnny Harris (YT 다큐) [B3] | 책상 위 지도·종이 실물 | 손글씨 주석 + 산세리프 | 실물 지도·사진을 카메라로 촬영 | 바랜 종이 톤 | 지도 경로 애니, 패럴랙스 | 현장↔지도 교차 | 한지 위 손 주석(코드 붓선) |
| 4 | OverSimplified (YT 역사) [B4] | 극단적 단순 배경 | 거의 없음 | 캐릭터만, 배경 최소 | 평면 단색 | 표정·타이밍 개그 | **3~5초마다 반전** | 릴스 0~2초 훅 뒤 3초 간격 반전 |
| 5 | Extra History (YT 역사) [B5] | 일러스트 패널 | 자막형 | 일러스트 단독 | 따뜻한 중채도 | 컷 전환 위주 | 시리즈 + 오류 정정 편("Lies") | 오류 정정·출처 공개를 신뢰 장치로 |
| 6 | Google Arts & Culture "Art Zoom" (YT/IG) [B6] | 원화 고해상도 한 점 | 소자막 | 원화 단독, 붓자국까지 확대 | 원화 그대로 | 느린 줌·팬, 음악 동기 | 1작품 1영상 | 원화 1점 = 릴스 1편 포맷 |
| 7 | The Met (IG/릴스) [B7] | 작품+캡션 블록 | 세리프 제목 | 작품 단독, 디테일 크롭 연속 | 작품 색 추출 | 디테일 크롭 슬라이드 | 소장번호까지 표기 | 출처 두 겹(BENCHMARK-visual §1-4) 유지 |
| 8 | LACMA (IG) [B7] | 밈 템플릿 + 작품 | 짧은 구어체 | 작품을 **요즘 상황 대사**에 대입 | 작품 색 | 정지 | 주 1~2회 유머 | "원화 × 요즘 한국" 대입 장 1개 |
| 9 | The New Yorker (IG) [B8] | 일러스트 표지 1점 크게 | 고유 세리프, 여백 넓음 | 일러스트 단독, 글 0 | 작가별 상이, 테두리 없음 | 표지 일러스트 루프 애니 | 표지 단독 게시 | 표지 장 = 글자 최소·그림 최대 |
| 10 | The New York Times (IG/릴스) [B9] | 그래픽 데스크 차트 + 사진 | 신문 세리프 + 산세리프 라벨 | 사진 위 **주석 라벨**만 | 흑백+1포인트 | 주석이 하나씩 등장 | 질문→증거 3→결론 | 사진 위 알약 라벨(구글식)과 동일 원리 |
| 11 | The Pudding (웹/IG) [B10] | 데이터 시각 에세이 | 개성 서체 + 숫자 강조 | 그림·데이터 혼합 | 주제별 고유 팔레트 | 스크롤 연동 | 질문형 제목 | 수치 3개(영양소 기준)를 코드 그래픽 장으로 |
| 12 | It's Nice That (IG) [B11] | 엄격한 그리드, 큰 여백 | 제목 1서체 고정 | 작품 1점 + 작은 캡션 | 흰 바탕 | 정지·짧은 루프 | 일관 틀 | 표지 틀 고정·내부 장 변주 |
| 13 | 6699press (IG, 한국) [B12] | 텍스트를 이미지처럼 배치 | **한글 타이포 실험** | 사진 거의 없음 | 2~3색 별색 | — | 출판물 단위 | 한글 제목을 그림처럼(함렛 블랙 크게) |
| 14 | FNT·Everyday Practice (한국 스튜디오) [B12] | 포스터 그리드 | 한글·라틴 혼용 | 오브제 사진 + 그래픽 | 강한 단색 면 | 포스터 모션 루프 | 프로젝트 단위 | 단색 면 띠의 색 변주(C 틀 띠) |
| 15 | 국립중앙박물관 (IG) [B13] | 누끼 + 큰 한글 제목 | 굵은 고딕/명조 | 유물 누끼, 배경 단색 | 유물 색 | 릴스: 유물 회전·확대 | 전시 연계 시리즈 | 표지 누끼 + 한글 큰 제목(이미 §1-4 규칙 2) |
| 16 | 간송미술관·대구간송 (IG) [B13] | 실물(천원권)→원화→디테일 | 명조 | **실물↔그림 비교** | 원화 톤 | 비교 전환 | 3장 비교 서사 | "오늘의 실물 ↔ 원화" 비교 장 |

공통 문법 5 (책가도 노트 적용형)
1. **줌 문법**: 디테일→전체(1·6·7·16). 릴스 기본 = 원화 디테일에서 시작해 병풍 전체로 빠진다.
2. **한 화면 한 주인공**(1·9·12): 장마다 주인공 1 + 조연 1, 나머지는 여백.
3. **질감 있는 바탕**(2·3): 한지·크라프트·종이 그림자. 2판 반려의 "AI 생성물" 느낌은 매끈한 스톡 사진·균일 오버레이에서 왔다.
4. **리듬의 변주**(4·10·14): 같은 틀 8장 금지. 띠 색·높이·구성(ⓐⓑⓒ)을 바꾼다(DS §9-1과 일치).
5. **출처의 시각화**(5·7·16): 소장번호·출처를 디자인 요소로. 신뢰가 곧 "AI틱하지 않음".

## 2. 에이전트에 '취향·안목'을 주는 설계 패턴 (근거 포함)

| 패턴 | 내용 | 근거 | KE 적용 |
|---|---|---|---|
| P1 생성자/평가자 분리 | 만든 에이전트가 채점하지 않는다. 별도 평가자가 기준표로 채점·피드백, 5~15회 반복 | Anthropic 하네스 설계 글: 자기평가는 "confidently praising… obviously mediocre" [P1]; 평가자–최적화자 패턴 [P2] | `creative-director`가 유일한 채점자. 생성 직원은 자가 점수 금지 |
| P2 기준을 채점 가능한 말로 | "좋은 디자인인가?"를 디자인 품질·독창성·완성도·기능 4축으로 쪼갬. 독창성 축에서 "AI 생성 흔적"을 감점 | [P1] | 루브릭 30항(§4-2) + "AI틱 감점표" |
| P3 기준 문구가 결과를 끈다 | 루브릭에 "museum quality" 같은 문구를 넣자 결과가 그쪽으로 수렴 | [P1] | 루브릭 문구 = 원하는 결과의 언어로(예: "한지 위 실물 같은") |
| P4 few-shot 보정 | 평가자에게 점수 분해가 달린 예시를 주어 점수 흔들림을 줄임 | [P1] | 대표 반려·통과 사례를 "보정 세트"로(§4-1) |
| P5 기본값을 이름 불러 금지 | 모델은 분포 중앙(무난한 기본값)으로 수렴 → 흔한 기본값을 구체적으로 금지 | Anthropic 쿡북 frontend aesthetics [P5]; "distributional convergence" 논의 [P6] | 금지 목록: 서양 스톡, 균일 흰 박스, 같은 틀 반복, '저장해 두고 꺼내 보는' 식 문장 |
| P6 차원별 지시 + 영감 출처 | 타이포·색·모션·배경을 따로 지시, 문화적 미감을 영감으로 지명 | [P5] | 직원을 차원별로 나눈 근거(타이포그래퍼·포토에디터 분리) |
| P7 best-of-N + VLM 판정 | N안 병렬 생성 → 시각 모델이 기준으로 고르고 피드백으로 프롬프트 수정(N=폭, K=깊이) | PRISM [P7], Reflect-DiT [P8], ViMax [P9] | 플레이트는 시드 4장 생성 → CD가 컨택트시트로 1장 선택 |
| P8 자율 루프는 진부해진다 | 사람 없이 이미지↔글 루프를 돌리면 12개 진부한 모티프로 수렴 | [P10] | 루프 상한 2회, 그 뒤는 대표 판단. 레퍼런스 보드로 외부 기준 주입 |
| P9 원칙 기반 페르소나 | 실존 작가 모사 대신 "무엇을 왜 하는가" 원칙으로 성격 부여(디자인 철학 먼저 쓰고 실행) | Anthropic canvas-design 스킬(설치됨) "design philosophy" 방식 | 일러스트레이터 = "민화 화원 규칙(정면성·다시점·길상 상징)" 페르소나 |
| P10 도구로 직접 본다 | 평가자가 결과물을 직접 열어 보고 비평(Playwright) | [P1] | CD는 컨택트시트·360px 축소본을 반드시 열어 본다(이미지 Read) |

## 3. 직원 로스터 제안 (초안 `docs/agents-draft/*.md`)

| 직원 | 역할 한 줄 | 입력 → 출력 | 검수 기준 | 모델 | 기존과 분담 |
|---|---|---|---|---|---|
| creative-director | 유일한 채점·반려자, 레퍼런스 보드 관리 | 모든 시각 산출물 → `CRITIQUE-vN.md`(30항 점수·반려 사유) | 루브릭 30항, 7 미만 1개라도 반려 | Opus | 새 역할. copy-editor의 시각판 |
| art-director | 세트별 시각 콘셉트·장별 VISUAL-BRIEF·3안 방향 | 카피 확정본 → `VISUAL-BRIEF.md`(장별 주인공·조연·구성 ⓐⓑⓒ) | DS §9 준수, 3연속 금지 | Opus | designer의 "디자인 시스템" 업무 이관 |
| photo-editor | 사진 선별·크롭·시선 흐름·라이선스 | 브리프 → `PHOTOS.json`(출처·크롭 좌표·톤 프리셋) | 사진 10항 | Sonnet(선별)·Opus(최종 크롭 판단은 CD) | 새 역할 |
| illustrator | AI 플레이트 프롬프트·시드 비교 | 브리프 → `plates/PROMPTS.md`, 4시드 컨택트시트 | 금지 목록, 원화 옆에서 약하지 않은가 | Opus | designer의 "장면 프롬프트" 이관 |
| typographer | 한글 위계·줄바꿈·글자 수·서체 | 카피+레이아웃 → `TYPE-SPEC.md`·줄바꿈 표 | 타이포 10항 | Sonnet | 새 역할 |
| motion-designer | 릴스·쇼츠 15~30초 모션(Remotion/FFmpeg) | 릴스 대본 → 컷시트·Remotion 소스 | 모션 10항 | Opus(설계)·Sonnet(구현) | producer의 숏폼 렌더 중 "설계" 이관 |
| video-editor | 롱폼 컷·리듬·B롤(유튜브 재개 시) | 대본·플레이트 → EDL·리듬표 | 모션 10항 중 리듬 5항 | Opus | producer는 조립·렌더만 |
| thumbnail-designer | 썸네일·릴스 커버·표지 3안 | 제목·훅 → 3안 + 360px 미리보기 | 1초 판독·글자 ≤4단어 | Opus | designer의 썸네일 이관 |

기존 `designer`는 폐지가 아니라 **분할 이관**(A2 결정). `producer`는 렌더·조립 전담으로 좁힌다. 공정:
`copy-editor 통과 → art-director 브리프 → (photo-editor ∥ illustrator ∥ typographer) → producer 렌더 → creative-director 채점 → 1회 수정 → 대표 PR`

## 4. 레퍼런스·스킬 체계

### 4-1. 레퍼런스 보드 (`design/refboard/`)
- 저장: `refboard.md` 한 파일 = 표(링크 URL·확인일·무엇이 좋은가 1줄·루브릭 항목 번호). **저작권 이미지 파일 저장 금지.**
- 파일 저장은 CC0·PD·공공누리 1유형만(`refboard/cc0/`, 출처·소장번호를 파일명에). 기존 `cardnews/docs/BENCHMARK-visual.md` §4-1 11개를 첫 항목으로.
- 보정 세트(P4): `refboard/calibration.md` — 대표 반려 사례(2판·3판·bio v4·프로필 v4)와 통과 사례에 루브릭 점수를 붙여 CD 프롬프트에 few-shot으로 넣는다. 이미지는 저장소 내 자체 산출물 경로만 참조.

### 4-2. 루브릭 30항 (각 0~10, CD 채점)
**사진 배치 10**: ①장 내용과 사진 사물이 1:1 일치 ②주인공 1개가 3초 안에 보임 ③시선 흐름(사진 속 방향→글 띠) ④크롭이 피사체 중심, 핵심 디테일 안 잘림 ⑤원화 위 본문 0 ⑥한국 실물(서양 스톡 금지) ⑦톤 프리셋 일관(DS §9-2) ⑧장 간 구성 변주(3연속 금지) ⑨실물↔원화 비교가 있으면 같은 스케일 ⑩출처 소자 가독(360px).
**타이포 10**: ①제목/본문/출처 3단 위계 ②360px에서 본문 판독 ③한 줄 글자 수 규칙 ④어절 단위 줄바꿈(조사 고아 금지) ⑤강조색 1곳 ⑥서체 2종 이하 ⑦자간·행간 DS 값 ⑧숫자는 크게(수치 3개) ⑨한글을 그림처럼 쓰는 장 1개(표지) ⑩AI틱 문구 0(copy-editor 판정 인용).
**모션 10**: ①0~2초에 주인공·훅 ②줌 문법(디테일↔전체) ③컷 길이 변주(같은 길이 3연속 금지) ④움직임 이유가 내용에 있음 ⑤이징 일관 ⑥자막 무음 판독 ⑦원화 변형 0(크롭·팬·줌만) ⑧질감(그레인·종이) 일관 ⑨마지막 1초 CTA·출처 ⑩음악·효과음 상용 라이선스 기록.
판정: 30항 평균 ≥8 그리고 7 미만 0개 = 통과. 그 외 반려(사유 = 항목 번호 + 고칠 방법 1줄).

### 4-3. 기존 스킬: 쓸 것 / 보류
| 스킬 | 판정 | 이유 |
|---|---|---|
| frontend-design, taste-skill | **쓴다**(원칙만) | 기본값 금지·의도된 미감(P5). 웹 UI 부분은 무시 |
| example-skills-canvas-design | **쓴다** | 디자인 철학 먼저 → 실행(P9). 일러스트레이터·AD |
| design-design-critique | **쓴다** | CD 비평 서식 뼈대 |
| design-accessibility-review | 쓴다(대비만) | 띠 위 글자 대비 점검 |
| ffmpeg-assemble, shorts-cut, cardnews-copy | **쓴다** | 사내 스킬, 그대로 |
| social-media-skills-youtube-thumbnail | 쓴다 | 썸네일 디자이너 |
| social-media-skills-graphic-designer | 보류 | LinkedIn 그래픽 전용 |
| social-media-skills-gemini-carousel/infographic | 보류 | Gemini 키 전제, 키 없음 |
| ui-ux-pro-max, example-skills-theme-factory | 보류 | 웹 UI·슬라이드용 |
| marketing-skills-image | 보류 | 광고 이미지 중심 |

### 4-4. 외부 스킬 후보 (복사 설치 가능 여부)
| 후보 | 출처 | 라이선스 | 판정 |
|---|---|---|---|
| Remotion Agent Skills(best-practices·captions·render 등 12) | github.com/remotion-dev/skills [T1] | **이 세션에서 LICENSE 파일 확인 못 함**(추정 E4) | 모션 디자이너용 1순위. 설치 전 skill-installer가 LICENSE·SHA 확인 |
| Remotion 본체 | remotion.dev/license [T2] | 개인·3인 이하 회사 무료, 상업 이용 가능 | 1인 회사라 무료 범위(추정 E5) |
| gan-style-harness (ECC) | tessl.io 레지스트리 [T3] | 미확인 | 참고만. 자체 CD 스킬로 충분 |

### 4-5. 자체 스킬 초안 3 (제목 + 목차)
1. **`ke-art-direction`** — ①레퍼런스 보드 형식 ②VISUAL-BRIEF 서식(장별 주인공·조연·구성·이유) ③금지 기본값 목록 ④보정 세트 사용법 ⑤3안 방향 쓰는 법.
2. **`ke-visual-critique`** — ①루브릭 30항 정의·채점 예시 ②360px 축소·컨택트시트 확인 절차 ③AI틱 감점표 ④반려 사유 서식 ⑤루프 상한 2회 규칙.
3. **`ke-motion-grammar`** — ①줌 문법 5패턴(디테일→전체, 비교 와이프, 주석 등장, 패럴랙스, 띠 슬라이드) ②컷 길이 표(15·30초) ③Remotion 컴포지션 뼈대 ④자막 무음 규칙 ⑤렌더 체크리스트.

## 5. 파일럿 제안 — 세트 11 4판 + 릴스 1편
| 단계 | 지금(3판까지) | 새 체계 |
|---|---|---|
| 기준 | 벤치마크 문서를 렌더 담당이 읽음 | CD가 refboard·보정 세트로 **판정 기준을 먼저 고정** |
| 기획 | VISUAL-BRIEF를 렌더 세션이 같이 씀 | art-director가 장별 주인공·조연·구성 ⓐⓑⓒ와 **3안 방향**(원화 중심/비교 중심/타이포 중심) |
| 사진 | 렌더 세션이 검색·배치 | photo-editor가 한국 실물 사진 후보 3개씩·크롭 좌표·시선 방향 기록 |
| 플레이트 | 프롬프트 팩 1벌 | illustrator가 장별 4시드 → CD가 컨택트시트에서 1장 선택(best-of-4) |
| 글자 | 렌더러 기본값 | typographer가 줄바꿈 표·360px 판독 확인 |
| 평가 | 만든 세션이 MATCH 표로 자가 확인 | **CD 독립 채점 30항 → 수정 1회 → 대표** |
| 릴스 | 카드 재활용 슬라이드 | motion-designer가 "디테일→병풍 전체" 줌 + 3초 반전 리듬, 15초/30초 컷시트 |

달라지는 결과(예상): ①같은 틀 반복·서양 스톡 같은 2판식 실패를 CD가 대표 전에 걸러낸다 ②장마다 주인공이 달라 넘김 리듬이 생긴다 ③릴스가 카드 슬라이드쇼가 아니라 원화 줌 영상이 된다.
비용·시간(추정 E6·E7): 추가 현금 0원(구독 범위 + 집 PC ComfyUI 전기료). 자식 세션 5~6개, 기존 1세션 대비 +2~3시간. 플레이트 4시드×8장 = 32장, 집 PC 1장 30~60초 가정 시 약 20~30분.

## 6. 자가 검증
| 성공 기준 | 결과 |
|---|---|
| 벤치마크 15+ (레이아웃·타이포·사진·컬러·모션·리듬 분해) | ✅ 16곳, 6축 + 적용점 |
| 설계 패턴 + 공개 근거 | ✅ 10패턴, 근거 P1~P10 |
| 로스터 표(역할·입출력·검수·모델·분담) | ✅ 8명 |
| 초안 6~8개 `docs/agents-draft/`, 각 ≤60행 | ✅ 8개 (행 수는 커밋 전 `wc -l` 확인) |
| 레퍼런스 저장 방식·루브릭 30항·스킬 판정·외부 후보·자체 초안 2~3 | ✅ §4 |
| 파일럿(목업 없이 글)·비용·시간 | ✅ §5 |
| `.claude/` 무변경 | ✅ (`git diff --stat`으로 확인) |
| 본 문서 ≤300행 | ✅ |

## 7. 추정 (기본값을 택한 지점)
- E1 벤치마크 분석은 공개 채널과 2차 자료 기준, 프레임 단위 시청 미실시.
- E2 한국 기관 계정(국중박·간송)은 기존 BENCHMARK-visual 관찰을 재사용, 이번에 재확인 못 함.
- E3 로스터 모델 배정(Opus/Sonnet)은 CLAUDE.md "판단=Opus, 반복=Sonnet" 규칙을 그대로 적용.
- E4 remotion-dev/skills LICENSE는 페이지에서 확인 실패 — 설치 전 확인 필요.
- E5 Remotion 무료 범위는 "3인 이하 회사" 기준 공개 문서로 판단.
- E6 파일럿 시간 +2~3시간은 세션 5~6개 × 20~30분 가정.
- E7 ComfyUI 1장 30~60초는 집 PC 사양 미확인 상태의 가정.
- E8 루브릭 통과선(평균 8, 7 미만 0개)은 Anthropic 사례의 "기준 + 임계값" 방식을 본뜬 임의값.

## 8. 대표 결정 목록 (기본값 미적용)
| # | 결정 | 선택지 | 리서처 추천(1줄) |
|---|---|---|---|
| A1 | 로스터 규모 | ⓐ 8명 전부 ⓑ 카드뉴스 5명(CD·AD·포토·일러·타이포)만 지금 ⓒ CD 1명만 먼저 | **ⓑ** — 유튜브 보류 중이라 영상 편집자·썸네일은 재개 때 |
| A2 | 기존 designer 처리 | ⓐ 분할 이관 후 폐지 ⓑ 유지 + 새 직원 추가 ⓒ designer를 AD로 개명 | ⓐ — 역할 중복이 자가 채점을 부른다 |
| A3 | CD 반려 권한 | ⓐ CD 반려 시 대표에게 안 올림 ⓑ 점수와 함께 항상 올림 | ⓑ — 초기엔 대표 눈과 CD 기준을 맞춰야 함 |
| A4 | 루브릭 통과선 | ⓐ 평균 8·최저 7 ⓑ 평균 7·최저 6 ⓒ 직접 지정 | ⓐ |
| A5 | best-of-N 수 | ⓐ 플레이트 4시드 ⓑ 2시드 ⓒ 8시드 | ⓐ — 집 PC 시간 대비 선택 폭 |
| A6 | 레퍼런스 보드에 넣을 첫 계정 | 표 §1 16곳 중 5곳 지정 | 6·2·16·9·13 (줌·증거·비교·표지·한글) |
| A7 | 일러스트레이터 페르소나 | ⓐ 민화 화원 규칙 ⓑ 한지 콜라주 작가 원리 ⓒ 둘 다 장별 선택 | ⓒ — V2(플레이트 스타일) 결정과 연동 |
| A8 | Remotion 스킬 설치 | ⓐ 라이선스 확인 후 설치 세션 ⓑ 보류 | ⓐ — 릴스 품질의 가장 큰 지렛대 |
| A9 | 파일럿 대상 | ⓐ 세트 11 4판 + 릴스 1 ⓑ 4판만 ⓒ 새 세트 | ⓐ |
| A10 | 자체 스킬 3개 작성 | ⓐ 3개 모두 ⓑ ke-visual-critique만 먼저 | ⓑ — CD가 먼저 서야 나머지가 의미 있음 |

## 출처 (확인 2026-10-02)
- [P1] Anthropic Engineering, Harness design for long-running application development — https://www.anthropic.com/engineering/harness-design-long-running-apps ; 해설 InfoQ https://infoq.com/news/2026/04/anthropic-three-agent-harness-ai/
- [P2] Claude Cookbook, Evaluator-optimizer — https://platform.claude.com/cookbook/patterns-agents-evaluator-optimizer ; https://agentpatterns.ai/patterns/agent-design/evaluator-optimizer/
- [P5] Claude Cookbook, Prompting for frontend aesthetics — https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics
- [P6] Why AI design looks generic — https://superdesign.dev/blog/why-ai-design-looks-generic ; https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website
- [P7] PRISM, Automated Black-box Prompt Engineering for T2I — https://arxiv.org/pdf/2403.19103
- [P8] Reflect-DiT — https://arxiv.org/pdf/2503.12271
- [P9] ViMax: Agentic Video Generation — https://arxiv.org/pdf/2606.07649
- [P10] Autonomous language-image loops converge to generic motifs — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12827715/
- 참고: VisJudge-Bench https://arxiv.org/html/2510.22373v2 ; Can MLLMs Critique Like Humans? https://arxiv.org/pdf/2606.29689
- [B1] Kurzgesagt — https://www.youtube.com/@kurzgesagt ; 공정 해설 https://www.classcentral.com/classroom/youtube-motion-design-process-art-direction-style-frames-109064
- [B2] Vox 12fps 기법 — https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/
- [B3] Johnny Harris — https://www.youtube.com/@johnnyharris
- [B4][B5] 역사 채널 비교 — https://vidpros.com/best-history-youtube-channels/ ; https://podcastle.ai/blog/who-is-oversimplified
- [B6] Google Arts & Culture Art Zoom — https://also.kottke.org/19/06/art-zoom
- [B7] 박물관 릴스 동향(The Art Newspaper) — https://theartnewspaper.com/2024/03/27/the-reels-deal-museums-embrace-instagrams-video-opportunities ; 계정 목록 https://yello.substack.com/p/these-are-my-11-must-follow-art-museums
- [B8] https://www.instagram.com/newyorkermag/ · [B9] https://www.instagram.com/nytimes/ · [B10] https://pudding.cool · [B11] https://www.instagram.com/itsnicethat/
- [B12] 한국 스튜디오(FNT·Everyday Practice·6699press·워크스) — https://design.co.kr/article/163803/ ; https://design.co.kr/article/128645/
- [B13] 기존 관찰 재사용 — `cardnews/docs/BENCHMARK-visual.md` §1-1 (cardnews/c1-1-design)
- [T1] https://github.com/remotion-dev/skills ; https://www.remotion.dev/docs/ai/skills · [T2] https://www.remotion.dev/docs/license/faq · [T3] https://tessl.io/registry/skills/github/affaan-m/ECC/gan-style-harness
