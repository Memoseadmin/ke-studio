# 집 PC(GPU) 세션 첫 지시문 — 2026-10-02 COO 작성

대표 PC(NVIDIA GPU, ComfyUI)에서 Claude Desktop 또는 터미널 `claude remote-control`로 저장소 폴더를 열고, 아래 블록을 첫 메시지로 붙여 넣는다. 클라우드 COO 세션은 GPU에 손을 못 대므로 **생성만 집에서**, 결과는 저장소로.

```
docs/HANDOFF.md와 CLAUDE.md를 읽어라. 너는 KE Studio의 집 PC GPU 작업자다(COO는 클라우드 세션). 규칙: 비밀값·.env 출력 금지, 저장소 settings·.mcp.json 변경 금지, 영상·원본 대용량은 커밋 금지(PNG 결과·프롬프트·시드 JSON만), 실존 인물·브랜드 로고·호랑이·까치 AI 생성 금지(디자인 시스템 §6·§10).

작업 1 — 프로필 사진 v4 AI 생성:
  git fetch origin cardnews/c1-1b && git checkout cardnews/c1-1b
  cardnews/profile/AVATAR-v4-PROMPTS.md의 ①②③ 프롬프트로 ComfyUI에서 각 2장(1024x1024) 생성.
  ②는 "AI 바탕만 + 글자는 코드"이므로 바탕만 생성하고 cardnews/design/render_avatar_v4.py로 글자 합성.
  결과 cardnews/profile/avatar-v4-ai-{1,2,3}-{a,b}.png + avatar-v4-GEN.json(모델·체크포인트·프롬프트·네거티브·시드·스텝·CFG) 
  + contact-profile-v4-ai.png(코드 렌더 A와 나란히 비교 시트, 라벨 "AI 생성(모델명)").
  커밋 메시지 "cardnews C1-1b: 프로필 사진 v4 AI 생성 6장(ComfyUI)" → git push -u origin cardnews/c1-1b.

작업 2 — (COO가 세트 11 3판 승인 후 프롬프트 팩을 주면) 세트 02~14 AI 배경:
  브랜치 cardnews/v3-sets-A~E 중 지정된 것 체크아웃 → posts/<날짜>/plates/PROMPTS.md대로 생성 → plates/*.png + GEN.json 커밋·푸시.
  실사 원본 그대로 금지, 배경 플레이트만. 편집·콜라주는 클라우드 세션이 한다.

끝나면 "완료: 브랜치, 커밋 SHA, 생성 N장, 모델명" 한 줄로 보고.
```

- 체크포인트·LoRA는 상업 사용 허용 라이선스만(docs/TOOLING_OPENSOURCE.md의 제외 목록 참고). 쓴 모델명은 GEN.json에 반드시 기록.
- 집 PC 세션이 푸시하면 클라우드 COO가 다음 체크인에서 회수한다.
