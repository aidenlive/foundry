#!/usr/bin/env bash
# Bootstrap a local Foundry development environment.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -m venv .venv
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -e "./cli[dev]"

echo "==> toolchain"
.venv/bin/foundry doctor || true

echo
echo "==> next steps"
echo "  source .venv/bin/activate"
echo "  foundry validate"
echo "  foundry config render --project demo --environment dev"
