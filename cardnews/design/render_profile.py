#!/usr/bin/env python3
"""책가도 노트(@chaekgado.note) 인스타그램 프로필 시각 패키지 목업 렌더러.

사용:
  python3 cardnews/design/render_profile.py            # 전부 생성 -> cardnews/profile/
  python3 cardnews/design/render_profile.py --final    # 게시용(모서리 MOCKUP 표기 생략). approved 전에는 쓰지 않는다

산출물(cardnews/profile/):
  avatar-A/B/C.png        1080x1080 프로필 사진 3안 (핵심 요소는 중앙 지름 860px 원 안)
  avatar-preview.png      3안 원형 마스크 320px·110px 비교
  highlight-01..05.png    1080x1920 하이라이트 커버 (01 한글 / 02 가볼 곳 / 03 비하인드 / 04 트렌드 / 05 문의)
  highlights-preview.png  5개 원형 110px + 이름 한 줄
  grid-preview.png        posts/2026-10-09~17 card-01 을 3:4 그리드 3x3(최신 왼쪽 위)로 배치

원칙: render_cards.py(수정 금지)의 TOKENS·load_fonts·save_png 를 import 해서 그대로 쓴다.
모든 도형은 이 파일 안에서 직접 그린 플랫 도형(외부 이미지·아이콘·글꼴 글리프 0).
'책' 한 글자(C안)도 글꼴이 아니라 사각형·다각형으로 조립한다. 인물·로고·IP·호랑이·까치 없음.
한지 결은 render_cards.hanji_background 와 같은 레시피(노이즈 블러 + 세로 결 + 5단계 포스터라이즈 + 9% 블렌드)를
임의 크기·고정 시드로 다시 구현했다(재실행해도 같은 PNG).
"""
import argparse
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_cards as rc  # noqa: E402  (토큰·폰트·저장 재사용. 이 파일은 수정하지 않는다)

T = rc.TOKENS
INK = T["ink"]
CARDNEWS = os.path.dirname(HERE)
OUT_DIR = os.path.join(CARDNEWS, "profile")
POSTS_DIR = os.path.join(CARDNEWS, "posts")

SS = 3                      # 슈퍼샘플 배율(도형 가장자리 안티에일리어싱)
AV = 1080                   # 프로필 사진 캔버스
AV_SAFE_R = 430             # 핵심 요소 안전 원 반지름(지름 860)
AV_LW = 22                  # 프로필 사진 잉크 선 굵기(110px 축소 시 약 2.2px)
HL_W, HL_H = 1080, 1920     # 하이라이트 커버 캔버스
HL_C = (540, 960)           # 중앙 원 중심
HL_DISC_R = 300             # 중앙 원 반지름(지름 600)
HL_ICON_R = 262             # 아이콘이 들어가야 하는 반지름(원 테두리 안쪽 여백 약 30px)
HL_ICON_K = 0.9             # 아이콘 좌표 배율(선 굵기는 HL_LW 그대로)
HL_LW = 14                  # 하이라이트 잉크 선 굵기(5개 공통)
HL_CROP_D = 680             # 미리보기용 커버 원형 크롭 지름(중앙 원 + 테 40px)
HL_DISC_FILL = T["yellow"]  # 5개 공통 원 바탕
HIGHLIGHTS = [("01", "한글"), ("02", "가볼 곳"), ("03", "비하인드"), ("04", "트렌드"), ("05", "문의")]
GRID_DATES = ["2026-10-17", "2026-10-16", "2026-10-15", "2026-10-14", "2026-10-13",
              "2026-10-12", "2026-10-11", "2026-10-10", "2026-10-09"]  # 1번 칸(왼쪽 위) = 최신
APP_TEXT = "#262626"        # 미리보기 이름 글자색(앱 화면 흉내)
APP_RING = "#DBDBDB"
FINAL = False


# ---------- 한지 결 (render_cards.hanji_background 레시피, 크기·시드 고정판) ----------
def _noise(size, sigma, seed):
    """균등 난수를 표준편차 sigma 근처로 줄인 회색 노이즈(Image.effect_noise 대용, 시드 고정)."""
    raw = Image.frombytes("L", size, random.Random(seed).randbytes(size[0] * size[1]))
    k = sigma / 73.9  # 균등분포 0~255 의 표준편차 약 73.9
    return raw.point(lambda v: max(0, min(255, int(128 + (v - 128) * k))))


_GRAIN = {}


def grain(size, seed=7):
    key = (size, seed)
    if key not in _GRAIN:
        w, h = size
        noise = _noise(size, 30, seed).filter(ImageFilter.GaussianBlur(1.8))
        fiber = _noise((max(1, w // 8), h), 60, seed + 1).resize(size, Image.BILINEAR)  # 세로 결
        _GRAIN[key] = Image.blend(noise, fiber, 0.35).point(lambda v: (v // 52) * 52).convert("RGB")
    return _GRAIN[key]


def textured(size, color, seed=7):
    """단색 + 한지 결 9% (카드 배경과 같은 비율)."""
    return Image.blend(Image.new("RGB", size, color), grain(size, seed), 0.09)


# ---------- 슈퍼샘플 펜: 좌표는 최종 캔버스 기준, 내부는 SS배로 그림 ----------
class Pen:
    """k, kc: 좌표만 kc 기준 k배(선 굵기는 그대로) -> 아이콘 크기를 바꿔도 5개 선 굵기가 같다."""
    def __init__(self, size, k=1.0, kc=(0, 0)):
        self.size = size
        self.k, self.kc = k, kc
        self.img = Image.new("RGBA", (size[0] * SS, size[1] * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def _xy(self, x, y):
        return ((self.kc[0] + self.k * (x - self.kc[0])) * SS, (self.kc[1] + self.k * (y - self.kc[1])) * SS)

    def _p(self, pts):
        return [self._xy(x, y) for x, y in pts]

    def poly(self, pts, fill=None, lw=0, outline=INK):
        """다각형. 외곽선은 변의 중앙에 걸치고 모서리는 둥글게(joint=curve)."""
        P = self._p(pts)
        if fill:
            self.d.polygon(P, fill=fill)
        if lw:
            self.d.line(P + P[:2], fill=outline, width=int(round(lw * SS)), joint="curve")

    def rect(self, box, fill=None, lw=0, outline=INK):
        x0, y0, x1, y1 = box
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, lw, outline)

    def ellipse(self, box, fill=None, lw=0, outline=INK):
        (x0, y0), (x1, y1) = self._p([box[:2], box[2:]])
        h = lw * SS / 2
        if lw:
            self.d.ellipse([x0 - h, y0 - h, x1 + h, y1 + h], fill=outline)
            if fill:
                self.d.ellipse([x0 + h, y0 + h, x1 - h, y1 - h], fill=fill)
        elif fill:
            self.d.ellipse([x0, y0, x1, y1], fill=fill)

    def circle(self, c, r, fill=None, lw=0, outline=INK):
        self.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill, lw, outline)

    def ring(self, c, r, lw, color):
        """테두리만 있는 원(반지름 r 에 중앙 정렬)."""
        h = lw / 2 * SS
        (x0, y0), (x1, y1) = self._p([(c[0] - r, c[1] - r), (c[0] + r, c[1] + r)])
        x0, y0, x1, y1 = x0 - h, y0 - h, x1 + h, y1 + h
        self.d.ellipse([x0, y0, x1, y1], outline=color, width=int(round(lw * SS)))

    def line(self, pts, lw, color=INK):
        P = self._p(pts)
        w = int(round(lw * SS))
        self.d.line(P, fill=color, width=w, joint="curve")
        for x, y in (P[0], P[-1]):  # 둥근 끝
            self.d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=color)

    def result(self):
        return self.img.resize(self.size, Image.LANCZOS)


def tr(pts, c, ang=0.0, s=1.0):
    """로컬 좌표(원점 중심) -> 회전(도, 시계방향) -> 확대 -> c 로 이동."""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + s * (x * ca - y * sa), c[1] + s * (x * sa + y * ca)) for x, y in pts]


def rect_pts(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def book_lying(pen, x0, y0, x1, y1, color, lw, pages_right=True):
    """눕힌 책: 표지색 몸통 + 한쪽 끝 책장(종이) 면 + 띠."""
    pen.rect((x0, y0, x1, y1), color, lw)
    pw = max(18, (y1 - y0) * 0.55)
    if pages_right:
        pen.rect((x1 - pw, y0 + lw * 0.5, x1 - lw * 0.5, y1 - lw * 0.5), T["paper"], 0)
        pen.line([(x1 - pw, y0), (x1 - pw, y1)], lw * 0.6)
    else:
        pen.rect((x0 + lw * 0.5, y0 + lw * 0.5, x0 + pw, y1 - lw * 0.5), T["paper"], 0)
        pen.line([(x0 + pw, y0), (x0 + pw, y1)], lw * 0.6)


def book_standing(pen, x0, y0, x1, y1, color, lw, band=T["paper"]):
    """세운 책: 책등 + 위쪽 띠 1줄."""
    pen.rect((x0, y0, x1, y1), color, lw)
    bh = (y1 - y0) * 0.12
    by = y0 + (y1 - y0) * 0.16
    pen.rect((x0, by, x1, by + bh), band, lw * 0.6)


# ---------- 프로필 사진 3안 (bg, core) ----------
def avatar_A():
    """A 책장 격자: 둥근 창 안에 칸 높이가 엇갈린 책가도식 책장(눕힌 책·세운 책·항아리) + 서랍."""
    bg = textured((AV, AV), T["paper"])
    pen = Pen((AV, AV))
    lw = AV_LW
    fl = lw * 1.3                                 # 틀·칸막이 굵기
    c, R = (540, 540), 404                        # 둥근 창 틀(중심선 반지름, 바깥 가장자리 ≈ 419 < 430)
    xm, yl, yr, yf = 540, 560, 470, 820           # 세로 칸막이 / 왼쪽·오른쪽 가로 칸막이(엇갈림) / 바닥 선반

    def half(y):                                  # 높이 y 에서 창 안쪽 반폭
        return math.sqrt(max(0, R * R - (y - c[1]) ** 2))
    pen.circle(c, R, T["white"])
    # 바닥 아래 서랍(크라프트 면 + 손잡이)
    a0 = math.degrees(math.asin((yf - c[1]) / R))
    seg = [(c[0] + R * math.cos(math.radians(a)), c[1] + R * math.sin(math.radians(a)))
           for a in [a0 + (180 - 2 * a0) * i / 40 for i in range(41)]]
    pen.poly(seg, T["kraft"])
    pen.rect((c[0] - 44, yf + 46, c[0] + 44, yf + 64), INK)
    # 칸막이·바닥
    pen.line([(xm, c[1] - R), (xm, yf)], fl)
    pen.line([(c[0] - half(yl), yl), (xm, yl)], fl)
    pen.line([(xm, yr), (c[0] + half(yr), yr)], fl)
    pen.line([(c[0] - half(yf), yf), (c[0] + half(yf), yf)], fl)
    bl = lw * 0.75
    # 왼쪽 위: 눕힌 책 3권
    bh, base = 72, yl - fl / 2
    for i, (w, off, col) in enumerate([(244, 0, T["red"]), (214, 22, T["celadon"]), (230, 8, T["kraft"])]):
        bx0 = 266 + off
        book_lying(pen, bx0, base - (i + 1) * bh, bx0 + w, base - i * bh, col, bl, pages_right=(i % 2 == 0))
    # 왼쪽 아래: 세운 책 4권
    base, sx = yf - fl / 2, 284
    for w, h, col in [(52, 196, T["night"]), (52, 166, T["red"]), (52, 212, T["wheat"]), (52, 150, T["celadon"])]:
        book_standing(pen, sx, base - h, sx + w, base, col, bl)
        sx += w + 8
    # 오른쪽 위: 둥근 항아리(일반 형태, 특정 작품 아님) + 눕힌 책 1권
    base = yr - fl / 2
    jx = 668
    pen.rect((jx - 38, base - 192, jx + 38, base - 156), T["white"], bl)
    pen.ellipse((jx - 90, base - 172, jx + 90, base), T["white"], bl)
    book_lying(pen, 778, base - 62, 868, base, T["red"], bl)
    # 오른쪽 아래: 눕힌 책 4권
    bh, base = 70, yf - fl / 2
    for i, (w, off, col) in enumerate([(230, 0, T["night"]), (236, 12, T["wheat"]),
                                       (252, 6, T["red"]), (222, 26, T["celadon"])]):
        bx0 = xm + 26 + off
        book_lying(pen, bx0, base - (i + 1) * bh, bx0 + w, base - i * bh, col, bl, pages_right=(i % 2 == 1))
    pen.ring(c, R, fl, INK)
    return bg, pen.result()


def avatar_B():
    """B 책 더미 + 해: 노란 해(햇살 7줄) 앞에 눕힌 책 4권.
    해를 붉은 원으로 두면 옅은 바탕 위 '붉은 원' = 일장기 연상 위험이 있어 노란 해 + 잉크 테 + 햇살로 그린다."""
    bg = textured((AV, AV), T["paper"])
    pen = Pen((AV, AV))
    lw = AV_LW
    sc, sr = (540, 424), 196
    for a in range(-180, 1, 30):  # 윗반원 햇살(아래쪽은 책에 가려짐)
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        pen.line([(sc[0] + ca * (sr + 46), sc[1] + sa * (sr + 46)), (sc[0] + ca * (sr + 100), sc[1] + sa * (sr + 100))], lw)
    pen.circle(sc, sr, T["yellow"], lw)
    books = [  # (x0, x1, 색, 책장 면 방향) 위에서 아래로
        (322, 770, T["red"], True),
        (272, 790, T["celadon"], False),
        (300, 818, T["white"], True),
        (252, 828, T["night"], False),
    ]
    bh = 80
    top = 502
    for i, (bx0, bx1, col, right) in enumerate(books):
        book_lying(pen, bx0, top + i * bh, bx1, top + (i + 1) * bh, col, lw, pages_right=right)
    return bg, pen.result()


def glyph_chaek(pen, box, color):
    """'책'을 사각형·다각형으로 조립(글꼴 미사용). box = (x0, y0, 크기)."""
    gx, gy, S = box

    def P(u, v):
        return (gx + u * S, gy + v * S)

    def R(u0, v0, u1, v1):
        pen.poly([P(u0, v0), P(u1, v0), P(u1, v1), P(u0, v1)], color)
    # ㅊ
    R(0.205, 0.00, 0.315, 0.11)                      # 꼭지
    R(0.02, 0.14, 0.50, 0.25)                        # 가로획
    pen.poly([P(0.20, 0.25), P(0.32, 0.25), P(0.135, 0.60), P(0.01, 0.60)], color)  # 왼 삐침
    pen.poly([P(0.20, 0.25), P(0.32, 0.25), P(0.51, 0.60), P(0.385, 0.60)], color)  # 오른 내림
    # ㅐ
    R(0.60, 0.00, 0.71, 0.62)
    R(0.71, 0.26, 0.86, 0.37)
    R(0.86, 0.00, 0.97, 0.66)
    # ㄱ 받침
    R(0.05, 0.74, 0.97, 0.85)
    R(0.86, 0.74, 0.97, 1.00)


def avatar_C():
    """C 낙관 '책': 붉은 바탕 + 종이색 정사각 테 + 도형으로 조립한 '책' 한 글자."""
    bg = textured((AV, AV), T["red"])
    pen = Pen((AV, AV))
    side = 584                                    # 테 바깥 반대각선 ≈ 426 < 430
    s0 = 540 - side / 2
    lw = 18
    pen.poly(rect_pts(s0, s0, s0 + side, s0 + side), None, lw, outline=T["paper"])
    S = 410
    glyph_chaek(pen, (540 - S / 2 + 2, 540 - S / 2, S), T["paper"])
    return bg, pen.result()


AVATARS = [("A", "책장 격자", avatar_A), ("B", "책 더미와 해", avatar_B), ("C", "낙관 '책'", avatar_C)]


# ---------- 하이라이트 아이콘 (원점 중심 로컬 좌표, 5개 공통 선 굵기 HL_LW) ----------
def icon_brush(pen, c):
    """01 한글: 먹 묻은 붓 한 자루(글자 없음)."""
    ang, lw = 40, HL_LW
    pen.poly(tr(rect_pts(-26, -214, 26, 52), c, ang), T["kraft"], lw)           # 붓대
    pen.poly(tr(rect_pts(-30, -232, 30, -190), c, ang), T["red"], lw)          # 붓대 끝 마개
    pen.poly(tr(rect_pts(-36, 44, 36, 88), c, ang), T["night"], lw)            # 쇠테
    tip = [(-40, 88), (-46, 124), (-40, 164), (-24, 200), (0, 234), (24, 200), (40, 164), (46, 124), (40, 88)]
    pen.poly(tr(tip, c, ang), T["white"], lw)                                  # 붓털
    dip = [(-42, 160), (-24, 200), (0, 234), (24, 200), (42, 160), (20, 150), (0, 160), (-20, 150)]
    pen.poly(tr(dip, c, ang), INK, 0)                                          # 먹 묻은 끝
    pen.circle(tr([(10, 262)], c, ang)[0], 16, INK)                            # 먹 방울


def icon_pin(pen, c):
    """02 가볼 곳: 위치 핀 + 낮은 산 두 봉우리."""
    lw = HL_LW
    cx, cy = c
    pen.poly([(cx - 196, cy + 200), (cx - 96, cy + 76), (cx - 4, cy + 200)], T["celadon"], lw)
    pen.poly([(cx - 56, cy + 200), (cx + 80, cy + 40), (cx + 196, cy + 200)], T["kraft"], lw)
    hc = (cx, cy - 70)
    r, tip = 122, (cx, cy + 186)
    dist = tip[1] - hc[1]
    al = math.degrees(math.acos(r / dist))
    a0, a1 = 90 - al, 90 + al - 360
    arc = [(hc[0] + r * math.cos(math.radians(a)), hc[1] + r * math.sin(math.radians(a)))
           for a in [a0 + (a1 - a0) * i / 60 for i in range(61)]]
    pen.poly([tip] + arc, T["red"], lw)
    pen.circle(hc, 50, T["paper"], lw)


def icon_screen(pen, c):
    """03 비하인드: 반쯤 접힌 4폭 병풍(책가도가 그려지는 자리). 칸마다 선반 1줄."""
    lw = HL_LW
    cx, cy = c
    n, pw, dz, ht = 4, 96, 34, 350
    xs = [cx - n * pw / 2 + i * pw for i in range(n + 1)]
    off = [0 if i % 2 == 0 else dz for i in range(n + 1)]
    top = cy - ht / 2 - dz / 2 - 10

    def ytop(i, x):  # 폭 i 의 윗변 높이(x 에서)
        return top + off[i] + (off[i + 1] - off[i]) * (x - xs[i]) / pw
    inner = [T["white"], T["wheat"], T["white"], T["wheat"]]
    books = [T["red"], T["celadon"], T["kraft"], T["red"]]
    for i in range(n):
        # 바깥 테(night 비단 테) + 안쪽 화면
        q = [(xs[i], ytop(i, xs[i])), (xs[i + 1], ytop(i, xs[i + 1])),
             (xs[i + 1], ytop(i, xs[i + 1]) + ht), (xs[i], ytop(i, xs[i]) + ht)]
        pen.poly(q, T["night"], lw)
        m, mv = 18, 26
        a, b = xs[i] + m, xs[i + 1] - m
        pen.poly([(a, ytop(i, a) + mv), (b, ytop(i, b) + mv), (b, ytop(i, b) + ht - mv), (a, ytop(i, a) + ht - mv)],
                 inner[i], 0)
        # 선반 1줄 + 책 한 덩이(면 기울기 따라)
        sh = ht * 0.58
        pen.line([(a, ytop(i, a) + sh), (b, ytop(i, b) + sh)], lw * 0.7)
        ba, bb = a + 8, b - 12
        pen.poly([(ba, ytop(i, ba) + sh - 70), (bb, ytop(i, bb) + sh - 70),
                  (bb, ytop(i, bb) + sh - lw * 0.35), (ba, ytop(i, ba) + sh - lw * 0.35)], books[i], lw * 0.6)
    for i in range(n + 1):  # 발
        y = top + off[i] + ht
        pen.rect((xs[i] - 14, y - 2, xs[i] + 14, y + 24), INK)


def icon_trend(pen, c):
    """04 트렌드: 키가 커지는 세운 책 3권 + 오르는 화살표."""
    lw = HL_LW
    cx, cy = c
    base = cy + 190
    pen.rect((cx - 186, base, cx + 186, base + 22), INK)
    for x0, h, col in [(-170, 130, T["kraft"]), (-55, 210, T["celadon"]), (60, 290, T["red"])]:
        book_standing(pen, cx + x0, base - h, cx + x0 + 96, base, col, lw)
    a, b = (cx - 175, cy - 20), (cx + 120, cy - 196)
    pen.line([a, b], lw * 1.6)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    L, Wd = 74, 46
    tip = (b[0] + math.cos(ang) * 40, b[1] + math.sin(ang) * 40)
    back = (tip[0] - math.cos(ang) * L, tip[1] - math.sin(ang) * L)
    nx, ny = -math.sin(ang), math.cos(ang)
    pen.poly([tip, (back[0] + nx * Wd, back[1] + ny * Wd), (back[0] - nx * Wd, back[1] - ny * Wd)], INK, lw * 0.6)


def icon_letter(pen, c):
    """05 문의: 봉투 + 붉은 낙관 사각(글자 없음)."""
    lw = HL_LW
    cx, cy = c
    x0, y0, x1, y1 = cx - 210, cy - 140, cx + 210, cy + 150
    pen.rect((x0, y0, x1, y1), T["white"], lw)
    pen.line([(x0, y1), (cx - 30, cy + 10)], lw * 0.8)
    pen.line([(x1, y1), (cx + 30, cy + 10)], lw * 0.8)
    pen.poly([(x0, y0), (x1, y0), (cx, cy + 44)], T["wheat"], lw)
    s = 92
    sc = (cx, cy + 40)
    pen.rect((sc[0] - s / 2, sc[1] - s / 2, sc[0] + s / 2, sc[1] + s / 2), T["red"], lw * 0.8)
    pen.rect((sc[0] - s / 2 + 22, sc[1] - s / 2 + 22, sc[0] + s / 2 - 22, sc[1] + s / 2 - 22), None, lw * 0.6, T["paper"])


ICONS = {"01": icon_brush, "02": icon_pin, "03": icon_screen, "04": icon_trend, "05": icon_letter}


def highlight(num):
    """하이라이트 커버 1장: (완성 이미지, 아이콘 레이어). 배경·원·선 굵기·색 규칙 5개 공통."""
    bg = textured((HL_W, HL_H), T["paper"])
    disc = Pen((HL_W, HL_H))
    disc.circle(HL_C, HL_DISC_R, HL_DISC_FILL, HL_LW)
    icon = Pen((HL_W, HL_H), k=HL_ICON_K, kc=HL_C)
    ICONS[num](icon, HL_C)
    disc_l, icon_l = disc.result(), icon.result()
    img = bg.convert("RGBA")
    img.alpha_composite(disc_l)
    img.alpha_composite(icon_l)
    return img.convert("RGB"), icon_l


# ---------- 공통: MOCKUP 표기(원형 크롭 밖 모서리), 검사, 원형 마스크 ----------
def mockup_corner(img, fonts):
    if FINAL:
        return
    d = ImageDraw.Draw(img)
    f = rc.font(fonts["latin"], 30)
    tw = rc.text_w(d, rc.MOCKUP_TAG, f)
    w, h = img.size
    x, y = w - 40 - tw - 14, h - 40 - 44
    # 바탕이 붉은 안(C)에서는 붉은 표기가 묻히므로 종이색으로
    col = T["red"] if contrast(_hex(img.getpixel((x - 20, y))), T["red"]) >= 3 else T["paper"]
    d.rounded_rectangle([x - 14, y - 6, x + tw + 14, y + 40], radius=8, outline=col, width=3)
    d.text((x, y), rc.MOCKUP_TAG, font=f, fill=col)


def _hex(rgb):
    return "#%02X%02X%02X" % tuple(rgb[:3])


def max_radius(layer, c, thr=24):
    """레이어에서 알파 > thr 인 픽셀의 중심 c 로부터 최대 거리(px, 이분 탐색)."""
    a = layer.getchannel("A").point(lambda v: 255 if v > thr else 0)
    if a.getbbox() is None:
        return 0
    lo, hi = 0, int(math.hypot(*layer.size)) + 1
    while hi - lo > 1:
        r = (lo + hi) // 2
        m = Image.new("L", layer.size, 255)
        ImageDraw.Draw(m).ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=0)
        if ImageChops.multiply(a, m).getbbox() is None:
            hi = r
        else:
            lo = r
    return hi


def circle_crop(img, c, d, out):
    """img 의 중심 c, 지름 d 영역을 out px 원형으로(RGBA, 가장자리 안티에일리어싱)."""
    box = (int(c[0] - d / 2), int(c[1] - d / 2), int(c[0] + d / 2), int(c[1] + d / 2))
    im = img.crop(box).resize((out, out), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (out * 4, out * 4), 0)
    ImageDraw.Draw(m).ellipse([0, 0, out * 4 - 1, out * 4 - 1], fill=255)
    im.putalpha(m.resize((out, out), Image.LANCZOS))
    return im


def _lum(hexc):
    v = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    v = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def contrast(a, b):
    la, lb = sorted([_lum(a), _lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


# ---------- 미리보기 ----------
def avatar_preview(avatars, fonts):
    pad, gap, big, small = 48, 56, 320, 110
    colw = big
    W = pad * 2 + 3 * colw + 2 * gap
    head = 84
    H = head + big + 40 + small + 30 + 60 + pad
    sheet = Image.new("RGB", (W, H), T["white"])
    d = ImageDraw.Draw(sheet)
    d.text((pad, 28), "프로필 사진 후보 (원형 마스크, 320px / 110px)" + ("" if FINAL else "  MOCKUP"),
           font=rc.font(fonts["body"], 30), fill=APP_TEXT)
    for i, (key, name, img) in enumerate(avatars):
        x = pad + i * (colw + gap)
        b = circle_crop(img, (AV / 2, AV / 2), AV, big)
        sheet.paste(b, (x, head), b)
        s = circle_crop(img, (AV / 2, AV / 2), AV, small)
        sy = head + big + 40
        sheet.paste(s, (x + (colw - small) // 2, sy), s)
        ly = sy + small + 30
        d.text((x + colw // 2, ly), f"{key}  {name}", font=rc.font(fonts["body"], 34), fill=APP_TEXT, anchor="ma",
               stroke_width=1, stroke_fill=APP_TEXT)
    return sheet


def highlights_preview(covers, fonts):
    size, gap, pad = 110, 52, 40
    ring_gap, ring_w = 6, 2
    cell = size + 2 * (ring_gap + ring_w)
    W = pad * 2 + 5 * cell + 4 * gap
    top = 70
    H = top + cell + 64 + pad
    sheet = Image.new("RGB", (W, H), T["white"])
    d = ImageDraw.Draw(sheet)
    d.text((pad, 22), "하이라이트 (원형 110px)" + ("" if FINAL else "  MOCKUP"), font=rc.font(fonts["body"], 26), fill="#8E8E8E")
    f = rc.font(fonts["body"], 26)
    for i, ((num, name), img) in enumerate(zip(HIGHLIGHTS, covers)):
        x = pad + i * (cell + gap)
        # 앱의 회색 테(1겹) + 흰 틈
        ring = Image.new("L", (cell * 4, cell * 4), 0)
        rd = ImageDraw.Draw(ring)
        rd.ellipse([0, 0, cell * 4 - 1, cell * 4 - 1], fill=255)
        rd.ellipse([ring_w * 4, ring_w * 4, cell * 4 - 1 - ring_w * 4, cell * 4 - 1 - ring_w * 4], fill=0)
        ring = ring.resize((cell, cell), Image.LANCZOS)
        sheet.paste(Image.new("RGB", (cell, cell), APP_RING), (x, top), ring)
        c = circle_crop(img, HL_C, HL_CROP_D, size)
        sheet.paste(c, (x + ring_gap + ring_w, top + ring_gap + ring_w), c)
        d.text((x + cell // 2, top + cell + 14), name, font=f, fill=APP_TEXT, anchor="ma")
    return sheet


def grid_preview(fonts):
    """card-01 9장을 3:4 칸 3x3 으로. 원본은 읽기만 한다(4:5 -> 3:4 가운데 크롭)."""
    cw, gap, cols = 358, 3, 3
    ch = round(cw * 4 / 3)
    head, foot = 76, 150
    W = cols * cw + (cols - 1) * gap
    H = head + 3 * ch + 2 * gap + foot
    sheet = Image.new("RGB", (W, H), T["white"])
    d = ImageDraw.Draw(sheet)
    d.text((20, 22), "@chaekgado.note 그리드 미리보기 (3:4 칸, 최신 = 왼쪽 위)" + ("" if FINAL else "  MOCKUP"),
           font=rc.font(fonts["body"], 28), fill=APP_TEXT)
    legend, crop_report = [], []
    for k, date in enumerate(GRID_DATES):
        p = os.path.join(POSTS_DIR, date, "card-01.png")
        src = Image.open(p).convert("RGB")
        w, h = src.size
        tw = round(h * 3 / 4)
        x0 = (w - tw) // 2
        # 잘려 나가는 좌우 띠에 잉크(어두운 픽셀)가 있는지 검사
        lost = [src.crop((0, 0, x0, h)), src.crop((x0 + tw, 0, w, h))]
        dark = sum(sum(s.convert("L").point(lambda v: 255 if v < 90 else 0).histogram()[255:]) for s in lost)
        crop_report.append((date, x0, w - x0 - tw, dark))
        tile = src.crop((x0, 0, x0 + tw, h)).resize((cw, ch), Image.LANCZOS)
        r, cidx = divmod(k, cols)
        sheet.paste(tile, (cidx * (cw + gap), head + r * (ch + gap)))
        typ = ""
        try:
            import json
            with open(os.path.join(POSTS_DIR, date, "cards.json"), encoding="utf-8") as fp:
                typ = json.load(fp).get("type", "")
        except Exception:
            pass
        legend.append(f"{k + 1} {date[5:].replace('-', '/')} {typ}")
    f = rc.font(fonts["body"], 26)
    ly = head + 3 * ch + 2 * gap + 22
    for row in range(3):
        d.text((20, ly + row * 40), "   ·   ".join(legend[row * 3:(row + 1) * 3]), font=f, fill=APP_TEXT)
    return sheet, crop_report


# ---------- 조립 ----------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--final", action="store_true", help="게시용: 모서리 MOCKUP 표기 생략(approved 후에만)")
    ap.add_argument("--out", default=OUT_DIR, help="출력 폴더(기본 cardnews/profile)")
    args = ap.parse_args()
    global FINAL
    FINAL = args.final
    os.makedirs(args.out, exist_ok=True)
    fonts = rc.load_fonts()
    print("fonts:", fonts)
    report = []

    avatars = []
    for key, name, fn in AVATARS:
        bg, core = fn()
        img = bg.convert("RGBA")
        img.alpha_composite(core)
        img = img.convert("RGB")
        mockup_corner(img, fonts)
        path = os.path.join(args.out, f"avatar-{key}.png")
        rc.save_png(img, path)
        r = max_radius(core, (AV / 2, AV / 2))
        report.append(f"avatar-{key}: {img.size[0]}x{img.size[1]}, core max r={r}px (limit {AV_SAFE_R}) "
                      f"{'OK' if r <= AV_SAFE_R else 'FAIL'}")
        avatars.append((key, name, img))
    rc.save_png(avatar_preview(avatars, fonts), os.path.join(args.out, "avatar-preview.png"))

    covers = []
    for num, name in HIGHLIGHTS:
        img, icon_l = highlight(num)
        mockup_corner(img, fonts)
        path = os.path.join(args.out, f"highlight-{num}.png")
        rc.save_png(img, path)
        r = max_radius(icon_l, HL_C)
        report.append(f"highlight-{num} {name}: {img.size[0]}x{img.size[1]}, icon max r={r}px "
                      f"(limit {HL_ICON_R}, disc {HL_DISC_R}) {'OK' if r <= HL_ICON_R else 'FAIL'}")
        covers.append(img)
    rc.save_png(highlights_preview(covers, fonts), os.path.join(args.out, "highlights-preview.png"))

    grid, crop_report = grid_preview(fonts)
    rc.save_png(grid, os.path.join(args.out, "grid-preview.png"))
    for date, lcut, rcut, dark in crop_report:
        report.append(f"grid {date}: 4:5->3:4 crop L{lcut}px R{rcut}px, dark px lost={dark}")

    report.append("contrast ink/paper %.1f, paper/red %.1f, ink/yellow %.1f, white/red %.1f" % (
        contrast(INK, T["paper"]), contrast(T["paper"], T["red"]), contrast(INK, T["yellow"]), contrast(T["white"], T["red"])))
    for line in report:
        print(" ", line)
    fails = [x for x in report if "FAIL" in x]
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
