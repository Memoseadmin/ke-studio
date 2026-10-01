# HANDOFF — 2026-10-01 (Phase 1-0 추가 스킬 설치 완료)

## 목표
KE Studio: Korea Explained 채널의 기획→대본→디자인→마케팅→업로드를 에이전트로 자동화. 수익 = 제휴·협찬·커머스.
첫 게이트: 링크 클릭률 1%, 첫 제휴 매출, 월 비용 20만원 이하(docs/PLAN.md).

## 현재 상태
- 작업 브랜치 `claude/admiring-clarke-beyyoi` (기본 브랜치 `claude/keen-thompson-bnikrl`보다 2커밋 앞섬. 새 세션은 이 브랜치를 체크아웃해서 시작).
- Phase 0 성공 기준 3/3 통과. Phase 1-0(추가 스킬 설치)은 대표 승인 범위 안에서 완료. 그중 1건은 보류.
- 직원 9명: `.claude/agents/`. 스킬 94개: `.claude/skills/` (기존 84 + design 7 + canvas-design + theme-factory + last30days). 등록부 docs/SKILLS.md.
- ffmpeg 6.1.1 있음. 이 VM의 Python은 3.11 → last30days를 쓰려면 새 세션에서 `bash scripts/setup.sh` 먼저 실행(3.12 설치).
- 환경변수는 GITHUB_TOKEN만 SET. YouTube·TTS·이미지 키는 UNSET. last30days 키는 모두 선택(ENV.md).

## 완료
- Phase 0: CLAUDE.md, .gitignore, PLAN, ENV, setup.sh, 에이전트 9명, 스킬 팩 4개, EP000 더미 전 과정, SKILL_CANDIDATES.md.
- Phase 1-0 (f8521cb, 1d59692): 대표 OK → skill-installer가 복사 설치. 5종 모두 고정 SHA 원본과 `diff -r` 차이 0.
  - design 팩 7개(`design-*`), `example-skills-canvas-design`, `example-skills-theme-factory`: Apache-2.0. 세션 스킬 목록에 등록 확인.
  - `last30days-last30days` @5103ba4: MIT. 135파일·17MB. 대표 결정으로 데모 mp3 1개 강제 커밋(SKILLS.md에 예외 기록). setup.sh 끝에 7줄 추가.
  - elevenlabs-tts: 보류(TTS 공급자 결정 후). `.env.example` 포함 문제는 그때 다시 판단.

## 실패한 시도와 이유
- 스킬을 원래 이름으로 호출 → Unknown. 이 환경은 **폴더명(팩 접두어 포함)** 으로 등록. 예: `design-design-system`, `example-skills-canvas-design`.
- 복사 직후 폴더명도 Unknown일 수 있음 → 세션 중 목록 갱신 후 등록됨(이번엔 바로 등록).
- skill-installer 서브에이전트에는 Skill 도구가 없음 → 등록 확인은 메인 세션이 스킬 목록으로 한다.
- 원본 그대로 원칙이 다른 규칙과 충돌: last30days mp3(오디오 금지), elevenlabs-tts `.env.example`(비밀 파일 패턴) → 둘 다 대표 판단으로 처리.
- `gh pr list` GraphQL 403 → GitHub MCP 도구 사용.
- 소셜 팩 post-writer·post-formatter는 LinkedIn 전용, hook-generator는 낚시형 → marketer.md에 우선순위 규칙.
- 라이선스 없는 youtube-uploader, google-trends-skill은 복사 불가 → 직접 작성 예정.

## 대표 결정 대기
1. 인스타 캐러셀(하루 1개, 5~7장) 2주 테스트를 Phase 1에 먼저 넣을지 (기본값: marketing.md에 캐러셀 1안만 추가)
2. PLAN.md "결정이 필요한 사항" 1~4
3. 환경변수 입력: YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN(Phase 2 전), 이미지·TTS 공급자 선택 → TTS가 ElevenLabs면 elevenlabs-tts 설치
4. 보류 스킬: nano-banana(시크릿 파일), ScrapeCreators(유료 키)

## 다음 할 일 (Phase 1 — EP001 반자동 검수 PR)
1. `bash scripts/setup.sh` 실행 → researcher가 last30days·niche-research로 EP001 소재 10개 → 1개 선정(구매 의도형, 트렌드 근거·출처)
2. writer → designer(canvas-design·theme-factory 사용 가능) → marketer → legal-reviewer 순으로 실행
3. 브랜치 ep/EP001(이 브랜치에서 분기) 푸시, 검수 시트 ①~⑧ PR 생성
4. 직접 작성 스킬(youtube-upload, ffmpeg-assemble, shorts-cut, kr-trend-radar)은 Phase 1~2에서 필요해질 때 작성
