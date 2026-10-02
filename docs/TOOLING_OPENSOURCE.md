# KE Studio 도구 조사 2: 오픈소스·무료 소스 (2026-10-02)

요청(대표): "상용 TTS·이미지 조합보다 획기적인 것, GitHub·무료·전 세계 오픈소스 중 퀄리티 높고 이런 영상에 쓸 수 있는 것."
범위: 오픈소스 TTS / 이미지 / 영상 / **코드 모션그래픽** / 무료·저가 컴퓨트 / 자동화 파이프라인 사례. 설치·실행 없이 웹 조사만 했다(조사 세션, 2026-10-02).
전제는 `docs/TOOLING_TTS_IMAGE.md`와 같다: 월 음성 약 5만 자(≈50분), 이미지 약 120장, 숏폼 20개/월, 1 USD ≈ 1,400원(추정).
**표기**
- 원화 금액은 모두 추정치다.
- ★(GitHub 스타)와 Elo는 2026-10-02 조회값을 반올림했다. Elo 일부는 페이지 요약을 거쳐 ±오차가 있을 수 있다.
- 각 행 끝의 [O#]는 맨 아래 출처 번호다. 확인하지 못한 항목은 "미확인"으로 적었다.

## 0. 한 줄 결론
"획기적인" 답은 **더 좋은 생성 모델이 아니라 생성을 줄이는 것**이다.
- 장면의 움직임·한글·종이·지도는 **코드 모션그래픽(Remotion 등)** 으로 만든다. AI 티가 원천적으로 없고 비용은 0원이다.
- AI 생성은 "민화 배경 플레이트"에만 쓴다. Apache-2.0 이미지 모델에 **자체 스타일 LoRA**를 학습해 쓴다.
- 오픈소스 TTS는 상업 이용 가능한 1위가 Elo 1092로, 상용 상위(1270~1320)와 격차가 아직 크다. 그래서 **음성만은 상용(저가)을 유지**하고 Kokoro를 0원 백업으로 둔다.

## 1. 요약 표 — 5개 조합 비교

| 조합 | 구성 | 월 비용(추정) | 품질 | 운영 난이도 | AI 티 위험 | 라이선스 |
|---|---|---|---|---|---|---|
| 상용 1안(기존) | ElevenLabs v3/v4 + Nano Banana 2 | ≈ 48,000원 | 음성 최상(Elo 1320), 이미지 상 | 낮음(API 2개) | **중**: 생성 이미지 슬라이드 + Ken Burns. 404 Media가 지목한 "슬롭" 외형과 가까움 | 유료 플랜 상용 OK |
| 가성비안(기존) | Google TTS + Recraft style_id | ≈ 8,000원 | 음성 상(1272), 이미지 중상 | 낮음 | 중 | 상용 OK |
| OSS-①<br>품질 우선 | Chatterbox(fal API) 또는 Step-Audio-EditX(시간제 GPU) + Qwen-Image-2512(fal) + 자체 LoRA + LTX-2.3 숏폼 훅(오디오 동시 생성) | ≈ 11,000원 + LoRA 1회 0.3~1.3만원 | 음성 중(1011~1092), 이미지 상(999), 영상 중상 | 중(API 3개 + LoRA) | 중: 영상 생성 클립이 AI 티의 최대 원천 | 모두 Apache/MIT. LTX는 연매출 $10M 미만 무료 + AI 라벨 의무 |
| OSS-②<br>비용 0 근접 | Kokoro(VM CPU, 0원) + FLUX.2 klein 4B 또는 Z-Image Turbo(fal, 장당 ≈$0.005) + 영상 생성 없음 | ≈ 1,000원 | 음성 중하(1063, 감정폭 좁음), 이미지 중 | 중(Kokoro 설치·청크 분할) | 중상: 단조 음성 + 정지 이미지 | Apache |
| **OSS-③<br>코드 모션그래픽 하이브리드 (추천)** | **Remotion**(코드 애니메이션: 한지·한글 획·지도·자막) + Z-Image Turbo 자체 민화×한지 LoRA(fal) + Gemini Flash TTS 유료 티어(Kokoro 백업) + 숏폼 훅만 선택적으로 LTX-2.3 | ≈ 7,500원 + LoRA 1회 ≈ 3,000~7,000원 | 음성 상(1272), 비주얼 **고유**(채널 전용 모션 언어) | 중상: 첫 3편은 장면 템플릿 제작 부담, 이후 재사용 | **낮음**: 움직임·글자·종이가 코드라서 생성 이미지 비중이 줄어든다 | Remotion은 직원 3명 이하 무료(4명↑ $25/석·월). 대안 HyperFrames는 Apache-2.0 |

월 비용 산식(추정)
- Gemini TTS: 50분 × 25 tok/s ≈ 75k 오디오 토큰 × $9/1M ≈ $0.7
- 이미지: 120장 × 1MP × $0.005 ≈ $0.6
- 숏폼 훅: 20개 × 5초 × $0.04/s = $4
- 합계 ≈ $5.3 ≈ 7,500원. OSS-①의 TTS는 Chatterbox fal 5만 자 × $0.025/1천 자 = $1.25.
- 다섯 조합 모두 월 20만 원 상한의 1/4 이하다.

## 2. COO 추천: OSS-③ 하이브리드

### 이유
1. **AI 티를 구조적으로 없앤다.** 상위 페이스리스 역사 채널(Simple History, History Matters, Kurzgesagt)의 공통점은 "단일 고유 모션 언어"였다(TOOLING_TTS_IMAGE.md C절). 코드 애니메이션은 그 언어를 채널 자산으로 만들고, 매 편 재사용할수록 단가가 내려간다.
2. **한글 장면이 우리 채널의 차별점**인데, 오픈 이미지 모델은 한글 렌더링을 공식 지원하지 않는다(Qwen-Image·Z-Image 모두 영·중만 명시) [O20][O22]. 한글 획 리빌은 코드로만 정확하게 만들 수 있다.
3. **비용은 상용 1안의 1/6 수준(≈7,500원)이다.** CPU VM에서 Remotion 렌더가 가능하고(헤드리스 Chromium, 이 VM에 사전 설치) [O30], GPU는 fal 호출로만 쓴다.
4. 라이선스가 명확하다.
   - Remotion: 1인 회사 무료 [O31]
   - Z-Image·klein 4B: Apache-2.0 [O20][O21]
   - Gemini 유료 티어: 상용 OK
   - 한국 지역 배제 조항이 있는 모델(Hunyuan 계열·MiniMax H3)은 전부 뺐다.
5. 오픈소스 TTS는 지금 상업 OK 최고점이 1092(Step-Audio-EditX, GPU 12GB 필요)여서 품질 손해가 크다 [O1]. 음성은 Gemini 유료(1272)를 쓰고, Kokoro(1063, CPU, 인라인 IPA)를 키 장애 시 0원 백업으로 둔다.

### 첫 샘플: EP002 S01 "1504, 돌담의 벽서 3장"(14초, 36단어) 절차
사전 조건
- 설치는 `scripts/setup.sh` 반영 + 대표 OK 후에 한다. 이번 조사 세션에서는 아무것도 설치하지 않았다.
- 키는 저장소에 넣지 않는다.

환경변수(대표가 클라우드 환경에 입력)

| 이름 | 용도 | 비고 |
|---|---|---|
| `FAL_KEY` | fal 공식 SDK가 읽는 이름 | `IMAGE_API_KEY`에 같은 값을 매핑해도 됨 |
| `GEMINI_API_KEY` | Gemini TTS | `TTS_API_KEY`에 매핑. **유료 티어 프로젝트** 키 |
| `REMOTION_LICENSE` | — | 불필요(1인 무료 조건). 4명 이상이 되면 회사 라이선스 |

| 단계 | 담당 | 무엇을·어디서 | 산출물 |
|---|---|---|---|
| 1 플레이트 | designer → producer | fal `fal-ai/z-image/turbo` [O22]로 "밤 돌담 + **빈** 한지 3장, 민화 플랫, 인물·문자 없음" 16:9를 4안 생성(시드 기록). LoRA는 기준 플레이트 10~20장이 승인된 뒤 `fal-ai/z-image-trainer`(1,000스텝 ≈ $2.26)로 학습 [O23] | `episodes/EP002/design/s01-plate-*.png`(썸네일 크기만 커밋) |
| 2 음성 | producer | Gemini 3.8 Flash TTS 유료 티어로 S01 36단어 생성. 같은 문장을 Kokoro(VM CPU, `[Hangul](/hˈɑːŋɡuːl/)` 인라인 IPA)로도 생성해 블라인드 A/B [O2][O3] | `render/EP002/s01.{gemini,kokoro}.wav`(커밋 제외) |
| 3 모션 | producer | Remotion 컴포지션 `S01Hook` 구성 [O30][O32]<br>① 한지 3장 순차 슬라이드인·말림<br>② 자모 획 리빌(자체 제작 중심선 JSON, 대본 메모대로 **실제 문장 금지**. 흐린 자모만)<br>③ "1504" 타이포<br>`durationInFrames` = TTS 길이 × 30. 출력은 ProRes 4444 알파 또는 VP9 WebM 알파 | `render/EP002/s01-motion.mov` |
| 4 합성 | producer | ffmpeg: 플레이트(Ken Burns) + 모션 알파 overlay + 한지 그레인 multiply + TTS + 자막 번인. 현 `ffmpeg-assemble` JSON에 장면별 `overlay_video` 필드를 추가하는 것은 **스킬 수정 제안**이고 이번 범위 밖 | `render/EP002/s01.mp4` + 컨택트시트 |
| 5 비교 | COO | 같은 S01을 상용 1안(생성 이미지 + ElevenLabs)으로도 렌더해 대표에게 2개 프레임 + 오디오를 PR로 블라인드 비교 | PR 코멘트 1개 |

#### 명령어 수준 절차 (이 세션에서는 실행하지 않음 — 키 입력과 setup.sh 반영 후 producer가 실행)
- 키 값은 저장소·채팅에 적지 않는다. 대표가 클라우드 환경 설정에 이름만 맞춰 넣는다:
  - `FAL_KEY` ← fal.ai 대시보드 → API Keys
  - `GEMINI_API_KEY` ← aistudio.google.com/apikey, 결제가 연결된 프로젝트
- 모델 ID·옵션명은 공식 문서 기준이다. 실행 직전에 링크를 다시 확인한다 [O3][O22][O30].
```bash
# 0) 준비 (setup.sh에 추가할 항목 — 대표 OK 후): Node 22 기존, Chromium 사전 설치됨
#    npx create-video@latest render/remotion-ke --template blank   # Remotion 프로젝트(커밋은 소스만)
#    python3 -m pip install kokoro soundfile; apt-get install -y espeak-ng   # Kokoro 백업용
mkdir -p render/EP002 episodes/EP002/design
# 1) 플레이트 (fal, Z-Image Turbo, 동기 엔드포인트) — 응답 JSON의 images[0].url을 내려받는다
curl -sS https://fal.run/fal-ai/z-image/turbo -H "Authorization: Key $FAL_KEY" -H "Content-Type: application/json" \
  -d '{"prompt":"Korean minhwa folk-painting flat illustration, night, old stone wall with three blank hanji paper sheets pasted on it, bold ink outlines, obangsaek palette muted, hanji paper texture, no text, no people, no logos","image_size":"landscape_16_9","num_images":4,"seed":1504}' \
  > render/EP002/s01-plate.json
# 2a) 음성 (Gemini TTS, 응답은 base64 PCM 24kHz mono s16le). 모델 ID는 GEMINI_TTS_MODEL로 분리(예: gemini-2.5-flash-preview-tts, 최신 ID는 [O3]에서 확인)
curl -sS "https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_TTS_MODEL}:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Read in a calm documentary tone: In the summer of 1504, three anonymous notices appeared in the Korean capital. ..."}]}],
       "generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":"Kore"}}}}}' \
  | python3 -c 'import sys,json,base64;d=json.load(sys.stdin);sys.stdout.buffer.write(base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]))' > render/EP002/s01.gemini.pcm
ffmpeg -f s16le -ar 24000 -ac 1 -i render/EP002/s01.gemini.pcm render/EP002/s01.gemini.wav
# 2b) 음성 백업 (Kokoro, CPU, 키 불필요): KPipeline(lang_code="a")(text, voice="af_heart") → 24kHz wav, 고유명사는 [word](/IPA/) 인라인
# 3) 모션 (Remotion, 알파 출력). S01Hook 컴포지션의 durationInFrames = ceil(TTS초 × 30)
npx remotion render S01Hook render/EP002/s01-motion.mov --codec=prores --prores-profile=4444   # 알파 픽셀 포맷은 [O30] 문서대로
# 4) 합성 (플레이트 Ken Burns + 모션 알파 + 음성). 한지 그레인·자막은 ffmpeg-assemble 규칙을 따른다
ffmpeg -loop 1 -i render/EP002/s01-plate.png -i render/EP002/s01-motion.mov -i render/EP002/s01.gemini.wav \
  -filter_complex "[0:v]scale=2112:1188,zoompan=z='min(zoom+0.0005,1.08)':d=1:s=1920x1080:fps=30[bg];[bg][1:v]overlay=0:0:shortest=1[v]" \
  -map "[v]" -map 2:a -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -shortest render/EP002/s01.mp4
```
성공 기준(샘플)
- 14초 ±1초, 1920×1080 30fps
- 화면에 읽히는 한글 문장 0개
- 인물·로고 0개
- 컨택트시트 1장 + 오디오 2종(Gemini/Kokoro)을 PR 코멘트로 블라인드 비교

Remotion 대신 쓸 대안: **HyperFrames**(HeyGen, Apache-2.0, HTML/CSS → 헤드리스 Chrome → FFmpeg, 인원 제한 없음) [O33]. 저장소가 2026년 신생이라 안정성은 미확인이다. 그래서 1순위는 성숙도가 높은 Remotion(★61k, 2026-10 활동)으로 둔다.

## 3. 대표가 결정할 것 (3개)
1. **비주얼 방향:** EP002 S01 A/B 샘플을 본 뒤 "코드 모션그래픽 하이브리드(OSS-③)"를 채널 표준으로 할지, "생성 이미지 슬라이드(상용 1안·가성비안)"를 유지할지.
2. **음성:** Gemini Flash TTS 유료(≈1천원/월, Elo 1272) / ElevenLabs(≈3.1만원, 1320) / Kokoro 오픈소스(0원, 1063) 중 기본값. 추천은 Gemini, Kokoro는 백업.
3. **자체 스타일 LoRA 학습:** 1회 약 3천~1.3만원 지출 여부와 학습 소재. 공개 민화 LoRA는 상업 권한이 불명확하거나 비상업이어서 쓰지 않는다. 학습 소재는 둘 중 하나다:
   - 승인된 자체 플레이트
   - 공공누리 1유형 등 상업 이용 가능한 퍼블릭 도메인 민화(해당 여부는 미확인, legal-reviewer 확인 필요)
- (2026-10-02, 대표 결정 A8) **Remotion 라이선스 확인 완료**: 1인 회사 = Free License 해당(개인·직원 ≤3 영리법인, 상업 이용 가능). 근거·가격은 docs/SKILLS.md "Remotion 라이선스 확인", 설치 줄은 scripts/setup.sh.

---

## A. 오픈소스 TTS (영어 내레이션)

블라인드 품질의 출처는 Artificial Analysis Speech Arena(오픈 웨이트 필터)다 [O1]. 전체 93개 중 오픈 웨이트는 16개.
- 오픈 웨이트 상위: Breeze TTS 2 1206, Fish S2 Pro 1117, Step-Audio-EditX 1092, Voxtral 1079, Kokoro 1063.
- 상용 비교: Eleven v4 1320, Qwen-Audio-3.1-TTS-Plus 1291, Gemini 3.8 Flash TTS 1272.
- Breeze·Fish·Voxtral은 상업 불가이므로, **상업 OK 1위는 Step-Audio-EditX, 2위는 Kokoro**다.

미확인으로 남긴 것:
- TTS Arena V2(HF)는 JS 렌더링이라 순위를 읽지 못했다 [O4].
- Reddit r/LocalLLaMA 블라인드 비교는 크롤러가 차단돼 링크를 확보하지 못했다.
- 기존 문서 [S18]의 Chatterbox ≈1011을 인용한다.

| 모델 | 저장소·★·최근 | 가중치 라이선스(상업) | CPU / GPU | 호스팅·가격 | 우리 적합도·발음 제어 | 출처 |
|---|---|---|---|---|---|---|
| **Kokoro-82M** | hexgrad/kokoro ★9.1k, v1.0 2025-01 | Apache-2.0 ✅ | **CPU 가능** | DeepInfra $0.62/1M자 | 상업 OK 중 CPU 1위. **인라인 IPA `[word](/IPA/)`** → Hunminjeongeum 등 직접 지정. 감정폭 좁음, 10분+는 문단 청크 필요 | [O2][O3][O5] |
| Chatterbox (EN·Multilingual V3 23개 언어·Turbo·Nano) | resemble-ai/chatterbox ★26.6k, Turbo 2025-12 | MIT ✅, Perth 워터마크 | Nano: 8코어 CPU 3배속(README) | fal $0.025/1천 자 | 감정 태그. IPA 입력 미확인 | [O6][O7] |
| Step-Audio-EditX 3B | HF stepfun-ai, 2025-11 | Apache-2.0 ✅ | GPU ≈12GB(AWQ 6~8GB) | 미확인 → RunPod 4090 $0.34/h | 상업 OK 품질 1위(1092). 편당 GPU 수 분(추정) | [O1][O8] |
| Qwen3-TTS 0.6B/1.7B | QwenLM/Qwen3-TTS ★13.6k, 2026-01 | Apache-2.0 ✅ | GPU | 미확인 | 한국어 포함 10개 언어, 보이스 디자인 | [O9] |
| MOSS-TTS v1.5 / Nano | OpenMOSS/MOSS-TTS ★4.2k, 2026-06 | Apache-2.0 ✅ | Nano 4코어 CPU 실시간 | 미확인 | "수십 분 롱폼 안정" 주장(README, 미검증) | [O10] |
| Kyutai Pocket TTS 100M | kyutai-labs/pocket-tts ★9.7k, 2026-08 | MIT(가중치 별도 표기 미확인) | CPU 2.3~2.5배속 | — | CPU 전용 설계. 품질 Elo 미확인 | [O11] |
| Dia 1.6B / Dia2 | nari-labs ★19.4k / 1.2k | Apache-2.0 ✅ | Dia GPU 10GB, Dia2 CPU 폴백 | — | 대화형. Dia2는 1회 약 2분 상한 | [O12] |
| Orpheus 3B | canopyai ★6.3k, 2025-05 | Apache(Llama 백본 조건 미확인) | GPU(llama.cpp CPU 경로 언급) | — | 감정 태그 | [O13] |
| Zonos v0.1 | Zyphra ★7.2k | Apache ✅ | GPU 6GB+ | — | eSpeak 음소 | [O14] |
| CosyVoice 3 | FunAudioLLM ★23.8k | Apache(가중치 별도 미확인) | GPU | — | 한국어 지원, CMU 음소 | [O15] |
| Higgs Audio v2 / v3 | boson-ai ★8.4k | v2: 연간 활성 사용자 10만 미만 무료 + 표기 / v3: **비상업** | GPU | — | 조건부 | [O16] |
| Fish S2 Pro / OpenAudio S1 | fishaudio ★32.9k | **Research License ❌** | — | — | 제외 | [O17] |
| F5-TTS | SWivid ★15.3k | **CC-BY-NC ❌** | — | — | 제외 | [O18] |
| XTTS-v2 | coqui-ai ★46k | **CPML 비상업 ❌**(Coqui 폐업으로 라이선스 구매 불가) | — | — | 제외 | [O19] |
| VibeVoice / IndexTTS2.5 / Voxtral / Breeze 2 | MS ★54.6k / bilibili ★24.3k / Mistral / BreezeBlue | VibeVoice: TTS 코드 철회, 연구용 / IndexTTS: 상업은 문의 / Voxtral: CC BY-NC / Breeze: 비상업 | — | — | 제외 | [O1][O19] |

판단
- **오픈소스 TTS로 "AI 티"를 줄이기는 아직 어렵다.** 상업 OK 최고점과 상용 상위 사이에 180~230 Elo 격차가 있다.
- Kokoro는 0원·CPU·IPA라는 세 가지 장점으로 백업과 숏폼 대량 테스트에 적합하다.
- 6개월 뒤 재조사할 후보: Step-Audio-EditX, MOSS-TTS, Qwen3-TTS.

## B. 오픈소스 이미지

품질 근거: AA Text-to-Image Arena(2026-10, 전체 1위 GPT Image 2.5 = 1197) [O24]. 라이선스 패밀리 정리 [O25].

| 모델 | URL·출시 | 가중치 라이선스 | 우리 상업 이용 | Elo | VRAM | 호스팅 가격 | 출처 |
|---|---|---|---|---|---|---|---|
| **Z-Image-Turbo 6B** | HF Tongyi-MAI/Z-Image-Turbo, 2025-11 | Apache-2.0 | ✅ | 941 | ≤16GB | fal $0.005/MP | [O20][O22] |
| **FLUX.2 [klein] 4B** | HF black-forest-labs, 2026-01 | Apache-2.0 | ✅ | 863 | ≈13GB | fal $0.005/MP | [O21] |
| **Qwen-Image-2512** / Edit-2511 | HF Qwen, 2025-12 | Apache-2.0 | ✅ | 999 | 20B, ≈40GB(추정) | fal $0.02/MP | [O26] |
| FLUX.2 [dev] 32B / [klein] 9B | HF black-forest-labs | FLUX Non-Commercial: **수익 활동에 모델 사용 = 비상업 목적 아님**, 출력은 상업 가능 | 자체 호스팅 ❌, 상용 라이선스를 가진 API(fal·BFL)로만 | 1000 / 941 | 대형 | fal $0.012/MP | [O27] |
| SD3.5 Large/Medium | stabilityai, 2024-10 | Community(연매출 $1M 미만 무료) | ✅ 조건부 | 839 / 759 | — | — | [O28] |
| HiDream-I1 / Lumina 2.0 | 2025-04 / 2025-03 | MIT(Llama 3.1 텍스트 인코더 조건 병행) / Apache | ✅ | 873 / 781 | — | — | [O24] |
| Qwen-Image-2.1 | HF Qwen, 2026-09-20 | **Qwen Research License ❌** | ❌ | 1034(오픈 1위) | 32GB | — | [O29] |
| Ideogram 4.0 오픈 웨이트 | 2026-06 | 가중치 비상업 | ❌(자체 호스팅) | 1011 | 24GB | — | [O24] |
| HunyuanImage 2.1 / 3.0 | Tencent | **"DOES NOT APPLY IN … SOUTH KOREA"** | ❌ 한국 배제 | 995 | — | — | [O34] |

### B-2. 스타일 일관성 도구
학습형(LoRA)
- fal FLUX LoRA fast: 1,000스텝 $2
- fal klein 4B trainer: 1,000스텝 $5
- **fal Z-Image trainer: 1,000스텝 $2.26** [O23]
- 직접 학습 도구 ostris/ai-toolkit(MIT, ★12.2k): FLUX.2·Z-Image·Qwen·Wan·LTX 지원, 24GB 설정 예시 있음 [O35]

학습 없이 참조 이미지로
- FLUX.2 다중 참조(@image1~)
- Qwen-Image-Edit-2511 다중 입력(일관성·드리프트 완화)

권장(추정)
- 1차 플레이트: Z-Image Turbo + 자체 민화×한지 LoRA
- 보정: Qwen-Image-Edit-2511 참조 편집
- 셋 다 Apache-2.0이라 API와 자체 호스팅 어느 쪽이든 안전하다.

### B-3. 공개 민화·한지 LoRA (HF·CivitAI 검색 결과) [O36][O37]

| LoRA | 베이스 | 라이선스·권한 | 판단 |
|---|---|---|---|
| Noveled/sd-minhwa-model-lora-sdxl 외 2개 | SDXL | openrail-m | 구형·저품질 |
| gguk2/Minhwa-LoRA-v1 | SD1.5 | openrail-m | 구형·저품질 |
| gptsdilike/Minhwa-01-Lora | — | cc-by-nc-4.0 | **상업 불가** |
| Hamsoon22/minhwa-tiger-lora-flux-01 | FLUX.1-dev | MIT 표기 | 베이스가 비상업이라 자체 호스팅 불가 |
| CivitAI "김홍도 화풍"(Z-Image), ShinYunBok-LoRA | — | 상업 권한 미확인 | **실존 화가 화풍 모사라 피한다** |
| CivitAI #81845 Traditional Korean Painting | SDXL 체크포인트 | Image/Rent/Sell 허용 | 구형 |

"hanji" 스타일 LoRA는 없다. → **자체 LoRA 학습이 사실상 유일한 길이고, 학습된 LoRA 자체가 채널의 고유 자산이 된다.**

### B-4. 한글
오픈 모델 카드는 영·중만 명시하고 한국어 품질은 미확인이다 [O20][O26]. 기존 규칙대로 **이미지 안에 한글을 생성하지 않고**, 한글은 Remotion/Pillow 오버레이로 넣는다.

## C. 오픈소스 영상 (숏폼 훅 3~5초·장면 모션)

AA Video Arena(오픈 웨이트, 오디오 포함):
- I2V: MiniMax H3 1181(제외) > MAGI-2 Preview 1093 > **LTX-2.5 Fast 1038** > LTX-2.3 Pro 949 [O38]
- T2V: H3 1139 > LTX-2.5 Fast 950 [O39]

무음 기준(2차 출처): LTX-2.3 Pro 1165, HunyuanVideo-1.5 1120, Wan 2.2 A14B 1119 [O40].

| 모델 | 라이선스 / 한국 | 소리 동시 생성 | 실행 | 호스팅 가격 | 판단 | 출처 |
|---|---|---|---|---|---|---|
| **LTX-2 / 2.3 / 2.5** (Lightricks) | LTX Community: 연매출 $10M 미만 무료, 제재국만 배제(**한국 OK**), **AI 생성 표기 의무** | ✅ | FP8 양자화본 제공 | fal 2.3 Fast 1080p $0.04/s, 2.5 Fast 720p ≈$0.09/s(2차) | **훅 1순위.** 20클립 × 5초 ≈ $4/월 | [O41][O42] |
| Wan 2.2 TI2V-5B / A14B | Apache-2.0 ✅ | ❌ | 5B: 4090에서 720p 5초 9분 미만 | fal A14B 720p $0.08/s, 5B $0.15/편 | 무음 2순위. **Wan 2.5~2.7은 API 전용(가중치 비공개)** | [O43] |
| MAGI-2 Preview 114B | Apache-2.0 ✅ | ✅ | H100 8장, 10초 고정 | Sand.ai API(가격 미확인) | 품질 높지만 자체 운영은 비현실적 | [O44] |
| Ovi 1.1 (Character.AI) | Apache-2.0 ✅ | ✅ | 24~32GB | 미확인 | 후보 | [O45] |
| Kandinsky 5.0 Lite | MIT ✅ | ❌ | offload 가능 | 미확인 | 보조 | [O46] |
| SkyReels V2/V3 | Skywork Community(지역 조항 미확인) | V2 ❌ | 14~51GB | 미확인 | 보류 | [O47] |
| CogVideoX-5B / Mochi 1 | 상업 조건 미확인 / Apache(미확인) | ❌ | — | — | 구형(480p 8fps 등) | [O48] |
| HunyuanVideo 1.5 | **한국 배제 ❌** | ❌ | — | — | 제외 | [O34] |
| MiniMax H3 | 한국·미국·EU 배제 ❌ | ✅ | — | — | 제외(SKILL_CANDIDATES.md) | — |

판단
- 생성 영상은 AI 티가 가장 강한 소재다. **숏폼 첫 3초 훅에만 제한적으로** 쓰고, 롱폼 장면 모션은 D절의 코드 애니메이션 + Ken Burns로 만든다.
- LTX를 쓰면 AI 라벨이 의무다. 우리 규칙(AI 생성물 공개 라벨)과 일치한다.

## D. "획기적" 대안 — 코드로 만드는 모션그래픽

| 도구 | 저장소·★·최근 | 라이선스·상업 | 헤드리스 CPU(리눅스) | 우리 적합도 | 출처 |
|---|---|---|---|---|---|
| **Remotion** (React) | remotion-dev/remotion ★61.4k, 2026-10 | 개인·**직원 3명 이하** 무료. 4명 이상 Creators $25/석·월, Automators 렌더당 $0.01(최소 $100/월) | ✅ 헤드리스 Chrome. 알파 출력: ProRes 4444·VP8/VP9 WebM·PNG 시퀀스. 속도는 2~4 vCPU에서 1080p 실시간 0.3~1배(추정) | **1순위.** 공식 Claude Code용 Agent Skills(★4.8k, 라이선스 미확인) 존재. `<Audio>`·자막·`@remotion/lottie` | [O30][O31][O32] |
| **HyperFrames** (HeyGen) | heygen-com/hyperframes ★55.3k, 2026-10 | Apache-2.0, "렌더 수수료·상업 임계값 없음" | ✅ HTML/CSS → Chrome → FFmpeg, 결정적 출력 | 1순위 대안. 에이전트 스킬 21개 | [O33] |
| Revideo | midrender/revideo ★4.1k | MIT | ✅ `renderVideo()` 헤드리스 API | Motion Canvas 계열 중 자동화에 적합 | [O49] |
| Motion Canvas | ★19.2k, 2026-07 | MIT | △ 렌더하려면 에디터를 띄워야 함 | 자동화 부적합 | [O50] |
| Manim CE / ManimGL | ★41.2k / ★94.4k | MIT | CE는 CPU(Cairo) ✅ / GL은 OpenGL 필요 | 지도·도표·연표에 강함. `Write`는 한글을 **외곽선 순서**로 그려 붓글씨 느낌이 없음(추정) | [O51] |
| Lottie (lottie-web) | ★32.1k, 2025-09 | MIT | puppeteer-lottie나 Remotion으로 영상화 | 아이콘 루프용. 원본 제작은 AE 등이 필요 | [O52] |
| p5.js | ★24.1k | LGPL-2.1(출력물 무관) | 헤드리스 캡처(미확인) | **한지 섬유·먹 번짐 생성 텍스처** 제작용 | [O53] |
| Blender bpy | GPL(출력물은 제작자 소유) | — | Cycles CPU는 느림. EEVEE는 OpenGL 필요 → GPU 없는 VM에서는 매우 느림 | 비추천(CPU VM) | [O54] |
| Theatre.js / Rive | ★12.7k(공개 저장소 2024-08 정지) / 런타임 MIT, 에디터 $9~/월 | — | 렌더러 아님 / GUI 도구 | 부적합 | [O55][O56] |
| editly / MoviePy 2 | ★5.5k / ★14.9k, MIT | — | ✅ | 사내 ffmpeg-assemble과 역할 중복 | [O57] |

### D-2. 한글 자모 획 그리기 — 우리만의 무기
- 공개 한글 획순 데이터는 사실상 하나뿐이다: `MagisterAdamus/hangeul-stroke-order`(자모 35자 다이어그램 SVG, **CC BY-SA 4.0** → 동일조건 조항이 걸림) [O58]. 한자용 hanzi-writer·KanjiVG 같은 애니메이션 데이터는 한글판이 없다 [O59].
- 그래서 **자모 약 30개의 중심선(median) 경로를 직접 그려 자체 JSON으로 만든다**(추정 1~2일). 음절 조합 규칙으로 배치하고, SVG `stroke-dasharray` 리빌 위에 붓 질감 stroke나 폰트 글리프 마스크를 얹는다. Remotion·HyperFrames에서 바로 구현할 수 있다.
- 이 데이터는 EP002(한글 탄압사) 같은 한글 회차와 인스타 카드뉴스(정지 프레임) 양쪽에서 재사용하는 **독점 자산**이 된다. 생성 AI로는 정확한 획순을 재현할 수 없다.

### D-3. 사내 ffmpeg 파이프라인 결합
- 장면 JSON에 장면 유형 필드를 추가해, 해당 장면만 Remotion으로 **장면 단위 알파 클립**을 렌더한다. 나머지는 지금처럼 플레이트 + Ken Burns로 처리한다.
- 겹치는 순서: 플레이트 → 모션 알파 overlay → 한지 그레인 → 자막 번인. 자막·loudnorm은 기존 스킬을 유지한다.
- 타이밍은 TTS 길이를 `durationInFrames`로 넘겨 맞춘다.
- 렌더된 프레임을 VLM이 보고 레이아웃을 교정하는 Code2Video의 "Critic" 루프(F절)를 검수 자동화에 차용할 수 있다.

## E. 무료·저가 컴퓨트·API (상업 이용 조건 포함)

| 옵션 | 무료분·단가 | 상업 이용·약관 주의 | 판단 | 출처 |
|---|---|---|---|---|
| HF ZeroGPU / PRO | 일일 쿼터: 무료 5분 / PRO($9/월) 40분, 초과 $1/10분. Gradio Spaces 전용 | Spaces 상업 이용 조건 미확인 | 데모 확인용 | [O60][O61] |
| HF Inference Providers | 월 크레딧: 무료 $0.10 / PRO $2, 공급자 단가에 마크업 없음 | 공급자별 약관 | 소량 테스트 | [O62] |
| Google AI Studio 무료 티어 | TTS 무료 티어 있음. 이미지(Nano Banana 2)는 무료 티어 없음 | **입력이 제품 개선에 쓰이고 사람이 검토할 수 있음**, EEA·UK·스위스 사용자 대상이면 유료 필수 | 미공개 대본은 넣지 않는다 → 유료 티어 | [O63][O64] |
| fal.ai | 시작 크레딧 ≈$20(2차, 미확인), 종량제. 서버리스 H100 $2.49/h~ | 모델별 상용 라이선스 제공 | **이미지·영상·LoRA 주 공급자로 권장** | [O65][O66] |
| Replicate | T4 $0.81/h, L40S $3.51/h, H100 $5.49/h | — | 대안 | [O67] |
| RunPod | 4090 $0.34/h(커뮤니티)~$0.74/h, L40S $0.79/h~, H100 PCIe $1.99/h~ | — | 자체 LoRA 학습·Step-Audio용 | [O68] |
| Vast.ai | 4090 ≈ $0.25~0.40/h(2차, 시세 변동) | — | 최저가지만 호스트 품질 편차 | [O69] |
| Modal | Starter 월 $30 크레딧, T4 ≈ $0.59/h | — | 월 $30 안에서 Kokoro·Step-Audio 서버리스가 사실상 무료(추정) | [O70] |
| Kaggle / Colab 무료 | Kaggle 주 약 30h GPU(2차) / Colab 무료는 SSH·원격 제어·UI 우회 금지 | Kaggle 상업 조건 미확인 / Colab 무료는 자동화 파이프라인에 부적합 | 수동 실험용 | [O71][O72] |
| GitHub Actions | 공개 저장소 무제한(4 vCPU), 비공개 2,000분/월 | 약관상 "소프트웨어 프로젝트의 제작·테스트·배포와 무관한" 사용과 CDN·서버리스 사용 금지 → **영상 렌더팜으로 쓰는 것은 약관 위험**(해석) | 쓰지 않는다. 렌더는 세션 VM에서 | [O73] |

## F. 오픈소스 자동화 파이프라인 사례 (★1k 이상, 2025~26 활동)

| 저장소 | ★ / 최근 / 라이선스 | 구조 | 가져올 것 | 가져오면 안 되는 것 |
|---|---|---|---|---|
| harry0703/MoneyPrinterTurbo [O74] | 128k / 2026-10 / MIT | LLM 대본 → Edge·Azure 등 TTS → Pexels 스톡 → 자막 → FFmpeg | TTS 단어 타임스탬프 자막, 작업 이력·배치 구조 | **스톡 슬라이드 + 주제만 넣으면 대량 생산** → inauthentic content 정책(2025-07-15)이 겨냥하는 템플릿 양산형 [O75] |
| gyoridavid/short-video-maker [O76] | 1.4k / 2025-06 / MIT(Remotion은 별도) | Kokoro-js → whisper.cpp → Pexels → **Remotion**. REST·MCP 제공 | **CPU만으로 Kokoro + whisper.cpp + Remotion 구성**(2 vCPU·3GB) — 우리 구조와 가장 가깝다 | Pexels 배경 |
| showlab/Code2Video [O77] | 2.1k / 2026-08 / MIT(ICML 2026) | Planner → Coder(Manim) → Critic(VLM이 레이아웃 교정) | **렌더 프레임 VLM 검수 루프** | 수학 교육풍 스타일 |
| TIGER-AI-Lab/TheoremExplainAgent [O78] | 1.5k / 2025-07 / MIT | LLM → Manim 계획 → 코드 → 렌더 오류 자가수정 | 렌더 실패 자동 수정 루프 | 활동 정지 |
| HKUDS/ViMax [O79] | 12.5k / 2026-09 / MIT | 감독·작가·프로듀서 멀티에이전트 → 이미지 → Veo·Seedance 영상 | 스토리보드 단계 설계, 캐릭터 일관성 관리 | 생성 영상 중심 → 비용과 AI 티 큼 |
| Anil-matcha/AI-Youtube-Shorts-Generator [O80] | 5.2k / 2026-10 / 라이선스 미확인 | 롱폼 → Whisper → LLM 하이라이트 → 9:16 크롭 | **자사 롱폼에서 숏폼 5개 추출** 로직(shorts-cut 보강) | 남의 영상 입력 |
| showlab/Paper2Video [O81] | 2.4k / 2026-03 / MIT | 논문 → 슬라이드·음성·커서 | 장면별 TTS 길이와 화면 동기화 | 슬라이드 외형 |
| RayVentura/ShortGPT [O82] | 8.0k / 2025-02 / MIT | LLM → TTS → 스톡·웹 → MoviePy | 편집 단계 JSON 마크업 아이디어 | 웹 소스 수집, 정지 상태 |
| linyqh/NarratoAI [O83] | 11.3k / 2026-09 / MIT | **기존 영상**에 AI 해설 + 재편집 | 없음 | **타인 영상 재편집 = 저작권·재사용 콘텐츠 위험** |

공통 결론
- 공개 파이프라인 대부분은 "스톡 + TTS + 자막" 템플릿이다. 우리는 **구조(장면 JSON → TTS → 비주얼 → ffmpeg)만 이미 갖고 있고**, 가져올 것은 세 가지로 한정한다:
  - 자막 타임스탬프
  - VLM 검수 루프
  - 자사 롱폼 → 숏폼 추출
- 스톡 영상·타인 영상·웹 스크래핑 소스는 쓰지 않는다.

## 출처 (확인 날짜: 전부 2026-10-02)
[O1] https://artificialanalysis.ai/text-to-speech/leaderboard?open_weights=true · [O2] https://github.com/hexgrad/kokoro · [O3] https://ai.google.dev/gemini-api/docs/pricing · [O4] https://huggingface.co/spaces/TTS-AGI/TTS-Arena-V2 · [O5] https://deepinfra.com/hexgrad/Kokoro-82M · [O6] https://github.com/resemble-ai/chatterbox , https://huggingface.co/ResembleAI/chatterbox-turbo · [O7] https://fal.ai/models/fal-ai/chatterbox/text-to-speech · [O8] https://huggingface.co/stepfun-ai/Step-Audio-EditX · [O9] https://github.com/QwenLM/Qwen3-TTS · [O10] https://github.com/OpenMOSS/MOSS-TTS · [O11] https://github.com/kyutai-labs/pocket-tts · [O12] https://github.com/nari-labs/dia , https://github.com/nari-labs/dia2 · [O13] https://github.com/canopyai/Orpheus-TTS · [O14] https://github.com/Zyphra/Zonos · [O15] https://github.com/FunAudioLLM/CosyVoice · [O16] https://github.com/boson-ai/higgs-audio , https://huggingface.co/bosonai/higgs-audio-v2-generation-3B-base/blob/main/LICENSE · [O17] https://huggingface.co/fishaudio/s2-pro · [O18] https://github.com/SWivid/F5-TTS · [O19] https://huggingface.co/coqui/XTTS-v2 , https://github.com/microsoft/VibeVoice , https://github.com/index-tts/index-tts , https://huggingface.co/mistralai/Voxtral-4B-TTS-2603 , https://www.orcarouter.ai/blog/breeze-tts-2-tops-open-weights-speech-arena
[O20] https://huggingface.co/Tongyi-MAI/Z-Image-Turbo · [O21] https://huggingface.co/black-forest-labs/FLUX.2-klein-4B , https://fal.ai/models/fal-ai/flux-2/klein/4b · [O22] https://fal.ai/models/fal-ai/z-image/turbo · [O23] https://fal.ai/models/fal-ai/z-image-trainer , https://fal.ai/models/fal-ai/flux-lora-fast-training , https://fal.ai/models/fal-ai/flux-2-klein-4b-base-trainer · [O24] https://artificialanalysis.ai/text-to-image/arena/leaderboard-text · [O25] https://invideo.io/blog/open-source-image-models-licenses/ · [O26] https://huggingface.co/Qwen/Qwen-Image-2512 , https://huggingface.co/Qwen/Qwen-Image-Edit-2511 , https://fal.ai/models/fal-ai/qwen-image-2512 · [O27] https://bfl.ai/legal/non-commercial-license-terms , https://fal.ai/models/fal-ai/flux-2 · [O28] https://stability.ai/community-license-agreement · [O29] https://huggingface.co/Qwen/Qwen-Image-2.1 , https://www.creativeainews.com/articles/qwen-image-2-1-research-license-commercial-use-2026/
[O30] https://github.com/remotion-dev/remotion , https://www.remotion.dev/docs/transparent-videos · [O31] https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md , https://www.remotion.pro/license · [O32] https://github.com/remotion-dev/skills · [O33] https://github.com/heygen-com/hyperframes · [O34] https://huggingface.co/tencent/HunyuanImage-3.0/blob/main/LICENSE , https://huggingface.co/tencent/HunyuanImage-2.1/blob/main/LICENSE , https://huggingface.co/tencent/HunyuanVideo-1.5/blob/main/LICENSE · [O35] https://github.com/ostris/ai-toolkit · [O36] https://huggingface.co/api/models?search=minhwa · [O37] https://civitai.com/api/v1/models?query=korean%20painting , https://civarchive.com/models/2420622 · [O38] https://artificialanalysis.ai/video/leaderboard/image-to-video/open-weights · [O39] https://artificialanalysis.ai/video/leaderboard/text-to-video/open-weights
[O40] https://magichour.ai/blog/ltx-2-3-vs-wan-2-2 · [O41] https://huggingface.co/Lightricks/LTX-2 · [O42] https://fal.ai/models/fal-ai/ltx-2.3/image-to-video/fast , https://aireiter.com/blog/ltx-2-5-api-pricing-guide · [O43] https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B , https://fal.ai/models/fal-ai/wan/v2.2-a14b/image-to-video · [O44] https://huggingface.co/sand-ai/MAGI-2-preview · [O45] https://github.com/character-ai/Ovi · [O46] https://huggingface.co/kandinskylab/Kandinsky-5.0-T2V-Lite-sft-5s · [O47] https://github.com/SkyworkAI/SkyReels-V2 · [O48] https://huggingface.co/zai-org/CogVideoX-5b · [O49] https://github.com/midrender/revideo
[O50] https://github.com/motion-canvas/motion-canvas · [O51] https://github.com/ManimCommunity/manim , https://docs.manim.community/en/stable/reference/manim.mobject.text.text_mobject.Text.html , https://github.com/3b1b/manim · [O52] https://github.com/airbnb/lottie-web , https://github.com/transitive-bullshit/puppeteer-lottie · [O53] https://github.com/processing/p5.js · [O54] https://www.blender.org/about/license/ , https://devtalk.blender.org/t/blender-2-8-unable-to-open-a-display-by-the-rendering-on-the-background-eevee/1436 · [O55] https://github.com/theatre-js/theatre · [O56] https://rive.app/pricing · [O57] https://github.com/mifi/editly , https://github.com/Zulko/moviepy · [O58] https://github.com/MagisterAdamus/hangeul-stroke-order · [O59] https://github.com/chanind/hanzi-writer , https://kanjivg.tagaini.net/
[O60] https://huggingface.co/docs/hub/spaces-zerogpu · [O61] https://huggingface.co/pricing · [O62] https://huggingface.co/docs/inference-providers/pricing · [O63] https://ai.google.dev/gemini-api/terms · [O64] https://ai.google.dev/gemini-api/docs/pricing · [O65] https://fal.ai/pricing · [O66] https://costbench.com/software/ai-media-apis/fal-ai/ · [O67] https://replicate.com/pricing · [O68] https://www.runpod.io/pricing · [O69] https://costbench.com/software/ai-gpu-cloud/vast-ai/ · [O70] https://modal.com/pricing · [O71] https://gpuperhour.com/blog/free-cloud-gpus-and-credits · [O72] https://research.google.com/colaboratory/faq.html · [O73] https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features , https://docs.github.com/en/billing/concepts/product-billing/github-actions
[O74] https://github.com/harry0703/MoneyPrinterTurbo · [O75] https://www.plagiarismtoday.com/2025/07/08/youtube-targets-inauthentic-content/ · [O76] https://github.com/gyoridavid/short-video-maker · [O77] https://github.com/showlab/Code2Video · [O78] https://github.com/TIGER-AI-Lab/TheoremExplainAgent · [O79] https://github.com/HKUDS/ViMax · [O80] https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator · [O81] https://github.com/showlab/Paper2Video · [O82] https://github.com/RayVentura/ShortGPT · [O83] https://github.com/linyqh/NarratoAI
