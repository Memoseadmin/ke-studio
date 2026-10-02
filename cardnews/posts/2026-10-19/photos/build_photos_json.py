#!/usr/bin/env python3
"""세트 11 PHOTOS.json 생성(3안 콜라주). 사진 파일이 src/ 에 있으면 사진 주인공 + 원화 프레임, 없으면 원화 디테일로 대체하고 pending 에 적는다."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
MET1 = {"kind": "artwork", "file": "src/met-853896.jpg", "title": "Books and Scholarly Accoutrements (two-panel folding screen, 19th century)", "title_ko": "책가도",
        "institution": "The Metropolitan Museum of Art", "accession": "2024.89.6", "object_url": "https://www.metmuseum.org/art/collection/search/853896",
        "image_url": "https://images.metmuseum.org/CRDImages/as/original/DP-40204-001.jpg"}
MET2 = {"kind": "artwork", "title": "Books and Scholars' Possessions (ten-panel folding screen, early 20th century)", "title_ko": "책거리",
        "institution": "The Metropolitan Museum of Art", "accession": "2005.385", "object_url": "https://www.metmuseum.org/art/collection/search/73134"}
CMA = {"kind": "artwork", "file": "src/cma-2011.37-print.jpg", "title": "Books and Scholars' Accoutrements (ten-panel folding screen, late 1800s)", "title_ko": "책가도",
       "institution": "Cleveland Museum of Art", "accession": "2011.37", "object_url": "https://clevelandart.org/art/2011.37",
       "image_url": "https://openaccess-cdn.clevelandart.org/2011.37/2011.37_print.jpg"}
MET_LIC = {"license": "CC0 1.0 (Met Open Access, API isPublicDomain=true, 2026-10-02 확인)", "license_url": "https://www.metmuseum.org/about-the-met/policies-and-documents/open-access",
           "credit": "그림: 메트로폴리탄미술관 〈책가도〉 CC0", "credit_short": "메트로폴리탄미술관 〈책가도〉·〈책거리〉 CC0"}
CMA_LIC = {"license": "CC0 1.0 (Cleveland Open Access, API share_license_status=CC0, 2026-10-02 확인)", "license_url": "https://www.clevelandart.org/open-access",
           "credit": "그림: 클리블랜드미술관 〈책가도〉 CC0", "credit_short": "클리블랜드미술관 〈책가도〉 CC0"}
def met2(f): return dict(MET2, file=f"src/met-73134-{f}.jpg", image_url=f"https://images.metmuseum.org/CRDImages/as/original/{f}.jpg")
def art(card, base, lic, crop, note, focus=(0.5, 0.5)):
    return dict(base, **lic, date="2026-10-19", card=card, crop_note=note, edit={"preset": "archive", "crop": list(crop), "focus": list(focus)}, credit_on_image=False)
def frame(base, lic, focus, slot=(904, 584), inset=14, seed=None, depth=18):
    return {"file": base["file"], "credit_short": lic["credit_short"], "license": lic["license"], "focus": list(focus), "slot": list(slot), "inset": inset, "depth": depth, **({"seed": seed} if seed else {})}
# researcher 목록(C1-1-photos.json 10/19 항목) 그대로. 사진 원본은 src/photo-NN-*.jpg
PHOTOS = {
  1: dict(kind="photo", file="src/photo-01-pen.jpg", title="노트에 펜으로 쓰는 손", page_url="https://commons.wikimedia.org/wiki/File:Pen-writing-notes-studying.jpg",
          author="Tookapic (Pexels)", license="CC0 1.0", license_url="https://creativecommons.org/publicdomain/zero/1.0/", credit="사진: Tookapic · CC0", credit_short="Tookapic · CC0",
          edit={"preset": "hanji-duotone", "focus": [0.55, 0.5]}, frame=frame(MET1, MET_LIC, (0.72, 0.18), slot=(904, 560), seed=21),
          risk_note="손만 보이고 얼굴 없음(researcher). 듀오톤이라 펜 색·브랜드 식별 불가"),
  3: dict(kind="photo", file="src/photo-03-inkstone.jpg", title="조선 벼루·문진·벼루함·촛대(진열장)", page_url="https://commons.wikimedia.org/wiki/File:Inkstone,_Paperweight,_Inkstone_case,_Candlestick.jpg",
          author="위키미디어 사용자 고려", license="CC BY 4.0", license_url="https://creativecommons.org/licenses/by/4.0/",
          credit="사진: 위키미디어 사용자 고려 · CC BY 4.0 · 크롭·보정", credit_short="위키미디어 사용자 고려 · CC BY 4.0 · 크롭·보정",
          edit={"preset": "muted-warm", "focus": [0.5, 0.55], "crop": [0.08, 0.15, 0.92, 0.85]}, frame=frame(met2("DP163173"), MET_LIC, (0.3, 0.6), seed=33),
          risk_note="유리 반사·설명판 글자는 크롭으로 제외(researcher). CC BY: 작가명+라이선스를 마지막 장 출처 줄에 표기"),
  4: dict(kind="photo", file="src/photo-02-openbook.jpg", title="책상 위 펼친 책과 끈 책갈피", page_url="https://commons.wikimedia.org/wiki/File:Open_book_1_(Unsplash).jpg",
          author="Alina Daniker (Unsplash)", license="CC0 1.0", license_url="https://creativecommons.org/publicdomain/zero/1.0/", credit="사진: Alina Daniker · CC0", credit_short="Alina Daniker · CC0",
          edit={"preset": "hanji-duotone", "focus": [0.5, 0.5]}, frame=frame(MET1, MET_LIC, (0.3, 0.45), seed=44),
          risk_note="researcher 예비 항목(10/17과 중복 가능). 2단계 '첫 문장'에 배치"),
  6: dict(kind="photo", file="src/photo-06-calligraphy.jpg", title="서예 10폭 병풍 뒷면(19세기 후반, 초서)", page_url="https://clevelandart.org/art/1998.286.b",
          author="작자 미상 / 클리블랜드미술관(1998.286.b)", license="CC0 1.0", license_url="https://creativecommons.org/publicdomain/zero/1.0/",
          credit="서예 병풍 · 클리블랜드미술관 · CC0", credit_short="서예 병풍 · 클리블랜드미술관(1998.286.b) · CC0",
          edit={"preset": "muted-warm", "focus": [0.5, 0.5], "crop": [0.18, 0.08, 0.56, 0.9]}, frame=frame(met2("DP163174"), MET_LIC, (0.5, 0.45), seed=66),
          risk_note="정자·흘림 대비용(researcher). 사람·로고 없음"),
}
ART = {
  1: art(1, MET1, MET_LIC, (1700, 560, 2290, 920), "대체: 오른쪽 폭 윗부분 두루마리·붓·부채"),
  2: art(2, met2("DP163173"), MET_LIC, (790, 1500, 1400, 1850), "둘째 폭: 책 더미·두루마리 꽂이·청화 항아리"),
  3: art(3, met2("DP163173"), MET_LIC, (780, 2230, 1240, 2560), "대체: 소반 위 벼루함"),
  4: art(4, MET1, MET_LIC, (690, 930, 1280, 1290), "대체: 쌓인 책갑"),
  5: art(5, met2("DP163174"), MET_LIC, (1660, 1770, 2020, 1960), "자명종 문자판(10분 루틴)"),
  6: art(6, met2("DP163174"), MET_LIC, (820, 960, 1300, 1235), "대체: 붓대·매화"),
  7: art(7, met2("DP163173"), MET_LIC, (1690, 2080, 2300, 2430), "문갑과 책(기록 남기기)"),
  8: art(8, CMA, CMA_LIC, (126, 143, 3282, 1463), "10폭 전경 띠(마지막 장)"),
}
photos, pending = [], []
for n in range(1, 9):
    p = PHOTOS.get(n)
    if p and os.path.isfile(os.path.join(H, p["file"])) and os.path.getsize(os.path.join(H, p["file"])) > 1000:
        photos.append(dict(p, date="2026-10-19", card=n, credit_on_image=False))
    else:
        if p:
            pending.append(f"card {n}: {p['file']} 미수신(위키미디어 429) -> 원화 디테일로 대체")
        photos.append(ART[n])
doc = {"set": "2026-10-19", "direction": "v3 3안 하이브리드 콜라주(대표 결정 2026-10-02)",
       "schema": "card, kind(artwork|photo), file(photos/ 기준), credit, credit_short, license, edit{preset, crop, focus}, frame{file, credit_short, license, focus, slot, inset, seed, depth}(사진만), credit_on_image",
       "note": "원본은 src/ 에 그대로. 편집 사본은 렌더 때 render/cardnews-v3/ 에만 생성(크롭·톤·질감·찢김 테두리·프레임 합성, 내용 변형 없음). 사진 크레딧은 마지막 장 출처 줄에 모은다(CC BY = 작가명+라이선스)",
       "pending": pending, "photos": photos}
json.dump(doc, open(os.path.join(H, "PHOTOS.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("photos:", [(e["card"], e["kind"]) for e in photos]); print("pending:", pending)
