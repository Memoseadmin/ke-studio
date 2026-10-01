# EP000 render-log — DUMMY 스모크 테스트

> **DUMMY** — 실제 에피소드 아님. FFmpeg 렌더 파이프라인 동작 확인용. 업로드 없음.

- 실행 시각: 2026-10-01 (UTC)
- 담당: producer

## 도구
| 도구 | 경로 | 버전 |
|---|---|---|
| ffmpeg | /usr/bin/ffmpeg | 6.1.1-3ubuntu5 |
| ffprobe | /usr/bin/ffprobe | 6.1.1-3ubuntu5 |

설치 시도 없음(이미 존재). 미존재 시 `scripts/setup.sh`가 설치 담당.

## 출력 (render/EP000/, 커밋 제외)
`git check-ignore -v` → `.gitignore:11:render/` 규칙으로 두 파일 모두 무시됨 확인.

| 파일 | 소스 | 코덱 | 해상도 | fps | 길이(s) | 크기(bytes) | 소요(s) |
|---|---|---|---|---|---|---|---|
| test-long-1280x720.mp4 | lavfi testsrc2 + sine 440Hz | h264/aac | 1280x720 (16:9) | 30 | 3.000 | 1,170,122 | ~1.7 |
| test-short-1080x1920.mp4 | lavfi testsrc2 + sine 660Hz | h264/aac | 1080x1920 (9:16) | 30 | 3.000 | 2,554,534 | ~2.1 |

명령(요지): `ffmpeg -f lavfi -i testsrc2=size=WxH:rate=30:duration=3 -f lavfi -i sine=...:duration=3 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest out.mp4`

## 라이선스
FFmpeg 내장 합성 소스(testsrc2/sine)만 사용 — 외부 음악·보이스·이미지 없음.

## 오류
없음.
