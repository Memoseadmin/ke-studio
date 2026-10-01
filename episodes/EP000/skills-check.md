# EP000 skills-check — DUMMY 검증 (skill-installer)

> **DUMMY** — 설치·수정·실행 없음. 읽기 전용 검증. 2026-10-01.

## 1. 폴더·SKILL.md
| 항목 | 기대 | 결과 |
|---|---|---|
| `.claude/skills/` 하위 폴더 수 | 84 | **84** ✅ |
| SKILL.md 없는 폴더 | 0 | **0** ✅ |
| 4개 접두사 외 폴더 | 0 | **0** ✅ |

## 2. 팩별 개수
| 접두사 | 개수 |
|---|---|
| `finance-` | 8 |
| `legal-` | 9 |
| `marketing-skills-` | 50 |
| `social-media-skills-` | 17 |
| **합계** | **84** |

## 3. frontmatter `name:`
- `name:` 필드 없는 SKILL.md: **0개** ✅ (84/84에 있음)
- 84개 스킬 간 `name:` 값 중복: **없음** ✅ (고유 name 84개)
- 비슷해서 헷갈릴 수 있는 이름(충돌은 아님): `journal-entry` vs `journal-entry-prep` (finance), `analytics` (marketing) vs `analytics-dashboard` (social-media)
- 참고: `name:` 값에는 팩 접두사가 없음(예: 폴더 `social-media-skills-post-formatter` → `name: post-formatter`). 이번 세션의 Skill 도구는 **폴더 이름**으로 등록했다: `Skill("post-formatter")`는 "Unknown skill"이었고 `Skill("social-media-skills-post-formatter")`는 로드됐다. `.claude/agents/publisher.md`는 커밋 86debca에서 이미 `skills: social-media-skills-post-formatter`로 수정됨 ✅.

## 4. 실행 가능한 스크립트 포함 여부
- `.py` / `.sh` / `.js` / `.mjs` / `.ts`: **0개**
- 실행 권한 비트가 있는 파일, shebang(`#!`) 파일: **0개**
- 파일 종류 전체: `.md` 263, `.json` 50(주로 `*/evals/`), `.csv` 1, `.html` 1
- 참고: `marketing-skills-ad-creative/assets/creative-review-template.html`에 인라인 `<script>`가 있음 — 브라우저에서 열 때만 실행되는 템플릿이고 실행하지 않았음.

## 실행한 명령(요지)
`find -maxdepth 1 -type d | wc -l`, 폴더별 `[ -f SKILL.md ]`, 접두사별 `ls -d`, frontmatter `name:` 추출(awk) → `sort | uniq -d`, 확장자·권한·shebang `find`/`grep`.
