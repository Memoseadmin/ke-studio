# KE Studio 통합 현황판 (COO 세션이 매 세션 시작·종료 때 갱신)

갱신: 2026-10-02 · 운영 원칙: **세션 1개(COO)가 모든 프로젝트를 관리**한다. 프로젝트마다 폴더·브랜치만 분리하고, 작업은 `.worktrees/<project>`(git worktree)로 병렬 진행한다. 대표는 PR 승인·반려와 결정 항목만 본다.

## 프로젝트
| 프로젝트 | 목적·수익 | 폴더 | 브랜치 | 문서 | 현재 Phase | 게이트 |
|---|---|---|---|---|---|---|
| A. Korea Explained (유튜브 롱폼+숏폼) | 구독형 혼합: 제휴 → YPP 광고 → 멤버십 | `episodes/`, `docs/` | 산출물 `ep/EPxxx`, 문서 `claude/admiring-clarke-beyyoi` | docs/PLAN.md · HANDOFF.md | Phase 5 대기(키·공급자) | 90일 구독 1,000 + 첫 제휴 매출 + 월 20만원 |
| B. 카드뉴스 (인스타그램 캐러셀, **한국어·한국 독자**) | **한국 브랜드 제휴·협찬 광고 게시물**(보조: 쿠팡파트너스) | `cardnews/` | `cardnews/main`(검수 PR은 `cardnews/c1-x`) | cardnews/docs/PLAN.md · HANDOFF.md | C1-1 시작 | 90일 팔로워 2,000 + 저장률 3% + 미디어킷 + 제안 5건 + 월 5만원 |

## 상태 한눈에
| 항목 | A 유튜브 | B 카드뉴스 |
|---|---|---|
| 승인된 PR | #1 EP001, #2 EP002 (approved) · **#3 ECC 설치 승인 대기** | 없음 |
| 업로드/게시 | 0건 (키 UNSET, FIX 3) | 0건 (계정 미개설) |
| 막힌 것 | TTS·이미지·YouTube 키, Amazon 트래킹 ID, 공급자 선택 | 인스타 비즈니스 계정, 링크 허브 URL, (선택) Meta API 토큰 |
| 이번 세션 할 일 | 키 들어오면 샘플 생성→렌더→업로드 게이트, EP003 기획 | C1-1: 트렌드 수집 → 14일 세트 → risk → 검수 PR |

## 대표 결정 큐 (하나로 합침)
1. ~~ECC 도입 범위~~ → 결정됨: 선별 도입, 별도 세션·브랜치
2. [A] TTS·이미지 공급자: 상용 1안/가성비안 **보류**, 오픈소스·무료 리서치(docs/TOOLING_OPENSOURCE.md) 결과 보고 결정
2. [A] 키 입력: TTS_API_KEY, IMAGE_API_KEY, YOUTUBE_* 3개(scripts/youtube_auth.py), 선택 MUAPI_API_KEY
3. [A] Amazon Associates 가입 + 트래킹 ID, 제휴 상품 확정
4. [A] 채널 마스코트 캐릭터 도입 여부(민화 소재 시안 3개 제안 중)
5. [B] ~~언어~~ KR 확정. 계정 이름·소개는 리서치 후 3안 중 선택(대표). **게시 = Meta Graph API 자동 예약 확정**(썸네일·문구는 PR에서 대표가 고름) → 인스타 비즈니스 계정 + `IG_ACCESS_TOKEN`·`IG_USER_ID` 필요. **제휴 = 가능한 프로그램 전부 등록해 두고 필요할 때 사용(대표 결정)** → docs/AFFILIATE_PROGRAMS.md 완성(28개: 지금 가입 15 / 첫 업로드 직전 2(Amazon·쿠팡) / 필요 시)
6. [공통] 월 비용 배정: A 15만 + B 5만(기본)

## 세션 위생 규칙 (대표 지시 2026-10-02, 매 세션 시작·종료 때 반드시)
1. 아래 표의 하위 세션을 `get_session`으로 전부 확인한다(status_bucket).
2. completed → 산출물 브랜치를 fetch해 결과 요약을 이 표에 적고 **archive_session**. failed → list_events로 원인 확인 후 재지시 또는 archive. idle(review_ready)인데 푸시가 없으면 send_message로 완료·푸시 지시.
3. 표에서 archived 행은 "완료(아카이브)"로 남긴다(삭제하지 않음). 새 세션을 만들면 즉시 이 표에 추가한다.
4. 대표가 직접 해야 하는 일(계정 가입·OAuth 동의·결제·토큰 발급)은 자동화하지 않는다. 그 전후 단계는 전부 자동화한다.

## 하위 세션 (COO가 만들고 결과를 회수)
| 세션 | 모델 | 브랜치 | 산출물 | 상태 |
|---|---|---|---|---|
| [B] C1-1 한국 트렌드 리서치 `session_01RNNuzoB3dzZumkcKBTL7Hc` | Opus 5.5 | cardnews/main | cardnews/research/C1-1-trends.md | 10-02 00:40 idle·미푸시(검증 대기로 멈춤) → 완료·푸시 지시함 |
| [A] EP003 기획 리서치 `session_0145scVsCxXku3zsXuRne9dq` | Opus 5.5 | ep/EP003 | episodes/EP003/research.md, trends-last30days.md | **완료(아카이브)** 커밋 1479ba1. 1위 "The Weekend All of Korea Makes Kimchi — and Why It's Disappearing"(서사형, 시리즈 "Korea's Calendar" 1편, 11/22 김치의 날). 후보 10(서사 7/구매 3), 사실 ✅11/△5/단일3/미검증1. 주의: 건강 효능·한중 김치 논쟁 회피 조건 |
| [공통] 오픈소스·무료 제작 도구 리서치 `session_0154P65p56MnDyX5xpf1hu4H` | Opus 5.5 | research/tooling-opensource | docs/TOOLING_OPENSOURCE.md | 2026-10-02 생성(대표: 상용 2안 대신 획기적·오픈소스 조사) |
| [공통] ECC 선별 스킬 10개 복사 설치 → 검수 PR `session_01QPhC1w7MVYrkXSAuq2pL8X` | Fable | ecc/install | .claude/skills/ecc-*, SKILLS.md | **완료(아카이브)** PR #3 https://github.com/Memoseadmin/ke-studio/pull/3 (10개, diff 0, ≈900토큰/턴). 대표 approved 대기 |
| [A] 구독자 급성장 전략 리서치 `session_01RWSgtzvYa76kJvHhx68VBX` | Opus 5.5 | research/growth | docs/GROWTH_STRATEGY.md(90일 플레이북) | 2026-10-02 생성(대표: 빠른 구독자 확보 방안) |
| [B] 한국 협찬 시장·단가·벤치마크 리서치 `session_015bpAd3rWkKHmBQvWjZJdXy` | Opus 5.5 | research/cardnews-sponsorship | cardnews/docs/SPONSORSHIP_MARKET.md(단가·계정 이름 3안) | 2026-10-02 생성(COO 추론으로 추가) |
- 리서치는 대표 지시로 별도 세션·Opus. 제작(writer/designer/marketer/legal)은 COO 세션의 서브에이전트.
- ECC(Everything Claude Code): 클라우드 세션은 플러그인을 로드하지 않으므로(공식 문서) 복사 설치만 가능. **대표 결정(2026-10-02): 쓸만한 스킬만 도입, 별도 세션·브랜치(`ecc/install`)에서 실행 → 검수 PR → approved 후 작업 브랜치에 병합.** docs/ECC_REVIEW.md(검토 중) 기준으로 선별.

## 공용 자원
- 직원 9명 `.claude/agents/`, 스킬 96개, 디자인 시스템 `episodes/EP001/design/design-system.md`, 비주얼 방향 "민화 플랫 × 한지 질감"(docs/TOOLING_TTS_IMAGE.md §D).
- 비용 상한 월 20만원(전 프로젝트 합). analyst가 월간 리포트에서 프로젝트별로 나눠 보고.
