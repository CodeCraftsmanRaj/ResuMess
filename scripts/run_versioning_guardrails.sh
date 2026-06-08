#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[guardrail] Running versioning regression tests..."
python -m pytest tests/versioning -q

echo "[guardrail] Running security guardrail tests..."
python -m pytest tests/security -q

echo "[guardrail] All versioning guardrails passed."
