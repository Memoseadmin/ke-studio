docs/HANDOFF.md와 CLAUDE.md를 읽어라. 프로젝트 재탐색은 하지 말고, 큰 파일은 통째로 읽지 마라.
먼저 `git fetch origin claude/admiring-clarke-beyyoi ep/EP001 && git checkout claude/admiring-clarke-beyyoi` (기본 브랜치에는 Phase 1~2가 없다. EP001 산출물은 ep/EP001 브랜치).
너는 KE Studio의 COO다. 이번 세션은 Phase 3 — EP001 마무리(반려 반영·키가 있으면 실제 렌더·승인 시 비공개 업로드) + EP002 기획 착수다. 시작 전 한 줄로 계획만 확인받고 진행하라.

먼저 PR https://github.com/Memoseadmin/ke-studio/pull/1 의 라벨·코멘트를 GitHub MCP 도구로 확인하라(gh CLI 금지).
HANDOFF "대표 결정 대기" 중 내 답이 이 메시지나 PR 코멘트에 있으면 반영하고, 없으면 기본값(상품은 가안 A·B 유지, 제목은 "Korean Screens" 안, KR판은 보류하고 EN만, publisher 게이트는 현행 유지, 보류 스킬은 그대로 보류)으로 진행하라.
커밋 규칙: 스킬·docs는 작업 브랜치, EP 산출물은 ep/EPxxx. 서브에이전트가 끝나면 바로 커밋·푸시.

Phase 3 성공 기준 (시작 전에 표로 다시 적고, 끝에 자가 검증표로 보고)
1. PR #1 반려 코멘트가 있으면 적힌 항목만 다시 만들었다. 코멘트와 상관없이 risk #8("Huntrix" → "HUNTR/X")을 대본·자막·render-input에 반영했고, 숏폼 1 편집안(훅·CTA 낭독 제거, 57.6초)을 marketer가 확인해 marketing.md에 기록했다. legal 재점검 결과 BLOCK 0을 유지한 채 ep/EP001에 푸시했다.
2. 환경변수(docs/ENV.md 기준)를 SET/UNSET으로만 확인했다(값 출력 금지). TTS·이미지 키가 SET이면 producer가 real 모드로 롱폼 1 + 숏폼 5를 렌더하고 render-log.md에 모델·날짜·시드·TTS·음악 라이선스를 기록한 뒤 legal이 FIX 5를 재판정했다. UNSET이면 렌더를 건너뛰고 "필요 키 목록"만 보고했다.
3. approved + risk FIX 0 + real 렌더가 모두 충족될 때만 publisher가 YouTube 비공개 업로드를 했다(키가 없으면 수동 업로드 패키지). 하나라도 빠지면 업로드 0건이고, 그 사유를 publish.log에 기록했다.
4. EP002(문화·역사 설명형, 50:50 비율 맞춤): ep/EP002 브랜치에 researcher가 소재 10개와 출처·사실검증이 붙은 research.md를 만들어 푸시했다. 건강·금융·법률 주제는 0개다.

첫 3개 작업
1. `bash scripts/setup.sh` 실행 → PR #1 라벨·코멘트 확인 → 반려 항목 + risk #8 + 숏폼 1 확인을 해당 직원(writer·marketer)에게만 맡김 → legal 재점검 → ep/EP001 푸시.
2. 환경변수 SET/UNSET 확인 → 키가 있으면 producer real 렌더(`.claude/skills/ffmpeg-assemble`·`shorts-cut`, 입력 `episodes/EP001/render-input/*.json`) → legal FIX 5 재판정. 키가 없으면 건너뜀.
3. 업로드 게이트(approved·FIX 0·real 렌더) 확인 → 충족 시에만 publisher. 이어서 ep/EP002를 만들고 researcher 실행(last30days 엔진은 general-purpose로, `LAST30DAYS_PYTHON=/usr/bin/python3.12`). 끝나면 세션 종료 절차.
