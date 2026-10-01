# Open Generative AI / muapi-cli 설치·검증 기록 (2026-10-01, 클라우드 세션)

역할: 환경 설정 담당(COO 세션) · 환경: Ubuntu 24.04.4 LTS, bash, root, GUI 없음(DISPLAY unset) · Node v22.22.0 · npm 10.9.4 · Python 3.11.15(기본) + 3.12.3(setup.sh 설치)
목표: 렌더 파이프라인(ffmpeg-assemble)의 장면 이미지·숏폼 영상 생성 공급자 후보로 muapi.ai(500+ 모델 단일 키)를 연동할 수 있는지 확인.

## 결론(2차 시도 후): **CLI 설치·모델 목록 검증 완료, 생성 검증은 키 대기.** 웹 앱 자체 호스팅 빌드는 권한 분류기가 계속 차단(대표 허용 후에도) → 중단. GUI 앱은 이 환경에서 불필요.

## 1. 공식 출처 확인 (설치본은 여기서만)
| 항목 | 값 | 확인 |
|---|---|---|
| 데스크톱·웹 앱 저장소 | https://github.com/Anil-matcha/Open-Generative-AI (MIT, v2.0.0, 2026-05-23 릴리스) | README·Releases 페이지 |
| 릴리스 파일 | macOS arm64/Intel .dmg, Windows .exe(서명 없음→SmartScreen 경고), Linux .AppImage/.deb | Releases |
| macOS 첫 실행 차단 해제 | `xattr -cr "/Applications/Open Generative AI.app"` 후 우클릭→열기 | README |
| 호스팅 웹 버전 | https://muapi.ai/open-generative-ai (무료 계정 가입, 설치 불필요) | README |
| CLI(npm) | `muapi-cli` 0.2.7, 저장소 https://github.com/SamurAIGPT/muapi-cli, MIT, 게시자 vadoo.tv | `npm view` |
| CLI(pip) | `muapi-cli` 0.2.7 (httpx·typer·rich·keyring 의존) | PyPI JSON |
| API 키 발급 | muapi.ai 로그인 → 메뉴 "API Keys"(/access-keys) | muapi.ai 홈 |
| 키 환경변수 | `MUAPI_API_KEY` (저장된 자격증명보다 우선) 또는 `muapi auth configure --api-key` | CLI README |
| 요금 | 선불 크레딧 종량제, 구독 없음, 크레딧 만료 없음. 모델별 단가는 문서에 없고 각 playground·응답 JSON에 표시. 상업 이용 조항·가입 무료 크레딧 액수는 공식 페이지에서 미확인 | docs/pricing |

## 2. 실행한 명령과 결과
| # | 명령 | 결과 |
|---|---|---|
| 1 | 앱·바이너리 흔적 검색(`which muapi`, /opt, /usr/local/bin, `npm ls -g`) | 미설치 |
| 2 | `npm view muapi-cli …` + 타르볼 내용 검사(설치 전) | postinstall이 GitHub Releases에서 플랫폼 바이너리 다운로드. 의존성 0 |
| 3 | `npm install -g muapi-cli` | **실패**: v0.2.7 릴리스에 `muapi-linux-x86_64` 없음(HTTP 404). 제거함 |
| 4 | `git clone --depth 1 --recurse-submodules …/Open-Generative-AI` → scratchpad | 성공(59MB, v2.0.0, 서브모듈 4개) |
| 5 | `npm run setup`(웹 버전 빌드) | **차단**: 권한 분류기 "Code from External" |
| 6 | `python3.12 -m pip install --user muapi-cli` | 실패: PEP 668 externally-managed |
| 7 | venv 생성 후 `pip install muapi-cli` | **차단**: 권한 분류기 "Untrusted Code Integration" |
| 8 | `muapi auth configure`, `muapi image models`, Image/Video Studio 생성 | **미실행**(설치 안 됨 + `MUAPI_API_KEY` UNSET) |

## 3. 남은 오류와 다음 조치
1. **설치 권한**: 대표가 이 작업을 원하면 Claude Code 권한 설정에 Bash 허용 규칙을 추가하거나(예: `pip install muapi-cli` 허용), 새 세션에서 수동 승인 모드로 실행. 또는 `scripts/setup.sh`에 넣을지 결정(지금은 넣지 않음).
2. **키**: muapi.ai 가입 → API Keys에서 발급 → 클라우드 환경 설정에 `MUAPI_API_KEY`로 입력(채팅에 붙여넣지 않음). 키가 있어야 `muapi image models`·이미지 1장·영상 1개 검증이 가능.
3. **GUI 앱은 이 환경에 맞지 않음**: 클라우드 VM은 화면이 없어 데스크톱 앱(.AppImage/.deb)을 열 수 없다. 파이프라인에는 CLI 또는 HTTP API만 쓴다. 대표 PC에서 눈으로 보려면 호스팅 웹 버전(무료 계정) 또는 데스크톱 앱을 쓰면 된다.
4. **공급자 결정과 묶어서**: muapi는 "여러 모델을 한 키로" 쓰는 중계 서비스라 편리하지만, 상업 이용 조항·면책·모델별 단가가 공식 문서에 없다. `docs/TOOLING_TTS_IMAGE.md`(리서치 진행 중) 비교표에 muapi를 한 행으로 넣어 직접 계약(Google·BFL·OpenAI 등)과 비교한 뒤 결정.

## 4. 초보자용 설명 (앱이 무엇인지)
- Open Generative AI = muapi.ai의 500여 개 생성 모델(Flux·Midjourney·Kling·Veo·Seedance 등)을 한 화면에서 쓰는 오픈소스 앱. 키 하나로 모든 모델을 쓰고, 쓴 만큼 크레딧이 빠진다.
- 탭: **Image Studio**(글→이미지, 이미지→이미지) / **Video Studio**(글→영상, 첫 프레임 이미지→영상) / **Lip Sync Studio**(사진·영상에 음성 맞추기) / **Audio Studio**(음악·오디오 생성). 그 밖에 Clipping·Workflow·Agent 탭.
- 우리 채널 순서(예정): 디자이너의 장면 프롬프트 → Image Studio(또는 CLI)로 플레이트 생성 → 썸네일 3장 → 숏폼용 Video Studio 짧은 모션(선택) → ffmpeg-assemble로 조립. 실존 인물·로고·립싱크 아바타는 쓰지 않는다(CLAUDE.md).

## 5. 2차 시도 (대표 "권한 허용" 후, 같은 날)
| # | 명령 | 결과 |
|---|---|---|
| 9 | `python3.12 -m venv ~/.venvs/muapi && ~/.venvs/muapi/bin/pip install muapi-cli` | **성공**. `muapi CLI 0.2.7` |
| 10 | `muapi auth status` | API key: not set, Config: /root/.muapi/config.json, Base URL https://api.muapi.ai/api/v1 |
| 11 | `muapi image models` | **성공(키 없이 동작)**: 103행. flux-2-pro/dev/flex, flux-kontext, imagen4(+fast/ultra), gpt-image-2, midjourney(v7), nano-banana-pro, hidream, wan2.7 등 |
| 12 | `muapi video models` | veo3/3.1/4, kling v2.1~v3 omni, wan2.1~2.7, seedance-pro 등 |
| 13 | `muapi models list` 에서 TTS 검색 | **TTS·음성 모델 없음**(오디오는 suno 음악뿐) → TTS는 별도 공급자 필요 |
| 14 | `git clone Open-Generative-AI && npm run setup` | **차단**(분류기, 설명 없음). 재시도 안 함 |
| 15 | `muapi auth configure` / 이미지·영상 생성 | **미실행**: `MUAPI_API_KEY` UNSET |

- setup.sh에 muapi-cli venv 설치 블록 추가, ENV.md에 `MUAPI_API_KEY` 행(후보) 추가.
- 검증 상태: 자동화 조건 "`muapi image models`가 모델 목록 출력" ✅ / 이미지 1장·영상 1개 생성 ❌(키 없음) / 앱이 경고 없이 열림 ❌(GUI 없는 환경, 해당 없음).
- 다음: 대표가 muapi.ai 가입 → API Keys 발급 → 환경 설정에 `MUAPI_API_KEY` 입력 → 새 세션에서 `muapi image generate "<장면 프롬프트>" --model flux-2-pro --download render/test`로 1장 생성 → 비용·품질 확인 → `docs/TOOLING_TTS_IMAGE.md` 비교표와 함께 공급자 확정.
