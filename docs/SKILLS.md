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

## 포함 스킬
- **finance**: audit-support close-management financial-statements journal-entry journal-entry-prep reconciliation sox-testing variance-analysis 
- **legal**: brief compliance-check legal-response legal-risk-assessment meeting-briefing review-contract signature-request triage-nda vendor-check 
- **marketing-skills**: ab-testing ad-creative ads ai-seo analytics aso attribution churn-prevention co-marketing cold-email community-marketing competitor-profiling competitors content-strategy copy-editing copywriting cro customer-research directory-submissions emails events free-tools image influencer-marketing launch lead-magnets marketing-council marketing-ideas marketing-loops marketing-plan marketing-psychology offers onboarding paywalls popups pricing product-marketing programmatic-seo prospecting public-relations referrals revops sales-enablement schema seo-audit signup site-architecture sms social video 
- **social-media-skills**: analytics-dashboard content-matrix gemini-carousel gemini-infographic graphic-designer hook-generator newsletter-voice niche-research pinned-comment post-formatter post-scorer post-writer profile-optimizer quote-post reels-scripting voice-builder youtube-thumbnail 

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
