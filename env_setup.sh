#!/usr/bin/env bash
# Create a Python venv if not present, install requirements, and show how to run generate_session.py
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

PY=${PY:-python3}
if ! command -v "$PY" >/dev/null 2>&1; then
  echo "No $PY found. Please install Python 3 (homebrew: brew install python)"
  exit 1
fi

# Use .venv in repo root
if [ ! -d ".venv" ]; then
  echo "Creating venv in .venv"
  "$PY" -m venv .venv
fi

# Activate and install
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

cat <<'EOF'
Done. To run the session generator (interactive login), run:

# Activate venv (if not already active)
source .venv/bin/activate
# Then run the script
python generate_session.py

You will be prompted for the Telegram login code and possibly 2FA password.
The script will print SESSION_STRING and save it to .session_string
EOF
