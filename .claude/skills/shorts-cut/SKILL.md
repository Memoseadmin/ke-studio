---
name: shorts-cut
description: KE Studio 사내 스킬. 숏폼 컷 플랜 JSON(장면 번호 + 문단·문장 구간, 훅·CTA 문장)과 ffmpeg-assemble 매니페스트로 1080x1920 9:16 숏폼을 만든다. 상단 훅 텍스트, 자막 번인, 선택적 하단 제휴 고지 바·엔드 카드·AI 고지 라벨을 지원하고 60초(max_seconds)를 넘으면 파일을 만들지 않는다. producer가 marketing.md의 숏폼 컷 플랜을 렌더할 때 쓴다.
---

# shorts-cut (사내 작성, KE Studio)

marketing.md 숏폼 컷 플랜을 9:16 영상으로 만든다. 범용 도구이며 EP마다 플랜 JSON만 바꾼다.
공용 모듈 `.claude/skills/ffmpeg-assemble/scripts/kemedia.py`가 필요하다(같은 저장소의 ffmpeg-assemble 스킬).

## 요구 사항
- Python 3.9+, Pillow, ffmpeg/ffprobe(`scripts/setup.sh`). 없으면 무엇이 없는지 출력하고 멈춘다(임의 설치 금지).
- 장면 정보: ffmpeg-assemble이 만든 `long.manifest.json`(권장. 실제 모드에서 장면 오디오를 문장 단위로 잘라 쓸 수 있음) 또는 장면 JSON(`"scenes": "...json"`).

## 실행 (저장소 루트에서)
```bash
# 길이만 확인 (60초 초과가 있으면 종료 코드 4)
python3 .claude/skills/shorts-cut/scripts/shorts_cut.py episodes/EPxxx/render-input/shorts.en.json --dry-run
# 렌더 + 검수용 컨택트시트(숏폼당 1프레임)
python3 .claude/skills/shorts-cut/scripts/shorts_cut.py episodes/EPxxx/render-input/shorts.en.json \
  --mode mockup --contact-sheet episodes/EPxxx/render-preview/shorts-contact.png
```
옵션(JSON): `hook_max_px`(기본 120), `segment_gap`, `burn_subtitles`, `cue_max_chars`, `music`, `loudnorm`. CLI: `--manifest`, `--only short-1 short-3`, `--mode auto|mockup|real`, `--preset`, `--crf`, `--keep-work`, `--manifest-out`.

## 플랜 JSON
```json
{
  "manifest": "render/EPxxx/long.manifest.json",
  "size": [1080, 1920], "fps": 30, "wpm": 150, "max_seconds": 60, "mode": "auto",
  "mockup_label": "MOCKUP — final AI plate pending",
  "ai_label": {"text": "AI voice & images", "seconds": 1.0},
  "shorts": [
    {
      "id": "short-1", "output": "render/EPxxx/short-1.mp4",
      "hook": "FOUR WORDS MAX",
      "segments": [
        {"role": "hook", "scene": "S05", "text": "훅 내레이션 문장."},
        {"scene": "S05", "paragraphs": [1, 3, 4]},
        {"scene": "S08", "exclude_sentences": [-1]},
        {"scene": "S01", "sentences": [1]},
        {"role": "cta", "scene": "S05", "text": "CTA 문장.", "audio": "render/EPxxx/tts/short-1-cta.wav"}
      ],
      "disclosure_bar": "Affiliate link · I may earn a commission",
      "end_card": {"text": "화면에만 보이는 마무리 문구", "seconds": 4},
      "preview_at": 20.0,
      "notes": "컷 플랜과 다르게 처리한 부분과 이유"
    }
  ]
}
```
- 구간 선택: `paragraphs`(1부터), `sentences`(선택된 문단 안의 문장 번호, 음수는 뒤에서부터), `exclude_sentences`. 또는 `text`로 직접 문장 지정(훅·CTA).
- 세그먼트 화면은 해당 장면의 `image_vertical` > `image`(9:16 커버 크롭, 1.5배 넘게 확대되면 경고) > 목업 패널 순. `screen`·`plate`·`image`로 세그먼트별 덮어쓰기 가능.
- 길이: `duration` > 오디오 길이 > 단어 수 ÷ `wpm`. 오디오는 세그먼트 `audio`(+`audio_in`/`audio_out`) > 매니페스트의 장면 오디오를 문장 큐 시각으로 잘라 씀(타임스탬프가 추정치면 경고) > 무음.
- `max_seconds` 초과 숏폼은 렌더하지 않고 구간별 길이를 출력한다. 줄이는 결정은 marketer·writer 몫이며, producer가 임의로 줄였다면 `notes`와 렌더 로그에 남긴다.

## 레이아웃 (design-system §4, 1080x1920 기준)
- 글자 안전 영역 x 60~940, y 260~1440. 상단 220px·하단 480px·오른쪽 140px에는 글자를 두지 않는다.
- 훅: y 268부터, 최대 120px(2줄 우선, 안 되면 3줄), 노랑 + 잉크 외곽선. 영상 내내 표시.
- 자막: 64px(최소 52px) 흰색 + 잉크 5px 외곽선, 최대 2줄, 하단 기준 y 1400(고지 바가 있으면 y 1336).
- 고지 바: 노랑 바탕·잉크 글자 40~44px, y 1440에 바닥을 맞춰 처음부터 끝까지 고정. 문구는 marketer 지정 그대로(EN은 "commission" 명시).
- AI 라벨: 마지막 `seconds`초 동안 y 1098 중앙. 엔드 카드: 마지막 N초 동안 가운데 패널을 덮는 종이색 카드.

## 출력
- `short-N.mp4`(H.264 High, yuv420p, 30fps, AAC 48kHz), `short-N.srt`, `shorts.manifest.json`(구간별 단어 수·길이·오디오 출처, ffprobe 결과, 경고, 폰트·라이선스).
- 종료 코드: 0 성공 / 3 ffprobe 검증 실패 / 4 max_seconds 초과(해당 숏폼 파일 미생성).

## 규칙
- 영상은 `render/`에만 두고 커밋하지 않는다. 실존 인물·로고·패키지·스틸·캐릭터 금지, 목업은 텍스트·단색·도형만.
- 제휴 상품이 나오는 숏폼은 고지 바를 처음부터 끝까지 넣는다. API 키 값은 출력하지 않는다.
