# C1-1 수동 게시 패키지 (10/9~10/22, 캐러셀 14개)

갱신 2026-10-02 · COO. **자동 게시(R2 + Graph API)가 막혀 있는 동안 쓰는 대표용 안내.** 키가 고쳐지면 COO가 `ig_publish.py --schedule` 큐 + 매일 KST 루틴으로 바꾸고, 이 문서는 기록으로 남긴다.

- 승인: PR #4 approved → final 렌더(MOCKUP 없음, `RENDER.json` mode=final) → legal v3 → `cardnews/main` 머지.
- 파일: 날짜 폴더마다 `card-01.png`~`card-NN.png`(1080x1350, 4:5) + `caption.txt`(전문 그대로 붙여넣기). `contact.png`·`cards.json`·`RENDER.json`은 올리지 않는다.
- 릴스(하루 1개, 캐러셀 6시간 뒤. 단 캐러셀 19:00인 10/13·10/15·10/20·10/22는 같은 날 21:00, 대표 결정 2026-10-02)는 **C1-1b PR 승인 후** 같은 폴더에 추가된다. 승인 전에는 캐러셀만 올린다.

## 게시 일정 (KST)
| 날짜 | 시각 | 장 | 첫 줄(훅) | 폴더 |
|---|---|---|---|---|
| 10/09 금 | 11:00 | 7 | 오늘 한글날, 왜 100돌일까요 | [2026-10-09](https://github.com/Memoseadmin/ke-studio/tree/cardnews/main/cardnews/posts/2026-10-09) |
| 10/10 토 | 10:00 | 9 | 궁궐 5곳 축제, 이틀 남았습니다 | [2026-10-10](https://github.com/Memoseadmin/ke-studio/tree/cardnews/main/cardnews/posts/2026-10-10) |
| 10/11 일 | 11:00 | 7 | 호랑이 옆에 까치가 있는 이유 | [2026-10-11](https://github.com/Memoseadmin/ke-studio/tree/cardnews/main/cardnews/posts/2026-10-11) |
| 10/12 월 | 12:00 | 8 | 산별 단풍 절정, 날짜만 모았습니다 | [2026-10-12](https://github.com/Memoseadmin/ke-studio/tree/cardnews/main/cardnews/posts/2026-10-12) |
| 10/13 화 | 19:00 | 7 | 빵을 샀는데 주인공은 책갈피 | [2026-10-13](https://github.com/Memoseadmin/ke-studio/tree/cardnews/main/cardnews/posts/2026-10-13) |
| 10/14 수 | 12:00 | 8 | 10월 남은 주말 3번, 날짜별 정리 | [2026-10-14](https://github.com/Memoseadmin/ke-studio/tree/cardnews/main/cardnews/posts/2026-10-14) |
| 10/15 목 | 19:00 | 7 | 라면 수출, 반년에 9억 4천만 달러 | [2026-10-15](https://github.com/Memoseadmin/ke-studio/tree/cardnews/main/cardnews/posts/2026-10-15) |
| 10/16 금 | 12:00 | 7 | 한글은 원래 28자였습니다 | [2026-10-16](https://github.com/Memoseadmin/ke-studio/tree/cardnews/main/cardnews/posts/2026-10-16) |
| 10/17 토 | 10:00 | 7 | 편의점 협업 상품, 사기 전 체크 5 | [2026-10-17](https://github.com/Memoseadmin/ke-studio/tree/cardnews/main/cardnews/posts/2026-10-17) |
| 10/18 일 | 11:00 | 7 | 품절된 키링, 원래는 나라의 도장 | [2026-10-18](https://github.com/Memoseadmin/ke-studio/tree/cardnews/main/cardnews/posts/2026-10-18) |
| 10/19 월 | 12:00 | 8 | 요즘 손으로 책을 베끼는 사람이 늘었습니다 | [2026-10-19](https://github.com/Memoseadmin/ke-studio/tree/cardnews/main/cardnews/posts/2026-10-19) |
| 10/20 화 | 19:00 | 7 | 라면 먹을래요, 25년째 남은 한마디 | [2026-10-20](https://github.com/Memoseadmin/ke-studio/tree/cardnews/main/cardnews/posts/2026-10-20) |
| 10/21 수 | 12:00 | 8 | 닫는 전시 3, 앞으로 볼 전시 2 | [2026-10-21](https://github.com/Memoseadmin/ke-studio/tree/cardnews/main/cardnews/posts/2026-10-21) |
| 10/22 목 | 19:00 | 7 | 해외에서 23만 명이 배우는 한국어 | [2026-10-22](https://github.com/Memoseadmin/ke-studio/tree/cardnews/main/cardnews/posts/2026-10-22) |

## 폰에서 게시하는 순서 (1개당 약 3분)
1. 위 표의 폴더를 연다 → `card-01.png`부터 차례로 열어 길게 눌러 사진 앱에 저장(번호 순서 유지).
2. `caption.txt`를 열어 전문 복사(해시태그 5개와 마지막 AI 표시 줄 포함, 고치지 않는다).
3. 인스타 **+ → 게시물** → 사진을 card-01부터 순서대로 선택 → 비율 4:5 그대로(잘림 없음) → 필터 없음.
4. 문구에 붙여넣기. **유료 파트너십 라벨은 끈다**(C1-1은 협찬 0건). 위치·사람 태그 없음.
5. 공유. 10/9 게시 전 **프로필 링크**가 설정돼 있어야 08·12 캡션의 "프로필 링크에 모아 둡니다"가 참이 된다(legal 권고 12).

## 대표가 미리 할 일 (자동 게시로 바꾸려면)
- R2: Cloudflare → R2 → API 토큰 관리 → 새 토큰(객체 읽기·쓰기, chaekgado-cards) → 한 번만 보이는 **Access Key ID(32자)·Secret Access Key(64자)** 전체를 환경 설정에 다시 입력.
- IG: 앱 대시보드 → Instagram 제품 → "Instagram 로그인으로 API 설정" → @chaekgado.note 추가 → 토큰 생성(**IGAA…**) → `IG_ACCESS_TOKEN` 교체. 같은 화면에서 계정 옆에 표시되는 숫자 ID를 `IG_USER_ID`에 넣는다(페이스북 페이지 ID 아님). 맞는지는 COO가 `ig_publish.py --check`로 확인한다(값은 출력하지 않음).
- 위 두 개가 되면 COO가 `r2_upload.py --execute` → `ig_publish.py --pr 4 --schedule` 큐 → 매일 KST 게시 루틴으로 전환한다.
