# KE Studio 통합 현황판 (COO 세션이 매 세션 시작·종료 때 갱신)

갱신: 2026-10-02 · 운영 원칙(대표 지시 2026-10-02 개정): **이 세션(COO)은 대표의 명령·총괄 의사결정·기획만 다룬다. 모든 실작업은 난이도별로 자식 세션에 배분**(판단·리서치·제작 = Opus, 반복·스크립트·검증 = Sonnet)하고 COO가 결과를 회수해 대표에게 보고한다. **대표가 결정하지 않은 사항은 기본값으로 진행하지 않고 끝까지 대표에게 묻는다.** 프로젝트마다 폴더·브랜치만 분리하고, 작업은 `.worktrees/<project>`(git worktree)로 병렬 진행한다. 대표는 PR 승인·반려와 결정 항목만 본다.

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
| 막힌 것 | TTS·이미지·YouTube 키, Amazon 트래킹 ID, 공급자 선택 | ~~R2·IG 키~~ **둘 다 통과(2026-10-02)** · 남은 것: **디자인 v3**(대표: 현재 품질 불가, 리서치 중) · 링크 허브 URL · PR #5 결정 5개 |
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
6-1. [A] **유튜브 결정(2026-10-02)**: N1 채널명 = **"Korea" 없는 이름으로 재탐색**(Opus 세션) · N2 제작 = **원화 아카이브 × 코드 모션**(AI 플레이트는 보조) · N3 = **Remotion**. N4 촬영 = **폰만(0원)으로 시작** · N5 AI 표시 체크 = **사실적 AI 영상·이미지 편만** · N6 썸네일 = **낙관+한지 테두리 / 노란 바 둘 다 만들어 A/B**. N7 카테고리 = **Education** · N9 숏폼 = **YT Shorts + TikTok + IG Reels(영어 새 계정)** · N10 EP002 공개일 = **키·채널 준비 후 재결정** · N13 = **OAuth 프로덕션 전환 + 감사 신청, 통과 전 수동 업로드**. N11 LoRA/로컬 = **나중에 결정**(세트 02 AI 배경 샘플 후). 미결: N8 유료 프로모션(legal 판정 후), N12 도메인·상표(이름 확정 후).
6-2. [B] bio v3 3안 → 대표 "다시: '민화 원화' 말을 빼고" → v4 Opus 세션 `session_017b2PHN9TM8TMubVawfVykv`.
7. [B] **디자인 v3(대표 결정 2026-10-02)**: **이미지는 장 내용에서 출발(대표 지적: 1판은 주제·사진 불일치) — 장별 VISUAL-BRIEF 먼저, 사진이 주인공, 원화는 프레임·장식만.** 현재 카드 품질 불가 → ① **10/09 세트 01 = AI 없이 프로토타입**(퍼블릭 도메인 원본 + 편집된 실사 + 코드 그래픽 + OFL 서체) ② **02~14 = AI 배경 + 편집된 실사**(실사 원본 그대로 금지, 톤·크롭·질감 편집 필수) ③ 대표 PC NVIDIA GPU 있음 → 로컬 ComfyUI 생성 가능, **FAL_KEY 보류**. 리서치(DESIGN_SOURCES.md) 후 시각 방향 3안 중 택1 → v3 검수 PR → approved 후 R2 업로드·게시
8. [B] **독자·언어(대표 2026-10-02)**: "일단 한국어로 계속 시작". 대표 메모: 한국 문화 관심층은 외국인이 더 많을 수 있고, 여행·음식·축제를 통합한 최신 트렌드 카드뉴스가 목표 → C1-2 기획 때 **이중언어 레이어(한글 제목 + 영어 부제, 캡션 영어 요약, KR/EN 해시태그)** 안을 다시 올림. 소재 비율은 여행·음식·축제·전시 유지
10. [공통] **MCP 커넥터(대표 2026-10-02)**: Canva·Figma·HyperFrames·Google Drive·Metricool·vidIQ 연결 결정(대표가 claude.ai/customize/connectors에서 직접, 새 세션부터 사용). 추가 요청 "AI 디자인·실사 사진·리서치용" → COO 추천: Unsplash(라이선스 ≠ CC0, legal 후 결정)·Parallel Search·Firecrawl, AI 이미지는 레지스트리 없음 → muapi 유지/커스텀 커넥터. 상세 docs/MCP_CONNECTORS.md
11. [공통] **muapi(Open-Generative-AI)(대표 2026-10-02)**: 지금은 CLI 설치만, 키는 대표 발급 후 통보 → 첫 결과물 = [A] EP002 S01 플레이트+5초 영상 + [B] 세트 02 AI 배경 1장(둘 다)
12. [A] 채널명: 1차 상위 5 보류 → 2차 "쉬운 영어 일반어 조합" 탐색 중. [B] bio v4 반려(AI틱) → v5. 디자인 시스템 v1.1 → **v1.2**(§9 원화 비중 유동적, §8-3 톤 강화) 확정
9. [B] **첫 게시(대표 2026-10-02)**: **10/2 오늘 프로토타입 1개 = 세트 11 필사 입문(v3 1안 렌더)** → 10/3~10/8은 v3 전환·프로필 세팅 → 10/9부터 14일 플랜대로. 캡션·프로필 문안은 marketer가 재초안(대표: "다시 초안 생성"). **대표 결정(2026-10-02 재질문)**: v3 = **3안 하이브리드 콜라주**(편집 실사 + 민화 프레임·문양) · 서체 **B 한지 모던** · **AI 고지 문구 삭제, 출처만**(카드·캡션 모두; 게시 게이트 (3)을 '출처 줄'로 변경) · 프로필 사진 = **v3 원화 톤으로 재제작**(A/B/C 폐기). 스킬 4개는 이미 설치됨(b7cdaa7). **추가 결정(2026-10-02)**: 이름 필드 `책가도 노트 | 민화 원화로 보는 오늘의 한국` · 19:00일 릴스 = **같은 날 21:00** · 링크 허브 = **무료 허브 서비스(Linktree류, 대표 개설 후 URL)** · bio = **다시 쓰기, 여행·음식·축제 트렌드를 앞에**(Opus 자식 세션) · 세트 11 = **3안으로 다시 만들어 오늘(10/2) 게시**(1안 렌더 21bbd0e는 기록). 디자인 시스템 = **4:5 규격·원화 사용 규칙 추가(v1.1)** · 호작도 = **퍼블릭 도메인 호작도 원화 허용**(자체 그림·AI 생성은 금지 유지) · LoRA = 나중에 결정 · 이중언어 = C1-2

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
- 리서치는 대표 지시로 별도 세션·Opus. 제작(writer/designer/marketer/legal)은 COO 세션의 서브에이전트. **단 2026-10-02 대표 지시: 포스트 세트 제작(렌더·캡션·자가 검수)도 자식 세션으로 병렬 처리 가능 — 판단이 필요한 제작은 Opus, 재렌더·업로드·게시 같은 반복 실행은 Sonnet.** 자식 세션은 자기 브랜치(`cardnews/v3-sets-X`)에 푸시, COO가 legal → 머지 → PR.
- ECC(Everything Claude Code): 클라우드 세션은 플러그인을 로드하지 않으므로(공식 문서) 복사 설치만 가능. **대표 결정(2026-10-02): 쓸만한 스킬만 도입, 별도 세션·브랜치(`ecc/install`)에서 실행 → 검수 PR → approved 후 작업 브랜치에 병합.** docs/ECC_REVIEW.md(검토 중) 기준으로 선별.

| ~~`session_0123PjHg4syrrzozsBss7aRr`(Fable, 모델 규칙 위반으로 아카이브)~~ → [B] Instagram API 읽기 전용 연결 테스트 + 게시 스크립트(dry-run) `session_01A3aHmduYXmSGmBrsgyd3gd` | Sonnet 5.5 | tooling/ig-publisher → 작업 브랜치 머지 | scripts/ig_publish.py·r2_upload.py·ig_token_refresh.py·README-ig.md, cardnews/docs/IG_CONNECTION.md | **완료(아카이브)**. 연결 테스트는 `IG_ACCESS_TOKEN`·`IG_USER_ID` **UNSET이라 건너뜀**(대표가 환경 설정에 저장했는지 확인 필요). dry-run 정상(게이트: approved 라벨·목업 차단 동작). 업로드·게시 0건 |

| [B] 환경변수 검증 — R2 왕복 테스트 + IG 읽기 전용 `session_01JSpa9BYvBC9XNTLrdgMyCy` | Sonnet 5.5 | tooling/ig-publisher(**미푸시**: 그 세션의 git push가 권한 분류기에 막힘, 커밋 f2330b5 로컬만) | 보고는 list_events로 회수 | **완료(아카이브)**. 변수 8개 전부 SET. **R2 실패**: `R2_ACCESS_KEY_ID`가 20자(32자여야 함 → 잘못된 값 붙여넣음). **IG 실패**: `IG_USER_ID`=1336287509569193은 페이스북 페이지 ID(IG 계정 ID 아님), `/me/accounts` 빈 목록(토큰에 페이지 미연결, 계정 제한 추정). 토큰 자체는 유효·권한 5개 granted. 경로 B(graph.instagram.com)는 페이스북 토큰이라 불가 |

| [B] 환경변수 **재검증** — R2 왕복 + IG 경로 A/B `session_01THknjq4c1h44pboBGRvAWV` | Sonnet 5.5 | 없음(읽기 전용, 파일 변경 0) | 보고는 list_events로 회수 | **완료(아카이브)** 2026-10-02. **대표 수정 전 상태 그대로**: R2 키 ID 20자(32 필요)·시크릿 32자(64 필요) → put `InvalidArgument`(업로드 0). IG 토큰 `EAA`(페이스북 로그인) 유효, 권한 5개 granted, `/me/accounts` 페이지 0개, `IG_USER_ID`=페이지 ID(username 없음). 경로 B `graph.instagram.com/me` 400 code 190(EAA 토큰이라 당연) → **IGAA 토큰 새로 발급 필요**. COO가 `ig_publish.py`에 `IG_API_BASE` 분기·`--check` 추가(9e34674) |
| [B] R2 키 재검증(대표 재입력 후) — 왕복 + PNG Content-Type `session_01DDLFtMWVtKakRHoPAvY46L` | Sonnet 5.5 | 없음(읽기 전용, 파일 변경 0) | 보고는 list_events로 회수 | **완료(아카이브)**. 길이 KEY_ID 64·SECRET 32(**두 값이 서로 바뀜**). 계정 엔드포인트 SSLError로 put 미실행(업로드 0) |
| [B] R2 계정 ID 일치 확인 `session_01AL8dBNE2STSUkrwrwxLoLL` | Sonnet 5.5 | 없음(읽기 전용) | list_events | **완료(아카이브)**. 새 `R2_ACCOUNT_ID`(32자 hex)가 이전 정상값과 **다름**, 키 두 값과도 다름 → 존재하지 않는 계정이라 SSL 핸드셰이크 거부(COO 세션의 이전 값은 R2가 400 응답 = 정상 주소). 네트워크 차단 아님 |
| [B] IG 경로 B 토큰 확인 + R2 재확인 `session_01PgobjmxjLQgda47utgKtdH` | Sonnet 5.5 | 없음(읽기 전용) | list_events | **완료(아카이브)**. **IG 통과**: 토큰 IGAA, `ig_publish.py --check` 경로 B·username=chaekgado.note·IG_USER_ID 일치, BUSINESS, content_publishing_limit 0/100(24h). 쓰기 API 미호출. R2는 대표 재입력 전 값이라 미통과(32/64/32, 계정 불일치) |
| [B] R2 재확인 #3 `session_014VArU1639pxzGs4QGvyY94` | Sonnet 5.5 | 없음(읽기 전용) | list_events | **완료(아카이브)**. 계정 ID는 **정상값으로 복구됨**(이전 정상 계정과 일치). 키는 여전히 KEY_ID 64자/SECRET 32자(**서로 바뀜**) → put `InvalidArgument`. 하위 세션이 값을 바꿔 넣어 보는 시도는 권한 분류기에 차단(자격증명 탐색) → COO도 하지 않음, 대표가 두 칸을 맞바꿔야 함 |
| [B] R2 재확인 #4(키 맞바꾼 후) `session_011HdKKY5mUKiwMzarqftQqF` | Sonnet 5.5 | 없음(읽기 전용) | list_events | **완료(아카이브)**. 더 나빠짐: `R2_ACCESS_KEY_ID` **UNSET**, `R2_SECRET_ACCESS_KEY` **63자**(1자 누락), `R2_ACCOUNT_ID` 32자이나 정상값과 **다시 불일치** → put SSLError(존재하지 않는 계정). FAL_KEY UNSET. 대표가 세 값을 처음부터 다시 입력해야 함 |
| [B] R2 재확인 #5(새 토큰 입력 후) `session_01RQWUDFEuckBSLcuiLZBxvq` | Sonnet 5.5 | 없음(읽기 전용) | list_events | **완료(아카이브) — R2 통과**: 계정 ID 정상, 키 32/64, PNG put→head→공개 GET 200(image/png)→delete→404 전부 OK. FAL_KEY UNSET(대표 결정: AI 생성 0안 우선 검토 중이라 보류) |
| [A] **유튜브 채널 런칭 실행 계획 리서치**(이름·실사+모션그래픽 제작·썸네일·마케팅·유튜브 설정 체크리스트·4주 캘린더·대표 결정 목록) `session_01Yau1J62KqGoxS5vZt9LHYo` | Opus 5.5 | research/youtube-launch | docs/YOUTUBE_LAUNCH_PLAN.md | **완료(아카이브)** 9259c07 → 작업 브랜치 머지. 549행·출처 82. 핵심: "Korea Explained"는 핸들·도메인 선점+동명 8곳 → **"Korea, Annotated" 추천** · 제작 = 원화 아카이브 × Remotion 코드 모션(편당 100~400원·대표 1.5h 추정) · 썸네일 3~4단어 흰 대문자+원화 디테일+낙관·한지 테두리 · 마케팅 상위 3(숏폼 원본 직접 업로드+AI 라벨, Collaborations, Reddit 링크 없는 답변) · 개설 체크리스트 42항목(신분증 인증·OAuth 프로덕션·API 감사가 선행) · **대표 결정 N1~N13(기본값 미적용)** |
| [A] 채널명 재탐색(Korea 없는 이름) `session_016zt8mJerJYqG1MGQU8jGNc` | Opus 5.5 | research/channel-name | docs/CHANNEL_NAME.md | **완료(아카이브)** 7a12df0. 후보 15, YT 핸들 34·도메인 24×3 실측. 상위 5: Hanji Archive(22) / Ink & Hanji / Joseon Annotated / The Minhwa Files / The Folding Screen(전부 핸들·.com 미등록). 탈락: Tiger & Magpie·Morning Calm·Red Seal(선점). 상표·IG 핸들 미확인. **대표 답(10/2): "더 찾아봐" → 2차 세션** |
| [B] bio v4('민화 원화' 제거) `session_017b2PHN9TM8TMubVawfVykv` | Opus 5.5 | cardnews/c1-1b | PROFILE.md §2 v4 | **완료(아카이브)** 8c74ac1. A 80자(추천)/B 91자/C 56자. **대표 답(10/2): '저장해 두고 꺼내 보는 카드' 식 문장이 AI틱 → 반려, v5 세션** |
| [B] bio v5(AI틱한 문장 제거, 사람 말투) `session_012bk5xgh6WEmbZ1XDAmdKHH` | Opus 5.5 | cardnews/c1-1b | PROFILE.md §2 v5 | 진행 중 |
| [B] 디자인 시스템 v1.1(4:5·원화 규칙·3안·호작도 예외) `session_01927v4EQ12E5YM2ieLPcc6u` | Sonnet 5.5 | claude/admiring-clarke-beyyoi | episodes/EP001/design/design-system.md | **완료(아카이브)** cb8bba7 작업 브랜치에 머지 |
| [B] 프로필 소개문 재초안(트렌드 앞세움) + 프로필 패키지 정리 `session_01JWwghZRnG8zi1hVX21cKHC` | Opus 5.5 | cardnews/c1-1b | cardnews/profile/PROFILE.md v3 | **완료(아카이브)** 6552806. bio 3안(A 큐레이터형 93자 추천 / B 친구형 98자 / C 선언형 66자), 이름 확정 반영, 허브 4항목+UTM, 고정 순서(10/2 11→10/9 01→10/11 03→10/22 14). 대표 선택 대기 |
| [B] 세트 11 장별 실사 사진 소싱(내용 일치) `session_01LN42UszjCU2PRCMQyZiRJV` | Opus 5.5 | cardnews/c1-1-design | posts/2026-10-19/photos/PHOTOS.v3.json·.md·fetch_photos.py | **완료(아카이브)** 69c3ae2. 1~5장 main+alt 10장 전부 CC0(Unsplash 2017-06 이전 Commons 사본 9 + Pexels 1), BY-SA 4건 제외, 얼굴 0, 흐림·크롭 지시 4건. **6·7장 missing**(대안: 클리블랜드 서예 병풍 CC0 디테일 / 코드 그래픽), 8장 불필요. 위키미디어 429는 Unsplash CDN 사본으로 우회 |
| [공통] muapi-cli 재설치·검증 + Open-Generative-AI 웹 앱 빌드 재시도 `session_01S6xWKVitD4nJypPdcQ65Pr` | Sonnet 5.5 | claude/admiring-clarke-beyyoi | docs/OPEN_GENERATIVE_AI_SETUP.md §6 | 진행 중(대표 지시 10/2 "앱 설치해서 이용", 키는 대표 발급 후) |
| [A] 채널명 2차 탐색(쉬운 영어 일반어 조합) `session_017JRNZbo75BmGY53YqdFxps` | Opus 5.5 | research/channel-name | docs/CHANNEL_NAME.md §6 | 진행 중 |
| [B] 디자인 시스템 v1.2(§9 원화 비중 유동화·§8-3 톤 강화, 대표 결정 10/2) `session_01LrJcNB2rBDHVHbfZDN3qo6` | Sonnet 5.5 | claude/admiring-clarke-beyyoi | design-system.md v1.2 | 진행 중 |
| [공통] ruflo(구 claude-flow) 스킬 조사·복사 설치 → 검수 PR(대표 지시 10/2 "자식 세션 에이전트 분리용") `session_01UQcZmvgEZNEB4oSHKqYKnu` | Opus 5.5 | skills/ruflo | .claude/skills/ruflo-*, docs/SKILLS.md, 검수 PR | 진행 중 |
| [A] EP002·EP001 publish.log 기록(키 UNSET, 제작 건너뜀) `session_01NwVoCoDaV5L12GALoa3ftZ` | Sonnet 5.5 | ep/EP002·ep/EP001 | publish.log | 진행 중 |
| [B] 세트 11 v3 3안 **2판** 렌더(글↔이미지 일치, 대조표 MATCH-v3.md) `session_011mFvAibQZu1MTWegZJXMGb` | Opus 5.5 | cardnews/c1-1-design | posts/2026-10-19/card-01~08·contact.png·RENDER.json·MATCH-v3.md | 진행 중 |
| [B] **세계 수준 카드뉴스 디자인 소싱 리서치**(벤치마크·렌더 파이프라인·OFL 한글 서체(옛한글)·CC0 질감·퍼블릭 도메인 민화·생성 모델 프롬프트·스킬 후보+자체 스킬 초안 3·v3 방향 3안) `session_01QRFKHY6jLwZbZvM1zjf2nX` | Opus 5.5 | research/cardnews-design → cardnews/main 머지 예정 | cardnews/docs/DESIGN_SOURCES.md | **완료(아카이브)** 25f4d10 → cardnews/main 머지. 진단: 중국어 대체 서체+가짜 볼드, 무관한 클립아트 반복, 빈 띠, 위계 없음, 옛한글 깨짐, 질감 소멸. **추천: 렌더러 HTML/CSS→Playwright Chromium(VM 실측 1.1초/장, 옛한글·세로쓰기 OK, Pillow 폐기)** · 서체 세트 B(함렛 Black/마루부리/Black Han Sans, 옛한글은 Noto Serif KR) · 퍼블릭 도메인 원화 31점(Met·Cleveland CC0, e뮤지엄 1유형) · **v3 1안 "원화 아카이브"(AI 0·유료 API 0·월 0원) 추천**, 2안 LoRA 플레이트, 3안 콜라주 · 스킬 후보 4+자체 초안 3(부록 A) · 대표 결정 7건(§8) |

## 공용 자원
- 직원 9명 `.claude/agents/`, 스킬 96개, 디자인 시스템 `episodes/EP001/design/design-system.md`, 비주얼 방향 "민화 플랫 × 한지 질감"(docs/TOOLING_TTS_IMAGE.md §D).
- 비용 상한 월 20만원(전 프로젝트 합). analyst가 월간 리포트에서 프로젝트별로 나눠 보고.
