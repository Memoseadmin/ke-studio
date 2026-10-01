# KE Studio 통합 현황판 (COO 세션이 매 세션 시작·종료 때 갱신)

갱신: 2026-10-01 · 운영 원칙: **세션 1개(COO)가 모든 프로젝트를 관리**한다. 프로젝트마다 폴더·브랜치만 분리하고, 작업은 `.worktrees/<project>`(git worktree)로 병렬 진행한다. 대표는 PR 승인·반려와 결정 항목만 본다.

## 프로젝트
| 프로젝트 | 목적·수익 | 폴더 | 브랜치 | 문서 | 현재 Phase | 게이트 |
|---|---|---|---|---|---|---|
| A. Korea Explained (유튜브 롱폼+숏폼) | 구독형 혼합: 제휴 → YPP 광고 → 멤버십 | `episodes/`, `docs/` | 산출물 `ep/EPxxx`, 문서 `claude/admiring-clarke-beyyoi` | docs/PLAN.md · HANDOFF.md | Phase 5 대기(키·공급자) | 90일 구독 1,000 + 첫 제휴 매출 + 월 20만원 |
| B. 카드뉴스 (인스타그램 캐러셀) | 협찬·광고 게시물 | `cardnews/` | `cardnews/main`(검수 PR은 `cardnews/c1-x`) | cardnews/docs/PLAN.md · HANDOFF.md | C1-1 시작 | 90일 팔로워 2,000 + 저장률 3% + 미디어킷 + 제안 5건 + 월 5만원 |

## 상태 한눈에
| 항목 | A 유튜브 | B 카드뉴스 |
|---|---|---|
| 승인된 PR | #1 EP001, #2 EP002 (approved) | 없음 |
| 업로드/게시 | 0건 (키 UNSET, FIX 3) | 0건 (계정 미개설) |
| 막힌 것 | TTS·이미지·YouTube 키, Amazon 트래킹 ID, 공급자 선택 | 인스타 비즈니스 계정, 링크 허브 URL, (선택) Meta API 토큰 |
| 이번 세션 할 일 | 키 들어오면 샘플 생성→렌더→업로드 게이트, EP003 기획 | C1-1: 트렌드 수집 → 14일 세트 → risk → 검수 PR |

## 대표 결정 큐 (하나로 합침)
1. [A] TTS·이미지 공급자: "1안(ElevenLabs+Nano Banana)" / "가성비(Google TTS+Recraft)"
2. [A] 키 입력: TTS_API_KEY, IMAGE_API_KEY, YOUTUBE_* 3개(scripts/youtube_auth.py), 선택 MUAPI_API_KEY
3. [A] Amazon Associates 가입 + 트래킹 ID, 제휴 상품 확정
4. [A] 채널 마스코트 캐릭터 도입 여부(민화 소재 시안 3개 제안 중)
5. [B] 계정 언어 EN(기본) / KR 병행, 인스타 비즈니스 계정·링크 허브 URL, Meta API 토큰 여부
6. [공통] 월 비용 배정: A 15만 + B 5만(기본)

## 공용 자원
- 직원 9명 `.claude/agents/`, 스킬 96개, 디자인 시스템 `episodes/EP001/design/design-system.md`, 비주얼 방향 "민화 플랫 × 한지 질감"(docs/TOOLING_TTS_IMAGE.md §D).
- 비용 상한 월 20만원(전 프로젝트 합). analyst가 월간 리포트에서 프로젝트별로 나눠 보고.
