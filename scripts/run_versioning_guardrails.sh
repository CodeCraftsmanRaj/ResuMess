#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[guardrail] Running versioning regression tests..."
uv run pytest tests/versioning -q

echo "[guardrail] Running security guardrail tests..."
uv run pytest tests/security -q

echo "[guardrail] All versioning guardrails passed."
