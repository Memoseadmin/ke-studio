#!/usr/bin/env python3
"""KE Studio 카드뉴스(인스타 4:5) 렌더러. v2(2026-10-02): 동봉 글꼴 + 글자 단위 폴백 + 사진 칸 + AI 플레이트.

사용:
  python3 render_cards.py <post_dir>                       # <post_dir>/cards.json -> card-NN.png + contact.png
  python3 render_cards.py --all cardnews/posts             # 날짜 폴더 전부
  python3 render_cards.py --all cardnews/posts --out DIR   # 결과만 DIR/<날짜>/ 에 저장(원본 폴더 PNG를 덮어쓰지 않음)
  python3 render_cards.py --all cardnews/posts --final     # 게시용(MOCKUP 표기 없음). approved 후에만

규격: cardnews/design/template.md + DESIGN-v2.md. 디자인 토큰은 EP001 design-system.md v1.0 §1~§3·§6을 그대로 쓴다.
레이어: 배경(paper+한지 결) -> 그림 칸(사진 > AI 플레이트 > 코드 도형) -> 텍스트 -> MOCKUP.
글꼴: cardnews/design/fonts/(Black Han Sans·Pretendard, OFL)를 먼저 찾는다(v2 프로필). 없으면 시스템 글꼴(legacy 프로필,
      기존 렌더와 같은 결과). 기본 글꼴에 없는 글자만 폴백 글꼴(WenQuanYi Zen Hei)로 그린다(기준선·크기 맞춤).
"""
import argparse
import datetime as _dt
import glob
import hashlib
import json
import math
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

# ---------- 토큰 (design-system.md §1, 값 변경 금지) ----------
TOKENS = {
    "red": "#C8102E",
    "yellow": "#FFD23F",
    "ink": "#111111",
    "paper": "#F7F3EA",
    "night": "#1B1F2A",
    "white": "#FFFFFF",
    "kraft": "#C9A877",   # 일러스트 보조(면적 15% 이하)
    "celadon": "#6FA89B",  # 일러스트 보조
    "wheat": "#F2D49B",    # 일러스트 보조
}
W, H = 1080, 1350
MARGIN = 72                      # 안전 영역(사방)
GRID_TOP, GRID_BOTTOM = 135, 1215  # 프로필 1:1 크롭 범위(헤드라인은 이 안에)
HANDLE = "@chaekgado.note"
ACCOUNT = "책가도 노트"
MOCKUP_TAG = "MOCKUP"
AI_NOTICE = "이미지·초안은 AI로 생성, 사실 확인은 사람이 했습니다"  # legal v3 통과 문구. 바꾸려면 legal 재검토
FINAL = False  # --final: 게시용 렌더(MOCKUP 표기 생략, RENDER.json에 mode=final 기록). approved 전에는 쓰지 않는다 (COO 2026-10-02)
RENDERER_VERSION = "v2.0 (2026-10-02)"

# 타이포 크기(px). 헤드라인 >=72, 본문 >=40 (폰 가독)
SIZE = {
    "cover_head": 128, "cover_sub": 44, "cover_handle": 40,
    "body_head": 88, "body_text": 44, "body_num": 40,
    "last_cta": 84, "last_src": 40, "last_handle": 40,
    "label": 34, "mockup": 30,
    "credit": 26,  # v2 사진 크레딧(출처 표기 전용 예외, DESIGN-v2 §4)
}

# 행간·자간(프로필별). legacy = v1 값 그대로(기존 렌더와 같은 픽셀). v2 = 진짜 글꼴에 맞춘 값(DESIGN-v2 §2)
SPACING = {
    "legacy": {"cover_head_lh": 1.15, "cover_sub_lh": 1.3, "body_head_lh": 1.15, "body_lh": 1.4, "check_lh": 1.3,
               "last_cta_lh": 1.15, "src_lh": 1.35, "head_track": 0.0, "body_track": 0.0},
    "v2": {"cover_head_lh": 1.15, "cover_sub_lh": 1.45, "body_head_lh": 1.15, "body_lh": 1.5, "check_lh": 1.4,
           "last_cta_lh": 1.15, "src_lh": 1.45, "head_track": -0.02, "body_track": -0.01},
}
PROFILE = "legacy"
USE_BUNDLED = True
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
FONT_CONFIG = os.path.join(FONT_DIR, "fonts.json")  # 역할별 글꼴 체인·행간·자간·라이선스. --fonts 로 교체
FONT_LICENSES = {  # 시스템 글꼴 패밀리 -> 라이선스(렌더 로그용). 동봉 글꼴은 fonts.json files 가 우선
    "Black Han Sans": "OFL-1.1",
    "Pretendard": "OFL-1.1",
    "WenQuanYi Zen Hei": "GPL-2.0 + font embedding exception (Debian fonts-wqy-zenhei)",
    "Liberation Sans": "OFL-1.1 (Debian fonts-liberation)",
    "DejaVu Sans": "Bitstream Vera + DejaVu public domain changes",
    "Noto Sans CJK": "OFL-1.1",
}
FONT_FILES_META = {}  # 동봉 글꼴 경로 -> fonts.json files 항목(라이선스·출처·sha256)


def sp(key):
    return SPACING[PROFILE][key]


# ---------- 폰트 탐색 ----------
def _fc_list():
    try:
        out = subprocess.run(["fc-list", ":", "file", "family", "style"],
                             capture_output=True, text=True, timeout=10).stdout
    except Exception:
        return []
    rows = []
    for line in out.splitlines():
        parts = line.split(":")
        if len(parts) >= 2:
            rows.append((parts[0].strip(), parts[1].strip(), ":".join(parts[2:]).strip()))
    return rows


_FC = None


def find_font(candidates):
    """candidates: [(family_substring, style_substring_or_None), ...] -> path or None"""
    global _FC
    if _FC is None:
        _FC = _fc_list()
    for fam, style in candidates:
        for path, family, st in _FC:
            st_l = st.lower()
            if fam.lower() in family.lower() and (style is None or (style.lower() in st_l and "italic" not in st_l)):
                return path
        # fc-list가 없을 때 흔한 경로 글롭
        for pat in [f"/usr/share/fonts/**/*{fam.replace(' ', '')}*", f"{os.path.expanduser('~')}/.fonts/**/*{fam.replace(' ', '')}*"]:
            hits = sorted(glob.glob(pat, recursive=True))
            if hits:
                return hits[0]
    return None


class FontConfigError(Exception):
    """fonts.json 의 동봉 글꼴에 라이선스 기록이 없거나 파일이 바뀜(--final 에서는 렌더 거부)."""


def _resolve_font_entry(entry, base_dir):
    """'파일명'(설정 폴더 기준) 또는 'system:패밀리[:스타일]' -> 경로 또는 None."""
    if entry.startswith("system:"):
        parts = entry.split(":")
        return find_font([(parts[1], parts[2] if len(parts) > 2 and parts[2] else None)])
    p = entry if os.path.isabs(entry) else os.path.join(base_dir, entry)
    return p if os.path.isfile(p) else None


def load_font_config(path):
    """fonts.json -> (chains{role: [paths]}, spacing, problems[]). 기본 글꼴(체인 첫 항목)이 없으면 None."""
    if not path or not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fp:
        cfg = json.load(fp)
    base = os.path.dirname(os.path.abspath(path))
    chains, problems = {}, []
    for role in ("head", "body", "bold", "latin"):
        entries = cfg.get("roles", {}).get(role) or cfg.get("roles", {}).get("body", [])
        paths = [p for p in (_resolve_font_entry(e, base) for e in entries) if p]
        if not paths:
            return None
        if role != "latin" and _resolve_font_entry(entries[0], base) is None:
            return None  # 의도한 기본 글꼴이 없으면 이 설정을 쓰지 않는다
        chains[role] = list(dict.fromkeys(paths))
    files = cfg.get("files", {})
    for role, paths in chains.items():
        for p in paths:
            if not os.path.abspath(p).startswith(base + os.sep):
                continue  # 시스템 글꼴
            meta = files.get(os.path.basename(p))
            if not meta or not meta.get("license"):
                problems.append(f"{os.path.basename(p)}: fonts.json files 에 license 기록 없음")
                continue
            lf = meta.get("license_file")
            if not lf or not os.path.isfile(os.path.join(base, lf)):
                problems.append(f"{os.path.basename(p)}: 라이선스 파일 {lf} 없음")
            if meta.get("sha256"):
                with open(p, "rb") as fp:
                    if hashlib.sha256(fp.read()).hexdigest() != meta["sha256"]:
                        problems.append(f"{os.path.basename(p)}: sha256 불일치(파일이 바뀜, OFL 수정본은 이름 변경 의무)")
            FONT_FILES_META[os.path.abspath(p)] = dict(meta, config=os.path.relpath(path, base))
    spacing = dict(SPACING["v2"], **cfg.get("spacing", {}))
    return {"chains": chains, "spacing": spacing, "problems": problems, "name": cfg.get("name", ""),
            "fake_bold": bool(cfg.get("fake_bold", False)), "path": path}


def load_fonts():
    """동봉 글꼴 설정(cardnews/design/fonts/fonts.json) 우선 -> 'v2' 레이아웃. 없으면 legacy(v1 탐색 순서 그대로)."""
    global PROFILE
    latin_path = find_font([("Liberation Sans", "Bold"), ("DejaVu Sans", "Bold")])
    cfg = load_font_config(FONT_CONFIG) if USE_BUNDLED else None
    if cfg:
        PROFILE = "v2"
        SPACING["v2"] = cfg["spacing"]
        for prob in cfg["problems"]:
            print("  font warn:", prob, file=sys.stderr)
        if cfg["problems"] and FINAL:
            raise FontConfigError("; ".join(cfg["problems"]))
        ch = cfg["chains"]
        return {"head": ch["head"][0], "body": ch["body"][0], "latin": ch["latin"][0], "fake_bold": cfg["fake_bold"],
                "bold": ch["bold"][0], "black": ch["head"][1] if len(ch["head"]) > 1 else ch["head"][0],
                "fallback": ch["body"][-1] if len(ch["body"]) > 1 else None, "profile": "v2",
                "chains": ch, "config": os.path.relpath(cfg["path"], os.path.dirname(FONT_DIR)), "config_name": cfg["name"],
                "config_problems": cfg["problems"]}
    PROFILE = "legacy"
    head_path = find_font([("Black Han Sans", None), ("Pretendard", "Black"), ("Pretendard", "Bold"),
                           ("WenQuanYi Zen Hei", None), ("Noto Sans CJK KR", "Bold"), ("Noto Sans CJK", None)])
    body_path = find_font([("Pretendard", "Regular"), ("Pretendard", None),
                           ("WenQuanYi Zen Hei", None), ("Noto Sans CJK KR", None), ("Noto Sans CJK", None)])
    if head_path is None:
        head_path = latin_path or "DejaVuSans.ttf"
    if body_path is None:
        body_path = head_path
    # 진짜 굵은 글꼴(Black Han Sans·Pretendard)이면 가짜 볼드(획 보강)를 끈다
    fake_bold = "BlackHanSans" not in head_path.replace(" ", "") and "Pretendard" not in head_path
    return {"head": head_path, "body": body_path, "latin": latin_path or head_path, "fake_bold": fake_bold,
            "bold": body_path, "black": head_path, "fallback": None, "profile": "legacy"}


_FONT_CACHE = {}


def font(path, size):
    key = (path, size)
    if key not in _FONT_CACHE:
        try:
            _FONT_CACHE[key] = ImageFont.truetype(path, size)
        except Exception:
            _FONT_CACHE[key] = ImageFont.load_default(size)
    return _FONT_CACHE[key]


# ---------- 글자 단위 폴백 (fontTools cmap) ----------
_CMAP_CACHE = {}
GLYPHS = {"chars": 0, "fallback": {}, "tofu": {}}  # 게시물 단위 집계(render_post가 초기화)


def font_cmap(path):
    """글꼴의 유니코드 cmap(set). fontTools가 없거나 읽기 실패면 None(= 검사 불가, 기본 글꼴로 그림)."""
    if path not in _CMAP_CACHE:
        try:
            from fontTools.ttLib import TTCollection, TTFont
            if str(path).lower().endswith((".ttc", ".otc")):
                tt = TTCollection(path).fonts[0]
            else:
                tt = TTFont(path, lazy=True)
            _CMAP_CACHE[path] = set(tt.getBestCmap().keys())
        except Exception:
            _CMAP_CACHE[path] = None
    return _CMAP_CACHE[path]


def font_info(path):
    """렌더 로그용: 패밀리·스타일·버전·라이선스·sha256."""
    if not path:
        return None
    info = {"path": str(path)}
    try:
        from fontTools.ttLib import TTCollection, TTFont
        tt = TTCollection(path).fonts[0] if str(path).lower().endswith(".ttc") else TTFont(path, lazy=True)
        nm = tt["name"]
        info.update({"family": nm.getDebugName(1), "style": nm.getDebugName(2), "version": nm.getDebugName(5)})
    except Exception:
        pass
    fam = info.get("family") or ""
    meta = FONT_FILES_META.get(os.path.abspath(str(path)))
    if meta:
        info.update({"bundled": True, "license": meta.get("license"), "license_file": meta.get("license_file"),
                     "source": meta.get("source")})
    else:
        info["license"] = next((v for k, v in FONT_LICENSES.items() if k.lower() in fam.lower()), "unknown")
    try:
        with open(path, "rb") as fp:
            info["sha256"] = hashlib.sha256(fp.read()).hexdigest()
    except Exception:
        pass
    return info


_SCALE_CACHE = {}


def _ref_height(path, ref="한"):
    f = font(path, 200)
    l, t, r, b = f.getbbox(ref, anchor="ls")
    return max(1, -t)


def fallback_scale(primary, fb):
    """폴백 글꼴 크기 보정: 기준 글자 '한'의 잉크 높이를 기본 글꼴에 맞춘다."""
    key = (primary, fb)
    if key not in _SCALE_CACHE:
        try:
            s = _ref_height(primary) / _ref_height(fb)
            _SCALE_CACHE[key] = min(1.25, max(0.8, s))
        except Exception:
            _SCALE_CACHE[key] = 1.0
    return _SCALE_CACHE[key]


class TStyle:
    """글꼴 체인 + 크기 + 자간(em). paths[0] = 기본 글꼴, 나머지 = 글자 단위 폴백(체인 순서대로)."""

    def __init__(self, paths, size, track=0.0):
        self.paths = [p for p in paths if p]
        self.size = size
        self.track = track
        self.fonts = [font(self.paths[0], size)] + [
            font(p, max(1, round(size * fallback_scale(self.paths[0], p)))) for p in self.paths[1:]]
        self.cmaps = [font_cmap(p) for p in self.paths]

    @property
    def primary(self):
        return self.fonts[0]

    def which(self, ch):
        for i, cm in enumerate(self.cmaps):
            if cm is None or ord(ch) in cm:
                return i
        return -1  # 어느 글꼴에도 없음 = 두부

    def runs(self, s, record=False):
        out = []
        for ch in s:
            i = self.which(ch)
            if record and ch not in "\n":
                GLYPHS["chars"] += 1
                if i == -1:
                    GLYPHS["tofu"][ch] = GLYPHS["tofu"].get(ch, 0) + 1
                elif i > 0:
                    name = os.path.basename(self.paths[i])
                    GLYPHS["fallback"].setdefault(ch, name)
            i = max(i, 0)
            if out and out[-1][0] == i:
                out[-1][1] += ch
            else:
                out.append([i, ch])
        return out

    def simple(self, s):
        """기본 글꼴 한 벌로 그려도 되는가(legacy와 같은 경로)."""
        return self.track == 0 and all(i == 0 for i, _ in self.runs(s))

    def pieces(self, s):
        """(font, text, advance) 목록. 자간이 있으면 글자 단위."""
        out = []
        for i, run in self.runs(s):
            f = self.fonts[i]
            if self.track:
                for ch in run:
                    out.append((f, ch, f.getlength(ch) + self.track * self.size))
            else:
                out.append((f, run, f.getlength(run)))
        return out

    def advance(self, s):
        ps = self.pieces(s)
        total = sum(a for _, _, a in ps)
        if self.track and ps:
            total -= self.track * self.size  # 마지막 글자 뒤 자간은 폭에 넣지 않음
        return total

    def ink(self, s):
        """기준선 원점 기준 잉크 상자 (l, t, r, b)."""
        x, box = 0.0, None
        for f, t, a in self.pieces(s):
            l, tt, r, b = f.getbbox(t, anchor="ls")
            cur = (x + l, tt, x + r, b)
            box = cur if box is None else (min(box[0], cur[0]), min(box[1], cur[1]), max(box[2], cur[2]), max(box[3], cur[3]))
            x += a
        return box or (0, 0, 0, 0)


def style(fonts, role, size):
    """역할별 글꼴 체인(fonts.json roles). 예: head = Black Han Sans -> Pretendard Black -> WenQuanYi. legacy = 한 벌."""
    if fonts.get("profile") != "v2":
        path = {"head": fonts["head"], "body": fonts["body"], "bold": fonts["body"], "latin": fonts["latin"]}[role]
        return TStyle([path], size, 0.0)
    track = {"head": sp("head_track"), "body": sp("body_track")}.get(role, 0.0)
    return TStyle(fonts["chains"][role], size, track)


# ---------- 텍스트 유틸 ----------
def text_w(draw, s, f):
    if isinstance(f, TStyle):
        if f.simple(s):
            f = f.primary
        else:
            return int(round(f.advance(s)))
    l, t, r, b = draw.textbbox((0, 0), s, font=f)
    return r - l


def put_text(d, xy, s, st, fill, anchor=None, stroke=0, stroke_fill=None):
    """글자 단위 폴백을 지원하는 draw.text. 기본 글꼴 한 벌이면 기존 draw.text 와 같은 호출."""
    if not isinstance(st, TStyle):
        d.text(xy, s, font=st, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=stroke_fill or fill)
        return
    st.runs(s, record=True)
    if st.simple(s):
        d.text(xy, s, font=st.primary, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=stroke_fill or fill)
        return
    anchor = anchor or "la"
    x, y = xy
    asc, desc = st.primary.getmetrics()
    total = st.advance(s)
    x0 = x - {"l": 0, "m": total / 2, "r": total}[anchor[0]]
    base = y + {"a": asc, "m": (asc - desc) / 2, "s": 0, "d": -desc}.get(anchor[1], asc)
    for f, t, a in st.pieces(s):
        d.text((x0, base), t, font=f, fill=fill, anchor="ls", stroke_width=stroke, stroke_fill=stroke_fill or fill)
        x0 += a


def ref_extent(st):
    """줄 하나의 시각 높이 기준(글자 '한'의 잉크 위·아래, 기준선 원점). 줄마다 내용이 달라도 블록 높이가 일정."""
    l, t, r, b = st.primary.getbbox("한", anchor="ls")
    return t, b


def lines_baselines(st, n, lh, top, bottom):
    """n줄을 [top, bottom] 안에 잉크 기준으로 세로 가운데 정렬한 기준선 y 목록(v2)."""
    t, b = ref_extent(st)
    span = (n - 1) * lh + (b - t)
    y_first = top + ((bottom - top) - span) / 2 - t
    return [y_first + i * lh for i in range(n)]


def put_text_in_box(d, box, s, st, fill, align="center", pad=0):
    """상자 안에 잉크 기준 세로 가운데로 한 줄(v2: 알약·표 칸·크레딧)."""
    x0, y0, x1, y1 = box
    t, b = ref_extent(st)
    base = y0 + ((y1 - y0) - (b - t)) / 2 - t
    if align == "center":
        put_text(d, ((x0 + x1) / 2, base), s, st, fill, anchor="ms")
    elif align == "right":
        put_text(d, (x1 - pad, base), s, st, fill, anchor="rs")
    else:
        put_text(d, (x0 + pad, base), s, st, fill, anchor="ls")


# v2 줄 끝 금칙: 혼자 떨어진 이 기호는 다음 단어에 붙여 같은 줄로 보낸다(줄 끝 "→"·"□" 방지, 글자는 그대로)
NO_LINE_END = {"→", "□", "☑", "·", "(", "『", "「", "①", "②", "③", "④", "⑤"}


def _units(para):
    words = para.split(" ")
    if PROFILE != "v2":
        return words
    out, carry = [], None
    for i, w in enumerate(words):
        if carry is not None:
            w = carry + " " + w
            carry = None
        if w in NO_LINE_END and i < len(words) - 1:
            carry = w
            continue
        out.append(w)
    if carry is not None:
        out.append(carry)
    return out


def wrap(draw, text, f, maxw):
    """공백 우선, 길면 글자 단위로 줄바꿈. 명시적 \n 유지."""
    lines = []
    for para in text.split("\n"):
        cur = ""
        for word in _units(para):
            cand = word if not cur else cur + " " + word
            if text_w(draw, cand, f) <= maxw:
                cur = cand
                continue
            if cur:
                lines.append(cur)
            cur = ""
            for ch in word:
                if text_w(draw, cur + ch, f) <= maxw:
                    cur += ch
                else:
                    lines.append(cur)
                    cur = ch
        lines.append(cur)
    return lines


# 잘림 경고: 줄 상한·항목 상한으로 글자가 소리 없이 빠지는 곳을 전부 기록(risk-C1-1 #16·#17 재발 방지)
NOTES = []  # 장 단위 경고(render_post가 장마다 비움)


def clip(lines, k, what):
    lines = [ln for ln in lines]
    if len(lines) > k:
        dropped = " / ".join(lines[k:])
        NOTES.append(f"잘림: {what} {len(lines)}줄 > 상한 {k}줄, 빠진 부분 '{dropped}'")
    return lines[:k]


def draw_lines(draw, lines, f, x, y, fill, line_gap=1.18, stroke=0, anchor_center=False):
    size = f.size
    for ln in lines:
        if anchor_center:
            put_text(draw, (W // 2, y), ln, f, fill, anchor="ma", stroke=stroke)
        else:
            put_text(draw, (x, y), ln, f, fill, stroke=stroke)
        y += int(size * line_gap)
    return y


# ---------- 배경: paper + 한지 결 ----------
def hanji_background(seed=7):
    bg = Image.new("RGB", (W, H), TOKENS["paper"])
    # 결을 5단계로 포스터라이즈 -> 색 수가 적어 PNG 용량이 작다(장당 ~250KB)
    noise = Image.effect_noise((W, H), 30).filter(ImageFilter.GaussianBlur(1.8))
    fiber = Image.effect_noise((W // 8, H), 60).resize((W, H), Image.BILINEAR)  # 세로 결
    grain = Image.blend(noise, fiber, 0.35).point(lambda v: (v // 52) * 52).convert("RGB")
    return Image.blend(bg, grain, 0.09)


# ---------- 플랫 모티프(글자 없음) ----------
def motif_bookshelf(layer, box, accent):
    """책가도 책장 격자: 칸 + 책 묶음(단색 직사각형)."""
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    cols, rows = 4, 2
    cw, rh = (x1 - x0) / cols, (y1 - y0) / rows
    d.rectangle(box, outline=TOKENS["ink"], width=6)
    for c in range(1, cols):
        d.line([(x0 + c * cw, y0), (x0 + c * cw, y1)], fill=TOKENS["ink"], width=6)
    for r in range(1, rows):
        d.line([(x0, y0 + r * rh), (x1, y0 + r * rh)], fill=TOKENS["ink"], width=6)
    palette = [TOKENS["kraft"], accent, TOKENS["celadon"], TOKENS["wheat"], TOKENS["night"]]
    k = 0
    for r in range(rows):
        for c in range(cols):
            cx0, cy1 = x0 + c * cw + 18, y0 + (r + 1) * rh - 10
            # 눕힌 책 3~4권 쌓기
            n = 3 + (c + r) % 2
            bh = (rh - 40) / 4
            for i in range(n):
                col = palette[(k + i) % len(palette)]
                bw = cw - 36 - (i * 11 % 40)
                d.rectangle([cx0 + (i * 7 % 20), cy1 - (i + 1) * bh, cx0 + bw, cy1 - i * bh - 6],
                            fill=col, outline=TOKENS["ink"], width=4)
            k += 1


def motif_dancheong(layer, box, accent):
    """단청 띠: 반복 사각 + 반원 패턴."""
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    band_h = min(120, y1 - y0)
    yb = y0 + (y1 - y0 - band_h) // 2
    d.rectangle([x0, yb, x1, yb + band_h], fill=TOKENS["night"], outline=TOKENS["ink"], width=6)
    step = 90
    x = x0 + 20
    i = 0
    while x + step <= x1 - 20:
        col = [accent, TOKENS["celadon"], TOKENS["wheat"]][i % 3]
        d.pieslice([x, yb + 14, x + step - 20, yb + band_h - 14 + (step - 20 - band_h + 28)],
                   180, 360, fill=col, outline=TOKENS["ink"], width=3)
        d.rectangle([x + 20, yb + band_h - 38, x + step - 40, yb + band_h - 14], fill=TOKENS["paper"], outline=TOKENS["ink"], width=3)
        x += step
        i += 1


def motif_moon_mountain(layer, box, accent):
    """십장생풍 달·산 실루엣(동물 없음)."""
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    r = (y1 - y0) // 3
    cx = x1 - r - 40
    d.ellipse([cx - r, y0, cx + r, y0 + 2 * r], fill=accent, outline=TOKENS["ink"], width=6)
    wdt = x1 - x0
    peaks = [(x0, y1), (x0 + wdt * 0.18, y0 + (y1 - y0) * 0.45), (x0 + wdt * 0.36, y1 - 60),
             (x0 + wdt * 0.55, y0 + (y1 - y0) * 0.3), (x0 + wdt * 0.78, y1 - 40), (x1, y0 + (y1 - y0) * 0.6), (x1, y1)]
    d.polygon(peaks, fill=TOKENS["night"], outline=TOKENS["ink"])
    peaks2 = [(x0, y1), (x0 + wdt * 0.3, y0 + (y1 - y0) * 0.65), (x0 + wdt * 0.6, y1 - 20),
              (x0 + wdt * 0.85, y0 + (y1 - y0) * 0.72), (x1, y1)]
    d.polygon(peaks2, fill=TOKENS["celadon"], outline=TOKENS["ink"])


def motif_peony(layer, box, accent):
    """모란(민화 꽃) 단순 도형: 원 겹침 + 잎."""
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    R = min(x1 - x0, y1 - y0) // 2 - 10
    for i in range(6):
        a = math.pi * 2 * i / 6
        px, py = cx + math.cos(a) * R * 0.45, cy + math.sin(a) * R * 0.45
        d.ellipse([px - R * 0.42, py - R * 0.42, px + R * 0.42, py + R * 0.42], fill=accent, outline=TOKENS["ink"], width=5)
    d.ellipse([cx - R * 0.3, cy - R * 0.3, cx + R * 0.3, cy + R * 0.3], fill=TOKENS["yellow"] if accent != TOKENS["yellow"] else TOKENS["red"], outline=TOKENS["ink"], width=5)
    for sx in (-1, 1):
        d.polygon([(cx + sx * R * 0.6, cy + R * 0.7), (cx + sx * R * 1.0, cy + R * 0.95), (cx + sx * R * 0.5, cy + R * 1.0)],
                  fill=TOKENS["celadon"], outline=TOKENS["ink"])


def motif_hanji(layer, box, accent):
    """한지 결: 가로 결 띠 + 작은 사각 도장(글자 없음)."""
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    for i, y in enumerate(range(y0 + 10, y1 - 10, 34)):
        d.line([(x0, y), (x1, y)], fill=TOKENS["kraft"] if i % 2 else TOKENS["wheat"], width=10)
    s = 110
    d.rectangle([x1 - s - 20, y1 - s - 20, x1 - 20, y1 - 20], fill=accent, outline=TOKENS["ink"], width=6)
    d.rectangle([x1 - s + 10, y1 - s + 10, x1 - 50, y1 - 50], outline=TOKENS["paper"], width=6)


BANNED_MOTIF_WORDS = ["호랑이", "까치", "tiger", "magpie", "캐릭터", "로고", "logo", "얼굴", "배우", "아이돌", "드라마", "still"]


def pick_motif(visual: str):
    """visual 문자열 -> (모티프 함수, 경고). 디자인 시스템 §6-3(호랑이·까치 조수 모티프 금지)에 걸리면 달·산으로 대체."""
    v = (visual or "").lower()
    warn = None
    # "로고 금지", "얼굴 없음"처럼 금지·부정 맥락의 언급은 소재가 아니라 제약이므로 매칭에서 뺀다 (COO 2026-10-02)
    v_pos = " ".join(c for c in re.split(r"[.,\n]", v) if not re.search(r"금지|없음|없는|없이|제외|않음", c))
    if any(w in v_pos for w in BANNED_MOTIF_WORDS):
        warn = f"visual '{visual}' 에 금지 소재(인물/로고/IP 또는 호랑이·까치) 포함 -> 달·산 모티프로 대체"
        return motif_moon_mountain, warn
    if any(w in v for w in ["책가도", "책장", "책", "chaekgado", "bookshelf", "book"]):
        return motif_bookshelf, warn
    if any(w in v for w in ["단청", "dancheong", "띠", "처마"]):
        return motif_dancheong, warn
    if any(w in v for w in ["달", "산", "moon", "mountain", "십장생"]):
        return motif_moon_mountain, warn
    if any(w in v for w in ["꽃", "모란", "peony", "화조"]):
        return motif_peony, warn
    if any(w in v for w in ["한지", "hanji", "결", "도장"]):
        return motif_hanji, warn
    return motif_bookshelf, warn


# ---------- 그림 칸: 사진 > AI 플레이트 > 코드 도형 ----------
class PhotoError(Exception):
    """사진 출처·라이선스 표기가 없거나 상업 이용 불가 -> 렌더 거부."""


PHOTO_EXT = (".jpg", ".jpeg", ".png", ".webp")


def license_status(lic):
    """상업 이용·변경(크롭) 가능 여부. ok / review(legal 확인) / blocked."""
    l = re.sub(r"[\s_\-·.]+", "", str(lic).lower())
    if not l:
        return "blocked"
    if any(k in l for k in ["ccbync", "noncommercial", "비영리", "상업금지", "상업적이용금지", "ccbynd", "noderiv", "변경금지",
                            "editorial", "allrightsreserved", "저작권자허락"]) or re.search(r"(제|type)?[234]유형|kogltype[234]", l):
        return "blocked"
    if re.search(r"공공누리(제)?1유형|kogltype1|(^|[^0-9])1유형", l) or any(k in l for k in [
            "cc0", "publicdomain", "퍼블릭도메인", "pdm", "unsplash", "pexels", "pixabay"]):
        return "ok"
    if "ccbysa" in l or "sharealike" in l:
        return "review"  # 카드가 2차적저작물이면 같은 조건 공개 의무 -> legal 판단
    if re.search(r"ccby(\d|$)", l) or l.startswith("ccby"):
        return "ok"
    return "blocked"  # 확인되지 않은 라이선스는 쓰지 않는다(design-system §6-8)


def load_photos(post_dir, date=None):
    """<post_dir>/photos/PHOTOS.json -> {n: entry}. researcher 목록(C1-1-photos.json)과 같은 필드를 받는다.
    필수: card, credit, license. 파일: file(로컬, photos/ 안) 없으면 card-NN.{jpg,png,...}.
    선택: date, source, source_url, author, license_url, file_url, focus([x,y] 0~1 또는 {"x":..,"y":..})."""
    pdir = os.path.join(post_dir, "photos")
    jpath = os.path.join(pdir, "PHOTOS.json")
    loose = sorted(f for f in glob.glob(os.path.join(pdir, "card-*")) if f.lower().endswith(PHOTO_EXT))
    if not os.path.isfile(jpath):
        if loose:
            raise PhotoError(f"{pdir}: 사진 파일 {len(loose)}개가 있는데 PHOTOS.json 이 없다 -> 렌더 거부(출처 표기 강제)")
        return {}
    with open(jpath, encoding="utf-8") as fp:
        data = json.load(fp)
    entries = data.get("photos", []) if isinstance(data, dict) else data
    out = {}
    for e in entries:
        if date and e.get("date") and str(e["date"]) != str(date):
            continue
        n = int(e.get("card") or e.get("n") or 0)
        if n <= 0:
            raise PhotoError(f"{jpath}: card 번호 없는 항목 {e}")
        credit = str(e.get("credit") or "").strip()
        lic = str(e.get("license") or "").strip()
        if not credit:
            raise PhotoError(f"{jpath}: card {n} credit 없음 -> 렌더 거부(출처 표기 강제)")
        if not lic:
            raise PhotoError(f"{jpath}: card {n} license 없음 -> 렌더 거부")
        st = license_status(lic)
        if st == "blocked":
            raise PhotoError(f"{jpath}: card {n} license '{lic}' 는 상업 이용·변경 가능 목록에 없다 -> 렌더 거부")
        fname = e.get("file")
        if fname:
            path = os.path.join(pdir, os.path.basename(fname))
        else:
            hits = [f for f in loose if os.path.basename(f).lower().startswith(f"card-{n:02d}.")]
            path = hits[0] if hits else None
        if not path or not os.path.isfile(path):
            raise PhotoError(f"{jpath}: card {n} 사진 파일이 없다({fname or f'card-{n:02d}.jpg'}). place_photos.py --download 먼저")
        fx, fy = 0.5, 0.5
        foc = e.get("focus")
        if isinstance(foc, (list, tuple)) and len(foc) == 2:
            fx, fy = float(foc[0]), float(foc[1])
        elif isinstance(foc, dict):
            fx, fy = float(foc.get("x", 0.5)), float(foc.get("y", 0.5))
        rec = dict(e)
        rec.update({"card": n, "path": path, "focus": [min(1, max(0, fx)), min(1, max(0, fy))], "license_status": st})
        out[n] = rec
    for f in loose:
        m = re.match(r"card-(\d+)\.", os.path.basename(f))
        if m and int(m.group(1)) not in out and not any(os.path.basename(r["path"]) == os.path.basename(f) for r in out.values()):
            raise PhotoError(f"{f}: PHOTOS.json 에 출처 항목이 없는 사진 -> 렌더 거부")
    return out


def cover_crop(im, bw, bh, fx=0.5, fy=0.5):
    """비율 유지 확대·축소 후 초점(fx, fy) 기준으로 잘라 bw x bh 를 채운다(늘리기·찌그러뜨리기 없음)."""
    iw, ih = im.size
    sc = max(bw / iw, bh / ih)
    nw, nh = max(bw, math.ceil(iw * sc)), max(bh, math.ceil(ih * sc))
    im = im.resize((nw, nh), Image.LANCZOS)
    left = int(round(min(max(fx * nw - bw / 2, 0), nw - bw)))
    top = int(round(min(max(fy * nh - bh / 2, 0), nh - bh)))
    return im.crop((left, top, left + bw, top + bh)), sc


def photo_layer(entry, box, fonts):
    """사진 칸: 초점 크롭 + 약한 톤 정리(채도 0.94, paper 4%) + 먹 테두리 6px + 오른쪽 아래 크레딧 한 줄."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    im = ImageOps.exif_transpose(Image.open(entry["path"])).convert("RGB")
    src_size = im.size
    im, sc = cover_crop(im, bw, bh, *entry["focus"])
    if sc > 1.5:
        NOTES.append(f"사진 해상도 부족: {os.path.basename(entry['path'])} {src_size[0]}x{src_size[1]} -> {sc:.2f}배 확대")
    im = ImageEnhance.Color(im).enhance(0.94)
    im = Image.blend(im, Image.new("RGB", im.size, TOKENS["paper"]), 0.04)
    layer.paste(im, (x0, y0))
    d = ImageDraw.Draw(layer)
    d.rectangle([x0, y0, x1, y1], outline=TOKENS["ink"], width=6)
    # 크레딧: ink 82% 알약 위 white, 26px Pretendard Bold
    st = style(fonts, "bold", SIZE["credit"])
    credit = entry["credit"]
    tw = text_w(d, credit, st)
    maxw = bw - 2 * 18 - 28
    if tw > maxw:
        NOTES.append(f"잘림: 사진 크레딧 폭 {tw}px > {maxw}px '{credit}'")
    ph = SIZE["credit"] + 16
    px1, py1 = x1 - 14, y1 - 14
    px0, py0 = px1 - tw - 28, py1 - ph
    pill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(pill).rounded_rectangle([px0, py0, px1, py1], radius=ph // 2, fill=(17, 17, 17, 209))
    layer = Image.alpha_composite(layer, pill)
    d = ImageDraw.Draw(layer)
    put_text_in_box(d, (px0, py0, px1, py1), credit, st, TOKENS["white"], align="center")
    return layer


_PLATE_META = {}


def plates_meta(post_dir):
    if post_dir not in _PLATE_META:
        p = os.path.join(post_dir, "plates", "PLATES.json")
        try:
            with open(p, encoding="utf-8") as fp:
                _PLATE_META[post_dir] = json.load(fp)
        except Exception:
            _PLATE_META[post_dir] = None
    return _PLATE_META[post_dir]


SOURCES = {}  # 장별 그림 칸 출처(render_post가 RENDER.json에 기록)


def plate_layer(post_dir, n, visual, box, accent, fonts=None, photos=None, allow_photo=True):
    """그림 칸 레이어. 우선순위: photos/card-NN(+PHOTOS.json) > plates/card-NN.png(AI) > 코드 도형."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if photos and n in photos:
        if allow_photo:
            SOURCES[n] = {"slot": "photo", "file": os.path.basename(photos[n]["path"]),
                          **{k: photos[n].get(k) for k in ["credit", "license", "license_status", "source", "source_url",
                                                            "author", "license_url", "file_url", "focus"] if photos[n].get(k) is not None}}
            if photos[n].get("license_status") == "review":
                NOTES.append(f"사진 라이선스 legal 확인 필요: card {n} '{photos[n].get('license')}'(동일조건변경허락 등)")
            return photo_layer(photos[n], box, fonts), "photo"
        NOTES.append(f"사진 무시: card {n} 은 사진 칸이 없는 장 유형(마지막 장 단청 띠 유지)")
    custom = os.path.join(post_dir, "plates", f"card-{n:02d}.png")
    if not allow_photo and PROFILE == "v2":
        # 마지막 장 = 템플릿 §4-3 단청 띠 고정(세트마다 같은 끝맺음, AI 생성·사진 없음)
        motif_dancheong(layer, box, accent)
        SOURCES[n] = {"slot": "code", "motif": "motif_dancheong"}
        return layer, None
    if os.path.exists(custom):
        im = Image.open(custom).convert("RGBA")
        bw, bh = box[2] - box[0], box[3] - box[1]
        if PROFILE == "v2":
            # 비율이 다르면 늘리지 않고 가운데 기준으로 잘라 채운 뒤 먹 테두리(사진 칸과 같은 틀)
            im, _ = cover_crop(im, bw, bh)
            layer.paste(im, (box[0], box[1]), im)
            ImageDraw.Draw(layer).rectangle(list(box), outline=TOKENS["ink"], width=6)
        else:
            im = im.resize((bw, bh), Image.LANCZOS)
            layer.paste(im, (box[0], box[1]), im)
        meta = plates_meta(post_dir) or {}
        card_meta = next((c for c in meta.get("cards", []) if int(c.get("card", 0)) == n), {})
        SOURCES[n] = {"slot": "ai_plate", "file": f"plates/card-{n:02d}.png",
                      **{k: meta.get(k) for k in ["model", "endpoint", "model_license", "terms_url"] if meta.get(k)},
                      **{k: card_meta.get(k) for k in ["seed", "generated_at", "prompt_sha256"] if card_meta.get(k) is not None}}
        return layer, "custom plate"
    fn, warn = pick_motif(visual)
    fn(layer, box, accent)
    SOURCES[n] = {"slot": "code", "motif": fn.__name__}
    return layer, warn


# ---------- 공통 요소 ----------
def signature_bar(d, x, y, w):
    """design-system §3 시그니처: yellow 14px 바 + ink 2px 테두리."""
    d.rectangle([x, y, x + w, y + 14], fill=TOKENS["yellow"], outline=TOKENS["ink"], width=2)


def mockup_tag(img, fonts):
    if FINAL:
        return
    d = ImageDraw.Draw(img)
    f = font(fonts["latin"], SIZE["mockup"])
    tw = text_w(d, MOCKUP_TAG, f)
    x, y = W - MARGIN - tw - 24, H - 52 - 24
    d.rounded_rectangle([x - 14, y - 6, x + tw + 14, y + SIZE["mockup"] + 10], radius=8, outline=TOKENS["red"], width=3)
    d.text((x, y), MOCKUP_TAG, font=f, fill=TOKENS["red"])


def handle_line(d, fonts, y, size, fill=TOKENS["ink"], center=False):
    st = style(fonts, "body", size)
    if center:
        put_text(d, (W // 2, y), HANDLE, st, fill, anchor="ma")
    else:
        put_text(d, (MARGIN, y), HANDLE, st, fill)


def head_stroke(fonts, size=88):
    """Black Han Sans 부재 시 획 두께 보강(목업). 크기 비례, 48px 미만은 1."""
    if not fonts["fake_bold"]:
        return 0
    return max(1, size // 40)


def label_style(fonts):
    """라벨·알약 글꼴: v2 = Pretendard Bold(색 바탕 위 굵기), legacy = 본문 글꼴."""
    return style(fonts, "bold" if PROFILE == "v2" else "body", SIZE["label"])


# ---------- 장 유형 1: 표지 ----------
def render_cover(post, card, fonts, post_dir, photos=None):
    img = hanji_background()
    n = card.get("n", 1)
    # 그림 칸: 상단(배경 장식, 텍스트 뒤)
    box = (MARGIN, 150, W - MARGIN, 560)
    plate, warn = plate_layer(post_dir, n, card.get("visual", "책가도 책장"), box, TOKENS["red"], fonts, photos)
    img.paste(plate, (0, 0), plate)
    d = ImageDraw.Draw(img)
    # 상단 라벨: 계정명 + 유형
    f_lab = label_style(fonts)
    lab_box = [MARGIN, MARGIN, MARGIN + text_w(d, ACCOUNT, f_lab) + 40, MARGIN + 52]
    d.rounded_rectangle(lab_box, radius=10, fill=TOKENS["ink"])
    if PROFILE == "v2":
        put_text_in_box(d, lab_box, ACCOUNT, f_lab, TOKENS["paper"])
    else:
        put_text(d, (MARGIN + 20, MARGIN + 8), ACCOUNT, f_lab, TOKENS["paper"])
    ptype = post.get("type", "")
    if ptype:
        tw = text_w(d, ptype, f_lab)
        tag_box = [W - MARGIN - tw - 40, MARGIN, W - MARGIN, MARGIN + 52]
        d.rounded_rectangle(tag_box, radius=10, fill=TOKENS["red"])
        if PROFILE == "v2":
            put_text_in_box(d, tag_box, ptype, f_lab, TOKENS["white"])
        else:
            put_text(d, (W - MARGIN - tw - 20, MARGIN + 8), ptype, f_lab, TOKENS["white"])
    # 헤드라인 블록(paper 단색 블록 위, 그리드 크롭 안)
    f_h = style(fonts, "head", SIZE["cover_head"])
    lines = clip(wrap(d, card.get("headline", post.get("title", "")), f_h, W - 2 * MARGIN - 80), 2, "표지 헤드라인")  # 2줄 상한
    lh = int(SIZE["cover_head"] * sp("cover_head_lh"))
    block_h = lh * len(lines) + 70
    y0 = 600
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + block_h], fill=TOKENS["paper"], outline=TOKENS["ink"], width=6)
    if PROFILE == "v2":
        for ln, base in zip(lines, lines_baselines(f_h, len(lines), lh, y0 + 6, y0 + block_h - 6)):
            put_text(d, (MARGIN + 40, base), ln, f_h, TOKENS["ink"], anchor="ls")
    else:
        y = y0 + 36
        for ln in lines:
            put_text(d, (MARGIN + 40, y), ln, f_h, TOKENS["ink"], stroke=head_stroke(fonts, SIZE["cover_head"]), stroke_fill=TOKENS["ink"])
            y += lh
    signature_bar(d, MARGIN + 40, y0 + block_h + 24, 320)
    # 부제
    f_s = style(fonts, "body", SIZE["cover_sub"])
    sub = card.get("body", "")
    ys = y0 + block_h + 70
    for ln in clip(wrap(d, sub, f_s, W - 2 * MARGIN - 40), 2, "표지 부제"):
        put_text(d, (MARGIN + 40, ys), ln, f_s, TOKENS["ink"])
        ys += int(SIZE["cover_sub"] * sp("cover_sub_lh"))
    if ys > H - MARGIN - 50:
        NOTES.append(f"잘림: 표지 부제가 핸들 줄(y {H - MARGIN - 50})과 겹침 (y {ys})")
    # 핸들 + 넘김 힌트(화살표 대신 점 3개)
    handle_line(d, fonts, H - MARGIN - 50, SIZE["cover_handle"])
    for i in range(3):
        d.ellipse([W // 2 - 40 + i * 32, H - MARGIN - 36, W // 2 - 40 + i * 32 + 16, H - MARGIN - 20], fill=TOKENS["ink"])
    return img, warn


# ---------- 장 유형 2: 본문 (기본 / 체크리스트 / 비교표) ----------
def _body_header(d, fonts, card, total):
    n = card.get("n", 0)
    s = f"{n}/{total}"
    if PROFILE == "v2":
        f_n = style(fonts, "bold", SIZE["body_num"])
        tw = text_w(d, s, f_n)
        pill = [MARGIN, MARGIN, MARGIN + tw + 44, MARGIN + 60]
        d.rounded_rectangle(pill, radius=30, fill=TOKENS["yellow"], outline=TOKENS["ink"], width=3)
        put_text_in_box(d, pill, s, f_n, TOKENS["ink"])
        f_lab = label_style(fonts)
        put_text_in_box(d, (MARGIN, MARGIN, W - MARGIN, MARGIN + 60), ACCOUNT, f_lab, TOKENS["ink"], align="right")
    else:
        f_n = font(fonts["latin"], SIZE["body_num"])
        tw = text_w(d, s, f_n)
        d.rounded_rectangle([MARGIN, MARGIN, MARGIN + tw + 44, MARGIN + 60], radius=30, fill=TOKENS["yellow"], outline=TOKENS["ink"], width=3)
        d.text((MARGIN + 22, MARGIN + 9), s, font=f_n, fill=TOKENS["ink"])
        f_lab = style(fonts, "body", SIZE["label"])
        put_text(d, (W - MARGIN, MARGIN + 12), ACCOUNT, f_lab, TOKENS["ink"], anchor="ra")
    # 헤드라인
    f_h = style(fonts, "head", SIZE["body_head"])
    lines = clip(wrap(d, card.get("headline", ""), f_h, W - 2 * MARGIN), 2, "본문 헤드라인")
    y = 200
    for ln in lines:
        put_text(d, (MARGIN, y), ln, f_h, TOKENS["ink"], stroke=head_stroke(fonts, SIZE["body_head"]), stroke_fill=TOKENS["ink"])
        y += int(SIZE["body_head"] * sp("body_head_lh"))
    signature_bar(d, MARGIN, y + 10, 200)
    return y + 60


def render_body(post, card, fonts, post_dir, total, photos=None):
    img = hanji_background()
    d = ImageDraw.Draw(img)
    y = _body_header(d, fonts, card, total)
    layout = card.get("layout") or ("checklist" if post.get("type") == "체크리스트" and ("\n" in card.get("body", "") or "·" in card.get("body", "")) else "body")
    if card.get("table"):
        layout = "table"
    f_b = style(fonts, "body", SIZE["body_text"])
    if layout == "checklist":
        items = [s.strip() for s in card.get("body", "").replace("·", "\n").split("\n") if s.strip()]
        items = clip(items, 4, "체크리스트 항목")
        for it in items:
            d.rectangle([MARGIN, y + 6, MARGIN + 40, y + 46], fill=TOKENS["yellow"], outline=TOKENS["ink"], width=3)
            d.line([(MARGIN + 9, y + 26), (MARGIN + 18, y + 36), (MARGIN + 33, y + 14)], fill=TOKENS["ink"], width=5)
            lines = clip(wrap(d, it, f_b, W - 2 * MARGIN - 64), 2, "체크리스트 항목 줄")
            yy = y
            for ln in lines:
                put_text(d, (MARGIN + 64, yy), ln, f_b, TOKENS["ink"])
                yy += int(SIZE["body_text"] * sp("check_lh"))
            y = yy + 18
    elif layout == "table":
        rows = clip(card["table"], 4, "비교표 행")
        colw = (W - 2 * MARGIN) // 2
        rh = 92
        for i, row in enumerate(rows):
            for j in range(2):
                x0 = MARGIN + j * colw
                fill = TOKENS["red"] if i == 0 and j == 0 else TOKENS["night"] if i == 0 else TOKENS["paper"]
                d.rectangle([x0, y, x0 + colw, y + rh], fill=fill, outline=TOKENS["ink"], width=4)
                txt = str(row[j]) if j < len(row) else ""
                col = TOKENS["white"] if i == 0 else TOKENS["ink"]
                ln = clip(wrap(d, txt, f_b, colw - 32), 1, "비교표 칸")[0]
                if PROFILE == "v2":
                    put_text_in_box(d, (x0, y, x0 + colw, y + rh), ln, f_b, col)
                else:
                    put_text(d, (x0 + colw // 2, y + rh // 2), ln, f_b, col, anchor="mm")
            y += rh
        y += 24
    else:
        lines = clip(wrap(d, card.get("body", ""), f_b, W - 2 * MARGIN), 3, "본문")
        for ln in lines:
            put_text(d, (MARGIN, y), ln, f_b, TOKENS["ink"])
            y += int(SIZE["body_text"] * sp("body_lh"))
    # 그림 칸(아래쪽, 사진·플레이트 교체 지점)
    top = max(y + 40, 760)
    box = (MARGIN, top, W - MARGIN, H - MARGIN - 110)
    if box[3] - box[1] < 160:
        NOTES.append(f"잘림: 그림 칸 높이 {box[3] - box[1]}px (<160, 본문이 길어 칸이 눌림)")
    plate, warn = plate_layer(post_dir, card.get("n", 0), card.get("visual", ""), box, TOKENS["red"], fonts, photos)
    img.paste(plate, (0, 0), plate)
    d = ImageDraw.Draw(img)
    handle_line(d, fonts, H - MARGIN - 50, SIZE["label"])
    return img, warn


# ---------- 장 유형 3: 출처·CTA ----------
def render_last(post, card, fonts, post_dir, total, photos=None):
    img = hanji_background()
    d = ImageDraw.Draw(img)
    # 상단 단청 띠(플레이트 교체 지점, 사진·AI 생성 안 함)
    box = (MARGIN, MARGIN, W - MARGIN, MARGIN + 160)
    plate, warn = plate_layer(post_dir, card.get("n", total), card.get("visual", "단청 띠"), box, TOKENS["red"], fonts, photos,
                              allow_photo=False)
    img.paste(plate, (0, 0), plate)
    d = ImageDraw.Draw(img)
    # CTA (red 블록 위 white, 대비 5.9)
    cta = card.get("headline") or "저장해 두고 다시 보기"
    f_c = style(fonts, "head", SIZE["last_cta"])
    lines = clip(wrap(d, cta, f_c, W - 2 * MARGIN - 80), 2, "CTA")
    lh = int(SIZE["last_cta"] * sp("last_cta_lh"))
    y0 = 320
    bh = lh * len(lines) + 70
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + bh], fill=TOKENS["red"], outline=TOKENS["ink"], width=6)
    if PROFILE == "v2":
        for ln, base in zip(lines, lines_baselines(f_c, len(lines), lh, y0 + 6, y0 + bh - 6)):
            put_text(d, (W // 2, base), ln, f_c, TOKENS["white"], anchor="ms")
    else:
        y = y0 + 36
        for ln in lines:
            put_text(d, (W // 2, y), ln, f_c, TOKENS["white"], anchor="ma", stroke=head_stroke(fonts, SIZE["last_cta"]), stroke_fill=TOKENS["white"])
            y += lh
    signature_bar(d, W // 2 - 160, y0 + bh + 24, 320)
    # 출처 1~2줄
    f_s = style(fonts, "body", SIZE["last_src"])
    ys = y0 + bh + 90
    put_text(d, (MARGIN, ys), "출처", style(fonts, "head", 48), TOKENS["ink"], stroke=head_stroke(fonts, 48), stroke_fill=TOKENS["ink"])
    ys += 70
    # 공개 카드에는 원본 URL을 찍지 않는다(캡션·sources.txt가 담당). 마지막 장 body = 출처 이름 줄 (COO 2026-10-02)
    sources = [card["body"]] if card.get("body") else [s for s in post.get("sources", [])[:2] if not str(s).startswith("http")]
    for src in sources[:2]:
        for ln in clip(wrap(d, str(src), f_s, W - 2 * MARGIN), 2, "출처 줄"):
            put_text(d, (MARGIN, ys), ln, f_s, TOKENS["ink"])
            ys += int(SIZE["last_src"] * sp("src_lh"))
        ys += 10
    # 협찬 슬롯(있을 때만, 상단 광고 표기는 캡션 첫 줄이 담당)
    sponsor = post.get("sponsor_slot") if post.get("render_sponsor_slot") else None  # 내부 기획 정보, 기본 비표시 (COO 2026-10-02)
    if sponsor and sponsor not in ("", "none", "없음"):
        d.rectangle([MARGIN, ys + 20, W - MARGIN, ys + 110], fill=TOKENS["wheat"], outline=TOKENS["ink"], width=4)
        put_text(d, (MARGIN + 24, ys + 44), clip(wrap(d, f"협찬 슬롯: {sponsor}", f_s, W - 2 * MARGIN - 48), 1, "협찬 슬롯")[0], f_s, TOKENS["ink"])
        ys += 130
    if ys > H - MARGIN - 120:
        NOTES.append(f"잘림: 출처 줄이 AI 고지 줄(y {H - MARGIN - 120})과 겹침 (y {ys})")
    # AI 생성물 표시 + 핸들
    f_ai = style(fonts, "body", SIZE["label"])
    if text_w(d, AI_NOTICE, f_ai) > W - 2 * MARGIN:
        NOTES.append("잘림: AI 고지 줄이 안전 영역 폭을 넘음")
    put_text(d, (W // 2, H - MARGIN - 120), AI_NOTICE, f_ai, TOKENS["ink"], anchor="ma")
    handle_line(d, fonts, H - MARGIN - 56, SIZE["last_handle"], center=True)
    return img, warn


# ---------- 저장 ----------
SAVE_RGB = False


def save_png(img, path, rich=False):
    """기본 PNG-8(적응 팔레트 256색, 플랫 디자인이라 손실 거의 없음). --rgb 또는 사진·AI 플레이트가 든 장은 24비트."""
    if SAVE_RGB or rich:
        img.convert("RGB").save(path, optimize=True)
    else:
        img.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(path, optimize=True)


# ---------- 조립 ----------
def render_post(post_dir, fonts, verbose=True, out_dir=None):
    path = os.path.join(post_dir, "cards.json")
    with open(path, encoding="utf-8") as fp:
        post = json.load(fp)
    out_dir = out_dir or post_dir
    os.makedirs(out_dir, exist_ok=True)
    cards = sorted(post.get("cards", []), key=lambda c: c.get("n", 0))
    total = len(cards)
    photos = load_photos(post_dir, post.get("date"))  # 크레딧·라이선스 없으면 PhotoError(렌더 거부)
    GLYPHS.update({"chars": 0, "fallback": {}, "tofu": {}})
    SOURCES.clear()
    _PLATE_META.pop(post_dir, None)
    outputs, warns, truncs = [], [], []
    for i, card in enumerate(cards):
        n = card.get("n", i + 1)
        NOTES.clear()
        if i == 0:
            img, warn = render_cover(post, card, fonts, post_dir, photos)
        elif i == total - 1:
            img, warn = render_last(post, card, fonts, post_dir, total, photos)
        else:
            img, warn = render_body(post, card, fonts, post_dir, total, photos)
        mockup_tag(img, fonts)
        out = os.path.join(out_dir, f"card-{n:02d}.png")
        save_png(img, out, rich=SOURCES.get(n, {}).get("slot") in ("photo", "ai_plate"))
        outputs.append(out)
        if warn and warn not in ("custom plate", "photo"):
            warns.append(f"card-{n:02d}: {warn}")
        for note in NOTES:
            warns.append(f"card-{n:02d}: {note}")
            if note.startswith("잘림"):
                truncs.append(f"card-{n:02d}: {note}")
        # 글자수 규칙 점검(경고만)
        if len(card.get("headline", "")) > 14:
            warns.append(f"card-{n:02d}: headline {len(card['headline'])}자 (>14)")
        if len(card.get("body", "")) > 60:
            warns.append(f"card-{n:02d}: body {len(card['body'])}자 (>60)")
    contact = contact_sheet(outputs, post.get("post_id", os.path.basename(post_dir)), fonts)
    cpath = os.path.join(out_dir, "contact.png")
    contact.save(cpath, optimize=True)
    tofu = sum(GLYPHS["tofu"].values())
    if tofu:
        warns.append(f"두부(글리프 없음) {tofu}자: {''.join(sorted(GLYPHS['tofu']))}")
    if verbose:
        print(f"[{post_dir}] {len(outputs)} cards -> {out_dir}/card-01..{total:02d}.png, contact.png"
              f" | 글자 {GLYPHS['chars']} · 폴백 {len(GLYPHS['fallback'])}종 · 두부 {tofu} · 잘림 {len(truncs)}")
        for w in warns:
            print("  warn:", w)
    chains = fonts.get("chains") or {r: [fonts[r]] for r in ("head", "body", "latin")}
    used = list(dict.fromkeys(p for ps in chains.values() for p in ps))
    log = {"mode": "final" if FINAL else "mockup", "rendered_at": _dt.datetime.utcnow().isoformat() + "Z",
           "fonts": {k: str(v) for k, v in fonts.items() if k in ("head", "body", "latin", "fake_bold", "bold", "fallback", "profile")},
           "cards": total, "renderer": "render_cards.py",
           "renderer_version": RENDERER_VERSION, "profile": fonts.get("profile", "legacy"),
           "font_config": fonts.get("config"), "font_chains": {r: [os.path.basename(p) for p in ps] for r, ps in chains.items()},
           "fonts_detail": {os.path.basename(p): font_info(p) for p in used},
           "glyph_check": {"method": "fontTools cmap, 글자 단위 체인 해석", "chars_drawn": GLYPHS["chars"],
                           "fallback_chars": GLYPHS["fallback"], "tofu": tofu, "tofu_chars": sorted(GLYPHS["tofu"])},
           "truncations": truncs, "warnings": warns,
           "image_slots": {f"card-{k:02d}": v for k, v in sorted(SOURCES.items())},
           "photo_credits": [{"card": k, **{x: v.get(x) for x in ["credit", "license", "source", "author", "source_url"] if v.get(x)}}
                             for k, v in sorted(SOURCES.items()) if v.get("slot") == "photo"]}
    with open(os.path.join(out_dir, "RENDER.json"), "w", encoding="utf-8") as fp:
        json.dump(log, fp, ensure_ascii=False, indent=2)
    return outputs, cpath, warns, {"tofu": tofu, "truncations": len(truncs), "chars": GLYPHS["chars"]}


def contact_sheet(paths, title, fonts, tile=None, per_row=4):
    """장 전체 나열 1장. legacy 타일 320x400, v2 타일 360x450(피드 폭 약 360px 검수, gemini-carousel 검수 규칙)."""
    tile = tile or ((360, 450) if PROFILE == "v2" else (320, 400))
    pad, head = 24, 70
    rows = (len(paths) + per_row - 1) // per_row
    cols = min(per_row, len(paths))
    cw = pad + cols * (tile[0] + pad)
    ch = head + rows * (tile[1] + pad + 30) + pad
    sheet = Image.new("RGB", (cw, ch), TOKENS["night"])
    d = ImageDraw.Draw(sheet)
    tag = MOCKUP_TAG if PROFILE != "v2" or not FINAL else "final"
    d.text((pad, 20), f"{title}  contact ({tile[0]}x{tile[1]} tiles)  {tag}", font=font(fonts["latin"], 28), fill=TOKENS["yellow"])
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB").resize(tile, Image.LANCZOS)
        x = pad + (i % per_row) * (tile[0] + pad)
        y = head + (i // per_row) * (tile[1] + pad + 30)
        sheet.paste(im, (x, y))
        d.text((x, y + tile[1] + 6), os.path.basename(p), font=font(fonts["latin"], 22), fill=TOKENS["white"])
    return sheet


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("post_dir", nargs="?", help="cards.json 이 있는 게시물 폴더")
    ap.add_argument("--all", metavar="POSTS_DIR", help="하위 폴더 중 cards.json 이 있는 것 전부 렌더")
    ap.add_argument("--rgb", action="store_true", help="PNG-24로 저장(기본은 PNG-8 적응 팔레트, 사진·AI 플레이트 장은 자동 24비트)")
    ap.add_argument("--final", action="store_true", help="게시용 렌더: MOCKUP 표기 생략, RENDER.json mode=final (approved 후에만)")
    ap.add_argument("--out", metavar="DIR", help="결과를 DIR/<게시물 폴더명>/ 에 저장(입력 폴더의 PNG·RENDER.json을 덮어쓰지 않음)")
    ap.add_argument("--no-bundled-fonts", action="store_true", help="동봉 글꼴을 쓰지 않음(legacy 프로필, v1과 같은 결과)")
    ap.add_argument("--fonts", metavar="JSON", help="글꼴 설정 파일(기본 cardnews/design/fonts/fonts.json)")
    ap.add_argument("--strict", action="store_true", help="두부·잘림이 1건이라도 있으면 종료 코드 3(검수 자동화용)")
    args = ap.parse_args()
    global SAVE_RGB, FINAL, USE_BUNDLED, FONT_CONFIG
    SAVE_RGB = args.rgb
    FINAL = args.final
    USE_BUNDLED = not args.no_bundled_fonts
    if args.fonts:
        FONT_CONFIG = os.path.abspath(args.fonts)
    try:
        fonts = load_fonts()
    except FontConfigError as e:
        print(f"글꼴 설정 거부(--final): {e}", file=sys.stderr)
        return 2
    print("fonts:", {k: v for k, v in fonts.items()})
    targets = []
    if args.all:
        for d in sorted(glob.glob(os.path.join(args.all, "*"))):
            if os.path.isfile(os.path.join(d, "cards.json")):
                targets.append(d)
    elif args.post_dir:
        targets.append(args.post_dir)
    else:
        ap.error("post_dir 또는 --all 을 지정하세요")
    if not targets:
        print("cards.json 을 가진 폴더가 없습니다"); return 1
    total_warn, tot = 0, {"tofu": 0, "truncations": 0, "chars": 0, "cards": 0}
    for t in targets:
        out = os.path.join(args.out, os.path.basename(os.path.normpath(t))) if args.out else None
        try:
            outs, _, warns, st = render_post(t, fonts, out_dir=out)
        except PhotoError as e:
            print(f"[{t}] 렌더 거부: {e}", file=sys.stderr)
            return 2
        total_warn += len(warns)
        for k in ("tofu", "truncations", "chars"):
            tot[k] += st[k]
        tot["cards"] += len(outs)
    print(f"합계: {len(targets)}세트 {tot['cards']}장 · 그린 글자 {tot['chars']} · 두부 {tot['tofu']} · 잘림 {tot['truncations']} · 경고 {total_warn}")
    if args.strict and (tot["tofu"] or tot["truncations"]):
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
