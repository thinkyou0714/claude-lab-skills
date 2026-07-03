#!/bin/sh
# Idempotent dev-tooling bootstrap for Claude Code (local + web/cloud sessions).
# Runtime deps: NONE (stdlib only) — the skills run without install. This only fetches the
# dev tools (ruff/pytest/mypy/codespell) needed for `make check`. No-op once ruff is present.
dir="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$dir" || exit 0

if [ -f pyproject.toml ] && ! command -v ruff >/dev/null 2>&1; then
  if command -v uv >/dev/null 2>&1; then
    uv pip install --system -e ".[dev]" 2>/dev/null || pip install -e ".[dev]" 2>/dev/null || true
  else
    pip install -e ".[dev]" 2>/dev/null || true
  fi
fi

exit 0
