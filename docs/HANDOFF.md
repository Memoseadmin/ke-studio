# HANDOFF — 2026-10-01 (Phase 0 완료)

## 목표
KE Studio: Korea Explained 채널의 기획→대본→디자인→마케팅→업로드를 에이전트로 자동화. 수익 = 제휴·협찬·커머스.
첫 게이트: 링크 클릭률 1%, 첫 제휴 매출, 월 비용 20만원 이하(docs/PLAN.md).

## 현재 상태
- 브랜치 `claude/keen-thompson-bnikrl`. Phase 0 성공 기준 3/3 통과(뼈대·에이전트 9개 더미·스킬 팩 4/4·후보표).
- 직원 9명: `.claude/agents/` (새 세션에서 subagent_type으로 바로 호출 가능).
- 스킬 84개: `.claude/skills/` (finance 8, legal 9, marketing-skills 50, social-media-skills 17). 등록부 docs/SKILLS.md.
- ffmpeg 6.1.1 세션 VM에 있음. 환경변수는 GITHUB_TOKEN만 SET, YouTube·TTS·이미지 키 UNSET.

## 완료
- CLAUDE.md(규범+기획서 고정 규칙), .gitignore(미디어·비밀키), docs/PLAN.md(요약)·PLAN.original.md(원문), docs/ENV.md, scripts/setup.sh
- EP000 더미: research, script.en/kr, design/(디자인 시스템·썸네일 3·장면 프롬프트), marketing, risk, render-log(테스트 렌더 2개), publish.log(승인 게이트 중단 확인), skills-check, reports/2026-10-DUMMY
- 팩 검증: finance-variance-analysis / legal-review-contract / marketing-skills-copywriting / social-media-skills-post-writer 모두 "Launching skill"
- 추가 스킬 후보표: docs/SKILL_CANDIDATES.md (대표 OK 대기)

## 실패한 시도와 이유
- 스킬을 원래 이름(variance-analysis)으로 호출 → Unknown. 이 환경은 **폴더명**으로 등록 → 에이전트 skills: 를 폴더명으로 수정.
- 복사 직후엔 폴더명도 Unknown → 세션 중 스킬 목록 갱신 후 성공. 새 세션은 시작부터 로드.
- `/help` 커맨드 검증 불가: 네 팩 모두 commands/ 없음 + 클라우드 미지원 → Skill 호출 기록으로 대체.
- `gh pr list` GraphQL 403 → GitHub MCP 도구 사용.
- 소셜 팩 post-writer/post-formatter는 LinkedIn 전용, hook-generator는 낚시형 → marketer.md에 우선순위 규칙 추가.
- 라이선스 없는 youtube-uploader, google-trends-skill은 복사 불가 → 직접 작성 예정.

## 대표 결정 대기
1. 추가 스킬 설치 OK 여부(SKILL_CANDIDATES.md 추천 ✅ 항목)
2. 인스타 캐러셀(하루 1개, 5~7장) 2주 테스트를 Phase 1에 먼저 넣을지
3. PLAN.md "결정이 필요한 사항" 1~4
4. 환경변수 입력: YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN(Phase 2 전), 이미지·TTS 공급자 선택

## 다음 할 일 (Phase 1 — EP001 반자동 검수 PR)
1. 대표 답변 반영: 후보 스킬 OK면 skill-installer로 복사 설치·검증
2. researcher → EP001 소재 10개 → 1개 선정(구매 의도형, 트렌드 근거·출처 포함)
3. writer → designer → marketer → legal-reviewer 순 실행, 브랜치 ep/EP001 + 검수 시트 PR 생성
