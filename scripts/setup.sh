#!/usr/bin/env bash
# KE Studio 클라우드 환경 setup script. 환경 설정의 setup script에 `bash scripts/setup.sh`로 등록.
set -euo pipefail
if ! command -v ffmpeg >/dev/null 2>&1; then
  (command -v apt-get >/dev/null && { sudo -n true 2>/dev/null && SUDO=sudo || SUDO=; $SUDO apt-get update -qq && $SUDO apt-get install -y -qq ffmpeg; }) || echo "WARN: ffmpeg 설치 실패"
fi
python3 -m pip install -q --upgrade google-api-python-client google-auth-oauthlib pillow || echo "WARN: pip 설치 실패"
ffmpeg -version 2>/dev/null | head -1 || true
