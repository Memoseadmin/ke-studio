# 스킬 팩 등록부

설치 방식: 임시 디렉터리에 clone → LICENSE·README 확인 → `skills/*/`를 `.claude/skills/<팩>-<스킬>/`로 원본 그대로 복사(`diff -r` 차이 0 확인). 네 팩 모두 `commands/`·`agents/` 폴더가 없어 복사할 커맨드·에이전트는 없음. finance·legal의 `.mcp.json`·`CONNECTORS.md`(외부 커넥터 설정)는 복사하지 않음. 설치 스크립트는 실행하지 않음.
SKILL.md 내용(`name` 포함)은 원본 그대로지만, 이 환경의 Skill 도구는 **폴더명**으로 등록한다(확인: 세션 스킬 목록에 `finance-variance-analysis` 등으로 표시). 호출·에이전트 지정은 폴더명을 쓴다.

설치일: 2026-10-01

| 팩 | 출처 | 커밋 SHA | 라이선스 | 스킬 수 |
|---|---|---|---|---|
| finance | https://github.com/anthropics/knowledge-work-plugins (finance/) | da38ec1ee89d41e5380e652a97382695003396e7 | Apache-2.0 | 8 |
| legal | https://github.com/anthropics/knowledge-work-plugins (legal/) | da38ec1ee89d41e5380e652a97382695003396e7 | Apache-2.0 | 9 |
| marketing-skills | https://github.com/coreyhaines31/marketingskills | 5b2c0007766c6a1cf1d53fd8fc73e979e0821022 | MIT | 50 |
| social-media-skills | https://github.com/charlie947/social-media-skills | 8cefb5b6d03757885faa6918bd8bfaef202a83db | MIT | 17 |
| design | https://github.com/anthropics/knowledge-work-plugins (design/) | da38ec1ee89d41e5380e652a97382695003396e7 | Apache-2.0 | 7 |
| example-skills | https://github.com/anthropics/skills (skills/canvas-design, skills/theme-factory만) | 8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4 | Apache-2.0 | 2 |
| last30days | https://github.com/mvanhorn/last30days-skill (skills/last30days) | 5103ba478b380552207a3754b74c7655d64208cd | MIT | 1 |
| ecc | https://github.com/affaan-m/ECC (skills/ 중 선별 10개) | c05b2d6614f62f6db0047669aa4eefb223d478f9 | MIT | 10 |

## 포함 스킬
- **finance**: audit-support close-management financial-statements journal-entry journal-entry-prep reconciliation sox-testing variance-analysis 
- **legal**: brief compliance-check legal-response legal-risk-assessment meeting-briefing review-contract signature-request triage-nda vendor-check 
- **marketing-skills**: ab-testing ad-creative ads ai-seo analytics aso attribution churn-prevention co-marketing cold-email community-marketing competitor-profiling competitors content-strategy copy-editing copywriting cro customer-research directory-submissions emails events free-tools image influencer-marketing launch lead-magnets marketing-council marketing-ideas marketing-loops marketing-plan marketing-psychology offers onboarding paywalls popups pricing product-marketing programmatic-seo prospecting public-relations referrals revops sales-enablement schema seo-audit signup site-architecture sms social video 
- **social-media-skills**: analytics-dashboard content-matrix gemini-carousel gemini-infographic graphic-designer hook-generator newsletter-voice niche-research pinned-comment post-formatter post-scorer post-writer profile-optimizer quote-post reels-scripting voice-builder youtube-thumbnail 
- **design**: accessibility-review design-critique design-handoff design-system research-synthesis user-research ux-copy (폴더명 예: `design-design-system`)
- **example-skills**: canvas-design theme-factory (anthropics/skills 마켓플레이스의 `example-skills` 플러그인 중 이 2개만)
- **last30days**: last30days (폴더명 `last30days-last30days`)
- **ecc**: content-engine article-writing agent-self-evaluation growth-log living-docs-governance council market-research strategic-compact context-budget safety-guard (폴더명 `ecc-content-engine` 등, 호출도 폴더명)

## 직원별 지정 스킬 (.claude/agents/*.md의 skills:)
| 직원 | 스킬 |
|---|---|
| researcher | social-media-skills-niche-research |
| writer | marketing-skills-copywriting, marketing-skills-copy-editing, marketing-skills-video |
| designer | social-media-skills-youtube-thumbnail, social-media-skills-graphic-designer, marketing-skills-image |
| marketer | marketing-skills-copywriting, -social, -video; social-media-skills-hook-generator, -post-writer, -reels-scripting, -pinned-comment |
| publisher | social-media-skills-post-formatter |
| legal-reviewer | legal-review-contract, legal-legal-risk-assessment, legal-compliance-check |
| analyst | finance-variance-analysis |

## 연결 검증
(아래 검증 결과 섹션 참조)

### 결과 (2026-10-01, EP000)
| 팩 | Skill 도구 호출 | 더미 산출물 |
|---|---|---|
| finance | `finance-variance-analysis` → "Launching skill" ✅ | episodes/EP000/finance-variance.md |
| legal | `legal-review-contract` → "Launching skill" ✅ | episodes/EP000/legal-contract-review.md |
| marketing-skills | `marketing-skills-copywriting` → "Launching skill" ✅ | episodes/EP000/titles.md |
| social-media-skills | `social-media-skills-post-writer`, `-hook-generator`, `-post-formatter` → "Launching skill" ✅ | episodes/EP000/social-captions.md |

- 원래 이름(`variance-analysis` 등)은 "Unknown skill". 복사 직후엔 폴더명도 Unknown이었고, 세션 스킬 목록이 갱신된 뒤 성공(새 세션에선 시작부터 로드됨).
- `/help` 확인은 해당 없음: 네 팩 모두 commands/ 없음, `/help`는 클라우드 세션 미지원. 대신 Skill 도구 호출 기록으로 검증.
- 84개 모두 SKILL.md·`name:` 보유, `name` 중복 없음, 실행 스크립트 없음(episodes/EP000/skills-check.md).

## 한눈에 보기 (비개발자용)
- **finance**: 숫자 분석 도구. 애널리스트가 매주·매월 "계획 대비 실제 매출이 왜 다른지"를 쪼개 볼 때 쓴다.
- **legal**: 계약·규정 점검 도구. 리스크 담당이 협찬 계약서와 업로드 전 고지 문구·저작권을 점검할 때 쓴다.
- **marketing-skills**: 카피·마케팅 도구 50종. 작가·마케터가 제목, 설명란, 대본 문장을 다듬을 때 쓴다.
- **social-media-skills**: SNS 도구 17종. 마케터·리서처가 숏폼 훅, 캡션, 썸네일 아이디어, 주간 화제 수집에 쓴다.
- **design**: 디자인 점검 도구 7종. 디자이너가 썸네일·화면 비평, 디자인 규칙 정리, 짧은 문구(UX 카피) 다듬기에 쓴다.
- **example-skills**: canvas-design(글자 중심 썸네일·카드뉴스를 PNG/PDF로, 무료 글꼴 포함)과 theme-factory(색·글꼴 테마 10종).
- **last30days**: 트렌드 조사 도구. 리서처가 "지난 30일간 사람들이 이 주제에 대해 실제로 뭐라고 하는지"를 Reddit·HN·YouTube 등에서 모을 때 쓴다.

## Phase 1-0 추가 설치 (2026-10-01, 대표 OK: SKILL_CANDIDATES "OK 시 순서" 1번)
- 접두어는 기존 규칙(플러그인 매니페스트의 plugin `name`, 예: marketingskills 저장소 → `marketing-skills`)을 따름. canvas-design·theme-factory는 anthropics/skills 마켓플레이스의 `example-skills` 플러그인 소속.
- design: 팩 폴더에 LICENSE 없음. 저장소 루트 LICENSE(Apache-2.0)만 있어 기존 팩처럼 이 표에만 기록. `.mcp.json`·`CONNECTORS.md`·`README.md`는 복사하지 않음. canvas-design·theme-factory는 스킬 폴더 안 `LICENSE.txt`(Apache-2.0)와 글꼴 OFL 고지문까지 원본 그대로 포함.
- 세 팩 모두 `commands/`·`agents/` 없음, 필요한 API 키 없음, 실행 스크립트 없음, setup.sh 변경 없음.

| 설치 폴더 | 파일 수 | `diff -r` | 비밀 파일 | Skill 도구 호출 |
|---|---|---|---|---|
| design-{accessibility-review, design-critique, design-handoff, design-system, research-synthesis, user-research, ux-copy} | 7 × 1 | 차이 0 | 없음 | 새 세션에서 로드 예정(설치 담당 세션에 Skill 도구 없음) |
| example-skills-canvas-design | 83 | 차이 0 | 없음 | 새 세션에서 로드 예정 |
| example-skills-theme-factory | 13 | 차이 0 | 없음 | 새 세션에서 로드 예정 |
| last30days-last30days | 135 (17MB) | 차이 0 | 없음 | 새 세션에서 로드 예정 |

### last30days 설치 메모
- **예외: 데모 mp3 1개 강제 커밋, 대표 결정 2026-10-01**(COO가 전달). `assets/claude-code-rap.mp3`(2,354,231 bytes)만 `.gitignore`의 `*.mp3`에 걸려 `git add -f`로 그 경로 하나만 추가. `.gitignore`는 수정하지 않음. `git check-ignore --no-index`로 확인한 무시 대상은 이 파일 1개뿐.
- 필요 키 없음(Reddit·HN·Polymarket·GitHub·웹은 무료). 선택 키 14개 + `SCRAPECREATORS_API_KEY`는 docs/ENV.md에 "선택"으로 표시.
- 첫 실행 setup 마법사(브라우저 쿠키 읽기, CLI 자동 설치)는 쓰지 않는다. 대신 scripts/setup.sh 끝에 Python 3.12+ 확보(없으면 uv로 설치), yt-dlp 설치, node 확인을 추가.
- 스킬 폴더의 `agents/openai.yaml`은 Codex용 설정으로 스킬 폴더 안에 원본 그대로 둠(Claude 직원 파일 아님, `.claude/agents/`로 복사하지 않음). 저장소 루트에 `commands/`·`agents/` 없음.

### 보류 (복사하지 않음)
| 후보 | 상태 | 이유 / 메모 |
|---|---|---|
| glebis/claude-skills `elevenlabs-tts` @7524dff0c54bb85645b6bb2b0c6c148f4f7c3e29 (MIT) | TTS 공급자 결정 후 설치(HANDOFF 대표 결정 대기 4번) | 스킬 폴더에 `.env.example` 포함(비밀 파일 패턴 `.env*`, `.gitignore`의 `.env.*`에도 걸림, 내용은 열어 보지 않음). 폴더 자체가 플러그인(`.claude-plugin/`, 자체 `.gitignore`). 필요 키 `ELEVENLABS_API_KEY`, pip `elevenlabs==2.23.0`, `python-dotenv==1.0.0` |

## ECC 선별 설치 (2026-10-02, 대표 결정: 쓸만한 스킬만, 별도 세션·브랜치 `ecc/install`)
- 근거: docs/ECC_REVIEW.md (가) 최소안 5개 + (나) 중간안에서 MCP 의존·경로 불일치·중복이 없는 5개 = 10개. 검토 대상 10개 모두 저장소에 존재하고 frontmatter `origin: ECC` 보유(건너뛴 스킬 없음).
- 방법: 임시 디렉터리에 `git clone --depth 1` → `git rev-parse HEAD` = c05b2d66…(ECC_REVIEW.md와 동일, 추가 고정 불필요) → `cp -r skills/<s> .claude/skills/ecc-<s>` → `diff -r` 차이 0. 스크립트·install.sh·설치 마법사 실행 없음. 임시 디렉터리는 작업 후 삭제.
- 복사하지 않은 것: hooks/·scripts/·rules/·commands/·agents/ 전부(ECC_REVIEW.md §3: `~/.claude/plugins/ecc*` 전제라 이 환경에서 무효). `.claude/settings.json`·CLAUDE.md·hooks는 만들지 않음(대표 결정 대기).
- 비밀 파일 없음(`.env*`·키 파일 0개). `.gitignore`에 걸리는 파일 없음. 필요한 API 키·외부 설치 없음, setup.sh 변경 없음.
- 컨텍스트 비용: 설명 10개 합 3,381자 + 폴더명 ≈ 3.6k자 ≈ **900토큰/턴** (ECC_REVIEW.md 추정치 기준, 기존 ≈12k토큰의 7~8%).

| 설치 폴더 | 파일 수 | `diff -r` | 한 줄 용도 | 비고 |
|---|---|---|---|---|
| ecc-content-engine | 1 | 차이 0 | 플랫폼별(YouTube·TikTok·뉴스레터) 콘텐츠 시스템, 출처 우선, 품질 게이트 | — |
| ecc-article-writing | 1 | 차이 0 | 예시에서 뽑은 '사람 목소리'로 롱폼 집필, 금지 표현 목록 | — |
| ecc-agent-self-evaluation | 7 | 차이 0 | 작업 후 5축(정확·완결·명료·실행성·간결) 1~5점 자가 채점 | 부속 `scripts/evaluate.py`(표준 라이브러리만, 네트워크 없음)는 **실행하지 않고 참조만**. 참조 경로 불일치: `references/hook-integration.md`·`templates/evaluation-report.md`가 `hooks/hooks.json`·`skills/agent-self-evaluation/scripts/evaluate.py`(ECC 플러그인 루트 기준)를 가리킴 → 이 저장소에선 `.claude/skills/ecc-agent-self-evaluation/scripts/evaluate.py`. 원문 미수정 |
| ecc-growth-log | 1 | 차이 0 | 완료 작업에서 '사건'이 아닌 '재사용 규칙'을 뽑는 로그 템플릿 | — |
| ecc-living-docs-governance | 1 | 차이 0 | 문서를 헌법/지도/상태/이력 역할로 나눠 썩지 않게 관리 | description에 중국어 트리거 문구 포함(원문) |
| ecc-council | 1 | 차이 0 | 4관점 회의로 모호한 go/no-go 결정 | 본문이 `~/.claude/notes`에 쓰지 말라고 언급(금지 지침이라 영향 없음) |
| ecc-market-research | 1 | 차이 0 | 출처 표기 시장·경쟁 조사 | — |
| ecc-strategic-compact | 1 | 차이 0 | 단계 경계에서 수동 /compact 권고 기준 | 참조 경로 불일치: 본문 §설치가 `hooks/hooks.json`의 `suggest-compact.js`, `~/.claude/settings.json`, `~/.claude/scripts/hooks/`, `~/.claude/memory/`, `~/.claude/rules/`, `token-optimizer` MCP를 언급 → 이 환경엔 없음. **지침(언제 compact할지)만 사용**, hook 연동은 하지 않음 |
| ecc-context-budget | 1 | 차이 0 | 스킬·에이전트·MCP·규칙의 컨텍스트 소비 감사 | 감사 대상에 `.mcp.json`·MCP 서버 포함(없으면 0으로 처리될 뿐, 의존 아님) |
| ecc-safety-guard | 1 | 차이 0 | 파괴적 명령(rm -rf, push --force, DROP TABLE) 경고 지침 | 참조 경로 불일치: PreToolUse hook 연동과 `~/.claude/safety-guard.log` 기록은 ECC hooks 전제 → 이 환경엔 없음. 지침 패턴만 사용, 실제 차단 hook은 대표 결정(ECC_REVIEW.md §5-2) 대기 |

- 한눈에 보기: ECC는 "콘텐츠·문서·운영 습관" 도구 10종. 작가·마케터는 content-engine·article-writing, COO는 council·living-docs-governance·growth-log·agent-self-evaluation·strategic-compact·context-budget, 리서처는 market-research, 전 직원 공통 주의 지침은 safety-guard.
- 직원 `skills:` 지정은 이번에 바꾸지 않음(COO 결정). 등록 확인: 복사 직후 설치 세션의 스킬 목록에 `ecc-content-engine` 등 10개가 폴더명으로 올라옴(원문 `name:`은 그대로). 실제 호출 검증은 다음 작업 세션에서.

## 자체 작성(사내) 스킬 (2026-10-01, Phase 2 EP001, producer 작성)
외부 원본이 없는 사내 스킬이라 "복사 설치·원본 무수정" 규칙의 대상이 아니다. 고칠 때는 이 저장소에서 PR로 바꾸고 SKILL.md의 사용법도 함께 갱신한다.

| 팩 | 출처 | 커밋 SHA | 라이선스 | 스킬 수 |
|---|---|---|---|---|
| 사내 · ffmpeg-assemble | 자체 작성 `.claude/skills/ffmpeg-assemble/` (SKILL.md, scripts/assemble.py·kemedia.py·script_to_scenes.py, examples/) | 외부 원본 없음(이 저장소 커밋 이력이 기준) | 사내 전용(KE Studio) | 1 |
| 사내 · shorts-cut | 자체 작성 `.claude/skills/shorts-cut/` (SKILL.md, scripts/shorts_cut.py, examples/) | 외부 원본 없음(이 저장소 커밋 이력이 기준) | 사내 전용(KE Studio) | 1 |

- 의존: Python 3.9+, Pillow, ffmpeg/ffprobe(`scripts/setup.sh` 기존 항목, setup.sh 변경 없음). API 키·네트워크 불필요. shorts-cut은 `ffmpeg-assemble/scripts/kemedia.py`(공용 모듈)를 불러 쓴다.
- 폰트: 지정 폰트(Anton·Pretendard·Black Han Sans)를 `fc-list`로 찾고 없으면 설치된 대체 폰트(Liberation Sans, OFL 1.1 / WenQuanYi Zen Hei, GPL-2 + 폰트 임베딩 예외)를 쓴다. 쓴 폰트와 라이선스는 매니페스트에 기록된다.
- 사용 직원: producer. `.claude/agents/producer.md`의 `skills:` 지정은 COO 결정(이번에는 수정하지 않음).
- 검증: EP001 목업 렌더(롱폼 1 + 숏폼 5, 결과는 `episodes/EP001/render-log.md`). 실제 모드(플레이트+TTS+음악)는 임시 폴더의 합성 테스트 소재로만 확인했다.
- 한눈에 보기: **ffmpeg-assemble**은 장면 목록을 롱폼 영상과 자막 파일로 묶는 도구, **shorts-cut**은 그 장면에서 문단·문장을 골라 60초 이하 세로 숏폼을 만드는 도구다.
