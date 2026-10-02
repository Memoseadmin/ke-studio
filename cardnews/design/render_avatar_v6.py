#!/usr/bin/env python3
"""책가도 노트 프로필 사진 v6: 대표 피드백(2026-10-02, v5 본 뒤 "다시 수정") 반영 6안. 코드 렌더만(AI 생성 0).

피드백: ① 붓글씨 서체 변경(Nanum Brush Script 말고) ② 바탕 책가도 크롭 부위 변경.
  유지: 낙관 없음(v5-A 기준), 바탕 가시성 75%, 세로 "책가도" 3자.
  서체 3안(OFL 1.1, 구글 폰트, 파일 커밋 안 함):
    a 명조   Nanum Myeongjo ExtraBold (실제 굵기 파일, 가짜 볼드 아님)
    b 붓 명조 Song Myung (붓 획 명조, 궁체 느낌)
    c 굵은 고딕 Black Han Sans
  크롭 2안(같은 원화 클리블랜드미술관 〈책가도〉 2011.37 CC0):
    x 9~10폭 가운데 칸: 필통(붓 꽂힌)·붉은 합·청화 화병·붉은 잔 — 책갑 아님
    y 5~8폭 전경: 4폭 × 3단, 칸 여러 개가 보이는 넓은 크롭
  서체 변형 금지: v4/v5의 마스크 팽창(weight 9 = 가짜 볼드)을 쓰지 않는다(weight 1). 먹 번짐·그레인은 바깥 테·질감만.
  판독: 110px 대비비 4.5:1 이상. 미달이면 글자 뒤 한지색 여백(halo) 불투명도만 단계적으로 올린다(바탕 75% 고정).

사용:
  python3 cardnews/design/render_avatar_v6.py --download   # 서체 -> ~/.fonts/ke/, 원화 -> render/avatar-v3/src/ (커밋 제외)
  python3 cardnews/design/render_avatar_v6.py

산출물(cardnews/profile/, v5 이전 파일은 건드리지 않음):
  avatar-v6-{a,b,c}{x,y}.png, -320.png, -110.png   정사각(업로드용)
  contact-profile-v6.png                           v5-A(현재) + 2행(크롭) × 3열(서체), 원형 320/110 + 대비비
  avatar-v6-RENDER.json                            서체·라이선스·크롭 좌표·가시성·대비
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_cards as rc  # noqa: E402  (수정하지 않음)
import render_profile as rp  # noqa: E402  (circle_crop·max_radius, 수정하지 않음)
import render_avatar_v3 as v3  # noqa: E402  (download·hanji, 수정하지 않음)
import render_avatar_v4 as v4  # noqa: E402  (paper_bg·ink_layer, 수정하지 않음)
import render_avatar_v5 as v5  # noqa: E402  (art·halo·legibility_110·detail_score, 수정하지 않음)

OUT_DIR = v5.OUT_DIR
AV, SAFE_R = v3.AV, v3.SAFE_R
VIS = 0.75
CR_MIN = v5.CR_MIN
# (dilate, blur, alpha): v5와 같은 31/16/0.82부터, 미달 시만 올림. 마지막 단계는 여백을 넓고 덜 흐리게(글자 모양은 그대로)
HALO_STEPS = [(31, 16, 0.82), (31, 16, 0.88), (31, 16, 0.94), (31, 16, 1.0), (41, 12, 1.0), (51, 10, 1.0)]
X = 470  # v5-A와 같은 세로 글자 중심 x
YS = (290, 520, 750)  # v5-A와 같은 3자 중심 y

GF = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
FONTS6 = {
    "a": {"key": "nanum_myeongjo_xb", "path": "nanummyeongjo/NanumMyeongjo-ExtraBold.ttf", "family": "Nanum Myeongjo",
          "style": "ExtraBold", "kind": "명조·세리프", "size": 300},
    "b": {"key": "song_myung", "path": "songmyung/SongMyung-Regular.ttf", "family": "Song Myung",
          "style": "Regular", "kind": "붓 획 명조(궁체 느낌)", "size": 320},
    "c": {"key": "black_han_sans", "path": "blackhansans/BlackHanSans-Regular.ttf", "family": "Black Han Sans",
          "style": "Regular", "kind": "굵은 고딕", "size": 270},
}
for f in FONTS6.values():  # v4.ink_layer가 서체 키로 경로를 찾으므로 런타임에만 등록(파일 수정 없음)
    v4.FONTS[f["key"]] = {"file": f["path"].replace("/", "_"), "family": f["family"], "license": "SIL OFL 1.1",
                          "source_url": GF + f["path"], "license_url": GF + f["path"].split("/")[0] + "/OFL.txt"}

CROPS = {
    "x": {"box": [2677, 595, 3272, 1190], "name": "필통·화병 칸",
          "note": "10폭 중 9~10폭 가운데 단: 왼쪽 아래 붓 꽂힌 필통·붉은 합·보자기 함, 오른쪽 청화 화병(분홍 꽃)·붉은 잔, 위 책갑 일부"},
    "y": {"box": [1360, 149, 2660, 1449], "name": "병풍 전경(4폭)",
          "note": "10폭 중 5~8폭 × 위 3단: 책갑·주전자·병·과일 그릇·향로·꽃 화분 등 칸 12개 안팎이 한 번에 보임"},
}


def download():
    os.makedirs(v4.FONT_DIR, exist_ok=True)
    for f in FONTS6.values():
        dst = os.path.join(v4.FONT_DIR, f["path"].replace("/", "_"))
        if not os.path.exists(dst) or os.path.getsize(dst) == 0:
            subprocess.run(["curl", "-sSfL", "-o", dst, GF + f["path"]], check=True)
            print("downloaded", dst)
    v3.download()


def halo(img, mask, dilate, blur, alpha):
    """render_avatar_v5.halo와 같은 방식(글자 둘레 한지색 반투명 층), 팽창·흐림만 인자로."""
    h = mask.filter(ImageFilter.MaxFilter(dilate)).filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(h).astype(np.float32)[..., None] / 255 * alpha
    out = np.asarray(img).astype(np.float32) * (1 - a) + np.array(v5.PAPER, np.float32) * a
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def text_mask(lines):
    """글자 마스크(팽창 없음 = 서체 그대로). 여백·판독 계산용."""
    SS = 2
    m = Image.new("L", (AV * SS, AV * SS), 0)
    d = ImageDraw.Draw(m)
    for txt, fk, size, cy in lines:
        d.text((X * SS, cy * SS), txt, font=ImageFont.truetype(v4.font_path(fk), size * SS), fill=255, anchor="mm")
    return m.resize((AV, AV), Image.LANCZOS)


def render_one(fk, ck):
    f, c = FONTS6[fk], CROPS[ck]
    seed = 2026 + ord(fk) * 3 + ord(ck)
    size = f["size"]
    while True:  # 원형 안전 반경(430) 안에 들 때까지 글자 크기만 줄임(모양 변형 없음)
        lines = [(ch, f["key"], size, y) for ch, y in zip("책가도", YS)]
        ink = v4.ink_layer({"lines": lines, "x": X, "weight": 1}, seed)
        r = rp.max_radius(ink, (AV / 2, AV / 2), thr=60)
        if r <= SAFE_R or size <= 200:
            break
        size -= 10
    a_img, a_sha = v5.art(c["box"])
    base = v4.paper_bg(seed)
    base = Image.blend(base, a_img, VIS)
    mask = text_mask(lines)
    tries = []
    for dil, bl, ha in HALO_STEPS:
        bg = halo(base, mask, dil, bl, ha)
        out = bg.convert("RGBA")
        out.alpha_composite(ink)
        out = out.convert("RGB")
        cr = v5.legibility_110(out, mask)
        tries.append({"dilate": dil, "blur": bl, "alpha": ha, "contrast_110": cr, "pass": cr >= CR_MIN})
        if cr >= CR_MIN:
            break
    rec = {
        "key": fk + ck, "text": "책가도", "method": "code_render",
        "font": {"family": f["family"], "style": f["style"], "kind": f["kind"], "license": "SIL OFL 1.1",
                 "source_url": GF + f["path"], "license_url": GF + f["path"].split("/")[0] + "/OFL.txt",
                 "sha256": v5.sha(v4.font_path(f["key"])), "size_px": size, "synthetic_bold": False},
        "background_art": v5.art_rec(c["box"], c["note"], VIS, a_sha) | {"crop_name": c["name"]},
        "halo": {k: tries[-1][k] for k in ("dilate", "blur", "alpha")},
        "halo_steps": tries,
        "steps": v5.BASE_STEPS + [f"art crop saturation -20% + lut-v1, opacity {int(VIS * 100)}%",
                                  f"halo: paper color under text, mask max{tries[-1]['dilate']}+blur{tries[-1]['blur']}, alpha {tries[-1]['alpha']}",
                                  f"ink: render_avatar_v4.ink_layer ({f['family']} {f['style']}, weight 1 = no dilation, bleed 22%, grain)",
                                  "seal: none"],
        "max_radius": {"ink": r, "limit": SAFE_R},
        "legibility_110": {"contrast": tries[-1]["contrast_110"], "threshold": CR_MIN, "pass": tries[-1]["pass"]},
        "detail_std": v5.detail_score(out, mask),
        "ai_generated": False, "content_changed": False,
    }
    return out, rec


def contact(cur, cells, recs, fonts, pick):
    sq, big, small, gap, pad, head, txt = 320, 320, 110, 36, 40, 140, 104
    cw = sq
    ch = sq + 14 + big + 14 + small + txt
    W = pad * 2 + cw * 4 + gap * 3
    H = head + ch * 2 + 40 + 40
    sheet = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(sheet)
    body = lambda s: rc.font(fonts["body"], s)  # noqa: E731
    d.text((pad, 22), "프로필 사진 v6 — 대표 피드백: ① 서체 변경(Nanum Brush 말고) ② 책가도 크롭 부위 변경",
           font=body(28), fill=rp.APP_TEXT)
    d.text((pad, 64), "행 = 크롭 ⓧ/ⓨ · 열 = 서체 ⓐ 명조 / ⓑ 붓 명조 / ⓒ 굵은 고딕 · 각 칸: 정사각 → 원형 320 → 원형 110(실제 크기)",
           font=body(19), fill="#6B6B6B")
    d.text((pad, 90), "공통: 바탕 가시성 75% · 낙관 없음 · 서체 변형(가짜 볼드) 없음 · 대비 = 110px 획 vs 획 바깥 WCAG, 문턱 4.5:1",
           font=body(19), fill="#6B6B6B")

    def put(img, x, y, lab, sub, sub2, mark=None):
        sheet.paste(img.resize((sq, sq), Image.LANCZOS), (x, y))
        c = rp.circle_crop(img, (AV / 2, AV / 2), AV, big)
        sheet.paste(c, (x, y + sq + 14), c)
        s = rp.circle_crop(img, (AV / 2, AV / 2), AV, small)
        sy = y + sq + 14 + big + 14
        sheet.paste(s, (x + (cw - small) // 2, sy), s)
        ly = sy + small + 12
        d.text((x + cw // 2, ly), lab, font=body(22), fill=rp.APP_TEXT, anchor="ma", stroke_width=1, stroke_fill=rp.APP_TEXT)
        d.text((x + cw // 2, ly + 32), sub, font=body(17), fill="#6B6B6B", anchor="ma")
        d.text((x + cw // 2, ly + 56), sub2, font=body(17), fill="#6B6B6B", anchor="ma")
        if mark:
            d.rectangle([x - 10, y - 10, x + cw + 10, ly + 82], outline="#C8102E", width=5)
            d.text((x + cw - 4, y - 8), mark, font=body(20), fill="#FFFFFF", anchor="ra",
                   stroke_width=4, stroke_fill="#C8102E")

    put(cur, pad, head, "현재  v5-A", "Nanum Brush · 책갑 칸(5~6폭)", "바탕 75% · 110px 4.55:1")
    ly0 = head + ch + 40
    d.text((pad, ly0 + 20), "ⓧ 행(위): 필통·화병 칸", font=body(21), fill=rp.APP_TEXT)
    d.text((pad, ly0 + 50), "9~10폭 가운데 단", font=body(17), fill="#6B6B6B")
    d.text((pad, ly0 + 100), "ⓨ 행(아래): 병풍 전경", font=body(21), fill=rp.APP_TEXT)
    d.text((pad, ly0 + 130), "5~8폭 × 위 3단", font=body(17), fill="#6B6B6B")
    for r, ck in enumerate("xy"):
        y = head + r * (ch + 40)
        for i, fk in enumerate("abc"):
            k = fk + ck
            rec = recs[k]
            x = pad + (i + 1) * (cw + gap)
            put(cells[k], x, y, f"v6-{k}  {FONTS6[fk]['family']}",
                f"ⓧ {CROPS[ck]['name']}" if ck == "x" else f"ⓨ {CROPS[ck]['name']}",
                f"110px {rec['legibility_110']['contrast']}:1 · 여백 {rec['halo']['dilate']}/{rec['halo']['blur']}/{rec['halo']['alpha']}",
                "추천" if k == pick else None)
    return sheet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", action="store_true")
    ap.add_argument("--pick", default="by")
    a = ap.parse_args()
    if a.download:
        download()
    keys = [f + c for c in "xy" for f in "abc"]
    names = [f"avatar-v6-{k}{s}.png" for k in keys for s in ("", "-320", "-110")] + ["contact-profile-v6.png", "avatar-v6-RENDER.json"]
    clash = [n for n in names if os.path.exists(os.path.join(OUT_DIR, n))]
    if clash and os.environ.get("KE_V6_REWRITE") != "1":
        sys.exit(f"이미 있음(덮어쓰지 않음): {clash}  (v6 재렌더 의도면 KE_V6_REWRITE=1)")
    fonts = rc.load_fonts()
    cells, recs = {}, {}
    for k in keys:
        img, rec = render_one(k[0], k[1])
        cells[k], recs[k] = img, rec
        img.save(os.path.join(OUT_DIR, f"avatar-v6-{k}.png"), optimize=True)
        for s in (320, 110):
            img.resize((s, s), Image.LANCZOS).save(os.path.join(OUT_DIR, f"avatar-v6-{k}-{s}.png"), optimize=True)
        print(k, "size", rec["font"]["size_px"], "halo", rec["halo"]["alpha"], "cr110", rec["legibility_110"]["contrast"],
              "r", rec["max_radius"], "detail", rec["detail_std"])
    cur = Image.open(os.path.join(OUT_DIR, "avatar-v5-A.png")).convert("RGB")
    contact(cur, cells, recs, fonts, a.pick).save(os.path.join(OUT_DIR, "contact-profile-v6.png"), optimize=True)
    meta = {"feedback": "2026-10-02 대표(v5 컨택트시트 본 뒤): ① 붓글씨 서체 변경(Nanum Brush 말고) ② 바탕 책가도 크롭 부위 변경",
            "kept": "낙관 없음(v5-A), 바탕 가시성 75%, 세로 '책가도'",
            "visibility_def": "원화 크롭 블렌드 불투명도", "visibility": VIS,
            "legibility_def": "110px 축소본 획 vs 획 바깥 고리 WCAG 대비비(render_avatar_v5.legibility_110), 문턱 4.5(추정)",
            "no_synthetic_bold": "마스크 팽창 없음(weight 1). 크기만 조정",
            "crops": CROPS, "recommended": a.pick, "variants": [recs[k] for k in keys]}
    with open(os.path.join(OUT_DIR, "avatar-v6-RENDER.json"), "w", encoding="utf-8") as fp:
        json.dump(meta, fp, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
