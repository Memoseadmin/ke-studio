# Korea Explained: Design System v1.0 (채널 공통)

> **채널 공통 1장. EP002 이후 모든 에피소드가 이 파일을 그대로 재사용한다.** 에피소드 폴더에 복사·수정하지 말고 이 파일을 참조한다. 변경은 대표 승인 후 버전을 올려 이 파일에서만 한다.
> 최초 작성: 2026-10-01, designer, EP001. 참고: EP000 더미 토큰(값 유지, 규칙 보강). 스킬: social-media-skills-youtube-thumbnail, social-media-skills-graphic-designer, marketing-skills-image(SKILL.md 지침 적용).

## 1. 색 토큰

| 토큰 | Hex | 용도 |
|---|---|---|
| `ke-red` (primary) | `#C8102E` | 핵심 단어 블록·하이라이트(고추·단청) |
| `ke-yellow` (accent) | `#FFD23F` | 양은냄비 옐로. 강조 텍스트, 시그니처 바 |
| `ke-ink` | `#111111` | 텍스트·외곽선·일러스트 선 |
| `ke-paper` | `#F7F3EA` | 밝은 배경(한지 톤) |
| `ke-night` | `#1B1F2A` | 어두운 배경 |
| `ke-white` | `#FFFFFF` | 어두운 배경 위 텍스트 |
| 일러스트 보조(면적 15% 이하) | `#F2D49B` 면 · `#E0662A` 국물 · `#C9CDD2` 스테인리스 · `#C9A877` 크라프트 무지 패키지 · `#6FA89B` 차트 보조(청자) | 텍스트에 쓰지 않음 |

- 한 장에 **배경 1색(night 또는 paper) + 강조 1색(red 또는 yellow)** 이 지배. 나머지는 소품 색.
- 텍스트 대비(WCAG, 계산값): yellow/night 11.4 · white/night 16.5 · white/red 5.9 · ink/yellow 13.1 · ink/paper 17.1 · red/paper 5.3. **금지 조합**: yellow 글자/red 바탕(4.1), red 글자/night 바탕(2.8). 기준 4.5:1 이상.

## 2. 폰트 (전부 상용 무료)

| 역할 | 폰트 | 라이선스 |
|---|---|---|
| EN 헤드라인(썸네일·타이틀 카드, 대문자) | Anton | SIL OFL 1.1 (Google Fonts) |
| KR 헤드라인 | Black Han Sans | SIL OFL 1.1 (Google Fonts) |
| 자막·본문·차트 라벨(EN/KR) | Pretendard (EN 대체: Inter) | SIL OFL 1.1 / SIL OFL 1.1 |
| 목업 대체(현재 VM에 설치됨, `fc-list` 2026-10-01 확인) | EN: Liberation Sans Bold · KR: WenQuanYi Zen Hei | SIL OFL 1.1 · GPL-2 + font embedding exception(목업 라벨 전용) |

- Anton·Black Han Sans·Pretendard는 VM에 없음. 설치 여부는 `scripts/setup.sh` 담당(COO) 결정. `make_thumbs.py`는 설치되면 자동으로 Anton을 쓴다.
- 영어 철자는 `script.en.md`와 같은 미국식(favorite, aluminum). 화면 문구에 em dash 쓰지 않음.

## 3. 썸네일 레이아웃 (1280x720, 16:9)

- **텍스트 4단어 이하**, 대문자 1~3줄, 제목을 그대로 반복하지 않고 보완. 작은 글씨(부제·출처·가격) 금지.
- **안전 영역**: 사방 64px 안에 텍스트·핵심 오브젝트. **우하단 240x100(x 1040~1280, y 620~720)은 재생시간 배지 자리**라 비움.
- 기본 그리드: 텍스트 왼쪽 45%(x 64~600) / 초점 오브젝트 오른쪽 55%. 가로로 긴 소재는 텍스트 상단 + 오브젝트 하단. 텍스트는 우하단에 두지 않음.
- **얼굴 없는 채널**: 진행자 사진·인물 대신 **단일 초점 사물(냄비·그릇·소품)이 화면 30~50%**. (youtube-thumbnail 스킬의 "얼굴 30~50%" 규칙을 사물로 대체)
- 타이포: 대문자 캡하이트 90px 이상(320px 폭에서 약 22px). 복잡한 배경 위에는 ink 6px 외곽선 또는 단색 블록. 그림자·3D·그라데이션 글자 금지.
- **시그니처**: 텍스트 블록 아래 14px `ke-yellow` 바(ink 2px 테두리). 채널 인식용으로 매 편 유지.
- 스타일: 평면 에디토리얼 일러스트, 굵고 깨끗한 ink 선, 은은한 종이 질감, 흰 김(steam).
- **모바일 검수(필수)**: 1280 원본 + 320x180(피드) + 168x94(추천 사이드바)로 축소해 문구 판독·잘림·대비 확인. 실패 시 수정 후 재검수.
- 파일: PNG/JPG, sRGB, YouTube 업로드 2MB 이하, 저장소 커밋 500KB 이하. 이름 `thumb-1..3.png`, 비교 시트 `thumbs-compare.png`(폭 1920 이하, 300KB 이하).
- AI 생성 이미지는 **글자 없는 플레이트**로 만들고 문구는 후편집에서 위 폰트로 얹는다.

## 4. 숏폼 9:16 (1080x1920)

- 문구 안전 영역: x 60~940, y 260~1440. 상단 220px(상태바·검색), 하단 480px(캡션·채널명·음악), 오른쪽 140px(좋아요·댓글 버튼)에는 글자 금지.
- 초점 오브젝트는 중앙 1:1(y 420~1500) 안에. 프로필 그리드·피드 크롭 대비. 플랫폼 UI는 수시로 바뀌므로 업로드 미리보기로 최종 확인.
- 첫 1초 훅 문구 4단어 이하(Anton 120~140px). 자막 Pretendard Bold 64px, 흰색 + ink 5px 외곽선, y 1150~1400.
- 제휴 고지 바(필요 시): Pretendard 40px 이상, 안전 영역 안, 상품이 나오는 구간 내내 고정. 문구는 marketer 지정 그대로.
- 16:9 원본(1920x1080)에서 세로로 자르면 608x1080 → 1.78배 확대라 화질 저하. **숏폼 후보 장면은 9:16 네이티브로 따로 생성**하거나 원본을 3840x2160 이상으로 만든다.

## 5. AI 이미지 프롬프트 공통 문자열

- 스타일(프롬프트 끝에 붙임): `flat editorial illustration, bold clean ink outlines, warm limited palette of night navy (#1B1F2A), chili red (#C8102E), pot yellow (#FFD23F) and cream paper (#F7F3EA), subtle paper grain, soft white steam, calm cinematic lighting`
- 네거티브(항상 포함): `text, letters, numbers, captions, logos, brand names, trademarks, product packaging graphics, printed labels, readable signage, real people, faces, celebrity likeness, copyrighted characters, mascots, film or TV stills, posters, watermarks, UI elements`
- 네거티브 입력란이 없는 생성기(예: Gemini)는 본문 끝에 `No text, no logos, no brand packaging, no real people or faces.`를 그대로 넣는다.
- 생성 시 기록: 모델명·날짜·프롬프트·시드를 해당 에피소드 `design/`에 남긴다(AI 생성물 공개 라벨·인간 검수 근거).

## 6. 금지 사항 (썸네일·장면·숏폼 공통)

1. **실존 인물 얼굴·닮은꼴**(배우·아이돌·셰프·인플루언서). 인물이 꼭 필요하면 얼굴 없는 뒷모습 실루엣 또는 손만.
2. **브랜드 로고·상표·패키지 디자인 재현**: 라면 봉지·컵, 편의점 간판·브랜드 색 조합, 스트리밍·게임쇼 로고. 패키지는 **무지 패키지**(크라프트·흰색·파스텔 단색, 인쇄 없음)만. 빨강+검정 봉지, 한자 큰 글자 같은 특정 브랜드 연상 요소도 금지.
3. **저작권 캐릭터·마스코트**(애니·게임·웹툰). KPop Demon Hunters 캐릭터와 그 연상 요소(아이돌 3인조 무대, 호랑이·까치 조수 모티프) 포함.
4. **영화·드라마·예능 스틸 재현**: 유명 장면의 세트·의상·구도·색보정 모방, 포스터 패러디.
5. AI 생성 이미지 안의 글자·숫자(전부 후편집 오버레이). 흰 바탕 빨간 십자(적십자 표장 혼동) 금지.
6. 낚시 연출: 과장 반응 얼굴, 빨간 화살표·원 남발, 가짜 "BANNED/SECRET" 문구, 사실과 다른 숫자.
7. 건강·효능·안전 암시(예: healthy, safe), "best/authentic" 같은 과장, 가격 표기.
8. 상용 라이선스가 확인되지 않은 사진·아이콘·폰트·지도(지도 윤곽은 퍼블릭 도메인 Natural Earth 벡터 권장).
