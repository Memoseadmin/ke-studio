#!/usr/bin/env bash
# 카드뉴스 v3 서체(세트 B, cardnews/docs/DESIGN_SOURCES.md §4) 받아 오기. 서체 파일은 커밋하지 않는다(v3/fonts/.gitignore).
# Hahmlet·Black Han Sans·Noto Serif KR = google/fonts ofl/ (OFL-1.1), MaruBuri = 네이버 한글한글아름답게(오픈 라이선스, 상업적 사용 허용).
# 받은 파일의 sha256은 render_v3.py 가 RENDER.json 에 기록한다(google/fonts main 은 바뀔 수 있으므로).
set -uo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)/fonts"
mkdir -p "$DIR"
fetch() { [ -s "$DIR/$1" ] && return 0; curl -fsSL --retry 3 -m 300 -o "$DIR/$1.part" "$2" && mv "$DIR/$1.part" "$DIR/$1" || { rm -f "$DIR/$1.part"; echo "WARN: $1 다운로드 실패 ($2)"; }; }
GF=https://raw.githubusercontent.com/google/fonts/main/ofl
fetch "Hahmlet[wght].ttf"        "$GF/hahmlet/Hahmlet%5Bwght%5D.ttf"
fetch "OFL-Hahmlet.txt"          "$GF/hahmlet/OFL.txt"
fetch "BlackHanSans-Regular.ttf" "$GF/blackhansans/BlackHanSans-Regular.ttf"
fetch "OFL-BlackHanSans.txt"     "$GF/blackhansans/OFL.txt"
fetch "NotoSerifKR[wght].ttf"    "$GF/notoserifkr/NotoSerifKR%5Bwght%5D.ttf"
fetch "OFL-NotoSerifKR.txt"      "$GF/notoserifkr/OFL.txt"
NV=https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri
fetch "MaruBuri-Regular.ttf"     "$NV/MaruBuri-Regular.ttf"
fetch "MaruBuri-Bold.ttf"        "$NV/MaruBuri-Bold.ttf"
ls -la "$DIR" | grep -E "ttf|txt" || true
