docs/HANDOFF.md와 CLAUDE.md를 읽어라. 그다음 docs/PROJECTS.md(통합 현황판: 운영 규범·대표 결정 큐·하위 세션 표)와 cardnews/docs/HANDOFF.md(origin/cardnews/main)를 읽어라. 프로젝트 재탐색 금지, 큰 파일은 필요한 부분만.
먼저 `git fetch origin claude/admiring-clarke-beyyoi cardnews/main cardnews/c1-1b cardnews/c1-1-design ep/EP001 ep/EP002 ep/EP003 && git checkout claude/admiring-clarke-beyyoi`. worktree: `.worktrees/cardnews`(cardnews/main), `.worktrees/c1-1-design`(cardnews/c1-1-design), `.worktrees/c1-1b`(cardnews/c1-1b) (`.git/info/exclude`에 `.worktrees/`).

너는 KE Studio COO다. **운영 규범(대표 2026-10-02)**: 이 세션은 대표의 명령·총괄 결정·기획만 다룬다. 모든 실작업은 난이도별 자식 세션(create_session, 판단·리서치·제작 = claude-opus-5-5 / 반복·검증·문서 편집 = claude-sonnet-5-5)에 배분하고 결과를 회수해 대표에게 보고한다. **대표가 결정하지 않은 사항은 기본값으로 진행하지 말고 AskUserQuestion으로 끝까지 물어라**(선택지·추천·근거 포함, 한 번에 4개 이하). 시작 전 한 줄로 계획만 확인받고 진행. 환경변수는 SET/UNSET으로만 확인(값 출력 금지). 하위 세션의 git push가 막히면 보고만 회수하고 대신 푸시하지 않는다.

먼저 PROJECTS.md "세션 위생 규칙"대로 하위 세션 표를 전부 get_session으로 확인: 완료면 브랜치 fetch → 결과를 표에 적고 archive_session, 진행 중이면 list_events로 상태만. 그다음 GitHub MCP로 PR #5(C1-1b)와 열린 cardnews PR의 라벨·코멘트 확인(gh CLI 금지).

이번 세션 성공 기준 (시작 전에 표로 적고, 끝에 자가 검증표)
[B1] 세트 11(cardnews/posts/2026-10-19, 오늘 첫 게시) v3 3안 2판: 사진 소싱 세션 결과(PHOTOS.v3.json) 회수 → Opus 자식 세션이 DESIGN-v3.md·VISUAL-BRIEF.md 기준으로 장별 "글↔이미지" 일치 렌더(AI 라벨 없음, 출처 줄) → contact.png + 대조표를 대표에게 보여 주고 확인 → legal(새 사진 라이선스·출처 줄·캡션 A안) → 검수 PR(cardnews/c1-1-design → cardnews/main, 8장 contact + 캡션 전문 + 출처표) → approved 라벨 → **새 Sonnet 세션**에서 `r2_upload.py <dir> --execute` → `ig_publish.py <dir> --pr N --execute`(경로 B 자동) → publish.log 기록. 게시 전 대표에게 한 줄 확인.
[B2] 채널명(docs/CHANNEL_NAME.md)·bio v4(PROFILE.md)·디자인 시스템 v1.1 결과 회수 → 대표에게 선택지로 질문 → 반영·푸시. PR #5는 대표 결정(프로필 사진 v3 재제작·bio v4·21:00) 반영 후 재검수 요청.
[B3] 세트 01(10/9, AI 없이: 공개 원화+편집 실사)과 02~14(AI 배경은 대표 PC ComfyUI 또는 보류, 편집 실사 필수)를 Opus 자식 세션 5개(브랜치 cardnews/v3-sets-A~E, 3세트씩)에 배분 — 각 세션 프롬프트에 DESIGN-v3.md·VISUAL-BRIEF 규칙·사진 라이선스 규칙(CC0/공공누리1/CC BY, 얼굴·로고 0, 2차 가공 허용)·원화 목록(DESIGN_SOURCES §5)·금지 사항을 동일하게 넣는다. 결과 회수 → legal 일괄 → 머지 → 검수 PR.
[A1] 채널명 확정 후 YOUTUBE_LAUNCH_PLAN.md §5 개설 체크리스트 중 대표가 직접 할 항목(브랜드 계정·핸들·신분증 인증·OAuth 프로덕션·API 감사 신청·키 3종)을 순서대로 안내. N8(유료 프로모션)은 legal 판정 후 질문, N12(도메인·상표)는 이름 확정 후 질문.
[A2] 키 UNSET이면 A 제작은 건너뛰고 publish.log만 기록. 키 SET이면 EP002 S01 샘플(Remotion 템플릿 + 원화) → 대표 확인.
[공통] PROJECTS.md 상태표·결정 큐·하위 세션 표 갱신, 두 HANDOFF 갱신, 전부 푸시, 새 세션 안내 블록 1개.

첫 3개 작업
1. 세션 위생(하위 세션 4개 + 남은 것 확인·회수·아카이브) → PR #5 라벨·코멘트 → 환경변수 SET/UNSET → 사진 소싱 결과가 있으면 [B1] 2판 자식 세션(Opus) 즉시 착수, 없으면 소싱 세션에 "확보분만 커밋·푸시" 지시.
2. [B2] 채널명·bio v4·디자인 시스템 결과를 대표에게 질문(AskUserQuestion) → 반영.
3. [B1] 2판 확인 → legal → PR → 승인 → 새 세션 게시 → [B3] 세트 01~14 병렬 세션 착수 → 종료 절차.
