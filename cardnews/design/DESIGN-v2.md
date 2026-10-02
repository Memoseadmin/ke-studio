# 책가도 노트 디자인 v2 (Pillow 렌더러 개선) — **v3로 대체됨**

> 2026-10-02 designer. **상태: 대체됨.** 대표 결정으로 렌더러는 HTML/CSS → Chromium(v3, `cardnews/design/v3/`, `DESIGN-v3.md`)으로 바뀌었다. v2는 커밋 가능한 상태로 정리만 하고 더 손대지 않는다. 시각 방향은 v3 문서를 따른다.
> 글(cards.json·caption.txt)은 한 글자도 바꾸지 않았다.

## 1. 바뀐 것 (render_cards.py, 기존 동작 유지)
| 항목 | 내용 |
|---|---|
| 글꼴 설정 | `cardnews/design/fonts/fonts.json`: 역할별 체인(head·body·bold·latin), 행간·자간, 파일별 라이선스·sha256. OFL 글꼴이면 무엇이든 이 파일만 고쳐 바꾼다. `--fonts PATH`로 다른 설정 사용 |
| 동봉 글꼴 | Black Han Sans 1.001, Pretendard 1.309(Regular·Bold·Black) + OFL 2개. 원본과 sha256 일치 |
| 글자 단위 폴백 | 기본 글꼴 cmap(fontTools)에 없는 글자만 다음 글꼴로. 기준선은 공유하고, 크기는 '한' 잉크 높이로 맞춘다. 실제 폴백: · ↑ → ① ③는 Pretendard Black, ㅿ ㆁ ㆆ는 WenQuanYi |
| 가짜 볼드 | 진짜 굵은 글꼴이면 끈다(fake_bold false) |
| 잘림 경고 | 줄 상한·항목 상한으로 빠지는 글자를 전부 `잘림:` 경고로 남기고 RENDER.json `truncations`에 기록. `--strict`면 종료 코드 3 |
| 금칙 | 줄 끝에 홀로 남는 → □ · ( 『 ①~⑤는 다음 단어에 붙인다(v2 프로필에서만) |
| 그림 칸 | 사진(`photos/PHOTOS.json`, 크레딧·라이선스 없으면 렌더 거부) > AI 플레이트(`plates/card-NN.png`, 늘리지 않고 크롭) > 코드 도형. 마지막 장은 단청 띠로 고정 |
| 출력 | `--out DIR`(원본 PNG를 덮어쓰지 않음), `--no-bundled-fonts`(v1 결과와 같음). 사진·AI가 든 장은 PNG-24로 저장 |
| RENDER.json | 글꼴 체인·버전·라이선스·sha256, 글리프 검사(그린 글자 수·폴백 글자·두부), 잘림, 장별 그림 출처(사진 크레딧·AI 모델·seed) |

## 2. 같이 만든 도구 (v3에서도 재사용 가능)
- `gen_plates.py` + `plate_style.json` + `plate_subjects.json`: fal `fal-ai/z-image/turbo`용 프롬프트를 만든다. 기본 dry-run으로 `plates/prompts.json`만 쓰고, `--execute`일 때만 `FAL_KEY`로 호출한다(키 값은 출력하지 않는다). `--sets`, `--cards`, `--variants N`(표지 시안), `--pick DATE:CARD=V`를 지원한다. seed = MMDD×1000 + 장×10 + 시안. 금지어 검사와 마지막 장 제외 규칙이 들어 있다.
  - 현재: 14세트 중 13세트의 prompts.json(88장, 예상 약 $0.45, 추정). 세트 01은 대표 결정(AI 미사용)에 따라 제외했다.
  - `--backend local`(ComfyUI 목록 내보내기)은 v3 전환으로 **구현하지 않았다**.
- `place_photos.py`: researcher 목록(`photos/C1-1-photos.json`)을 게시물별 `photos/PHOTOS.json`으로 옮긴다. 원본은 `photos/src/`에 두고, 실사는 기본 `edit.preset = muted-warm`을 붙인다. 라이선스 판정은 렌더러와 같다(공공누리 1유형·CC0·CC BY는 허용, BY-SA는 legal 확인, NC·ND·2~4유형은 거부).
  - 51개 후보를 점검한 결과 전부 통과했다(dry-run).

## 3. 검증
| 기준 | 결과 |
|---|---|
| 104장 두부(fontTools cmap, 그린 글자 단위) | **0건** (그린 글자 9,010자) |
| 잘림(줄·항목 상한) | **0건** (14세트, `--strict` 종료 코드 0) |
| 기존 동작(legacy 프로필) | 같은 배경으로 v1 렌더러와 104장 픽셀 비교 → **차이 0장** |
| 사진 칸 | 합성 시험 이미지로 확인: 초점 크롭, 크레딧 알약 표시. 크레딧이 없거나 PHOTOS.json이 없거나 NC 라이선스면 종료 코드 2로 거부 |
| gen_plates | 키가 없으면 종료 코드 2. 모의 호출로 seed·시안·채택·PLATES.json 기록 확인 |

## 4. 미리보기 자가 비평 (design-critique 구조, `preview-v2/` 3세트)
- **첫인상**: 글꼴 교체만으로 제목 위계가 살아났다. 반면 그림은 같은 책장 도형이 반복되고, 본문 아래에 약 300px 빈 띠가 남는다.
- **위계**: 제목(Black Han Sans) → 본문 → 그림 순서로 읽힌다. 본문(Pretendard 44px)은 360px 폭에서 약 15px로 읽히지만 가볍다.
- **일관성**:
  - 마지막 장 띠가 세트마다 달랐다(책장·한지·단청) → 단청으로 고정해 반영했다.
  - 줄 끝 → □ 고아 문제는 금칙으로 반영했다.
- **접근성**: 대비는 ink/paper 17.1, white/red 5.9로 통과.
- **남은 것**: 빈 띠와 내용과 무관한 도형은 좌표를 바꿔야 고칠 수 있다. 템플릿 좌표 유지 조건 때문에 v2에서는 고치지 않았고, v3에서 해소했다.
