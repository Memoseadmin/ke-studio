# Instagram 연결 점검 (읽기 전용)

확인 시각: 2026-10-02 01:45 UTC

## 1. 연결 테스트
| 항목 | 결과 |
|---|---|
| `IG_ACCESS_TOKEN` | UNSET |
| `IG_USER_ID` | UNSET |
| `IMAGE_HOST_BASE_URL` | UNSET |
| `GITHUB_TOKEN` | SET |

둘 중 하나라도 UNSET이므로 Graph API 호출(a~d)은 **건너뜀**. 이름·핸들·팔로워·권한 표·만료 추정 모두 미확인.
- 권한 확인 대상: `instagram_content_publish`, `instagram_basic`, `pages_show_list`, `pages_read_engagement` — 미확인
- 만료 추정: 토큰 없음 → 발급일 확인 필요(장기 토큰이면 발급일+60일)
- 오류 전문: 없음(호출하지 않음)

대표 몫: 클라우드 환경 설정에 위 세 변수 입력 후 이 점검을 재실행.

## 2. dry-run (cardnews/c1-1의 posts/2026-10-09, 읽기 전용 가져옴, 게시 호출 없음)
```
[DRY-RUN] cardnews/posts/2026-10-09  cards=7
게이트:
  FAIL  approved 라벨  (--pr 없음)
  FAIL  목업 아님  (RENDER.json 없음(모드 확인 불가))
  PASS  AI 표시 문구  (마지막 비해시태그 줄(해시태그가 맨 끝): 이미지·초안은 AI로 생성, 사실 확인은 사람이 했습니다)
  PASS  해시태그 ≤5  (hashtags=5)
요청 목록(토큰 제외):
  POST https://graph.facebook.com/v21.0/{IG_USER_ID}/media
    {"image_url": "<IMAGE_HOST_BASE_URL>/card-01.png", "is_carousel_item": "true"}
  POST https://graph.facebook.com/v21.0/{IG_USER_ID}/media
    {"image_url": "<IMAGE_HOST_BASE_URL>/card-02.png", "is_carousel_item": "true"}
  POST https://graph.facebook.com/v21.0/{IG_USER_ID}/media
    {"image_url": "<IMAGE_HOST_BASE_URL>/card-03.png", "is_carousel_item": "true"}
  POST https://graph.facebook.com/v21.0/{IG_USER_ID}/media
    {"image_url": "<IMAGE_HOST_BASE_URL>/card-04.png", "is_carousel_item": "true"}
  POST https://graph.facebook.com/v21.0/{IG_USER_ID}/media
    {"image_url": "<IMAGE_HOST_BASE_URL>/card-05.png", "is_carousel_item": "true"}
  POST https://graph.facebook.com/v21.0/{IG_USER_ID}/media
    {"image_url": "<IMAGE_HOST_BASE_URL>/card-06.png", "is_carousel_item": "true"}
  POST https://graph.facebook.com/v21.0/{IG_USER_ID}/media
    {"image_url": "<IMAGE_HOST_BASE_URL>/card-07.png", "is_carousel_item": "true"}
  POST https://graph.facebook.com/v21.0/{IG_USER_ID}/media
    {"media_type": "CAROUSEL", "children": "<child ids>", "caption": "오늘 한글날, 왜 100번째일까요\n\n훈민정음 반포는 1446년, 올해로 580돌입니다.\n그런데 한글날 자체는 1926년 '가갸�
  POST https://graph.facebook.com/v21.0/{IG_USER_ID}/media_publish
    {"creation_id": "<carousel id>"}
  (schedule) cardnews/queue.json 에 기록될 항목: 2026-10-09T09:00+09:00 — dry-run이라 기록 안 함
전체 게이트: FAIL
```
해석:
- 요청 순서: 자식 7개 → 캐러셀(caption) → media_publish. 토큰은 출력되지 않음.
- approved 라벨: 이 dry-run은 `--pr` 없이 실행해 FAIL(PR 지정 필요).
- 목업 게이트 FAIL: 해당 게시물에 `RENDER.json`이 없음. 렌더 단계에서 `{"mode": "real|mockup"}` 파일을 만들어야 `--execute` 가능(없으면 안전하게 중단).
- AI 문구 게이트: 실제 캡션은 해시태그가 맨 끝 줄이라, 해시태그 줄을 제외한 마지막 줄에서 확인(PASS). 지시문의 "마지막 줄"과 다르니 캡션 규격 확정 필요.
