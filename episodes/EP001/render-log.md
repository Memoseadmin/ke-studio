# EP001 렌더 로그 (목업)

직원: producer / 기준일: 2026-10-01 / 브랜치: ep/EP001 / 판: **EN만**(KR 보류, 대표 기본값) / 제목: Why Ramyeon Keeps Showing Up on Korean Screens
상태: **목업 렌더 완료, 업로드용 아님.** 영상·오디오·자막·매니페스트는 `render/EP001/`(gitignore 대상)에만 있다. **영상·오디오 파일은 저장소에 커밋하지 않는다.** 저장소에 들어갈 수 있는 것은 이 로그, `render-preview/` PNG 2장, `render-input/` JSON 2개(재현용 텍스트, 커밋 여부는 COO 결정)뿐이다.
제휴 상품: 가안 A 라면 멀티팩, B 양은냄비. 링크는 자리표시자다(영상 안에는 링크 없음, 고지 문구만).

## 1. 렌더 모드: 목업
- 이유: `TTS_API_KEY`, `IMAGE_API_KEY`, `OPENAI_API_KEY`, `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`이 UNSET이다. SET은 `GITHUB_TOKEN` 하나다. 변수 이름만 확인했고 값은 읽지도 출력하지도 않았다. 그래서 AI 플레이트와 TTS 없이 렌더했다.
- 화면: Pillow 텍스트 슬라이드. 장면 번호·제목, 대본 "텍스트:" 문구, 카드·막대 도형, 계획 플레이트 요약(scene-prompts.md "요약:"), 우상단 "MOCKUP — final AI plate pending"을 넣었다. 오디오는 무음이다. 자막은 번인하고 .srt로도 냈다.

## 2. 도구·버전·소요 시간
| 항목 | 값 |
|---|---|
| 스킬 | ffmpeg-assemble 1.0.0, shorts-cut 1.0.0(사내 작성, 공용 모듈 kemedia 1.0.0) |
| ffmpeg / ffprobe | 6.1.1-3ubuntu5 (libx264 core 164 r3108 31e19f9, ffmpeg 내장 AAC) |
| Python / Pillow | 3.11.15 / 12.3.0 |
| 인코딩 설정 | H.264 High, yuv420p, CRF 20, preset medium, tune stillimage, 30fps CFR, AAC 192k 48kHz 2ch, +faststart |
| 롱폼 소요 | 139.2초(프레임 생성 9.3초 + 인코딩 126.6초), 07:25:06~07:27:25 UTC |
| 숏폼 5개 소요 | 76.2초(편당 프레임 1.1~1.7초 + 인코딩 9.4~14.7초), 07:27:31~07:28:47 UTC |

## 3. 결과 파일 (ffprobe 실측, `render/EP001/`)
| 파일 | 길이(초) | 해상도 | fps | 코덱(영상/음성) | 크기(bytes) | 자막 큐 |
|---|---|---|---|---|---|---|
| long.mp4 | 591.200 (9:51.2) | 1920x1080 | 30 | h264 High / aac 2ch | 9,624,484 (9.18 MiB) | long.srt 153 |
| short-1.mp4 | 57.600 | 1080x1920 | 30 | h264 High / aac 2ch | 1,064,686 | 22 |
| short-2.mp4 | 58.400 | 1080x1920 | 30 | h264 High / aac 2ch | 1,075,141 | 24 |
| short-3.mp4 | 56.000 | 1080x1920 | 30 | h264 High / aac 2ch | 1,024,838 | 24 |
| short-4.mp4 | 59.200 | 1080x1920 | 30 | h264 High / aac 2ch | 1,132,432 | 22 |
| short-5.mp4 | 32.400 | 1080x1920 | 30 | h264 High / aac 2ch | 570,444 | 14 |
- 오디오는 6개 모두 max_volume -91.0 dB로 디지털 무음이다. 60초를 넘는 숏폼은 없다(가장 긴 것이 short-4의 59.2초). shorts-cut은 `max_seconds`를 넘으면 파일을 만들지 않는다(종료 코드 4, 시험으로 확인).
- 프리뷰(커밋 대상): `render-preview/long-contact.png`(1894x990, 464,794 B, 장면별 중간 프레임 12개), `render-preview/shorts-contact.png`(1704x698, 299,864 B, 숏폼별 40% 지점 1프레임). 둘 다 600KB 이하다.

## 4. 사용 소재와 라이선스
| 소재 | 출처 | 라이선스 |
|---|---|---|
| 슬라이드·카드·막대·바 | Pillow 자체 생성(kemedia.py). 외부 이미지·아이콘·사진 **0개** | 자체 제작 |
| 영문 글꼴 | LiberationSans-Bold.ttf, LiberationSans-Regular.ttf(fonts-liberation 2.1.5, VM 기본 설치) | SIL OFL 1.1 |
| 한글 글꼴 | wqy-zenhei.ttc(fonts-wqy-zenhei 0.9.45, VM 기본 설치). "라면 먹을래요?"와 한글 플레이트 요약에만 쓰임 | GPL-2 + font embedding exception |
| 오디오 | ffmpeg anullsrc 무음. **보이스·음악 없음** | 해당 없음 |
| 생성 모델 | **없음.** AI 이미지·TTS 미사용 | 해당 없음 |
- 지정 폰트(Anton·Black Han Sans·Pretendard, 모두 OFL)는 설치돼 있지 않아 위 대체 글꼴을 썼고, 따로 설치하지 않았다. 글꼴은 프레임 픽셀로만 들어가고 글꼴 파일은 배포하지 않는다. DejaVu는 대체 순서에 있지만 이번에는 쓰이지 않았다.
- 실존 인물, 로고, 패키지, 영화·애니 스틸, 캐릭터, 상표 이미지는 없다. 브랜드·작품명(GS25, CU, Nongshim, Netflix 등)은 대본 지시대로 글자로만 표기했다.

## 5. 길이 추정 근거 (낭독 단어 수 ÷ 150wpm, 추정치이며 TTS 실측으로 교체)
| S01 | S02 | S03 | S04 | S05 | S06 | S07 | S08 | S09 | S10 | S11 | S12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 39w 15.6s | 73w 29.2s | 160w 64.0s | 149w 59.6s | 161w 64.4s | 170w 68.0s | 87w 34.8s | 81w 32.4s | 100w 40.0s | 163w 65.2s | 186w 74.4s | 109w 43.6s |
- 합계 1,478단어 = 591.2초로 대본 메타의 9.85분과 같다. [F#] 태그와 화면 메모는 뺐다. 파서가 센 단어 수는 12개 장면 헤더와 모두 일치한다. 장면 경계는 대본 타임코드(0:16, 0:45 … 9:51)와 같다.
- 자막 큐는 문장을 롱폼 84자, 숏폼 46자 이하로 나누고 장면 안에서 단어 수에 비례해 시간을 나눴다. 그래서 실제 낭독과는 싱크가 맞지 않는다.

| 숏폼(marketing.md §5) | 구성 | 단어 | 길이 |
|---|---|---|---|
| 1 `ONE LINE, TWO MEANINGS` | S01 1문장 + S03 1~3문단(훅 내레이션·CTA 낭독 없음, 6절 1번) | 144 | 57.6s |
| 2 `JJAPAGURI → RAM-DON` | 훅 13 + S05 1·3·4·5문단 120 + CTA 13 | 146 | 58.4s |
| 3 `DEMON HUNTERS, CUP RAMYEON` | 훅 10 + S06 1·3·4문단 122 + CTA 8 | 140 | 56.0s |
| 4 `RAMYEON YOU CAN VISIT` | 훅 13 + S07 1문단 61 + S08 마지막 문장 제외 63 + CTA 11 | 148 | 59.2s |
| 5 `THE YELLOW RAMYEON POT` | 훅 11 + S11 3문단(냄비) 46 + CTA 24. 하단 바 "Affiliate link · I may earn a commission"을 처음부터 끝까지 표시 | 81 | 32.4s |
- 공통: 상단 훅 문구, 자막 번인, 마지막 1초에 "AI voice & images" 라벨. 이 라벨은 최종 레이아웃 자리표시다. 이 목업 자체에는 AI 생성물이 없다. 롱폼 S11에는 "Affiliate links · I may earn a commission" 하단 바를 장면 내내 넣었다.

## 6. 오류와 경고
1. **숏폼 1이 컷 플랜 그대로면 60초를 넘는다.** 훅 내레이션 12 + 원본 144 + CTA 13 = 169단어 = 67.6초다. 원본 구간(S01+S03)은 그대로 두고, 훅 내레이션과 CTA 낭독을 빼서 57.6초로 맞췄다. CTA 문구는 마지막 4초에 화면 카드(무음)로 보여 준다. **marketer 확인 필요.** 다른 안(S01 문장을 빼고 훅 내레이션을 살리는 안)은 60.4초라 역시 넘는다.
2. 여유가 짧다. short-4는 0.8초, short-2는 1.6초 남는다. TTS 실측이 150wpm보다 느리면 60초를 넘을 수 있다. 그 경우 shorts-cut이 렌더를 거부하므로 구간을 줄여야 한다(marketer·writer).
3. S06 자막에 그룹명 "Huntrix"가 들어 있다(long.srt, short-3.srt). 대본 S06 메모는 "공식 표기 확인 후 사용"이다. 최종 렌더 전에 writer 확인이 필요하다. 낭독문은 바꾸지 않았다.
4. 지정 폰트 미설치 경고가 4개 역할 모두에서 났다. Liberation은 Anton보다 폭이 넓어서 훅이 2줄로 줄바꿈된다.
5. 개발 중에 난 오류는 최종 렌더 전에 고쳤다. 자막 분할 함수가 짧은 단어와 긴 단어 조합에서 무한 재귀에 빠졌다. 알고리즘을 바꾼 뒤 무작위 입력 2만 건으로 시험해 통과했다. `/usr/bin/time`이 없어서 셸 시간으로 쟀다(설치는 시도하지 않음).
6. "MOCKUP — final AI plate pending"에는 em dash가 들어 있다. 화면 문구에 em dash를 쓰지 않는다는 디자인 규칙과 어긋나지만, COO가 지정한 목업 표기라 그대로 두었다. 최종 영상에는 나오지 않는다.
- 최종 렌더 오류는 없다. 6개 파일 모두 해상도·fps·코덱·길이 자동 검증을 통과했다.

## 7. 실제 렌더에 필요한 것
- 환경변수(이름만): `TTS_API_KEY`, `IMAGE_API_KEY`. 공급자를 정한 뒤 docs/ENV.md에서 이름을 확정한다. 업로드에는 `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`이 필요하다(publisher).
- 지정 폰트 3종(Anton, Black Han Sans, Pretendard, 모두 OFL)을 `scripts/setup.sh`에 넣을지 COO가 정한다. 설치되면 스킬이 `fc-list`로 찾아 자동으로 쓴다.
- TTS·음악 공급자 결정(상용 라이선스, 플랜명과 약관 사본 기록). TTS는 문장·단어 타임스탬프를 주는 곳을 권장한다. 그래야 자막 싱크와 숏폼 오디오 컷이 정확해진다.
- 플레이트: scene-prompts.md S01~S12의 16:9 이미지와, 숏폼용 9:16 네이티브(S03·S05·S06·S07·S08·S11)가 필요하다. 16:9를 9:16으로 자르면 1.78배 확대 경고가 난다.
- 그다음 `render-input/*.json`의 `image`·`image_vertical`·`audio`만 채우고 아래 명령을 `--mode real`로 다시 실행한다.

## 8. risk.md FIX 5(이미지·음악·보이스 저작권): 미해결
- 최종 AI 플레이트를 아직 만들지 않았고, scene-prompts.md 생성 기록 표(모델·날짜·시드·검수자)도 비어 있다. 담당: designer·producer.
- TTS·음악 공급자와 라이선스 출처가 정해지지 않았다. 이번 렌더는 보이스·음악이 0이라 4절에 적을 출처가 아직 없다.
- legal-reviewer의 최종 이미지 재점검은 실제 렌더 후, 업로드 전에 한다. **상태: 미해결 유지.** 이번 작업은 렌더 파이프라인과 로그 양식만 준비했다.

## 9. 재현 (저장소 루트)
`python3 .claude/skills/ffmpeg-assemble/scripts/assemble.py episodes/EP001/render-input/scenes.en.json --mode mockup --contact-sheet episodes/EP001/render-preview/long-contact.png`
`python3 .claude/skills/shorts-cut/scripts/shorts_cut.py episodes/EP001/render-input/shorts.en.json --mode mockup --contact-sheet episodes/EP001/render-preview/shorts-contact.png`

## 10. 자가 검증
| 성공 기준 | 결과 |
|---|---|
| 스킬 2개(SKILL.md frontmatter + Python, 목업·실제 모드) | 통과. 실제 모드는 임시 폴더의 합성 플레이트·사인파 오디오로 시험했다 |
| long.mp4 1920x1080 30fps H.264 + .srt, S01~S12 | 통과(591.2초, 153큐) |
| short-1~5 1080x1920, 60초 이하, 각 .srt | 통과(최대 59.2초) |
| 컨택트시트 2장 600KB 이하 | 통과(465KB / 300KB) |
| 영상·오디오 미커밋 | 통과(`git check-ignore`로 render/ 무시 확인) |
