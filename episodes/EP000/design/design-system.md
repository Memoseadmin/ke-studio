DUMMY
직원: designer
사용 스킬: youtube-thumbnail
호출 방식: Skill 도구 실패 — `<tool_use_error>Unknown skill: youtube-thumbnail</tool_use_error>` → .claude/skills/social-media-skills-youtube-thumbnail/SKILL.md 읽고 수동 적용 (레퍼런스 사진·brand-kit 없음 → 얼굴 없는 오브젝트 중심 구도로 대체)

# Korea Explained — Design System (1 page, dummy)

## Color tokens
| Token | Hex | Use |
|---|---|---|
| --ke-primary | #C8102E | 브랜드 레드 (고추·단청) |
| --ke-accent | #FFD23F | 고대비 액센트 (양은냄비 옐로) |
| --ke-ink | #111111 | 텍스트·외곽선 |
| --ke-paper | #F7F3EA | 밝은 배경 (한지 톤) |
| --ke-night | #1B1F2A | 어두운 배경 |
규칙: 한 썸네일에 primary + accent 2색 지배.

## Fonts
- EN 헤드라인: Anton (Google Fonts), 대문자
- KR 헤드라인: Black Han Sans (Google Fonts)
- 본문/자막: Pretendard / Inter

## Thumbnail layout (1280x720)
- 단일 초점 오브젝트가 프레임 30–50%, 오른쪽 2/3.
- 텍스트 ≤4단어, 왼쪽 1/3, 6px ink 외곽선, 360px 폭에서도 판독 가능.
- 하단 우측 100x40px는 YouTube 타임스탬프 영역 → 비움.
- 대비: 텍스트/배경 명도 대비 4.5:1 이상.

## Prohibitions
- 실존 인물 얼굴, 브랜드 로고·패키지 상표, 저작권 캐릭터, 드라마 스틸컷 복제
- 과장 반응 얼굴·빨간 화살표 남발 등 낚시 연출, 건강/효능 암시 문구
