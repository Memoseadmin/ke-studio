# ECC(Everything Claude Code) 도입 검토 — 설치 전 제안서

작성 2026-10-02 / 검토 대상: https://github.com/affaan-m/ECC · 커밋 `c05b2d6614f62f6db0047669aa4eefb223d478f9` · v2.2.3 · LICENSE **MIT**(Affaan Mustafa 2026, 21행 표준문)
방법: 임시 디렉터리에 `git clone --depth 1`만 수행(스크립트·설치 마법사 실행 없음), 검토 후 임시 디렉터리 삭제. **이 문서는 제안이며 아무것도 설치하지 않았다.**

## 1. 저장소 구조와 전제
| 구성 | 수량 | 메모 |
|---|---|---|
| skills/ | 293개(SKILL.md 293, 파일 585, 본문 76,343행) | origin 메타: ECC 208·community 45·직접포팅 8·병원 기여 4·기타 4·**표기 없음 24** |
| agents/ | 68개 | 대부분 언어별 reviewer/build-resolver(코딩). 비코딩: marketing-agent, agent-evaluator, chief-of-staff, seo-specialist |
| commands/ | 94개 | 플러그인 전용 shim 다수(`ecc:` 네임스페이스). save/resume-session·checkpoint·learn은 `~/.claude/session-data/` 전제 |
| rules/ | common 10파일(704행) + 언어팩 21 | `.claude/rules/`에 넣으면 매 턴 로드. common도 TDD·커밋·빌드 중심 |
| hooks/hooks.json | PreToolUse 9·PostToolUse 5·Stop 7·SessionStart/End·PreCompact | 전부 `node run-with-flags.js`→`scripts/hooks/*.js`(56개)→`scripts/lib`(178파일, scripts/ 3.6MB) 의존 |
| the-longform/shortform-guide.md | — | ECC 사용 가이드. 영상 롱폼·숏폼과 무관 |

클라우드 세션 제약 확인: 플러그인(`/plugin install`, enabledPlugins) 미로드 → agents·rules의 `ecc:` 호출 규약과 commands shim은 그대로 쓸 수 없다. 스킬 폴더·에이전트 md·`.claude/settings.json` hooks만 유효. 세션 VM은 매번 새로 생성되므로 `~/.claude/`에 쓰는 ECC 메모리·세션 저장은 **휘발**된다(우리는 이미 `docs/HANDOFF.md`를 저장소에 커밋하는 방식).

## 2. 콘텐츠 운영에 쓸모 있는 것 (후보 표)
컨텍스트 비용 = 스킬 이름+description이 매 턴 올라가는 양(설명 1개 평균 ≈320자 ≈ 80토큰). 복사 = `.claude/skills/ecc-<스킬>/` 원문 그대로.
| 경로 | 무엇을 하나 | 우리 이득 | 본문/비용 | 복사 | 추천 |
|---|---|---|---|---|---|
| skills/content-engine | 플랫폼별(YouTube·TikTok·뉴스레터) 콘텐츠 시스템, 출처 우선, 금지 패턴, 품질 게이트 | writer·marketer의 숏폼/카드뉴스 변주 기준 | 132행 / 80tok | 가능 | **도입** |
| skills/article-writing | 예시로 추출한 '사람 목소리'로 롱폼 집필, 금지 표현 목록 | 대본·설명란·뉴스레터 톤 통일 | 80행 / 60tok | 가능 | **도입** |
| skills/agent-self-evaluation | 작업 후 5축(정확·완결·명료·실행성·간결) 1~5점 자가 채점 | CLAUDE.md "자가 검증표" 규범을 표준 루브릭으로 | 182행+예시·템플릿 폴더 / 80tok | 가능 | **도입** |
| skills/growth-log | 완료 작업에서 '사건'이 아닌 '재사용 규칙'을 뽑는 로그 템플릿 | HANDOFF "실패한 시도와 이유" 품질 향상 | 128행 / 70tok | 가능 | **도입** |
| skills/living-docs-governance | 문서를 헌법/지도/상태/이력 역할로 나눠 썩지 않게 관리 | CLAUDE.md·PLAN·HANDOFF·PROJECTS 역할 정리 | 137행 / 90tok | 가능 | **도입** |
| skills/council | 4관점 회의로 모호한 go/no-go 결정 | COO의 주제 선정·게이트 판단 | 204행 / 50tok | 가능 | 중간안 |
| skills/research-ops | 증거 우선 최신 리서치 절차 | researcher 절차 보강. 단 `exa-search`·`deep-research`(MCP) 참조 → 일부만 유효 | 113행 / 80tok | 가능 | 중간안(보류 가능) |
| skills/market-research | 출처 표기 시장·경쟁 조사 | 제휴 카테고리 조사 | 87행 / 70tok | 가능 | 중간안 |
| skills/crosspost | 플랫폼별로 다르게 배포(동일 복붙 금지) | 숏폼·카드뉴스 교차 배포 규칙 | 123행 / 70tok | 가능 | 중간안 |
| skills/strategic-compact | 단계 경계에서 수동 /compact 권고 기준 | "컨텍스트 절반 시 종료 절차" 판단 보조(연동 hook 없이 지침만) | 156행 / 60tok | 가능 | 중간안 |
| skills/context-budget | 스킬·에이전트·규칙 컨텍스트 소비 감사 | 스킬 96개 정리 근거 산출 | 186행 / 80tok | 가능 | 중간안 |
| skills/iterative-retrieval | 서브에이전트가 필요한 컨텍스트를 단계적으로 보충하는 패턴 | 직원 위임 프롬프트 설계 | 212행 / 60tok | 가능 | 중간안 |
| skills/token-budget-advisor | 답변 깊이 25/50/75/100% 선택 제시 | 메인 세션 토큰 절약 | 122행 / 60tok | 가능 | 중간안 |
| skills/skill-stocktake | 스킬·커맨드 품질 감사(Quick/Full) | 기존 96개 스킬 정리 | 195행+3파일 / 70tok | 가능 | 중간안 |
| skills/safety-guard | 파괴적 명령(rm -rf, push --force, --no-verify) 경고 지침 | hooks 설계 참고(아래 §3) | 76행 / 60tok | 가능 | 중간안 |
| agents/agent-evaluator | 5축 루브릭으로 산출물 평가(sonnet, 읽기 전용 Bash) | 검수 PR 전 2차 평가자. 단 본문이 `skills/agent-self-evaluation/SKILL.md` 경로를 참조(우리 경로와 다름, 원문 수정 불가) | 215행 | `.claude/agents/` | 중간안(경로 불일치 감수) |
| agents/marketing-agent | 캠페인·카피 전략가(WebSearch 가능) | 기존 marketer와 중복 큼 | 159행 | 가능 | 보류 |
| rules/common/agents.md "Delegation Completion Contract" | 위임하면 결과 수집까지 책임, 대기 상태로 턴 종료 금지 | COO↔직원 운영에 직결. 단 rules 파일 전체는 `ecc:` 플러그인 규약 | 68행 | `.claude/rules/`(매 턴 로드) | 보류: 3줄 요지만 CLAUDE.md에 반영은 대표 결정 |
| skills/video-editing | 컷 편집→Remotion→보이스 | docs/SKILL_CANDIDATES.md에 이미 별건(fal·ElevenLabs MCP 의존 13파일) | 337행 | 가능 | 보류(별건 유지) |
| skills/security-scan, gateguard, delivery-gate, continuous-learning-v2, unified-memory | AgentShield npm·pip gateguard·python 데몬·Memory Vault 등 외부 설치/`~/.claude` 상주 전제 | 클라우드 세션에서 휘발·설치 필요 | — | 부적합 | 보류 |
| competitive-platform-analysis, benchmark-methodology, competitive-report-structure, brand-discovery | 경쟁사 스코어링·브랜드 인터뷰 | 유용하나 **origin 미표기**(제3자 기여 가능성) | — | 가능 | 보류(출처 확인 후) |

**제외**(코딩·인프라 전용, 약 250개): 언어/프레임워크 패턴·reviewer·build-resolver 전부, TDD·e2e·eval-harness, docker/k8s/terraform, DB·API·보안취약점 헌팅, 블록체인·결제·예측시장, 의료 4종, 제조·물류·관세·에너지, 네트워크·홈랩, Blender·taste(뮤직비디오 LUT), ECC 자체 운영(configure-ecc, ecc-guide, ecc-recipes, nasiko, hermes, openclaw), MCP 전제(exa, firecrawl, fal-ai-media, social-publisher 21회 참조). rules/common 10파일도 TDD·커밋·빌드 중심이라 제외. commands 94개는 `~/.claude` 또는 `ecc:` 전제라 전부 제외.

## 3. hooks 분석(복사 대상이 아님 → 자작 권고)
- 사실: ECC hooks는 모두 Node 래퍼가 `~/.claude/plugins/ecc*` 경로를 탐색해 `scripts/lib`를 require. 복사하려면 `scripts/`(3.6MB)를 저장소에 넣고 `CLAUDE_PLUGIN_ROOT`를 잡아야 하며, 매 도구 호출마다 node 프로세스가 뜬다. 저장 경로는 `os.homedir()` 기반(`ECC_AGENT_DATA_HOME`로 변경 가능)이지만 세션 VM 휘발.
- 네트워크: hook 스크립트 56개 중 외부 HTTP 호출은 `mcp-health-check.js`(MCP 서버 헬스 프로브)·`plan-canvas-pending.js`(로컬 서버)만. 텔레메트리 전송 없음. `desktop-notify`는 osascript/pwsh(리눅스 무효). 결론: 원격 유출 위험은 낮으나 **우리 환경에서 얻는 게 거의 없다.**
- 비밀키 유출 방지는 `governance-capture.js`가 패턴(AWS·JWT·gh 토큰·`.env` 경로)을 기록만 하고 차단하지 않음(옵트인 `ECC_GOVERNANCE_CAPTURE=1`).
- 권고: ECC hooks를 복사하지 말고, CLAUDE.md 규칙(".env 읽지 않기")과 safety-guard 패턴을 **자작 2줄 hook**으로 프로젝트 `.claude/settings.json`(현재 없음, 새 파일)에 넣는다. jq 1.7·node 22·python 3.11은 세션 VM에 있음. 예시(차단은 exit 2):
```json
{"hooks":{"PreToolUse":[
 {"matcher":"Read|Bash|Grep|Glob","hooks":[{"type":"command","command":"jq -r '[.tool_input.file_path,.tool_input.command,.tool_input.path,.tool_input.pattern]|map(.//\"\")|join(\" \")' | grep -Eq '(^|[ /])\\.env([. ]|$)' && { echo 'BLOCK: .env 접근 금지(CLAUDE.md)' >&2; exit 2; }; exit 0"}]},
 {"matcher":"Bash","hooks":[{"type":"command","command":"jq -r '.tool_input.command//\"\"' | grep -Eq 'rm -rf|push +(-f|--force)|--no-verify|reset --hard' && { echo 'BLOCK: 파괴적 명령(safety-guard 패턴)' >&2; exit 2; }; exit 0"}]}
]}}
```
  위험: 정규식이 과하게 걸릴 수 있음(예: `.env.example` 문서 언급도 차단) → 도입 후 1세션 관찰.

## 4. 추천 묶음 3안
| 안 | 구성 | 매 턴 추가 컨텍스트(추정) | 절차 | 위험 |
|---|---|---|---|---|
| **(가) 최소 — 권고** | 스킬 5: content-engine, article-writing, agent-self-evaluation, growth-log, living-docs-governance + 자작 hooks 2개 | ≈ 1.6k자 ≈ **400토큰**(현재 96개 ≈ 48.7k자 ≈ 12k토큰의 3%) | ① `ecc/install` 브랜치에서 scratch clone(SHA 고정) ② `cp -r skills/<s> .claude/skills/ecc-<s>` 5회 ③ `diff -r` 0 확인 ④ docs/SKILLS.md에 팩 `ecc` 행(URL·SHA·MIT·5개) 추가 ⑤ `.claude/settings.json` 신규 생성(§3 JSON) ⑥ 검수 PR | hooks 과차단, agent-self-evaluation의 부속 scripts/는 실행하지 않음(참조만) |
| (나) 중간 | 스킬 15: (가)5 + council, research-ops, market-research, crosspost, strategic-compact, context-budget, iterative-retrieval, token-budget-advisor, skill-stocktake, safety-guard; 에이전트 1~2: agent-evaluator(+marketing-agent 선택) | ≈ 4.8k자 ≈ **1.2k토큰** + 에이전트 설명 ≈ 100토큰 | (가)와 동일 + `cp agents/agent-evaluator.md .claude/agents/ecc-agent-evaluator.md`(frontmatter `name: agent-evaluator`는 원문 유지 → 등록명 충돌 여부 1회 확인) | research-ops가 참조하는 exa/deep-research 부재로 절차 일부 공회전, agent-evaluator의 스킬 경로 불일치, marketer와 중복 |
| (다) 전체 복사 — **비추천** | 스킬 293·에이전트 68·커맨드 94·rules | 스킬 설명 94.2k자+이름 5.4k자 ≈ **25k토큰/턴**(현재의 2배 추가, 합계 ≈ 37k ≈ 200k 창의 18%) + 에이전트 68개 ≈ 2.5k토큰 + rules 704행 ≈ 5k토큰 | — | 250여 개 코딩 스킬이 매 턴 비용만 소모, `ecc:` 호출 규약·`~/.claude` 전제 커맨드 전부 무효, python/sh 부속 파일 수백 개가 저장소에 유입, 세션 종료 절차(컨텍스트 절반) 도달이 빨라짐 |

## 5. 대표가 결정할 것
1. (가) 최소안으로 갈지, (나)까지 넓힐지. (다)는 반대.
2. 자작 hooks 2개(.env 차단·파괴적 명령 차단)를 `.claude/settings.json`에 신설할지 — ECC 코드 복사가 아니라 우리 파일이므로 CLAUDE.md "원문 변경 금지"와 무관.
3. rules/common/agents.md의 "위임 완결 계약" 3줄 요지를 CLAUDE.md 작업 규범에 반영할지(CLAUDE.md 수정은 대표 승인 사항).

## 6. 자가 검증표
| 기준 | 결과 |
|---|---|
| clone만 수행, 스크립트·install.sh·setup 미실행 | 충족(`git clone --depth 1` 1회, 이후 cat/grep/wc만) |
| 저장소 변경 = 이 문서 1개, git 명령(저장소) 0회 | 충족(`.claude/`·docs 다른 파일 미변경) |
| SHA·LICENSE 확인 | c05b2d66… / MIT 표준문. 부속 LICENSE 2개(taste-application/scripts, pi/core) 존재 → 해당 스킬은 제외 대상 |
| 후보 표에 경로·기능·이득·비용·복사 가능·추천 포함 | 충족(도입 5·중간 10·보류 7군·제외 요약) |
| hooks 네트워크 호출 점검 | 56개 스크립트 grep: 외부 HTTP는 mcp-health-check(MCP 프로브)만, 텔레메트리 없음 |
| 3안 각 항목 수·컨텍스트 추정·절차·위험 | 충족(§4) |
| 120행 이내 | 충족 |
| 임시 디렉터리 삭제 | 작성 직후 `rm -rf …/scratchpad/ecc` 실행(핸드백에 결과 기재) |
