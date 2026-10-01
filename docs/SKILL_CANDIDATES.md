# 추가 스킬 후보표 (대표 OK 전 — 아직 복사하지 않음)

조사일 2026-10-01. 각 저장소를 clone해 LICENSE와 SKILL.md를 직접 확인했다. "라이선스 없음"은 복사할 수 없다(저작권 기본 보호).

| 기능 | 후보 (저장소 @SHA) | 라이선스 | 필요한 키 | 선택 이유 / 주의 | 추천 |
|---|---|---|---|---|---|
| YouTube 업로드 | aviz85/claude-skills-library `youtube-uploader` @90bbc16 | **없음** | YouTube OAuth | 기능은 맞지만 라이선스가 없어 복사 불가 | ❌ |
| YouTube 업로드 | **직접 작성** `youtube-upload` | 자체 | `YOUTUBE_*` (ENV.md) | google-api-python-client로 private/예약 업로드 + approved 라벨 확인을 스킬에 내장 | ✅ |
| FFmpeg 조립 | affaan-m/everything-claude-code `video-editing` @c70874f | MIT | ElevenLabs·fal(선택) | 컷 편집→Remotion→보이스까지 넓은 가이드. 우리 파이프라인엔 과함 | △ 참고만 |
| FFmpeg 조립 | **직접 작성** `ffmpeg-assemble` | 자체 | 없음 | 장면 이미지+TTS+자막 → long.mp4. 필요한 것만 | ✅ |
| 숏폼 자동 컷 | **직접 작성** `shorts-cut` | 자체 | 없음 | marketing.md 컷 플랜(S번호 구간) → 9:16 60초 5개. 쓸 만한 MIT 기성품 못 찾음 | ✅ |
| 썸네일·이미지 | anthropics/skills `canvas-design` @8a1541c | Apache-2.0 | 없음 | 글자 중심 썸네일·카드뉴스를 PNG로. 키 불필요 | ✅ 설치됨(2026-10-01) |
| 썸네일·이미지 | glebis/claude-skills `nano-banana` @7524dff | MIT | `GEMINI_API_KEY` | 사진풍 이미지 생성. **원작자의 암호화된 `secrets.enc.yaml`이 들어 있어 그 파일은 복사 제외 필요**(원본 그대로 원칙과 충돌 → 대표 판단) | △ |
| 썸네일·이미지 | kkoppenhaver/cc-nano-banana @3b13699 | MIT | Gemini CLI 확장 | Gemini CLI 설치 필요. 클라우드 세션엔 번거로움 | ❌ |
| TTS | glebis/claude-skills `elevenlabs-tts` @7524dff | MIT | `ELEVENLABS_API_KEY` | 대본→음성 파일. 스크립트·requirements 포함 | ✅ (키 발급 후) |
| 디자인 | anthropics/knowledge-work-plugins `design` 팩(7) @da38ec1 | Apache-2.0 | 없음 | design-system, design-critique, ux-copy | ✅ 설치됨(2026-10-01) |
| 디자인 | anthropics/skills `theme-factory` | Apache-2.0 | 없음 | 색·폰트 테마 프리셋 10종 | ✅ 설치됨(2026-10-01) |
| 트렌드 | mvanhorn/last30days-skill @5103ba4 | MIT | Reddit·HN 무료, YouTube·X·TikTok 유료 키 | 지난 30일 여론 수집. 첫 실행 setup 마법사는 금지 → scripts/setup.sh로 대체 | ✅ |
| 트렌드 | ScrapeCreators/social-media-research-skills(13) @64ba7b4 | MIT | `SCRAPECREATORS_API_KEY`(유료) | trend-discovery, outlier-post-finder, comment-mining | △ 키 발급 후 |
| 트렌드 | terryds/google-trends-skill @e578606 | **없음** | 없음 | 복사 불가 | ❌ |
| 트렌드 | **직접 작성** `kr-trend-radar` | 자체 | 없음(목표) | Netflix Top10 공개 데이터 + Google Trends + 뉴스 랭킹 → K-드라마 속 음식·장소·제품 | ✅ |
| 기존 보유 | social-media-skills-niche-research | MIT | 없음 | 웹검색으로 지난 7일 이야기 20개. 이미 설치됨 | ✅ 사용 중 |

## OK 시 순서
1. 복사 설치(같은 절차·diff 검증): design 팩, canvas-design, theme-factory, last30days, elevenlabs-tts
2. 직접 작성: youtube-upload, ffmpeg-assemble, shorts-cut, kr-trend-radar (Phase 1~2에서 필요해질 때)
3. 보류: nano-banana(시크릿 파일 문제 결정 필요), ScrapeCreators(유료 키)
