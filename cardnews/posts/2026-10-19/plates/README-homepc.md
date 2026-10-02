# 집 PC(ComfyUI) 작업 순서 — 세트 11 4판 플레이트

1. `git fetch origin cardnews/c1-1-design && git checkout cardnews/c1-1-design && git pull --rebase origin cardnews/c1-1-design`
2. `cardnews/posts/2026-10-19/plates/PROMPTS-v4.md`(v4.1, 한지 콜라주 꼬리)를 연다. 모델 1순위 Z-Image-Turbo(Apache-2.0), 안 되면 SDXL base 1.0. LoRA 금지.
3. 프롬프트 10개 × 시드 4개(표 그대로) = 40장 생성. 프롬프트 = 장별 문장 + 스타일 꼬리, 네거티브 = §0 문자열.
4. 저장: `plates/v4/P{장}{a|b}-s{시드}.png` (예 `P02a-s1019020.png`). 크기는 생성 크기 그대로(축소·크롭은 클라우드가 한다).
5. 검수: 글자 닮은 획·사람·손·로고·호랑이·까치가 보이거나, 플랫 클립아트처럼 보이거나, 주제 사물이 화면을 채우면 그 파일은 지우고 `rejected`에 사유 기록.
6. `plates/GEN-v4.json` 작성: model, checkpoint 파일명·SHA256 앞 12자, license, comfyui 버전, 프롬프트 id별 {prompt, negative, size, steps, cfg, sampler, seeds[], picked, rejected[]}, created_at, operator "대표 PC".
7. `git add cardnews/posts/2026-10-19/plates/v4 cardnews/posts/2026-10-19/plates/GEN-v4.json && git commit -m "cardnews set 11 v4: AI plates (ComfyUI)"`
8. `git push -u origin cardnews/c1-1-design` (실패 시 2·4·8·16초 재시도) → "완료: 커밋 SHA, 생성 N장·채택 M장, 모델명" 한 줄 보고.
