#!/usr/bin/env bash
# KE Studio 클라우드 환경 setup script. 환경 설정의 setup script에 `bash scripts/setup.sh`로 등록.
set -euo pipefail
if ! command -v ffmpeg >/dev/null 2>&1; then
  (command -v apt-get >/dev/null && { sudo -n true 2>/dev/null && SUDO=sudo || SUDO=; $SUDO apt-get update -qq && $SUDO apt-get install -y -qq ffmpeg; }) || echo "WARN: ffmpeg 설치 실패"
fi
python3 -m pip install -q --upgrade google-api-python-client google-auth-oauthlib pillow || echo "WARN: pip 설치 실패"
ffmpeg -version 2>/dev/null | head -1 || true
# --- last30days 스킬(.claude/skills/last30days-last30days): Python 3.12+ 필요. 첫 실행 setup 마법사(브라우저 쿠키 읽기 등)는 쓰지 않음 ---
if ! { command -v python3.12 >/dev/null 2>&1 || python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)'; }; then
  command -v uv >/dev/null 2>&1 || python3 -m pip install -q uv || echo "WARN: uv 설치 실패"
  uv python install 3.12 || echo "WARN: Python 3.12 설치 실패(last30days 사용 불가)"
fi
python3 -m pip install -q --upgrade yt-dlp || echo "WARN: yt-dlp 설치 실패(last30days YouTube 수집)"
command -v node >/dev/null 2>&1 || echo "WARN: node 없음(last30days 요구 bin)"
# --- muapi-cli(이미지·영상 생성 중계 API, 공급자 후보. 2026-10-01 대표 허용) : Python 3.12 venv에 설치. npm 패키지는 Linux 바이너리가 없어 pip 경로 사용 ---
if command -v python3.12 >/dev/null 2>&1; then
  [ -x "$HOME/.venvs/muapi/bin/muapi" ] || { python3.12 -m venv "$HOME/.venvs/muapi" && "$HOME/.venvs/muapi/bin/pip" install -q muapi-cli; } || echo "WARN: muapi-cli 설치 실패"
  "$HOME/.venvs/muapi/bin/muapi" --version 2>/dev/null || true
fi
