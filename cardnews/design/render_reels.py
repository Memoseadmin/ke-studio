#!/usr/bin/env python3
"""책가도 노트 릴스(9:16, 무음) 렌더러.

사용:
  python3 cardnews/design/render_reels.py <post_dir> [--final] [--out render/reels]
  python3 cardnews/design/render_reels.py --all cardnews/posts [--final]
  python3 cardnews/design/render_reels.py <post_dir> --check     # 검증만(파일 생성 없음)

입력: <post_dir>/reel.json (스키마는 C1-1b 지시서 고정) + <post_dir>/card-NN.png(1080x1350, render_cards.py --final 결과).
출력:
  <out>/<id>.mp4            1080x1920, 30fps, H.264 High yuv420p BT.709, +faststart, 무음 AAC 트랙 1개 (커밋 금지)
  <out>/manifest.json       성공한 렌더 목록(id 기준 upsert)
  <post_dir>/reel-cover.png    1080x1920 커버(cover 카드 + 훅)
  <post_dir>/reel-preview.png  가로 띠(장면별 중간 프레임 + 엔드카드, 타일 270x480)
  <post_dir>/REEL_RENDER.json  렌더 기록(mode, 길이, 프레임, 오디오 처리, 글꼴, sha256, ffmpeg 버전)
검증(길이 15~30초, 합계 일치 ±0.1초, 카드 존재·규격, 자막 1~2줄·줄당 16자)에 실패하면 어떤 파일도 만들지 않는다.

레이어: 한지 배경(render_cards.hanji_background) -> 카드 PNG 축소 프레임(motion은 이 레이어에만)
        -> 상단 훅(전 구간 고정, head 글꼴) -> 하단 자막 번인(반투명 night 바, body 글꼴) -> 엔드카드 -> MOCKUP.
motion(프레임 고정, 프레임 안의 카드만 움직임, 진폭 5%):
  static | zoom_in(1.00->1.05) | zoom_out(1.05->1.00) | pan_down(1.05배, 카드 위->아래로 시선 이동) | pan_up(아래->위)
전환: 장면 사이 카드 레이어 크로스페이드(--xfade, 기본 0.25초, 0이면 컷). 자막은 경계에서 컷. 마지막 장면->엔드카드는 화면 전체 크로스페이드.
--final: 게시용(MOCKUP 생략, mode=final). approved 전에는 쓰지 않는다. 카드 폴더 RENDER.json이 mode=final이어야 하고 sponsor가 있으면 거부.
render_cards.py는 수정하지 않고 import만 한다(TOKENS, hanji_background, load_fonts, font, head_stroke, signature_bar, save_png).
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_cards as rc  # noqa: E402  (수정 금지 파일, 재사용만)

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DEFAULT_OUT = os.path.join(REPO, "render", "reels")

T = rc.TOKENS
RW, RH = 1080, 1920
FPS = 30
CARD_SRC = (1080, 1350)
HANDLE = rc.HANDLE

# ---------- 인스타 릴스 안전 영역: 이 구역에는 훅·자막 등 핵심 글자를 두지 않는다 ----------
SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT = 220, 380, 120
SAFE_Y0, SAFE_Y1, SAFE_X1 = SAFE_TOP, RH - SAFE_BOTTOM, RW - SAFE_RIGHT   # y 220~1540, x <=960
TEXT_CX, TEXT_MAXW = 540, 840            # 글자 블록은 x=540 가운데 정렬, 폭 840 이하 -> x 120~960

# ---------- 레이아웃(px) ----------
MOCKUP_BOX = {"right": 952, "top": 232, "size": 26}          # 우상단, 안전 영역 안쪽
HOOK_ZONE = (274, 446)                                        # 훅 블록(세로 가운데 정렬)
HOOK_1LINE_SIZES, HOOK_2LINE_SIZES, HOOK_LINE_GAP = (92, 80), (76, 72), 1.12
SIG_BAR = {"y": 456, "w": 160}                                # 훅 아래 yellow 시그니처 바
CARD_BOX = (196, 486, 688, 860)                               # x, y, w, h (원본 1080x1350의 0.637배, 4:5 유지)
SUB = {"size": 48, "line_h": 62, "pad_x": 32, "pad_y": 18, "bottom": 1528, "alpha": 0.80, "radius": 18}
SUB_MAX_CHARS, SUB_MAX_LINES = 16, 2
END = {"label": 34, "text_sizes": (76, 68), "text_pad": 36, "sub": 44, "handle": 48}
MOTION_AMP = 0.05
MOTIONS = ("static", "zoom_in", "zoom_out", "pan_up", "pan_down")
DUR_MIN, DUR_MAX, DUR_TOL = 15.0, 30.0, 0.1
SEG_MIN_DUR = 0.5

AUDIO_TRACK_REASON = ("소리 내용은 없음(audio=none). 무음 AAC-LC 48kHz 스테레오 트랙 1개를 넣는다: "
                      "Instagram 콘텐츠 게시 API 영상 규격이 오디오를 AAC 48kHz 이하·1~2채널로 정의하고, "
                      "오디오 스트림이 없는 파일을 가정하지 않는 업로더·편집기·플레이어가 있어 호환성을 위해 포함. "
                      "용량 증가는 수 KB 수준. --no-audio-track으로 끌 수 있음.")


class ReelError(Exception):
    pass


# ---------- 공용 ----------
def rel(path):
    ap = os.path.abspath(path)
    return os.path.relpath(ap, REPO) if ap.startswith(REPO + os.sep) else ap


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tool_version(cmd):
    try:
        out = subprocess.run([cmd, "-version"], capture_output=True, text=True, timeout=20).stdout
        return out.splitlines()[0].split(" Copyright")[0].strip()
    except Exception:
        return None


def hanji_background_9x16():
    """render_cards.hanji_background를 그대로 쓰되, 호출 순간에만 모듈 캔버스 크기를 1080x1920으로 바꾼다(파일 수정 없음)."""
    old = (rc.W, rc.H)
    rc.W, rc.H = RW, RH
    try:
        bg = rc.hanji_background()
    finally:
        rc.W, rc.H = old
    if bg.size != (RW, RH):  # render_cards 구현이 바뀌어 전역을 안 쓰게 되면 세로로 이어 붙인다
        tile = bg
        bg = Image.new("RGB", (RW, RH), T["paper"])
        for y in range(0, RH, tile.size[1]):
            bg.paste(tile.resize((RW, tile.size[1])), (0, y))
    return bg


def measure(d, text, f, stroke=0):
    l, t, r, b = d.textbbox((0, 0), text, font=f, stroke_width=stroke)
    return r - l


def split_two(d, text, f, maxw, stroke=0):
    """명시적 \\n 우선. 한 줄에 들어가면 1줄, 아니면 공백에서 가장 균형 잡힌 2줄. 불가하면 None."""
    if "\n" in text:
        lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
        return lines if all(measure(d, ln, f, stroke) <= maxw for ln in lines) else None
    text = text.strip()
    if measure(d, text, f, stroke) <= maxw:
        return [text]
    best = None
    for i, ch in enumerate(text):
        if ch != " ":
            continue
        a, b = text[:i].strip(), text[i + 1:].strip()
        wa, wb = measure(d, a, f, stroke), measure(d, b, f, stroke)
        if wa <= maxw and wb <= maxw and (best is None or max(wa, wb) < best[0]):
            best = (max(wa, wb), [a, b])
    return best[1] if best else None


def subtitle_lines(text):
    """자막 줄 나누기(글자 수 기준, 공백·문장부호 포함). \\n이 있으면 그대로, 16자 초과면 공백에서 균형 분할."""
    text = (text or "").strip()
    if not text:
        return []
    if "\n" in text:
        return [ln.strip() for ln in text.split("\n") if ln.strip()]
    if len(text) <= SUB_MAX_CHARS:
        return [text]
    best = None
    for i, ch in enumerate(text):
        if ch == " ":
            a, b = text[:i].strip(), text[i + 1:].strip()
            if len(a) <= SUB_MAX_CHARS and len(b) <= SUB_MAX_CHARS and (best is None or max(len(a), len(b)) < best[0]):
                best = (max(len(a), len(b)), [a, b])
    return best[1] if best else [text]  # 나눌 곳이 없으면 1줄 그대로 -> 검증에서 실패


# ---------- 검증 ----------
def load_spec(post_dir):
    path = os.path.join(post_dir, "reel.json")
    if not os.path.isfile(path):
        raise ReelError(f"reel.json 없음: {path}")
    try:
        with open(path, encoding="utf-8") as fp:
            return json.load(fp), path
    except json.JSONDecodeError as e:
        raise ReelError(f"reel.json 파싱 실패: {e}")


def validate(post_dir, spec, fonts, final):
    """오류 목록, 경고 목록, 정규화된 계획을 돌려준다. 오류가 하나라도 있으면 렌더하지 않는다."""
    errs, warns = [], []
    d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    rid = str(spec.get("id", ""))
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", rid):
        errs.append(f"id 형식 오류: {rid!r}")
    if list(spec.get("size", [RW, RH])) != [RW, RH]:
        errs.append(f"size는 [1080,1920]만 지원: {spec.get('size')}")
    if spec.get("audio", "none") != "none":
        errs.append(f"audio는 'none'만 지원(무음 릴스): {spec.get('audio')!r}")
    if spec.get("sponsor"):
        msg = "sponsor 지정됨: 화면 내 '광고' 표기는 이 렌더러에 없음"
        (errs if final else warns).append(msg + (" -> --final 거부" if final else ""))

    # 카드 RENDER.json(mode=final) 확인
    rj = os.path.join(post_dir, "RENDER.json")
    card_mode = None
    if os.path.isfile(rj):
        try:
            with open(rj, encoding="utf-8") as fp:
                card_mode = json.load(fp).get("mode")
        except Exception:
            card_mode = "unreadable"
    if card_mode != "final":
        msg = f"카드 RENDER.json mode={card_mode!r} (final 카드가 아님, 카드에 MOCKUP 표기가 남아 있을 수 있음)"
        (errs if final else warns).append(msg)

    # 훅
    hook = str(spec.get("hook", "")).strip()
    hook_plan = None
    if not hook:
        errs.append("hook 비어 있음")
    else:
        for size in HOOK_1LINE_SIZES:
            f = rc.font(fonts["head"], size)
            if measure(d, hook, f, rc.head_stroke(fonts, size)) <= TEXT_MAXW and "\n" not in hook:
                hook_plan = (size, [hook])
                break
        if hook_plan is None:
            for size in HOOK_2LINE_SIZES:
                f = rc.font(fonts["head"], size)
                lines = split_two(d, hook, f, TEXT_MAXW, rc.head_stroke(fonts, size))
                if lines and len(lines) <= 2:
                    hook_plan = (size, lines)
                    break
        if hook_plan is None:
            errs.append(f"hook가 72px 2줄(폭 {TEXT_MAXW}px)에 들어가지 않음: {hook!r}")

    # 장면
    segs = spec.get("segments") or []
    if not segs:
        errs.append("segments 비어 있음")
    plan_segs = []
    fsub = rc.font(fonts["body"], SUB["size"])
    for i, s in enumerate(segs, 1):
        card = str(s.get("card", ""))
        cpath = os.path.join(post_dir, card)
        if not card or not os.path.isfile(cpath):
            errs.append(f"장면{i}: 카드 파일 없음 {card!r}")
        else:
            try:
                with Image.open(cpath) as im:
                    if im.size != CARD_SRC:
                        errs.append(f"장면{i}: {card} 크기 {im.size} != 1080x1350")
            except Exception as e:
                errs.append(f"장면{i}: {card} 열기 실패 {e}")
        try:
            dur = float(s.get("dur", 0))
        except (TypeError, ValueError):
            dur = 0.0
        if dur < SEG_MIN_DUR:
            errs.append(f"장면{i}: dur {s.get('dur')!r} < {SEG_MIN_DUR}")
        motion = s.get("motion", "static") or "static"
        if motion not in MOTIONS:
            errs.append(f"장면{i}: motion {motion!r} (허용 {', '.join(MOTIONS)})")
        lines = subtitle_lines(s.get("subtitle", ""))
        if not lines:
            warns.append(f"장면{i}: subtitle 비어 있음(자막 바 없음)")
        if len(lines) > SUB_MAX_LINES:
            errs.append(f"장면{i}: 자막 {len(lines)}줄 (> {SUB_MAX_LINES})")
        for ln in lines:
            if len(ln) > SUB_MAX_CHARS:
                errs.append(f"장면{i}: 자막 줄 {len(ln)}자 > {SUB_MAX_CHARS} (공백 포함): {ln!r}")
            elif measure(d, ln, fsub) > TEXT_MAXW - 2 * SUB["pad_x"]:
                errs.append(f"장면{i}: 자막 줄 폭 초과: {ln!r}")
        plan_segs.append({"card": card, "path": cpath, "dur": dur, "motion": motion, "lines": lines})

    # 엔드카드
    end = spec.get("end_card") or {}
    try:
        end_dur = float(end.get("dur", 0))
    except (TypeError, ValueError):
        end_dur = 0.0
    if end_dur < SEG_MIN_DUR:
        errs.append(f"end_card.dur {end.get('dur')!r} < {SEG_MIN_DUR}")
    end_text, end_sub = str(end.get("text", "")).strip(), str(end.get("sub", "")).strip()
    end_plan = {"dur": end_dur, "text": None, "text_size": None, "sub": []}
    if not end_text:
        errs.append("end_card.text 비어 있음")
    else:
        for size in END["text_sizes"]:
            lines = split_two(d, end_text, rc.font(fonts["head"], size), TEXT_MAXW - 2 * END["text_pad"],
                              rc.head_stroke(fonts, size))
            if lines and len(lines) <= 2:
                end_plan["text"], end_plan["text_size"] = lines, size
                break
        if end_plan["text"] is None:
            errs.append(f"end_card.text가 2줄에 들어가지 않음: {end_text!r}")
    if end_sub:
        lines = split_two(d, end_sub, rc.font(fonts["body"], END["sub"]), TEXT_MAXW)
        if not lines or len(lines) > 2:
            errs.append(f"end_card.sub가 2줄에 들어가지 않음: {end_sub!r}")
        else:
            end_plan["sub"] = lines

    # 길이
    total = round(sum(p["dur"] for p in plan_segs) + end_dur, 3)
    try:
        spec_dur = float(spec.get("duration_sec"))
    except (TypeError, ValueError):
        spec_dur = None
        errs.append(f"duration_sec 누락/형식 오류: {spec.get('duration_sec')!r}")
    if spec_dur is not None:
        if abs(total - spec_dur) > DUR_TOL:
            errs.append(f"길이 불일치: segments+end_card = {total}s, duration_sec = {spec_dur}s (허용 ±{DUR_TOL})")
        for name, v in (("duration_sec", spec_dur), ("segments+end_card", total)):
            if not (DUR_MIN <= v <= DUR_MAX):
                errs.append(f"길이 범위 밖: {name} = {v}s (허용 {DUR_MIN:g}~{DUR_MAX:g}초)")

    cover = str(spec.get("cover") or (plan_segs[0]["card"] if plan_segs else ""))
    if not cover or not os.path.isfile(os.path.join(post_dir, cover)):
        errs.append(f"cover 카드 파일 없음: {cover!r}")

    plan = {"id": rid, "hook": hook_plan, "segs": plan_segs, "end": end_plan, "total": total,
            "spec_dur": spec_dur, "cover": cover, "card_mode": card_mode}
    return errs, warns, plan


# ---------- 합성 ----------
class Composer:
    def __init__(self, post_dir, plan, fonts, final, xfade):
        self.post_dir, self.plan, self.fonts, self.final = post_dir, plan, fonts, final
        self.xfade = max(0.0, min(0.3, xfade))
        self.cx, self.cy, self.cw, self.ch = CARD_BOX
        self.bbox = {}  # 글자 bbox 기록(안전 영역 자가 점검용)
        bg = hanji_background_9x16()
        self.base_end = bg.copy()
        self._draw_hook(self.base_end)
        self._mockup(self.base_end)
        self.base = self.base_end.copy()
        self._card_frame(self.base)
        self.cards = {}
        for s in plan["segs"] + [{"path": os.path.join(post_dir, plan["cover"])}]:
            if s["path"] not in self.cards:
                self.cards[s["path"]] = Image.open(s["path"]).convert("RGB")
        self.seg_base = [self._with_subtitle(self.base, s["lines"], i) for i, s in enumerate(plan["segs"])]
        self.end_frame = self._end_card(self.base_end.copy())
        self.starts, t = [], 0.0
        for s in plan["segs"]:
            self.starts.append(t)
            t += s["dur"]
        self.end_start = t
        self._cache = None

    # --- 고정 레이어 ---
    def _draw_hook(self, img):
        size, lines = self.plan["hook"]
        d = ImageDraw.Draw(img)
        f = rc.font(self.fonts["head"], size)
        st = rc.head_stroke(self.fonts, size)
        adv = int(size * HOOK_LINE_GAP)
        block = adv * (len(lines) - 1) + size
        y0 = (HOOK_ZONE[0] + HOOK_ZONE[1]) // 2 - block // 2
        for k, ln in enumerate(lines):
            y = y0 + k * adv + size // 2
            d.text((TEXT_CX, y), ln, font=f, fill=T["ink"], anchor="mm", stroke_width=st, stroke_fill=T["ink"])
            self._note("hook", d.textbbox((TEXT_CX, y), ln, font=f, anchor="mm", stroke_width=st))
        rc.signature_bar(d, TEXT_CX - SIG_BAR["w"] // 2, SIG_BAR["y"], SIG_BAR["w"])

    def _mockup(self, img):
        if self.final:
            return
        d = ImageDraw.Draw(img)
        f = rc.font(self.fonts["latin"], MOCKUP_BOX["size"])
        tw = measure(d, rc.MOCKUP_TAG, f)
        x1, y0 = MOCKUP_BOX["right"], MOCKUP_BOX["top"]
        x = x1 - 12 - tw
        d.rounded_rectangle([x - 12, y0, x1, y0 + MOCKUP_BOX["size"] + 12], radius=7, outline=T["red"], width=3)
        d.text((x, y0 + 5), rc.MOCKUP_TAG, font=f, fill=T["red"])
        self._note("mockup", (x - 12, y0, x1, y0 + MOCKUP_BOX["size"] + 12))

    def _card_frame(self, img):
        x, y, w, h = CARD_BOX
        sh = Image.new("L", img.size, 0)
        ImageDraw.Draw(sh).rectangle([x + 4, y + 12, x + w + 4, y + h + 12], fill=60)
        sh = sh.filter(ImageFilter.GaussianBlur(14))
        img.paste(Image.new("RGB", img.size, T["night"]), (0, 0), sh)
        ImageDraw.Draw(img).rectangle([x - 3, y - 3, x + w + 2, y + h + 2], outline=T["ink"], width=3)

    def _with_subtitle(self, base, lines, idx):
        img = base.copy()
        if not lines:
            return img
        ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        f = rc.font(self.fonts["body"], SUB["size"])
        bw = max(measure(d, ln, f) for ln in lines) + 2 * SUB["pad_x"]
        bh = len(lines) * SUB["line_h"] + 2 * SUB["pad_y"]
        x0, y1 = TEXT_CX - bw // 2, SUB["bottom"]
        y0 = y1 - bh
        night = tuple(int(T["night"][i:i + 2], 16) for i in (1, 3, 5))
        d.rounded_rectangle([x0, y0, x0 + bw, y1], radius=SUB["radius"], fill=night + (int(255 * SUB["alpha"]),))
        for k, ln in enumerate(lines):
            yc = y0 + SUB["pad_y"] + k * SUB["line_h"] + SUB["line_h"] // 2
            d.text((TEXT_CX, yc), ln, font=f, fill=T["white"], anchor="mm")
            self._note("subtitle", d.textbbox((TEXT_CX, yc), ln, font=f, anchor="mm"))
        self._note("subtitle_bar", (x0, y0, x0 + bw, y1))
        out = img.convert("RGBA")
        out.alpha_composite(ov)
        return out.convert("RGB")

    def _end_card(self, img):
        d = ImageDraw.Draw(img)
        e = self.plan["end"]
        fl = rc.font(self.fonts["body"], END["label"])
        size = e["text_size"]
        ft = rc.font(self.fonts["head"], size)
        st = rc.head_stroke(self.fonts, size)
        fs = rc.font(self.fonts["body"], END["sub"])
        fh = rc.font(self.fonts["body"], END["handle"])
        adv_t, adv_s = int(size * 1.18), int(END["sub"] * 1.3)
        label_h = END["label"] + 22
        red_h = adv_t * (len(e["text"]) - 1) + size + 2 * 34
        sub_h = adv_s * len(e["sub"]) if e["sub"] else 0
        parts = [label_h, 36, red_h, 26, 14, 40 if sub_h else 0, sub_h, 44, END["handle"]]
        y = (CARD_BOX[1] + SUB["bottom"]) // 2 - sum(parts) // 2
        # 계정 라벨(ink 알약, white 글자)
        lw = measure(d, rc.ACCOUNT, fl) + 36
        d.rounded_rectangle([TEXT_CX - lw // 2, y, TEXT_CX + lw // 2, y + label_h], radius=10, fill=T["ink"])
        d.text((TEXT_CX, y + label_h // 2), rc.ACCOUNT, font=fl, fill=T["white"], anchor="mm")
        self._note("end", (TEXT_CX - lw // 2, y, TEXT_CX + lw // 2, y + label_h))
        y += label_h + 36
        # CTA: red 블록 + white head 글꼴
        tw = max(measure(d, ln, ft, st) for ln in e["text"])
        bw = min(TEXT_MAXW, tw + 2 * END["text_pad"])
        d.rectangle([TEXT_CX - bw // 2, y, TEXT_CX + bw // 2, y + red_h], fill=T["red"], outline=T["ink"], width=4)
        for k, ln in enumerate(e["text"]):
            yc = y + 34 + k * adv_t + size // 2
            d.text((TEXT_CX, yc), ln, font=ft, fill=T["white"], anchor="mm", stroke_width=st, stroke_fill=T["white"])
        self._note("end", (TEXT_CX - bw // 2, y, TEXT_CX + bw // 2, y + red_h))
        y += red_h + 26
        rc.signature_bar(d, TEXT_CX - 110, y, 220)
        y += 14 + (40 if sub_h else 0)
        for k, ln in enumerate(e["sub"]):
            yc = y + k * adv_s + END["sub"] // 2
            d.text((TEXT_CX, yc), ln, font=fs, fill=T["ink"], anchor="mm")
            self._note("end", d.textbbox((TEXT_CX, yc), ln, font=fs, anchor="mm"))
        y += sub_h + 44
        d.text((TEXT_CX, y + END["handle"] // 2), HANDLE, font=fh, fill=T["ink"], anchor="mm")
        self._note("end", d.textbbox((TEXT_CX, y + END["handle"] // 2), HANDLE, font=fh, anchor="mm"))
        return img

    def _note(self, key, box):
        b = self.bbox.get(key)
        box = tuple(int(v) for v in box)
        self.bbox[key] = box if b is None else (min(b[0], box[0]), min(b[1], box[1]), max(b[2], box[2]), max(b[3], box[3]))

    # --- 움직이는 레이어(카드) ---
    def card_window(self, path, motion, p):
        p = min(1.0, max(0.0, p))
        W0, H0 = CARD_SRC
        if motion == "zoom_in":
            s = 1 + MOTION_AMP * p
        elif motion == "zoom_out":
            s = 1 + MOTION_AMP * (1 - p)
        elif motion in ("pan_up", "pan_down"):
            s = 1 + MOTION_AMP
        else:
            s = 1.0
        ww, wh = W0 / s, H0 / s
        cx, cy = W0 / 2, H0 / 2
        if motion == "pan_down":
            cy = wh / 2 + (H0 - wh) * p
        elif motion == "pan_up":
            cy = H0 - wh / 2 - (H0 - wh) * p
        box = (round(cx - ww / 2, 3), round(cy - wh / 2, 3), round(cx + ww / 2, 3), round(cy + wh / 2, 3))
        key = (path, box)
        if self._cache and self._cache[0] == key:
            return self._cache[1]
        img = self.cards[path].resize((self.cw, self.ch), Image.BICUBIC, box=box)
        self._cache = (key, img)
        return img

    def seg_card(self, i, t):
        s = self.plan["segs"][i]
        return self.card_window(s["path"], s["motion"], (t - self.starts[i]) / s["dur"])

    def seg_frame(self, i, t):
        h, n = self.xfade / 2, len(self.plan["segs"])
        card = self.seg_card(i, t)
        if h > 0 and i > 0 and t - self.starts[i] < h:
            a = (t - (self.starts[i] - h)) / self.xfade
            card = Image.blend(self.seg_card(i - 1, t), card, a)
        elif h > 0 and i < n - 1 and self.starts[i + 1] - t < h:
            a = (t - (self.starts[i + 1] - h)) / self.xfade
            card = Image.blend(card, self.seg_card(i + 1, t), a)
        img = self.seg_base[i]
        img.paste(card, (self.cx, self.cy))
        return img

    def frame(self, t):
        """t초의 화면. 반환 이미지는 다음 호출 때 바뀔 수 있으니 보관하려면 copy()."""
        h, n = self.xfade / 2, len(self.plan["segs"])
        E = self.end_start
        if t >= E + h or (h == 0 and t >= E):
            return self.end_frame
        if h > 0 and t >= E - h:
            a = (t - (E - h)) / self.xfade
            return Image.blend(self.seg_frame(n - 1, t), self.end_frame, a)
        i = max(k for k in range(n) if self.starts[k] <= t + 1e-9)
        return self.seg_frame(i, t)

    def cover(self):
        img = self.base.copy()
        img.paste(self.card_window(os.path.join(self.post_dir, self.plan["cover"]), "static", 0), (self.cx, self.cy))
        return img


def draw_guides(img):
    """안전 영역 밖(상 220·하 380·우 120)을 반투명 빨강으로 표시. 디버그 전용, 저장소 파일에는 쓰지 않는다."""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    c = (200, 16, 46, 90)
    d.rectangle([0, 0, RW, SAFE_Y0], fill=c)
    d.rectangle([0, SAFE_Y1, RW, RH], fill=c)
    d.rectangle([SAFE_X1, SAFE_Y0, RW, SAFE_Y1], fill=c)
    out = img.convert("RGBA")
    out.alpha_composite(ov)
    return out.convert("RGB")


def preview_strip(comp, plan, fonts, final, guides=False):
    tw, th, pad, head, foot = 270, 480, 16, 64, 44
    tiles = []
    for i, s in enumerate(plan["segs"]):
        tiles.append((comp.frame(comp.starts[i] + s["dur"] / 2).copy(), f"{i + 1} · {s['dur']:g}s · {s['motion']}"))
    tiles.append((comp.frame(comp.end_start + plan["end"]["dur"] / 2).copy(), f"END · {plan['end']['dur']:g}s"))
    W = pad + len(tiles) * (tw + pad)
    H = head + th + foot
    sheet = Image.new("RGB", (W, H), T["night"])
    d = ImageDraw.Draw(sheet)
    title = f"{plan['id']}  reel {plan['total']:g}s · {len(plan['segs'])} scenes + end · 1080x1920 30fps · {'FINAL' if final else 'MOCKUP'}"
    d.text((pad, 18), title, font=rc.font(fonts["latin"], 28), fill=T["yellow"])
    for k, (im, label) in enumerate(tiles):
        if guides:
            im = draw_guides(im)
        x = pad + k * (tw + pad)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, head))
        d.text((x, head + th + 8), label, font=rc.font(fonts["latin"], 24), fill=T["white"])
    return sheet


# ---------- 인코딩 ----------
def encode(comp, frames, out_tmp, audio_track):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{RW}x{RH}", "-r", str(FPS), "-i", "-"]
    if audio_track:
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
    cmd += ["-map", "0:v:0"] + (["-map", "1:a:0"] if audio_track else [])
    cmd += ["-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-level:v", "4.0",
            "-g", "60", "-maxrate", "12M", "-bufsize", "24M",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
    if audio_track:
        cmd += ["-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-shortest"]
    cmd += ["-frames:v", str(frames), "-t", f"{frames / FPS:.3f}", "-movflags", "+faststart", "-tag:v", "avc1",
            "-f", "mp4", out_tmp]
    with tempfile.TemporaryFile() as errf:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=errf)
        try:
            for k in range(frames):
                proc.stdin.write(comp.frame(k / FPS).tobytes())
            proc.stdin.close()
        except BrokenPipeError:
            pass
        rc_ = proc.wait()
        errf.seek(0)
        err = errf.read().decode("utf-8", "replace")[-2000:]
    if rc_ != 0:
        raise ReelError(f"ffmpeg 실패(code {rc_}): {err}")
    return cmd


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration,size:stream=codec_type,codec_name,profile,width,height,pix_fmt,r_frame_rate,nb_frames,"
                          "sample_rate,channels,color_space", "-of", "json", path],
                         capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        raise ReelError(f"ffprobe 실패: {out.stderr[-500:]}")
    return json.loads(out.stdout)


def check_probe(pr, frames, audio_track):
    v = [s for s in pr.get("streams", []) if s.get("codec_type") == "video"]
    a = [s for s in pr.get("streams", []) if s.get("codec_type") == "audio"]
    errs = []
    if len(v) != 1:
        errs.append(f"비디오 스트림 {len(v)}개")
    else:
        v = v[0]
        if (v.get("width"), v.get("height")) != (RW, RH):
            errs.append(f"해상도 {v.get('width')}x{v.get('height')}")
        if v.get("codec_name") != "h264" or v.get("pix_fmt") != "yuv420p":
            errs.append(f"코덱 {v.get('codec_name')}/{v.get('pix_fmt')}")
        if v.get("r_frame_rate") != f"{FPS}/1":
            errs.append(f"fps {v.get('r_frame_rate')}")
        if str(v.get("nb_frames")) != str(frames):
            errs.append(f"프레임 {v.get('nb_frames')} != {frames}")
    if len(a) != (1 if audio_track else 0):
        errs.append(f"오디오 스트림 {len(a)}개")
    dur = float(pr.get("format", {}).get("duration", 0))
    if abs(dur - frames / FPS) > 0.1:
        errs.append(f"컨테이너 길이 {dur:.3f}s != {frames / FPS:.3f}s")
    return errs


def atomic_save(write_fn, path):
    tmp = path + ".tmp"
    write_fn(tmp)
    os.replace(tmp, path)


def save_png8(img, path):
    def _w(tmp):
        img.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(
            tmp, format="PNG", optimize=True)
    atomic_save(_w, path)


def save_json(obj, path):
    def _w(tmp):
        with open(tmp, "w", encoding="utf-8") as fp:
            json.dump(obj, fp, ensure_ascii=False, indent=2)
            fp.write("\n")
    atomic_save(_w, path)


# ---------- 한 편 렌더 ----------
def render_reel(post_dir, fonts, out_dir, final, xfade, audio_track, guides, check_only):
    t0 = time.time()
    spec, spec_path = load_spec(post_dir)
    errs, warns, plan = validate(post_dir, spec, fonts, final)
    for w in warns:
        print(f"  warn: {w}")
    if errs:
        raise ReelError("검증 실패 -> 파일 생성 안 함\n  - " + "\n  - ".join(errs))
    frames = int(round(plan["total"] * FPS))
    if check_only:
        print(f"  OK(check): {plan['id']} {plan['total']}s {frames} frames, hook {plan['hook'][0]}px {len(plan['hook'][1])}줄")
        return None

    comp = Composer(post_dir, plan, fonts, final, xfade)
    for key, b in comp.bbox.items():  # 핵심 글자 안전 영역 자가 점검
        if key in ("hook", "subtitle", "subtitle_bar", "end", "mockup") and (b[1] < SAFE_Y0 or b[3] > SAFE_Y1 or b[2] > SAFE_X1):
            raise ReelError(f"레이아웃이 안전 영역을 벗어남: {key} {b}")

    os.makedirs(out_dir, exist_ok=True)
    mp4 = os.path.join(out_dir, f"{plan['id']}.mp4")
    tmp = os.path.join(out_dir, f".{plan['id']}.partial.mp4")
    try:
        t_enc = time.time()
        encode(comp, frames, tmp, audio_track)
        enc_sec = time.time() - t_enc
        pr = probe(tmp)
        perr = check_probe(pr, frames, audio_track)
        if perr:
            raise ReelError("출력 검증 실패 -> 삭제: " + "; ".join(perr))
        os.replace(tmp, mp4)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

    save_png8(comp.cover(), os.path.join(post_dir, "reel-cover.png"))
    save_png8(preview_strip(comp, plan, fonts, final), os.path.join(post_dir, "reel-preview.png"))
    if guides:
        save_png8(preview_strip(comp, plan, fonts, final, guides=True), os.path.join(out_dir, f"{plan['id']}.guides.png"))

    vs = next(s for s in pr["streams"] if s["codec_type"] == "video")
    digest = sha256(mp4)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    record = {
        "id": plan["id"], "mode": "final" if final else "mockup", "rendered_at": now, "renderer": "render_reels.py",
        "duration_sec": round(frames / FPS, 3), "duration_sec_spec": plan["spec_dur"], "frames": frames, "fps": FPS,
        "size": [RW, RH],
        "video": {"codec": vs.get("codec_name"), "profile": vs.get("profile"), "pix_fmt": vs.get("pix_fmt"),
                  "color": "bt709 tv", "crf": 18, "preset": "medium", "maxrate": "12M", "faststart": True},
        "audio": ({"content": "none", "track": "aac-lc 48kHz stereo silent (anullsrc)", "reason": AUDIO_TRACK_REASON}
                  if audio_track else {"content": "none", "track": None, "reason": "--no-audio-track"}),
        "transition": {"type": "card-layer crossfade, subtitle cut, end-card full crossfade" if comp.xfade else "cut",
                       "sec": comp.xfade},
        "scenes": [{"card": s["card"], "dur": s["dur"], "motion": s["motion"], "subtitle_lines": s["lines"]} for s in plan["segs"]],
        "end_card_dur": plan["end"]["dur"], "cover": plan["cover"], "hook_px": plan["hook"][0],
        "layout": {"card_box_xywh": list(CARD_BOX), "hook_zone_y": list(HOOK_ZONE), "subtitle_bottom_y": SUB["bottom"],
                   "safe_area": {"top": SAFE_TOP, "bottom": SAFE_BOTTOM, "right": SAFE_RIGHT},
                   "text_bbox": {k: list(v) for k, v in comp.bbox.items()}},
        "fonts": {k: str(v) for k, v in fonts.items()},
        "mp4": rel(mp4), "mp4_bytes": os.path.getsize(mp4), "mp4_sha256": digest,
        "ffmpeg": tool_version("ffmpeg"), "reel_json_sha256": sha256(spec_path),
        "cards_render_mode": plan["card_mode"], "warnings": warns,
        "elapsed_sec": round(time.time() - t0, 1), "encode_sec": round(enc_sec, 1),
    }
    save_json(record, os.path.join(post_dir, "REEL_RENDER.json"))
    print(f"  -> {rel(mp4)} {record['duration_sec']}s {frames}f {record['mp4_bytes'] / 1e6:.2f}MB "
          f"({record['elapsed_sec']}s) + reel-cover.png, reel-preview.png, REEL_RENDER.json")
    return {"id": plan["id"], "date": spec.get("date"), "reel_time_kst": spec.get("reel_time_kst"),
            "mode": record["mode"], "mp4": rel(mp4), "duration_sec": record["duration_sec"], "frames": frames,
            "bytes": record["mp4_bytes"], "sha256": digest, "post_dir": rel(post_dir), "rendered_at": now,
            "elapsed_sec": record["elapsed_sec"]}


def update_manifest(out_dir, entries):
    path = os.path.join(out_dir, "manifest.json")
    data = {"reels": []}
    if os.path.isfile(path):
        try:
            with open(path, encoding="utf-8") as fp:
                data = json.load(fp)
        except Exception:
            pass
    by_id = {e["id"]: e for e in data.get("reels", [])}
    for e in entries:
        by_id[e["id"]] = e
    data = {"updated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "renderer": "cardnews/design/render_reels.py", "reels": [by_id[k] for k in sorted(by_id)]}
    save_json(data, path)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("post_dir", nargs="?", help="reel.json이 있는 게시물 폴더")
    ap.add_argument("--all", metavar="POSTS_DIR", help="하위 폴더 중 reel.json이 있는 것 전부")
    ap.add_argument("--final", action="store_true", help="게시용(MOCKUP 생략). approved 후에만")
    ap.add_argument("--out", default=DEFAULT_OUT, help="mp4·manifest 폴더(기본: 저장소 render/reels, 커밋 제외)")
    ap.add_argument("--xfade", type=float, default=0.25, help="장면 전환 크로스페이드 초(0~0.3, 0=컷)")
    ap.add_argument("--no-audio-track", action="store_true", help="무음 AAC 트랙을 넣지 않음")
    ap.add_argument("--check", action="store_true", help="검증만 하고 아무 파일도 만들지 않음")
    ap.add_argument("--guides", action="store_true", help="안전 영역 표시 미리보기를 <out>/<id>.guides.png로 추가 저장")
    args = ap.parse_args()

    if args.all:
        targets = [d for d in sorted(glob.glob(os.path.join(args.all, "*"))) if os.path.isfile(os.path.join(d, "reel.json"))]
    elif args.post_dir:
        targets = [args.post_dir]
    else:
        ap.error("post_dir 또는 --all 을 지정하세요")
    if not targets:
        print("reel.json 을 가진 폴더가 없습니다", file=sys.stderr)
        return 1
    if not args.check:
        missing = [c for c in ("ffmpeg", "ffprobe") if shutil.which(c) is None]
        if missing:
            print(f"필수 도구 없음: {', '.join(missing)} (scripts/setup.sh로 설치. 이 스크립트는 설치하지 않음)", file=sys.stderr)
            return 2
    fonts = rc.load_fonts()
    print("fonts:", fonts)
    ok, failed = [], []
    for t in targets:
        print(f"[{t}]")
        try:
            r = render_reel(t, fonts, args.out, args.final, args.xfade, not args.no_audio_track, args.guides, args.check)
            if r:
                ok.append(r)
        except ReelError as e:
            print(f"  FAIL: {e}", file=sys.stderr)
            failed.append(t)
    if ok:
        print("manifest:", rel(update_manifest(args.out, ok)))
    print(f"done: {len(ok) if not args.check else len(targets) - len(failed)} ok, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
