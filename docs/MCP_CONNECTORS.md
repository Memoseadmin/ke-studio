# MCP 커넥터 연결 계획 (대표 지시 2026-10-02 "필요한 MCP는 추천해서 나한테 연결하라고 해라")

연결은 **대표가 직접** https://claude.ai/customize/connectors 에서 한다(OAuth·계정·요금은 대표 확인). 연결 뒤 **새 세션부터** 도구가 보인다(세션 시작 때 읽음). 조직 연결 커넥터는 2026-10-02 기준 0개.
COO 규칙: 세션이 MCP가 필요하다고 판단하면 이 표에 행을 추가하고 대표에게 "연결 요청"만 한다. 저장소 `.mcp.json`·settings는 바꾸지 않는다.

## 1. 대표가 연결하기로 한 것 (2026-10-02 결정)
| 커넥터 | 용도(어느 직원·어느 단계) | 상태 | 비고 |
|---|---|---|---|
| Canva | designer: 카드뉴스 레이아웃·템플릿 자동 채움·PNG 내보내기 | 연결 대기 | 무료 플랜. Canva 소재 상업 라이선스는 legal 확인 후 사용 |
| Figma | designer: 디자인 시스템·템플릿 관리, 변수·스크린샷 추출 | 연결 대기 | 무료 플랜 |
| HyperFrames (HeyGen) | producer: HTML 모션그래픽 → 영상 렌더(Remotion 대안, N3 비교) | 연결 대기 | 요금 미확인 |
| Google Drive | 공통: 영상·contact.png 등 저장소에 못 넣는 산출물 대표 공유 | 연결 대기 | 무료 |
| Metricool | publisher·analyst: 인스타 예약 게시·최적 시간·애널리틱스 | 연결 대기 | 무료 플랜 1브랜드. ig_publish.py 보완/대체는 대표 결정 |
| vidIQ | researcher·marketer: 유튜브 키워드·트렌드·썸네일 비교 | 연결 대기 | 유료 티어 가능성 |

## 2. 대표 추가 요청("AI 디자인·실사 사진·리서치용") — COO 추천
| 분야 | 레지스트리 결과 | 추천 | 주의 |
|---|---|---|---|
| AI 이미지 생성 | 레지스트리에 fal·Replicate·Midjourney 류 **없음** | muapi-cli(설치 세션 진행 중, `MUAPI_API_KEY` 대표 발급) 유지. 또는 fal/Replicate가 MCP URL을 제공하면 "커스텀 커넥터"로 추가(대표 결정) | 공급자 결정(PROJECTS 결정 큐 2)과 묶음 |
| 실사 사진 | **Unsplash** MCP 있음(검색·컬렉션·다운로드) | 연결 추천 | **Unsplash 라이선스 ≠ CC0**(2017-06 이후). 디자인 시스템 §9-2 "CC0·CC BY·공공누리1"에 Unsplash License를 추가할지 **legal 판정 후 대표 결정** |
| 리서치 | **Parallel Search**(무료·인증 없음), Exa, Firecrawl(스크랩) | Parallel Search + Firecrawl 연결 추천 | 한국 소스는 여전히 WebSearch 보조 |

## 3. 연결 뒤 할 일
1. 새 COO 세션에서 `ListConnectors`로 연결 확인 → 이 표 "상태" 갱신.
2. 커넥터별 첫 사용 세션(Sonnet)에서 읽기 전용 호출 1회로 검증 → PROJECTS 하위 세션 표에 기록.
3. 외부 서비스에 보내는 것은 공개 자료·캡션뿐. `.env`·키·대본 초안은 보내지 않는다.
