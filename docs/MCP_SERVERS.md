# MCP 서버 조사 — muapi · ruflo (2026-10-02, 스킬·도구 담당 리서처)

대표 질문(2026-10-02): "Open-Generative-AI(muapi) MCP 연결?" + "ruflo MCP 서버 연결 검토".
범위: 조사·초안만. `.mcp.json`·settings.json은 만들지도 바꾸지도 않았다(아래 블록은 **초안**). `npx ruflo init`·`muapi mcp install`류는 실행하지 않았다.
환경: `MUAPI_API_KEY` UNSET, `ANTHROPIC_API_KEY` UNSET → 생성·인증 호출 없음. 표시 규칙: **[실측]** 이 세션에서 직접 확인, **[문서]** 공식 문서·저장소 원문, **[추정]** 근거 부족.

## 0. 한 줄 결론
- **muapi**: 원격 MCP(`https://api.muapi.ai/mcp`, streamable-http, OAuth 2.0 + 동적 클라이언트 등록)가 **이미 있다** → claude.ai 커스텀 커넥터(ⓒ)가 프록시 없이 가능. 다만 생성은 곧 크레딧 소비라 허용 도구를 좁혀야 한다.
- **ruflo**: 핵심 서버(≈314개 도구)는 **로컬 전용**(stdio, 또는 localhost HTTP). 원격은 별도 서비스 **RuFlo AI Team**(`team.ruv.io/mcp`, 14개 도구, OAuth)뿐. 우리 흐름에 꼭 필요한 도구가 없고 보안 범위가 넓어 **도입 보류 추천**.

## 1. muapi MCP
| 항목 | 값 | 근거 |
|---|---|---|
| 로컬 서버 | `muapi mcp serve` (stdio, `--check-auth` 기본 → 키 없으면 시작 거부) | [실측] `~/.venvs/muapi/bin/muapi mcp --help`, muapi-cli 0.2.7 (setup.sh 블록으로 venv 재설치 후) |
| 원격 서버 | `https://api.muapi.ai/mcp` — streamable-http, serverInfo `muapi 0.1.0`, protocolVersion 2025-06-18 | [실측] 무인증 GET·`initialize` 응답 |
| 인증 | ① 헤더 `Authorization: Bearer <MUAPI_API_KEY>` ② 헤더 못 넣는 UI는 `https://api.muapi.ai/mcp/<KEY>`(키가 URL에 들어감 — 비추천) ③ OAuth 2.0 authorization_code+PKCE, 동적 등록 `POST /oauth/register`, 스코프 `generate:write generate:read files:write account:read keys:manage` | [실측] `/mcp` GET 안내문, `/.well-known/oauth-protected-resource`, `/.well-known/oauth-authorization-server` |
| 로컬 도구 25개 | 생성 6(image_generate·image_edit·video_generate·video_from_image·audio_create·audio_from_text) / 보정 4(upscale·bg_remove·face_swap·ghibli) / 편집 2(lipsync·clipping) / predict_result·upload_file / 키 3(list·create·delete) / 워크플로우 6(list·create·get·execute·status·outputs) / 계정 2(balance·**topup**) | [실측] 설치 패키지 `muapi/commands/mcp_server.py` TOOLS 목록 |
| 원격 도구 20개 | 위에서 워크플로우 6·upload_file 빠지고 `search_models`·`muapi_upload_image` 추가 | [실측] 원격 `tools/list`(무인증으로 목록 공개) |
| 문서상 수 | README "19 tools" — 실측(로컬 25/원격 20)과 다름 | [문서] github.com/SamurAIGPT/muapi-cli |
| 위험 도구 | `account_topup`(Stripe 결제 링크 생성), `keys_create/delete`(키 발급·삭제), `enhance_face_swap`·`edit_lipsync`(실존 인물 위험 — CLAUDE.md 금지 항목) | [실측] annotations readOnlyHint=false |

Claude Code 등록 예시(초안, **실행·커밋하지 않음**):
```bash
# ⓐ 대표 PC, 원격(권장 형태) — 키는 셸 변수로, 채팅·저장소에 쓰지 않는다
claude mcp add --transport http muapi https://api.muapi.ai/mcp --header "Authorization: Bearer $MUAPI_API_KEY"
# ⓐ' 대표 PC, 로컬 stdio
claude mcp add muapi -e MUAPI_API_KEY="$MUAPI_API_KEY" -- muapi mcp serve
```
```json
// ⓑ 클라우드 .mcp.json 초안 (저장소에 만들지 않음. ${VAR}는 Claude Code가 환경변수로 치환)
{ "mcpServers": { "muapi": { "type": "http", "url": "https://api.muapi.ai/mcp",
  "headers": { "Authorization": "Bearer ${MUAPI_API_KEY}" } } } }
```

## 2. ruflo MCP
| 항목 | 값 | 근거 |
|---|---|---|
| npm | `ruflo` 3.50.0, bin `ruflo → bin/ruflo.js`, 의존 `@claude-flow/cli ^3.50.0`, MIT, 수정 2026-10-02T00:21Z, 저장소 ruvnet/claude-flow(=ruflo) | [실측] `npm view ruflo` |
| 저장소 | github.com/ruvnet/ruflo HEAD `9e4fd17`(PR #6 때 97de39e에서 하루 새 갱신) | [실측] shallow clone(읽기만) |
| 시작 명령 | `claude mcp add claude-flow -- npx ruflo@latest mcp start` (stdio 기본). `mcp start -t http -p 8080` / `-t websocket`, host 기본 **localhost**, 엔드포인트 `/rpc`·`/health`·`/ws`. HTTP 모드 인증 옵션 없음 | [문서] README L195, `v3/@claude-flow/cli/src/commands/mcp.ts` |
| 도구 수 | README "314 MCP tools". 소스 `src/mcp-tools/*.ts`의 name 정의 ≈321(중복·내부 포함 [추정]) | [문서]+[실측 grep] |
| 범주(큰 순) | wasm-agent 27 · system 19 · browser 18+5 · metaharness 16 · **memory 14**+agentdb 6+embeddings 10 · **hooks 13** · **workflow 12** · **swarm 10**+coordination 7+hive-mind · autopilot 10 · claims 10 · ruvllm 10 · agent 9 · task 8 · session 8 · daa 8 · federation 7+9 · security 6 · policy 6 · neural 6 · managed-agent 6 · guidance 6 · config 6 · **terminal 5(`terminal_execute`=셸 실행)** · github 5 · mission 5 | [실측 grep, 근사치] |
| ai-team | 핵심 서버엔 없음. 별도 서비스 **RuFlo AI Team** v0.1.6: 원격 `https://team.ruv.io/mcp`(http), OAuth 2.1(인가 서버 `auth.cognitum.one`, 스코프 team:read/write/run), 14개 도구(team_create·team_list·team_board·run_*·task·memory·evidence…), Firestore 저장. "셸 실행·배포·구매 안 함"이라 명시 | [문서] plugins/ruflo-ai-team/README.md·.mcp.json, [실측] `/health` 200, tools/list 일부 |
| 요구 런타임 | Node ≥20. 선택 의존: `agentdb` 3.0.0-alpha, `agentic-flow` alpha, `better-sqlite3`(네이티브 빌드), `ruvector`, `@napi-rs/keyring` 등. `managed-agent` 도구 = `ANTHROPIC_API_KEY`+Managed Agents 베타(과금). flow-nexus = 외부 클라우드 가입 | [문서] package.json, SKILLS.md ruflo 절 |
| `init`가 바꾸는 파일 | `.claude/settings.json` 훅 병합, `.claude/helpers/*.cjs`(hook-handler·statusline·auto-memory), `.mcp.json` + `claude mcp add ruflo/ruv-swarm/flow-nexus`, `CLAUDE.md` 생성/덮어쓰기, `.claude/{agents,commands,skills}` 대량 생성, `.claude-flow/`, `.swarm/memory.db` → **CLAUDE.md "덮어쓰기 금지" 위반, 불가** | [문서] SKILLS.md L157(PR #6 조사) |
| 실행 확인 | `npx -y ruflo@3.50.0 --version` → **권한 분류기 차단("Code from External")**. 재시도 안 함 → `--help`·`--version` 실측 없음, 위 내용은 소스 읽기 기준 | [실측] |
| MCP만 연결 시 | `mcp start`는 `init` 없이도 동작(훅·CLAUDE.md 변경 없음) [문서 README]. 단 hooks_* 도구가 호출되면 파일 쓰기 가능 [추정] |

## 3. 연결 3안 비교표
### 3-1. muapi
| | ⓐ 대표 PC 로컬 Claude Code | ⓑ 클라우드 세션 `.mcp.json` | ⓒ claude.ai 커스텀 커넥터 | (현행) CLI 유지 |
|---|---|---|---|---|
| 설치 단계 | 2 (키 발급 → `claude mcp add --transport http …`) | 3 (키를 환경 설정에 → `.mcp.json` 커밋(대표 승인) → 새 세션). 원격 http라 세션마다 설치 0초, stdio면 venv ≈30초 | 2~3 (커넥터 추가에 URL 입력 → muapi.ai OAuth 동의). **프록시 불필요**(OAuth+DCR 실측) | 0 (setup.sh 블록 있음) |
| 월 비용 | 0원 + 생성 크레딧 종량 | 동일 | 동일 | 동일 |
| 보안 범위 | 키가 대표 PC에만. 훅·settings 변경 없음. 저장소 무변경 | `.mcp.json` 신규 = 저장소 설정 변경(대표 결정 필요). 키는 환경변수(`${MUAPI_API_KEY}`), 파일엔 없음. 분류기는 원격 http라 차단 가능성 낮음 [추정] | 키 대신 OAuth 토큰(스코프 지정 가능). 계정 전체 세션·Cowork에 노출. `/mcp/<KEY>` URL 방식은 키 노출이라 금지 | 키 = 환경변수, 도구 호출 = Bash 명령(권한 분류기가 매번 검사) |
| 우리 흐름 도구 3 | image_generate(플레이트), video_from_image(숏폼 모션), predict_result | 동일 | 동일 (+ search_models) | `muapi image generate … --download render/` |
| 결과물 위치 | 대표 PC → 저장소로 다시 옮겨야 함 | **세션 VM에 바로**(렌더 파이프라인과 같은 곳) | URL 반환 → 세션에서 다운로드 필요 | 세션 VM에 바로 |
| 추천 | △ 대표가 눈으로 샘플 볼 때만 | △ 설정 파일 변경 부담 대비 이득 작음 | ○ 2순위(쓰려면 이것) | **◎ 1순위** — 파이프라인 직결, 설정 변경 없음, 결제·키 도구가 아예 없음 |

### 3-2. ruflo
| | ⓐ 대표 PC 로컬 | ⓑ 클라우드 `.mcp.json` (stdio npx) | ⓒ 커스텀 커넥터 | 도입 안 함 |
|---|---|---|---|---|
| 설치 단계 | 2 (Node 20+ → `claude mcp add claude-flow -- npx ruflo@latest mcp start`) | 3 + 세션마다 `npx` 설치(@claude-flow/cli+선택 의존, 네이티브 빌드 포함 ≈1~3분 [추정]) | 핵심 서버: 원격 없음 → Cloudflare Tunnel+상시 PC 또는 VPS(월 ≈5~7천원 [추정]) + 인증 프록시 직접 구현. AI Team만: 2 (URL `https://team.ruv.io/mcp` + OAuth) | 0 |
| 월 비용 | 0원 | 0원(시간 비용) | 핵심: VPS ≈5~7천원+관리 [추정] / AI Team: 요금 미공개 | 0원 |
| 보안 범위 | 314개 도구 중 `terminal_execute`(셸)·hooks·config·browser·github 포함 → 사실상 셸 권한. `init` 안 하면 settings·훅 무변경 | 위 + 이 환경에서 **`npx ruflo` 실행이 분류기에 차단됨(실측)**, `.mcp.json` 신규 = 설정 변경, alpha 의존성 공급망 위험, `@latest`면 매 세션 버전 변동 | 핵심: localhost 서버를 인터넷에 노출(HTTP 모드 인증 없음) → **위험**. AI Team: 제3자(ruv.io·cognitum.one·Firestore)에 작업·메모 저장 | 없음 |
| 우리 흐름 도구 3 | (억지로 고르면) memory_store/search, workflow_run, swarm_init — 모두 COO+자식 세션·PROJECTS.md로 이미 대체 | 동일 | AI Team: team_create, run 관리, team_board | — |
| 추천 | △ 대표 개인 실험용만 | ✕ | ✕(핵심) / △(AI Team, 필요 생기면) | **◎** — PR #6 스킬(네이티브 Task만 사용)로 충분 |

## 4. 대표 결정 목록 (기본값 미적용 — 대표가 고를 때까지 아무것도 연결하지 않음)
| # | 질문 | 선택지 | 리서처 추천 | 근거 1줄 |
|---|---|---|---|---|
| M1 | muapi MCP 연결 방식 | ⓐ / ⓑ / ⓒ / CLI 유지 | **CLI 유지**(필요 시 ⓒ 추가) | 렌더는 세션 VM에서 하고 CLI가 이미 깔려 있어 MCP는 이득보다 결제·키 도구 노출이 큼 |
| M2 | ruflo MCP 연결 방식 | ⓐ / ⓑ / ⓒ / 도입 안 함 | **도입 안 함** | 필요한 도구가 없고, 셸 실행 도구 포함 + 이 환경에서 npx 차단 + init은 규범 위반 |
| M3 | 연결한다면 허용 도구 범위 | (a) 생성 6 + predict + search_models만 (b) +보정·업로드 (c) 전체 | **(a)** | `account_topup`·`keys_*`·`face_swap`·`lipsync`는 결제·키·실존 인물 위험이라 차단(`permissions.deny` 초안은 결정 후 별도) |
| M4 | ruflo 훅(`init`) 허용 | 허용 / 불허 | **불허** | settings.json 훅 병합·CLAUDE.md 덮어쓰기 = CLAUDE.md "덮어쓰기 금지" 정면 충돌 |

진행 시 대표가 할 일(자동화 안 함): M1=ⓒ면 claude.ai/customize/connectors에서 URL `https://api.muapi.ai/mcp` 추가 → muapi 로그인·동의. 그 뒤 새 세션에서 `search_models` 1회(읽기)로 검증.

## 5. 출처 (확인 2026-10-02)
- muapi-cli 저장소 README: https://github.com/SamurAIGPT/muapi-cli
- muapi 문서: https://muapi.ai/docs , https://muapi.ai/docs/agent-skills (MCP URL 미기재 → 저장소·엔드포인트로 확인)
- muapi 원격 MCP 실측: https://api.muapi.ai/mcp , https://api.muapi.ai/.well-known/oauth-protected-resource , https://api.muapi.ai/.well-known/oauth-authorization-server
- ruflo: https://github.com/ruvnet/ruflo (HEAD 9e4fd17, README·v3/@claude-flow/cli·plugins/ruflo-ai-team), `npm view ruflo`
- RuFlo AI Team: https://team.ruv.io/health , https://team.ruv.io/.well-known/oauth-protected-resource
- 미확인·추정: muapi 생성 단가, AI Team 요금, ruflo npx 설치 시간, 커넥터 경유 시 분류기 동작, ruflo 도구 수 grep 근사치.
