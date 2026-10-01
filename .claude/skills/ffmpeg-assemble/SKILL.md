---
name: ffmpeg-assemble
description: KE Studio 사내 스킬. 장면 목록 JSON(장면별 낭독문·화면 텍스트·이미지/오디오 경로·길이)을 1920x1080 30fps H.264 롱폼 MP4와 .srt, 매니페스트로 조립한다. 이미지·TTS가 없으면 목업 모드(Pillow 텍스트 슬라이드 + 무음 + 자막 번인), 있으면 실제 모드(플레이트 + TTS)로 렌더한다. producer가 롱폼을 만들거나 목업 프리뷰·검수용 컨택트시트가 필요할 때 쓴다.
---

# ffmpeg-assemble (사내 작성, KE Studio)

장면 목록 JSON을 받아 롱폼 영상을 조립한다. 에피소드와 무관한 범용 도구이며 EP마다 입력 JSON만 바꾼다.
같은 폴더의 `scripts/kemedia.py`는 shorts-cut 스킬도 함께 쓰는 공용 모듈이다(폰트·레이아웃·자막·ffmpeg).

## 요구 사항
- Python 3.9+, Pillow, ffmpeg/ffprobe(PATH). 설치는 `scripts/setup.sh`만 사용한다. 없으면 스크립트가 무엇이 없는지 출력하고 멈춘다(임의 설치 금지).
- 네트워크·API 키를 쓰지 않는다. TTS·이미지 생성은 이 스킬 밖에서 하고, 결과 파일 경로만 JSON에 넣는다.
- 폰트: 지정 폰트(Anton, Pretendard, Black Han Sans, 대체 Inter)를 `fc-list`로 찾고, 없으면 설치된 대체 폰트(Liberation Sans, DejaVu Sans, WenQuanYi Zen Hei)를 쓴다. 글자마다 글리프가 없으면 다음 폰트로 넘어간다(한글 → CJK 폰트). 사용한 폰트 파일과 라이선스는 매니페스트 `fonts`에 남는다.

## 실행 (저장소 루트에서. JSON 안의 상대 경로는 현재 작업 폴더 기준)
```bash
# 1) 대본(script.<lang>.md) → 장면 JSON 초안. 화면 텍스트는 "텍스트:" 줄의 "따옴표" 문자열, 요약은 scene-prompts.md의 "요약:"
python3 .claude/skills/ffmpeg-assemble/scripts/script_to_scenes.py episodes/EPxxx/script.en.md \
  --prompts episodes/EPxxx/design/scene-prompts.md --output-video render/EPxxx/long.mp4 \
  --out episodes/EPxxx/render-input/scenes.en.json
# 2) 초안 검토: 필요하면 screen.cards / screen.bars / screen.note / screen.order 추가
# 3) 길이만 확인
python3 .claude/skills/ffmpeg-assemble/scripts/assemble.py episodes/EPxxx/render-input/scenes.en.json --dry-run
# 4) 렌더 + 검수용 컨택트시트(장면당 1프레임, 600KB 이하)
python3 .claude/skills/ffmpeg-assemble/scripts/assemble.py episodes/EPxxx/render-input/scenes.en.json \
  --mode mockup --contact-sheet episodes/EPxxx/render-preview/long-contact.png
```
옵션: `--out`, `--mode auto|mockup|real`, `--preset`(기본 medium), `--crf`(기본 20), `--keep-work`(중간 프레임 보존), `--contact-max-kb`.

## 입력 JSON
```json
{
  "output": "render/EPxxx/long.mp4",
  "size": [1920, 1080], "fps": 30, "wpm": 150, "mode": "auto",
  "burn_subtitles": "auto",
  "mockup_label": "MOCKUP — final AI plate pending",
  "music": null, "music_volume": 0.12, "loudnorm": false, "scene_pad": 0.3,
  "scenes": [
    {
      "id": "S01", "title": "Hook",
      "narration": "문단1 문장들...\n\n문단2 ...",
      "screen": {"heading": "큰 문구", "lines": ["보조 문구"], "cards": ["2001", "2019"],
                 "bars": [{"label": "Vietnam", "value": 81, "display": "81", "highlight": false}],
                 "note": "출처 표기", "order": ["heading", "lines", "cards", "bars", "note"]},
      "plate": "계획된 AI 플레이트 요약(목업에만 작게 표시)",
      "image": null, "image_vertical": null, "audio": null,
      "duration": null, "subtitles": null, "bottom_bar": null
    }
  ]
}
```
- 길이 우선순위: `duration`(초) > 오디오 길이 + `scene_pad` > 낭독 단어 수 ÷ `wpm` × 60 > 3초. 모든 경계는 프레임 단위로 맞춘다.
- 자막: `subtitles`(장면 기준 `[{"text","start","end"}]`, TTS 타임스탬프가 있을 때)가 없으면 낭독문을 문장 → 84자 이하 덩어리로 나누고 단어 수 비례로 시간을 배분한다(추정치, 매니페스트 `cue_timing`에 표시).
- `bottom_bar`: 장면 전체 구간 하단 고정 바(예: 제휴 고지). `image_vertical`은 shorts-cut이 9:16 플레이트로 쓴다.
- 화면 텍스트(숫자·대사·작품명)는 항상 오버레이로 그린다. AI 플레이트 안에 글자를 넣지 않는다(design-system §5).

## 모드
| 모드 | 화면 | 오디오 | 자막 |
|---|---|---|---|
| mockup | 단색 배경 + 장면 번호·제목, 화면 텍스트, 카드·막대 도형, 계획 플레이트 요약, 우상단 MOCKUP 표기 | 무음 AAC | 번인 + .srt |
| real | `image`를 커버 크롭, 화면 텍스트는 반투명 패널 오버레이 | 장면별 `audio`(+선택 `music` 믹스, `loudnorm` -14 LUFS) | 기본은 .srt만(업로드용 CC). `burn_subtitles: true`면 번인 |
| auto(기본) | 장면별로 있는 것은 real, 없는 것은 mockup | 있으면 TTS, 없으면 무음 | 목업 장면이 하나라도 있으면 번인 |
`--mode real`은 이미지·오디오가 하나라도 없으면 렌더하지 않고 빠진 목록을 출력한다.

## 출력
- `long.mp4`: H.264 High, yuv420p, 30fps CFR, AAC 48kHz 스테레오, `+faststart`.
- `long.srt`, `long.manifest.json`(장면 시작·끝, 자막 큐와 문단·문장 번호, 폰트·라이선스, 도구 버전, ffprobe 결과, 경고, 소요 시간). shorts-cut이 이 매니페스트를 입력으로 쓴다.
- 종료 코드: 0 성공 / 3 ffprobe 검증 실패(해상도·fps·코덱·길이) / 그 외 오류는 메시지와 함께 중단.

## 규칙 (CLAUDE.md·design-system 요약)
- 영상·오디오는 `render/`에만 두고 커밋하지 않는다. 저장소에는 render-log.md와 작은 프리뷰 PNG만.
- 실존 인물, 브랜드 로고, 패키지, 영화·드라마 스틸, 상표 이미지를 넣지 않는다. 목업은 텍스트·단색·도형만 쓴다.
- 음악·보이스·이미지는 상용 라이선스 소스만 쓰고, 출처·모델·날짜·시드를 렌더 로그에 적는다.
- API 키 값은 출력·기록하지 않는다(키 이름만 docs/ENV.md).
