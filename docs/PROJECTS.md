# KE Studio 통합 현황판 (COO 세션이 매 세션 시작·종료 때 갱신)

갱신: 2026-10-02 03:00 · 운영 원칙: **세션 1개(COO)가 모든 프로젝트를 관리**한다. 프로젝트마다 폴더·브랜치만 분리하고, 작업은 `.worktrees/<project>`(git worktree)로 병렬 진행한다. 대표는 PR 승인·반려와 결정 항목만 본다.

## 프로젝트
| 프로젝트 | 목적·수익 | 폴더 | 브랜치 | 문서 | 현재 Phase | 게이트 |
|---|---|---|---|---|---|---|
| A. Korea Explained (유튜브 롱폼+숏폼) | 구독형 혼합: 제휴 → YPP 광고 → 멤버십 | `episodes/`, `docs/` | 산출물 `ep/EPxxx`, 문서 `claude/admiring-clarke-beyyoi` | docs/PLAN.md · HANDOFF.md | Phase 5 대기(키·공급자) | 90일 구독 1,000 + 첫 제휴 매출 + 월 20만원 |
| B. 카드뉴스 "책가도 노트" (인스타그램 캐러셀, **한국어·한국 독자**) | **한국 브랜드 제휴·협찬 광고 게시물**(보조: 쿠팡파트너스) | `cardnews/` | `cardnews/main`(검수 PR은 `cardnews/c1-x`) | cardnews/docs/PLAN.md · HANDOFF.md | C1-1 완료(PR #4) → C1-2 | 90일 팔로워 2,000 + 저장률 3% + 미디어킷 + 제안 5건 + 월 5만원 |

## 상태 한눈에
| 항목 | A 유튜브 | B 카드뉴스 |
|---|---|---|
| 승인된 PR | #1 EP001, #2 EP002 (approved) · #3 ECC 설치 approved → **작업 브랜치에 머지(9c97b71)** | **#4 C1-1 14일 세트 approved → cardnews/main 머지(98d2a96, final 렌더·legal v3 BLOCK 0)** · **#5 C1-1b 릴스 14개+프로필 패키지 검수 중** https://github.com/Memoseadmin/ke-studio/pull/5 · **디자인 v2(AI 민화 배경+실사 사진) 작업 중, 브랜치 cardnews/c1-1-design** |
| 업로드/게시 | 0건 (키 UNSET, FIX 3) | 0건 (계정 미개설) |
| 막힌 것 | TTS·이미지·YouTube 키, Amazon 트래킹 ID, 공급자 선택 | **R2_ACCESS_KEY_ID 재입력(32자)** · **IG_USER_ID 교체(IG 계정 ID) + 페이지↔IG 연결 또는 Instagram 직접 로그인 경로(B)로 전환** · 링크 허브 URL |
| 이번 세션 할 일 | 키 들어오면 샘플 생성→렌더→업로드 게이트, EP003 대본 | C1-2: PR #4 승인 → final 렌더 → R2·IG 검증 → 예약 게시 큐 |

## 대표 결정 큐 (하나로 합침)
1. ~~ECC 도입 범위~~ → 결정됨: 선별 도입, 별도 세션·브랜치
2. [A] 제작 도구(docs/TOOLING_OPENSOURCE.md §3): ①비주얼 = OSS-③ 코드 모션그래픽 하이브리드 채택 여부(EP002 S01 A/B 샘플 후) ②음성 기본값 Gemini(≈1천원, 추천)/ElevenLabs(≈3.1만)/Kokoro(0원) ③자체 민화 LoRA 학습(1회 0.3~1.3만원, 소재 = 자체 플레이트 vs 공공누리 민화, legal 확인) — 키: `GEMINI_API_KEY`(유료 티어), `FAL_KEY`
2-1. [A] 성장 전략(docs/GROWTH_STRATEGY.md §11): D1 숏폼 주 7개(파생 5+독립 질문형 2, 하루 1개) / D2 외부 커뮤니티 = r/KDRAMA 지정 스레드+r/korea 댓글 9:1+X·Threads / D3 콜라보 = 같은 규모 채널에 0원 제안(섭외 메시지는 PR 승인) — 전부 기본값(추천)으로 적용 중, 바꾸면 해당 주차만 수정
2-2. [A] PLAN.md 개정: YPP 신규 문턱 2배(2027-02-01) 반영, 멤버십→팬펀딩 문턱(500구독+3,000시간)으로 앞당김 — COO가 개정안 PR, 대표 승인
2. [A] 키 입력: TTS_API_KEY, IMAGE_API_KEY, YOUTUBE_* 3개(scripts/youtube_auth.py), 선택 MUAPI_API_KEY
3. [A] Amazon Associates 가입 + 트래킹 ID, 제휴 상품 확정
4. [A] 채널 마스코트 캐릭터 도입 여부(민화 소재 시안 3개 제안 중)
5. [B] ~~언어~~ KR 확정. **계정 이름 선택: ①책가도 노트(추천) ②알고보니 한국 ③민화 위클리**(핸들·상표는 대표가 앱에서 확인). 플랫폼: 무료 체험단 4곳+IG 크리에이터 마켓플레이스(기본안), 공동구매 보류. 사업자 등록은 첫 유료 협찬 전 3.3% 원천징수(기본안). **게시 = Meta Graph API 자동 예약 확정**(썸네일·문구는 PR에서 대표가 고름) → 인스타 비즈니스 계정 + `IG_ACCESS_TOKEN`·`IG_USER_ID` 필요. **제휴 = 가능한 프로그램 전부 등록해 두고 필요할 때 사용(대표 결정)** → docs/AFFILIATE_PROGRAMS.md 완성(28개: 지금 가입 15 / 첫 업로드 직전 2(Amazon·쿠팡) / 필요 시)
6. [공통] 월 비용 배정: A 15만 + B 5만(기본)

## 세션 위생 규칙 (대표 지시 2026-10-02, 매 세션 시작·종료 때 반드시)
1. 아래 표의 하위 세션을 `get_session`으로 전부 확인한다(status_bucket).
2. completed → 산출물 브랜치를 fetch해 결과 요약을 이 표에 적고 **archive_session**. failed → list_events로 원인 확인 후 재지시 또는 archive. idle(review_ready)인데 푸시가 없으면 send_message로 완료·푸시 지시.
3. 표에서 archived 행은 "완료(아카이브)"로 남긴다(삭제하지 않음). 새 세션을 만들면 즉시 이 표에 추가한다.
4. 대표가 직접 해야 하는 일(계정 가입·OAuth 동의·결제·토큰 발급)은 자동화하지 않는다. 그 전후 단계는 전부 자동화한다.
5. **하위 세션 모델 규칙(대표 지시 2026-10-02)**: 기본값(상위 세션과 같은 모델)으로 띄우지 않는다. COO가 작업 성격으로 판단해 `model`을 명시한다 — 리서치·전략·판단이 필요한 작업 = `claude-opus-5-5`, 스크립트·정리·반복·형식 변환 = `claude-sonnet-5-5`. PROJECTS 표의 "모델" 열에 기록.

## 하위 세션 (COO가 만들고 결과를 회수)
| 세션 | 모델 | 브랜치 | 산출물 | 상태 |
|---|---|---|---|---|
| [B] C1-1 한국 트렌드 리서치 `session_01RNNuzoB3dzZumkcKBTL7Hc` | Opus 5.5 | cardnews/main | cardnews/research/C1-1-trends.md | **완료(아카이브)** 커밋 30a94c4·bb54a77. 후보 14(EP 재활용 2 + 한국 트렌드 12, 전부 KR). 수집 25건 중 교차확인 8/단일 14/미검증 3 → 게시 전 원문 대조 필요(§5). 한국 소스는 WebSearch 대체, 인스타 해시태그 반응 미측정 |
| [A] EP003 기획 리서치 `session_0145scVsCxXku3zsXuRne9dq` | Opus 5.5 | ep/EP003 | episodes/EP003/research.md, trends-last30days.md | **완료(아카이브)** 커밋 1479ba1. 1위 "The Weekend All of Korea Makes Kimchi — and Why It's Disappearing"(서사형, 시리즈 "Korea's Calendar" 1편, 11/22 김치의 날). 후보 10(서사 7/구매 3), 사실 ✅11/△5/단일3/미검증1. 주의: 건강 효능·한중 김치 논쟁 회피 조건 |
| [공통] 오픈소스·무료 제작 도구 리서치 `session_0154P65p56MnDyX5xpf1hu4H` | Opus 5.5 | research/tooling-opensource | docs/TOOLING_OPENSOURCE.md | **완료(아카이브)** e62df3a, 작업 브랜치에 머지. 결론: "생성을 줄여라" — 움직임·한글·종이·지도는 Remotion 코드 모션그래픽(0원, AI 티 없음), AI는 민화 배경 플레이트만(Z-Image Turbo + 자체 LoRA, fal), 음성은 상용 저가 유지(Gemini Flash TTS ≈1천원, Kokoro 0원 백업). OSS-③ 하이브리드 월 ≈7,500원(+LoRA 1회 0.3~1.3만). 상업 불가 모델(Hunyuan 한국 배제, Qwen-Image-2.1·F5·XTTS·Fish 비상업) 제외 |
| [공통] ECC 선별 스킬 10개 복사 설치 → 검수 PR `session_01QPhC1w7MVYrkXSAuq2pL8X` | Fable | ecc/install | .claude/skills/ecc-*, SKILLS.md | **완료(아카이브)** PR #3 https://github.com/Memoseadmin/ke-studio/pull/3 (10개, diff 0, ≈900토큰/턴). 대표 approved 대기 |
| [A] 구독자 급성장 전략 리서치 `session_01RWSgtzvYa76kJvHhx68VBX` | Opus 5.5 | research/growth | docs/GROWTH_STRATEGY.md(90일 플레이북) | **완료(아카이브)** 작업 브랜치에 머지. 핵심: 업로드 간격은 성과와 무관(공식)→주 1편 유지, 바꿀 것 = ①검색 질문형 제목 ②시리즈 2개 고정+엔드스크린 ③숏폼 하루 1개 분산(주 7개 기본값)+관련 영상 링크 ④날짜 훅 역산(한글날 10/9·빼빼로 11/11·수능 11/19·설 2027-02-07) ⑤멤버십을 팬펀딩 문턱(500구독+3,000시간)으로 앞당김. **YPP 2027-02-01부터 신규 문턱 2배(8,000시간/숏폼 2,000만뷰)** → PLAN.md 수익 구조 개정 필요. r/videos·r/history 자기홍보 금지, YouTube Collaborations(최대 10명)+Reels·TikTok 직접 업로드 권장 |
| [B] 한국 협찬 시장·단가·벤치마크 리서치 `session_015bpAd3rWkKHmBQvWjZJdXy` | Opus 5.5 | research/cardnews-sponsorship → cardnews/main 머지 | cardnews/docs/SPONSORSHIP_MARKET.md(222행) | **완료(아카이브)**. 단가(추정): 1만 팔로워 피드 1건 10~30만, 5만 50~170만. 첫 현금 경로 = 지자체·관광재단 서포터즈(월 10~20만, 팔로워 조건 거의 없음)+체험단. 유료 협찬은 5천~1만 이후. 계정 이름 3안: ①책가도 노트(추천) ②알고보니 한국 ③민화 위클리. 첫 9개 그리드 제안. 규제: 표시는 첫 부분·더보기 금지 + 유료 파트너십 라벨. 참고: 해시태그 5개 상한, 캐러셀 8~10장 권장, 릴스 병행 |
- 리서치는 대표 지시로 별도 세션·Opus. 제작(writer/designer/marketer/legal)은 COO 세션의 서브에이전트.
- ECC(Everything Claude Code): 클라우드 세션은 플러그인을 로드하지 않으므로(공식 문서) 복사 설치만 가능. **대표 결정(2026-10-02): 쓸만한 스킬만 도입, 별도 세션·브랜치(`ecc/install`)에서 실행 → 검수 PR → approved 후 작업 브랜치에 병합.** docs/ECC_REVIEW.md(검토 중) 기준으로 선별.

| ~~`session_0123PjHg4syrrzozsBss7aRr`(Fable, 모델 규칙 위반으로 아카이브)~~ → [B] Instagram API 읽기 전용 연결 테스트 + 게시 스크립트(dry-run) `session_01A3aHmduYXmSGmBrsgyd3gd` | Sonnet 5.5 | tooling/ig-publisher → 작업 브랜치 머지 | scripts/ig_publish.py·r2_upload.py·ig_token_refresh.py·README-ig.md, cardnews/docs/IG_CONNECTION.md | **완료(아카이브)**. 연결 테스트는 `IG_ACCESS_TOKEN`·`IG_USER_ID` **UNSET이라 건너뜀**(대표가 환경 설정에 저장했는지 확인 필요). dry-run 정상(게이트: approved 라벨·목업 차단 동작). 업로드·게시 0건 |

| [B] 환경변수 검증 — R2 왕복 테스트 + IG 읽기 전용 `session_01JSpa9BYvBC9XNTLrdgMyCy` | Sonnet 5.5 | tooling/ig-publisher(**미푸시**: 그 세션의 git push가 권한 분류기에 막힘, 커밋 f2330b5 로컬만) | 보고는 list_events로 회수 | **완료(아카이브)**. 변수 8개 전부 SET. **R2 실패**: `R2_ACCESS_KEY_ID`가 20자(32자여야 함 → 잘못된 값 붙여넣음). **IG 실패**: `IG_USER_ID`=1336287509569193은 페이스북 페이지 ID(IG 계정 ID 아님), `/me/accounts` 빈 목록(토큰에 페이지 미연결, 계정 제한 추정). 토큰 자체는 유효·권한 5개 granted. 경로 B(graph.instagram.com)는 페이스북 토큰이라 불가 |

| [B] 환경변수 **재검증** — R2 왕복 + IG 경로 A/B `session_01THknjq4c1h44pboBGRvAWV` | Sonnet 5.5 | 없음(읽기 전용, 파일 변경 0) | 보고는 list_events로 회수 | **완료(아카이브)** 2026-10-02. **대표 수정 전 상태 그대로**: R2 키 ID 20자(32 필요)·시크릿 32자(64 필요) → put `InvalidArgument`(업로드 0). IG 토큰 `EAA`(페이스북 로그인) 유효, 권한 5개 granted, `/me/accounts` 페이지 0개, `IG_USER_ID`=페이지 ID(username 없음). 경로 B `graph.instagram.com/me` 400 code 190(EAA 토큰이라 당연) → **IGAA 토큰 새로 발급 필요**. COO가 `ig_publish.py`에 `IG_API_BASE` 분기·`--check` 추가(9e34674) |
| [B] R2 키 재검증(대표 재입력 후) — 왕복 + PNG Content-Type `session_01DDLFtMWVtKakRHoPAvY46L` | Sonnet 5.5 | 없음(읽기 전용, 파일 변경 0) | 보고는 list_events로 회수 | **완료(아카이브)**. 길이 KEY_ID 64·SECRET 32(**두 값이 서로 바뀜**). 계정 엔드포인트 SSLError로 put 미실행(업로드 0) |
| [B] R2 계정 ID 일치 확인 `session_01AL8dBNE2STSUkrwrwxLoLL` | Sonnet 5.5 | 없음(읽기 전용) | list_events | **완료(아카이브)**. 새 `R2_ACCOUNT_ID`(32자 hex)가 이전 정상값과 **다름**, 키 두 값과도 다름 → 존재하지 않는 계정이라 SSL 핸드셰이크 거부(COO 세션의 이전 값은 R2가 400 응답 = 정상 주소). 네트워크 차단 아님 |
| [B] IG 경로 B 토큰 확인 + R2 재확인 `session_01PgobjmxjLQgda47utgKtdH` | Sonnet 5.5 | 없음(읽기 전용) | list_events | **완료(아카이브)**. **IG 통과**: 토큰 IGAA, `ig_publish.py --check` 경로 B·username=chaekgado.note·IG_USER_ID 일치, BUSINESS, content_publishing_limit 0/100(24h). 쓰기 API 미호출. R2는 대표 재입력 전 값이라 미통과(32/64/32, 계정 불일치) |
| [B] R2 재확인 #3 `session_014VArU1639pxzGs4QGvyY94` | Sonnet 5.5 | 없음(읽기 전용) | list_events | **완료(아카이브)**. 계정 ID는 **정상값으로 복구됨**(이전 정상 계정과 일치). 키는 여전히 KEY_ID 64자/SECRET 32자(**서로 바뀜**) → put `InvalidArgument`. 하위 세션이 값을 바꿔 넣어 보는 시도는 권한 분류기에 차단(자격증명 탐색) → COO도 하지 않음, 대표가 두 칸을 맞바꿔야 함 |
| [B] R2 재확인 #4(키 맞바꾼 후) `session_011HdKKY5mUKiwMzarqftQqF` | Sonnet 5.5 | 없음(읽기 전용) | list_events | 진행 중 |

## 공용 자원
- 직원 9명 `.claude/agents/`, 스킬 96개, 디자인 시스템 `episodes/EP001/design/design-system.md`, 비주얼 방향 "민화 플랫 × 한지 질감"(docs/TOOLING_TTS_IMAGE.md §D).
- 비용 상한 월 20만원(전 프로젝트 합). analyst가 월간 리포트에서 프로젝트별로 나눠 보고.
