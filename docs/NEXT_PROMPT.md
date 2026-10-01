docs/HANDOFF.md와 CLAUDE.md를 읽어라. 프로젝트 재탐색은 하지 말고, 큰 파일은 통째로 읽지 마라.
먼저 `git fetch origin claude/admiring-clarke-beyyoi ep/EP001 && git checkout claude/admiring-clarke-beyyoi` (기본 브랜치에는 Phase 1이 없다. EP001 산출물은 ep/EP001 브랜치).
너는 KE Studio의 COO다. 이번 세션은 Phase 2 — EP001 피드백 반영 → 렌더 → (승인 시) 비공개 업로드다. 시작 전 한 줄로 계획만 확인받고 진행하라.

먼저 PR https://github.com/Memoseadmin/ke-studio/pull/1 의 라벨·코멘트를 GitHub MCP 도구로 확인하라(gh CLI 금지).
HANDOFF "대표 결정 대기" 중 내 답이 이 메시지나 PR 코멘트에 있으면 반영하고, 없으면 기본값(상품은 가안 A·B 유지, 제목은 "Korean Screens" 안, KR판은 보류하고 EN만 렌더, 보류 스킬은 그대로 보류)으로 진행하라.

Phase 2 성공 기준 (시작 전에 표로 다시 적고, 끝에 자가 검증표로 보고)
1. PR #1 반려 코멘트가 있으면 적힌 항목만 다시 만들고, risk.md 재점검 결과 BLOCK 0을 유지한 채 ep/EP001에 푸시했다(코멘트가 없으면 "해당 없음").
2. producer가 EP001 롱폼 1개 + 숏폼 5개를 세션 VM에 렌더했고(키가 없으면 목업 슬라이드+자막 프리뷰 렌더), `episodes/EP001/render-log.md`에 길이·해상도·사용 소재와 라이선스·생성 모델을 기록했다. 영상·오디오는 커밋하지 않는다.
3. 렌더 결과로 legal-reviewer가 risk.md FIX 5(최종 이미지·보이스·음악 라이선스)를 재판정했다.
4. publisher는 approved 라벨이 있을 때만 YouTube에 비공개 업로드했고(키가 없으면 수동 업로드 패키지), 라벨이 없으면 아무것도 업로드하지 않았다는 기록을 publish.log에 남겼다.

첫 3개 작업
1. `bash scripts/setup.sh` 실행 → PR #1 라벨·코멘트 확인 → 반려 항목이 있으면 해당 직원만 재실행 → legal 재점검 → ep/EP001 푸시.
2. 환경변수 이름(docs/ENV.md 기준)만 SET/UNSET으로 확인(값은 출력 금지) → producer로 렌더(필요하면 ffmpeg-assemble·shorts-cut 스킬을 직접 작성) → legal-reviewer가 FIX 5 재판정.
3. approved 라벨을 확인한 경우에만 publisher를 실행한다. 끝나면 세션 종료 절차.
