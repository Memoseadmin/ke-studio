# KE Studio 도구 조사: TTS·이미지 생성 API (2026-10-01)

전제: 영어 롱폼 8~12분×월 4편 + 숏폼 20개 ≈ **월 5만 자(≈50분 음성)**, 이미지 **월 120장**(플레이트 80 + 썸네일 12 + 숏폼 25 + 여유). 전체 도구 예산 상한 월 20만 원.
환율은 **1 USD ≈ 1,400 KRW로 가정(추정치)** — 2026-09-16 실측 1,377원 [S40]. 모든 원화 금액은 추정치이며 세금·환차 미포함. 가격은 각 제공자 공식 페이지 또는 2차 집계 사이트 기준이고 "확인 날짜"에 적은 날 기준으로 변동 가능.
Linux VM에서 HTTP API로 호출, 단일 키 환경변수(`TTS_API_KEY`, `IMAGE_API_KEY`) 전제. 대시보드 경로는 2026-10 기준 통상 경로로, UI 변경 가능(미검증 표시).

## 0. 결론 요약 (3+3)

| 구분 | 옵션 | 제공자·모델 | 월비용(추정) | 핵심 이유 |
|---|---|---|---|---|
| TTS | 최고 품질 | ElevenLabs **Eleven v3/v4** (Creator $22) | ≈ 30,800원 | 블라인드 Arena 1위(v4 Elo 1320) [S10]; seed·IPA 발음 제어 [S12][S13] |
| TTS | 최고 가성비 | Google **Gemini 2.5/3.1 Flash TTS** 또는 **Chirp 3 HD** (Gemini API 키 1개) | ≈ 0~2,100원 (Chirp 3 HD 무료 100만 자/월) | Arena 상위권(Gemini 3.8 Flash TTS Elo 1272) [S10]; SSML `<phoneme>`·IPA 지원 [S14]; 이미지와 키 공유 |
| TTS | 오픈소스 자체호스팅 | **Kokoro-82M** (Apache-2.0, CPU) | 0원 | 인라인 IPA 지원 [S15]; 2026-01 TTS Arena 1위 이력 [S16]; 단, 감정폭 좁음 [S17] |
| 이미지 | 최고 품질 | Google **Gemini 3.1 Flash Image (Nano Banana 2)** 2K | ≈ 17,000원 (1K ≈ 11,300원) | 스타일 레퍼런스 3장+캐릭터 4장 [S27]; 한글 렌더링 "Excellent" [S36] |
| 이미지 | 최고 가성비 | **Recraft V4 Styles** (style_id 고정) | ≈ 6,000원 | 스타일 ID 1회 생성 후 재사용, 상용권 명시 [S30][S31] |
| 이미지 | 오픈소스 자체호스팅 | **FLUX.2 [klein] 4B** (Apache-2.0) 또는 SD3.5 (Community) on Vast.ai RTX 4090 | ≈ 1,400~3,000원 + 세팅 시간 | 상용 자체호스팅 허용 라이선스 [S41]; GPU $0.29~0.34/h [S42] |

합계(최고 품질 조합) ≈ 48,000원/월, (가성비 조합) ≈ 8,000원/월 → 모두 20만 원 상한 내.

## A. TTS 비교

### A-1. 자연스러움 평판 — Artificial Analysis Speech Arena (블라인드 선호 Elo, 2026-09 확인) [S10]
Eleven v4 1320 › Cartesia Sonic 3.6 1273 › Gemini 3.8 Flash TTS 1272 › Qwen-Audio-3.0-TTS-Plus 1259 › Inworld Realtime TTS-2 1247 › Gemini 3.8 Flash-Lite TTS 1240 › Speechify Simba 3.2 1239 … ElevenLabs v3 Conversational 1200 › Sonic 3.5 1187 › Eleven v3 1171 › MiniMax Speech 2.8 HD 1170 › Speech 2.8 Turbo 1152.
2026년 상반기엔 Inworld TTS-1.5 Max(5월, 1247)·Alibaba Fun-Realtime-TTS(6월)가 1위를 번갈아 차지해 상위권 격차가 수십 Elo 이내 [S11]. 오픈소스 쪽은 Kokoro Elo ≈1,060, Chatterbox ≈1,011로 상용 상위권과 150~250 차이 [S18].
크리에이터 커뮤니티(Reddit 요약 글)에서는 다큐 내레이션용으로 ElevenLabs가 가장 자주 추천되고, 오픈소스 대안으로 Kokoro·Chatterbox 언급 [S19]. **주의**: Arena 점수는 짧은 문장 기준이라 10분 롱폼의 억양 단조로움·문단 경계 아티팩트는 별도 청취 테스트가 필요 (Kokoro는 10분 이상에서 경계 아티팩트 보고 [S17]).

### A-2. 제공자 비교표 (월 5만 자 기준, 원화는 추정치)

| 제공자·모델 | 가격 | 상용 라이선스 | API | 한국어 고유명사 발음 제어 | 세션 간 일관성 | 월비용(추정) | 출처 | 확인 날짜 |
|---|---|---|---|---|---|---|---|---|
| ElevenLabs Eleven v3 / v4 / Multilingual v2 | Creator $22/월 121k크레딧(v2 1자=1크레딧; Flash/Turbo 0.5~1) ; AA 표기 v4 $80/1M, v3 $50/1M | Starter $6 이상 유료 플랜(Free는 상용 불가) | REST/SDK | `<phoneme>` SSML은 **Flash v2만**; v3/v4는 `/IPA/` 슬래시 표기, 알리아스 사전은 API `pronunciation_dictionary_locators`(최대 3개) | `seed` 파라미터(best-effort), voice_id 고정 | $22 → ≈30,800원 | [S1][S10][S12][S13] | 2026-10-01 |
| OpenAI gpt-4o-mini-tts (tts-1-hd) | 텍스트 $0.60/1M tok + 오디오 $12/1M tok ≈ $0.015/분 ; tts-1-hd $30/1M자 | 유료 API 사용 시 상용 가능, 단 **AI 음성임을 청자에게 고지** 의무 | REST | SSML/음소 **없음**, `instructions` 자연어만 | seed 없음, 11개 고정 보이스 | ≈ $0.75~1.5 → 1,100~2,100원 | [S2][S20] | 2026-10-01 |
| Google Cloud TTS Chirp 3: HD | $30/1M자, **무료 100만 자/월** | Cloud 약관상 상용 가능 | REST(API 키 또는 서비스계정) | SSML `<phoneme>` IPA/X-SAMPA, customPronunciations, speaking_rate 0.25~2.0 ; 영어 30보이스 | 보이스명 고정(결정론적) | $0 (무료 한도 내) | [S3][S14][S21] | 2026-10-01 |
| Google Gemini 2.5 Flash TTS / 3.1 Flash TTS | $0.5/$10 (2.5) , $1/$20 (3.1) per 1M in/out 토큰; 오디오 25tok/초 | Gemini API 유료 티어 상용 가능(출력 권리 사용자) | Gemini API 키 1개 | 자연어 스타일 지시; SSML 미지원(프롬프트로 발음 안내) | 보이스명 고정, seed 없음 | ≈ $0.75~1.5 → 1,100~2,100원 | [S3][S22] | 2026-10-01 |
| Azure AI Speech Neural / HD | Neural $15/1M, HD ≈ $22~30/1M(2차출처), **무료 50만 자/월** | Azure 약관 상용 가능 | REST(키+리전 2변수) | SSML `<phoneme>`·커스텀 lexicon(업계 최다 제어) | 보이스명 고정 | $0~1.5 | [S4][S23] | 2026-10-01 |
| Cartesia Sonic 3.6 | ≈1크레딧/자; Pro $5/월 100k크레딧 | **Pro($5)부터 상용** | REST/WebSocket | 공식 문서상 발음 사전 확인 못함(미검증) | voice_id 고정 | $5 → 7,000원 | [S5][S24] | 2026-10-01 |
| Hume Octave 2 | Pro $70/월 100만 자 | **상용 라이선스는 Pro($70)부터** | REST | 미확인 | voice 저장 | $70 → 98,000원 (예산 과다) | [S6] | 2026-10-01 |
| MiniMax Speech 2.8 HD / Turbo | $100 / $60 per 1M자; 클로닝 $1.5/보이스 | 문서에 상용 조건 미명시(확인 필요) | REST(키+GroupId 가능성) | `pronunciation_dict` 치환 사전 | voice_id 고정 | $3~5 → 4,200~7,000원 | [S7][S25] | 2026-10-01 |
| Fish Audio s2.1-pro / S1 | $15/1M UTF-8 바이트 | 문서에 상용 조건 미명시(지원팀 문의) | REST | 미확인 | reference_id 고정 | ≈ $0.75 → 1,050원 | [S8] | 2026-10-01 |
| Inworld Realtime TTS-2 / Flash | $25 / $15 per 1M자(On-Demand) | 모든 유료 티어 상용 포함 | REST | 미확인 | voice 고정 | $0.75~1.25 → 1,050~1,750원 | [S9] | 2026-10-01 |
| Kokoro-82M (자체호스팅) | 0원(CPU 가능) | Apache-2.0 | 로컬 Python/FastAPI | 입력 텍스트 인라인 `[word](/IPA/)` | 보이스 벡터 파일 고정 → 완전 결정론 | 0원 | [S15][S17] | 2026-10-01 |
| Chatterbox (Resemble) | 0원 | MIT, 23개 언어, 감정 제어 | 로컬 | 미확인 | 참조 오디오 고정 | 0원(GPU 권장) | [S18] | 2026-10-01 |

### A-3. YouTube의 AI 음성 취급 (정책·알고리즘 증거)
- 2025-07-15 YPP "반복적 콘텐츠" → **"비진정성(inauthentic) 콘텐츠"**로 개정. 금지 대상은 "템플릿으로 대량 생산된·반복적·교육 가치 낮은" 콘텐츠이며 AI 음성 자체를 금지하지 않음. 고유 서사·인간 검수가 있으면 AI 사용 채널도 수익화 가능. 단 **AI 페르소나가 건강·법률·금융·정치 전문가 행세**하면 수익화 금지 [S43][S44].
- 합성 콘텐츠 **공개 라벨**: 사실처럼 보이는 합성물(딥페이크·실제 사건 변조·사실적 장면)만 의무. 비사실적 일러스트·자기 목소리 클론 더빙은 라벨 불필요. 라벨은 도달·수익에 불이익 없음이 명시 [S45]. → 우리 채널은 "AI 생성물 공개 라벨"을 자발적으로 붙여도 패널티 없음.
- 집행 사례: Screen Culture·KH Studio(AI 가짜 트레일러, 2025-04 수익화 중단 → 영구 삭제) [S46]; AI 내레이션 "Boring History" 계열(Sleepless Historian 등) 2025-09 404 Media 보도, YouTube "대량 생산 단속" 입장 표명 [S47]; 2026-07-31 Kurzgesagt(인간 제작)가 AI 슬롭 탐지기 오탐으로 추천 급감 후 복구 [S48]. 즉 알고리즘 측 "AI 느낌" 탐지는 실존하며 오탐도 있음.
- 시청자 반응: 연구·설문에서 인간 음성 신뢰도가 더 높지만 학습 효과는 동일, "로봇 같은 억양·단조로운 페이싱"이 초반 이탈의 주원인 [S49]. → 상위권 모델 + 문장별 호흡·SSML 제어가 핵심.

## B. 이미지 생성 API 비교 (월 120장)

| 제공자·모델 | 가격/장 | 스타일 일관성 기능 | 텍스트(한글) 렌더 | 상용권·면책(indemnity) | 월비용(추정) | API/비고 | 출처 | 확인 날짜 |
|---|---|---|---|---|---|---|---|---|
| Google Gemini 3.1 Flash Image (Nano Banana 2) | 0.5K $0.045 / 1K $0.067 / 2K $0.101 / 4K $0.151; Batch 50%↓ | 참조 이미지 최대 10장(스타일 3·캐릭터 4·오브젝트), 16:9·21:9, 1K~4K; **seed 없음** | 한글 "Excellent"(2026-05 비교) | 출력 권리 사용자; **면책은 Vertex AI 경로만** | 1K ≈ $8 → 11,300원 / 2K ≈ 17,000원 | Gemini API 키 1개로 TTS 공유. SynthID 워터마크. Imagen 4·Gemini 3 Pro Image는 2026-08-17 종료, 2.5 Flash Image 2026-01-15 종료 | [S26][S27][S28][S36][S37] | 2026-10-01 |
| OpenAI gpt-image-1.5 / 2.x | 1536×1024 medium $0.05, high $0.20(토큰 과금 $32/1M 출력) | edits 엔드포인트에 참조 이미지 여러 장; **seed 없음**; 10장 연속 생성 시 톤 드리프트 보고 | 양호(한글 미검증) | 출력 권리 사용자; Copyright Shield(API) | $6~24 → 8,400~33,600원 | REST | [S2][S29][S38] | 2026-10-01 |
| BFL FLUX.2 [pro] / [max] / FLUX.1 Kontext pro | pro $0.03/MP(+$0.015/추가MP, 1080p≈$0.046); max $0.07~; Kontext pro $0.04 | 참조 8장(FLUX.2), seed, 네거티브 프롬프트, Finetune(LoRA) | 양호(한글 "Limited") | API 출력 상용 가능; dev 가중치는 비상용 | ≈ $5.5~12 → 7,700~17,000원 | REST(x-key) | [S32][S33][S36] | 2026-10-01 |
| Ideogram 3.0 (Turbo/Default/Quality), 4.0 | API $0.03 / $0.06 / $0.09; 캐릭터 참조 +$0.10~; 4.0 ≈ $0.08 | style_reference_images, seed, 캐릭터 참조 | 텍스트 강점(영문) | 소유권 미주장·상용 허용 | $3.6~10.8 → 5,000~15,100원 | REST | [S34][S35] | 2026-10-01 |
| Recraft V4.1 / V4 Styles / V3 | V4.1 $0.035, V4 Styles $0.035~(Pro Vector $0.12), 스타일 생성 $0.044 1회, V3 $0.04 | **create-style(참조 1~10장) → style_id 재사용**: 프로젝트 전체 동일 룩 | 양호(벡터 가능) | 유료 플랜 전면 소유권·상용권 | ≈ $4.3 → 6,000원 | REST | [S30][S31] | 2026-10-01 |
| Stability Stable Image Ultra / Core / SD3.5 | Ultra $0.08, Core $0.03, SD3.5 L $0.065 | seed, negative prompt, style preset | 약함 | Community 라이선스(연매출 <$1M 무료) | $3.6~9.6 → 5,000~13,400원 | REST(크레딧) | [S39] | 2026-10-01 |
| Leonardo Production API (Phoenix/Lucid) | $0.0125~0.05 | Style reference, Elements | 보통 | 유료 플랜 상용 | $1.5~6 → 2,100~8,400원 | REST | [S50] | 2026-10-01 |
| Midjourney | 구독 $10~ | — | — | **공식 API 없음, 자동화 약관 금지(2026-08)** | 사용 불가 | 파이프라인 부적합 | [S51] | 2026-10-01 |
| fal.ai 호스팅 (FLUX LoRA 등) | LoRA 학습 $2/회, 추론 $0.02~0.03/장; FLUX.2 pro $0.03/MP | 자체 스타일 LoRA(10~50장 학습) | — | 모델별 라이선스 상속(확인 필요) | $2.4~3.6 + 학습 $2 | REST | [S52][S33] | 2026-10-01 |
| 자체호스팅: FLUX.2 [klein] 4B / Z-Image / SD3.5 | GPU 임대 RTX 4090 $0.29~0.34/h | seed·LoRA·ControlNet 자유 | 약~보통 | klein 4B·Z-Image Apache-2.0; SD3.5 Community; **FLUX.2 dev·Qwen-Image-2.1은 상용 제한** | ≈ 1~2 GPU시간/월 → 1,400~3,000원 | 직접 운영 | [S41][S42] | 2026-10-01 |

### B-2. 한국 문화 정확성 이슈
- 한복: Adobe 생성형 검색에서 "hanbok"에 일본식 의복이 섞여 나오고, AI 한복은 깃·동정·고름·배래 구조가 틀려 중국복처럼 보인다는 비판(2025 국가브랜드업 엑스포 사례) [S53]. → 프롬프트에 구조 요소를 명시(jeogori with white dongjeong collar band, long otgoreum ribbon, chima high-waist)하고 **인간 검수 체크리스트** 필수.
- 한글 자형: 2026-05 비교에서 Nano Banana 2만 한국어 "Excellent", Midjourney v7·FLUX Max "Limited" [S36]. 우리 파이프라인은 텍스트를 ffmpeg 오버레이로 넣으므로 **이미지 안 한글은 금지**(간판·현판은 빈 판으로 생성 후 폰트 오버레이).
- 실존 인물 얼굴·브랜드 로고 금지 규정 → 인물은 뒷모습·실루엣·민화식 비사실적 얼굴로만.

## C. 페이스리스 역사·문화 채널 사례 (공개 비즈니스 채널)

| 채널 | 비주얼 스타일 | 음성 | 스택 근거 | 정책/비고 | 출처 |
|---|---|---|---|---|---|
| Simple History | 종이 컷아웃·플랫 일러스트 애니메이션 | 인간 내레이터 | 창작자 Daniel Turner(일러스트레이터), 2014~, Electrify 투자 | 정상 수익화 | [S54] |
| History Matters (전 Ten Minute History) | 스틱피겨 미니멀 애니메이션, 3~10분 | 창작자 본인(영국식 건조 톤) | 리뷰·가이드 다수 | 저예산·고반복 포맷이지만 고유 서사로 정상 | [S55] |
| Kings and Generals | 애니메이션 전투 지도 + 다큐 리서치 | 인간 내레이터 팀 | 익명 브랜드, 연구·내레이터·애니메이터 팀, 3.7M 구독, 1만+ 패트런 | 광고 외 수익(패트런) 모델 참고 | [S56] |
| The Infographics Show / Armchair Historian | 모션그래픽 / 일러스트+지도 | 인간 내레이션 | 페이스리스 사례 정리 | 정상 | [S57] |
| History Time (Pete Kelly) | 아카이브+일러스트 롱폼 | 인간 | 404 Media 인터뷰 | AI 채널 범람의 피해 사례로 발언 | [S47] |
| Sleepless Historian · Boring History Bites · Dreamoria 등 | AI 생성 이미지 슬라이드 | **AI 내레이션**(글리치 보고) | 404 Media 2025-09-03 | YouTube "대량 생산 단속" 대상군; 영상 1편 230만 뷰 | [S47] |
| Epic Korean History | AI 생성 시네마틱 비주얼 + 오케스트라 BGM | 내레이션(미확인) | 채널 소개 | 한국사 영어 채널 벤치마크 | [S58] |
| Historika Shorts(교육상품) | 애니메이션 숏폼 | ElevenLabs | "ChatGPT+CapCut+Midjourney+ElevenLabs" 스택 공개 | 숏폼 스택 참고 | [S59] |
| Screen Culture · KH Studio | AI 가짜 트레일러 | — | Deadline 조사 | 2025-04 수익화 중단 → 영구 삭제(스팸·오해 메타데이터) | [S46] |
| Kurzgesagt | 플랫 모션그래픽 | 인간 | 2026-07-31 공개 | AI 슬롭 탐지기 **오탐** 후 복구 | [S48] |

리텐션 관찰: 상위 채널은 모두 **단일한 고유 비주얼 언어**(컷아웃, 스틱피겨, 지도 애니메이션)를 수년간 유지하고 매 초 화면이 대본과 맞물리는 방식("Paint Explainer 스타일"도 같은 원리로 고참여 스타일로 설명됨) [S60]. 사진형 AI 슬라이드 + 단조 AI 음성 조합은 404 Media가 지목한 "슬롭" 군과 같은 외형이라 알고리즘 오탐 위험이 가장 큼 [S47][S48]. 결론: 비사실적(일러스트) 스타일 + 장면당 1~2장 + 프로그램 모션·텍스트 레이어가 정책·리텐션 양면에서 유리.

## D. 최종 추천

### D-1. TTS 3안

| 옵션 | 제공자·모델·티어 | 월비용(추정) | 라이선스 주의 | API 키 발급 경로(통상 경로, UI 변경 가능) | env 매핑 |
|---|---|---|---|---|---|
| 최고 품질 | ElevenLabs Creator($22) + `eleven_v3`(또는 v4 GA 시) ; 긴 문장은 Multilingual v2 백업 | ≈ 30,800원 | Free 플랜은 상용 불가; v3/v4는 `<phoneme>` 미지원 → `/IPA/` 표기·알리아스 사전 사용 | elevenlabs.io 로그인 → 좌하단 프로필 → **Developers → API Keys → Create API Key** (권한: Text to Speech, Pronunciation Dictionaries) | `TTS_API_KEY`=xi-api-key (1변수) |
| 최고 가성비 | Google **Chirp 3: HD**(무료 100만 자/월) 또는 Gemini 2.5 Flash TTS | ≈ 0~2,100원 | Gemini API 무료 티어는 데이터 학습 활용 → **유료 티어** 사용; 면책은 Vertex만 | Chirp: console.cloud.google.com → APIs & Services → Credentials → Create credentials → **API key**(Text-to-Speech API 제한) ; Gemini: aistudio.google.com/apikey → **Create API key** | Chirp: `TTS_API_KEY`(REST `x-goog-api-key`) 또는 서비스계정 JSON → `GOOGLE_APPLICATION_CREDENTIALS` **2변수 가능** ; Gemini: `TTS_API_KEY`=`IMAGE_API_KEY`=GEMINI 키 |
| 오픈소스 | Kokoro-82M (Apache-2.0) 로컬 FastAPI 래퍼 → 동일 HTTP 인터페이스 | 0원(VM CPU) | 영어 전용·감정폭 좁음; 롱폼은 문단 단위 합성 후 ffmpeg concat | 키 불필요 | `TTS_API_KEY`=더미, `TTS_BASE_URL`=localhost |

차순위: Cartesia Sonic 3.6 Pro $5(Arena 2위, 상용 포함) — 발음 사전 지원 확인 후 채택 가능 [S5][S24]. Azure(SSML 제어 최강, 무료 50만 자)는 키+리전 2변수 필요 [S4][S23]. Hume는 상용 $70부터라 제외 [S6].

### D-2. 이미지 3안

| 옵션 | 제공자·모델 | 월비용(추정) | 라이선스 주의 | API 키 발급 경로 | env 매핑 |
|---|---|---|---|---|---|
| 최고 품질 | Gemini **3.1 Flash Image** 2K, 16:9, 스타일 참조 3장 | ≈ 17,000원(배치 시 8,500원) | SynthID 워터마크(비가시); 면책 필요하면 Vertex AI 경로; seed 없음 → 참조 이미지로 통제 | aistudio.google.com/apikey → Create API key(유료 프로젝트 연결) | `IMAGE_API_KEY`=GEMINI 키(TTS와 공유 가능) |
| 최고 가성비 | **Recraft V4 Styles**: create-style(민화 참조 5~10장) → style_id | ≈ 6,000원 | 유료 플랜/API 유닛만 상용·소유권; Free 산출물은 Recraft 소유·공개 | recraft.ai → 프로필 → **API → Generate API key**, API Units 충전 | `IMAGE_API_KEY`(Bearer) + `RECRAFT_STYLE_ID`(상수) |
| 오픈소스 | FLUX.2 [klein] 4B(Apache-2.0) 또는 SD3.5 Medium(Community) + 자체 스타일 LoRA, Vast.ai RTX 4090 온디맨드 | ≈ 1,400~3,000원 + 운영 시간 | FLUX.2 dev·FLUX.1 dev는 비상용 가중치 → 금지; 연매출 $1M 미만 조건(SD3.5) | GPU 임대 콘솔(키는 GPU 제공자용) | `IMAGE_API_KEY`=더미, `IMAGE_BASE_URL`=임대 VM |

차순위: FLUX.2 pro(seed·참조 8장, 1080p ≈ $0.046) [S32][S33], Ideogram 3.0 Default(style_reference·seed) [S34]. OpenAI gpt-image는 seed 없음·드리프트 보고 [S38]로 썸네일 전용 후보. Midjourney는 공식 API 없음·자동화 금지로 제외 [S51].

### D-3. 비주얼 스타일 방향 — "민화 플랫 일러스트 × 한지 질감"
- **콘셉트**: 조선 민화(호작도·책가도·십장생)의 평면 원근·굵은 먹선·오방색(적·청·황·백·흑)+단청 보색 포인트, 바탕은 한지 섬유 질감, 인물은 비사실적 얼굴(눈·입 단순화)로 실존 인물 규정 자동 충족. 민화 스타일 프롬프트는 주요 모델에서 재현 가능함이 프롬프트 갤러리로 확인됨 [S61].
- **프롬프트 골격(영문 고정 접두)**: `Korean minhwa folk-painting style flat illustration, bold ink outlines, obangsaek palette (vermilion, indigo, ochre, white, ink black) with dancheong accents, flat perspective, textured hanji paper background, no text, no logos, no photorealism, no real person likeness` + 장면 설명 + 구조 명시(한복 깃·동정·고름 / 한옥 기와·처마 / 소품).
- **20장 일관성 강제 절차**:
 1) **스타일 바이블**: 승인된 기준 플레이트 5~10장을 `episodes/_style/`에 저장 → Gemini는 매 요청 스타일 참조 3장 첨부, Recraft는 style_id 1회 생성 후 전 플레이트 재사용, FLUX/Ideogram/SD는 동일 seed + 참조 이미지.
 2) **seed 고정**: seed 지원 모델(FLUX·Ideogram·SD·ElevenLabs 음성)은 에피소드별 seed를 scene JSON에 기록해 재생성 가능하게.
 3) **네거티브/금지어**: `photorealistic, 3D render, anime, kimono, hanfu, qipao, logo, watermark, text, realistic face`(네거티브 미지원 모델은 자연어 금지문으로).
 4) **후처리 통일(ffmpeg)**: 모든 플레이트에 동일 LUT(채도·따뜻한 톤) + 한지 그레인 오버레이(blend=multiply, 8~12%) + 가벼운 비네트 → 모델 간 미세 차이를 흡수하고 "AI 광택"을 제거.
 5) **구성 템플릿**: 16:9 플레이트는 좌·우 1/3에 여백(텍스트 오버레이 안전영역), Ken Burns 이동 방향을 장면 JSON에 명시.
 6) **인간 검수 체크리스트**(risk.md): 한복 구조 4항목, 한옥 지붕 곡선·기와, 이미지 내 문자 0, 실존 인물·로고 0, 색상 팔레트 이탈 여부 — 불합격 플레이트만 재생성.

### D-4. 운영 메모
- 에피소드별 음성 캐시(장면 텍스트 해시 → mp3)로 재렌더 시 TTS 비용 0. 발음 사전(`pronunciation.json`: Joseon, Goryeo, Gyeongbokgung, Sejong 등)은 제공자별 포맷(ElevenLabs PLS/알리아스, Google SSML phoneme, Kokoro 인라인 IPA)으로 변환해 적용.
- 설명란에 "AI 음성·AI 일러스트 사용" 고지 문구를 제휴 고지 다음 줄에 고정(OpenAI 사용 시 의무, 그 외도 자발적) [S20][S45].
- 분기마다 AA Arena·가격 재확인(모델 종료 빈번: Imagen 4·Nano Banana 1세대 2026년 종료) [S28].

## 출처 (확인 날짜 전부 2026-10-01)
[S1] https://elevenlabs.io/pricing · [S2] https://developers.openai.com/api/docs/pricing · [S3] https://cloud.google.com/text-to-speech/pricing (요약: https://costbench.com/software/ai-voice-tools/google-cloud-text-to-speech/) · [S4] https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/ (HD 가격 2차: https://costbench.com/software/ai-voice-tools/microsoft-speech/) · [S5] https://cartesia.ai/pricing · [S6] https://www.hume.ai/pricing · [S7] https://platform.minimax.io/docs/guides/pricing-paygo.md · [S8] https://docs.fish.audio/developer-platform/models-pricing/pricing-and-rate-limits · [S9] https://inworld.ai/pricing · [S10] https://artificialanalysis.ai/text-to-speech/leaderboard · [S11] https://artificialanalysis.ai/articles/fun-realtime-tts-new-text-to-speech-model-topping-artificial-analysis-leaderboard , https://oakgen.ai/blog/inworld-tts-1-5-max-speech-arena · [S12] https://elevenlabs.io/docs/product/prompting/pronunciation · [S13] https://elevenlabs.io/docs/api-reference/text-to-speech/convert · [S14] https://docs.cloud.google.com/text-to-speech/docs/chirp3-hd · [S15] https://github.com/hexgrad/kokoro · [S16] https://pinggy.io/blog/best_open_source_self_hosted_text_to_speech_models/ · [S17] https://texttolab.com/blog/kokoro-tts-review , https://www.promptquorum.com/power-local-llm/kokoro-vs-elevenlabs · [S18] https://offlinetts.com/blog/tts-model-ranking-2026/ · [S19] https://discourse.weareopen.coop/news/best-ai-voice-overs-for , https://smallest.ai/blog/elevenlabs-alternatives-for-youtube-narration-best-voices-pricing-and-usage-tips · [S20] https://community.openai.com/t/where-is-the-usage-policy-for-ai-voiceovers/679737 , https://docs.agora.io/en/ai/models/tts/openai.md · [S21] https://costbench.com/software/ai-voice-tools/google-cloud-text-to-speech/free-plan/ · [S22] https://cloudprice.net/models/gemini-2.5-flash-preview-tts · [S23] https://speechify.ai/compare/build/text-to-speech/azure · [S24] https://docs.cartesia.ai/pricing · [S25] https://support.vapi.ai/t/32925970/minimax-voice-add-pronunciation-dict-parameter · [S26] https://ai.google.dev/gemini-api/docs/pricing , https://llmgateway.io/models/gemini-3.1-flash-image · [S27] https://ai.google.dev/gemini-api/docs/image-generation · [S28] https://ai.google.dev/gemini-api/docs/changelog , https://ecorpit.com/imagen-4-shutdown-gemini-flash-image-migration-2026/ · [S29] https://developers.openai.com/api/docs/guides/image-generation , https://pricepertoken.com/gpt-image-pricing · [S30] https://www.recraft.ai/pricing?tab=api · [S31] https://wavespeed.ai/blog/ai-guides/recraft-v4-style-api-guide/ , https://www.recraft.ai/docs/api-reference/pricing.md · [S32] https://developer.puter.com/tutorials/flux-api-pricing/ · [S33] https://pricepertoken.com/image/model/black-forest-labs-flux-2-pro , https://aident.ai/blog/fal-ai-image-pricing-per-image-vs-megapixel · [S34] https://pricepertoken.com/ideogram-pricing , https://developer.puter.com/ai/ideogram/ideogram-3.0/ · [S35] https://ideogram.ai/pricing/?pricing_tab=api · [S36] https://framia.converge.ai/page/en-US/blog/nano-banana-2-multilingual-text · [S37] https://cloud.google.com/archive/terms/generative-ai-indemnified-services-20260422 , https://terms.law/ai-output-rights/gemini/ · [S38] https://www.atlascloud.ai/blog/tips/openai-gpt-image-1.5-api-guide-next-generation-ai-image-generation · [S39] https://developer.puter.com/tutorials/stability-ai-api-pricing/ · [S40] https://longforecast.com/dollar-to-won-usd-to-krw-forecast-2017-2018-2019-2020-2021 · [S41] https://invideo.io/blog/open-source-image-models-licenses/ · [S42] https://www.spheron.network/blog/runpod-vs-vastai-2026/ , https://costbench.com/software/ai-gpu-cloud/vast-ai/ · [S43] https://support.google.com/youtube/answer/1311392 · [S44] https://gulfnews.com/technology/youtube-updates-monetisation-policies-ai-and-repetitive-content-ban-begins-july-15-1.500192660 , https://eliro.pro/blog/youtube-ai-content-rules-2026 · [S45] https://support.google.com/youtube/answer/14328491 · [S46] https://www.netinfluencer.com/youtube-terminates-ai-generated-fake-movie-trailer-channels/ , https://www.techspot.com/community/topics/youtube-demonetizes-fake-movie-trailer-channels-after-investigation.291540/ · [S47] https://www.404media.co/ai-generated-boring-history-videos-are-flooding-youtube-and-drowning-out-real-history/ · [S48] https://www.dexerto.com/youtube/youtubes-ai-slop-detector-incorrectly-targets-kurzgesagt-as-other-creators-fear-same-fate-3395930/ · [S49] https://techsmith.com/blog/ai-voices-avatars-in-training-videos , https://narrationbox.com/blog/why-viewers-drop-off-after-30-seconds-youtube , https://www.insideradio.com/free/edison-report-shows-listeners-want-humans-not-ai-hosting-podcasts/article_657e5407-3219-4840-9b44-01377c35e725.html · [S50] https://costbench.com/software/ai-media-apis/leonardo-ai-api/ · [S51] https://www.myarchitectai.com/blog/midjourney-apis , https://www.cometapi.com/does-midjourney-provide-an-api/ · [S52] https://muapi.ai/comparison/flux-lora-trainer · [S53] https://www.kmjournal.net/news/articleView.html?idxno=5563 · [S54] https://electrify.video/post/electrify-video-partners-announces-landmark-investment-in-simple-history , https://www.pluggedin.com/youtube-reviews/simple-history/ · [S55] https://screenwiseapp.com/guides/history-matters-youtube · [S56] https://becomeviral.com/blog/kings-and-generals-case-study , https://heepsy.com/youtube-profile/KingsandGenerals · [S57] https://www.overseeros.com/blog/best-faceless-youtube-channel-examples · [S58] https://www.mootion.com/use-cases/x-default/ugc/korean-history-overview · [S59] https://historikashorts.gumroad.com · [S60] https://fiverr.com/animatorathome/create-the-paint-explainer-style-animated-video (스타일 설명) · [S61] https://carat.im/en/prompt-gallery/korean-painting , https://carat.im/en/prompt-gallery/minhwa-style

## 부록(COO, 2026-10-01): muapi.ai 중계 경로 비교
| 항목 | muapi.ai (CLI 0.2.7 설치 검증, docs/OPEN_GENERATIVE_AI_SETUP.md) | 직접 계약(위 추천안) |
|---|---|---|
| TTS | **없음**(오디오는 Suno 음악뿐) → 어차피 별도 공급자 필요 | ElevenLabs / Google / Kokoro |
| 이미지·영상 | 키 1개로 103개 이미지 모델(flux-2-pro, nano-banana-pro, gpt-image-2, midjourney v7, imagen4) + veo/kling/wan/seedance 영상 | 모델별 키·약관 각각 |
| 가격 | 선불 크레딧 종량제. 공식 문서에 모델별 단가 없음(응답 JSON·playground에서 확인) → 가입 후 비교 필요 | 공식 단가표 있음 |
| 상업 이용·면책 | 공식 페이지에 조항 미확인 → **가입 후 약관 확인 전까지 보류** | Recraft 유료·Google 등은 명시 |
| 스타일 일관성 | 모델 옵션에 따름(seed·참조 이미지는 모델별) | Recraft style_id, Nano Banana 참조 이미지 |
| 판단 | 숏폼용 짧은 모션 영상(image-to-video)이 필요해질 때 유력. 이미지 기본 경로는 상업 조항이 확인된 직접 계약을 우선 | — |
