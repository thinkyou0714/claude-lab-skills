# AGENTS.md — claude-lab-skills

THINK YOU LAB 思考OS — 再利用可能な判断資産 (Skill) の公開リポジトリ。Claude Code plugin として
配布 (`.claude-plugin/`)。技術非依存の思考・設計 Skill 群。

- **Stack**: Python `>=3.9` (ランタイム依存なし = 標準ライブラリのみ)。dev ツールは `[dev]` extra (ruff/pytest/mypy/codespell)。
- **Skill packs**: `lab-thinking-core` / `lab-strategy-design` / `lab-automation-architecture` / `lab-communication-translation` / `lab-data-auth-ops` / `lab-implementation-flow`。
- **Setup**: dev ツールは `.claude/bootstrap.sh` (SessionStart) が `make install` 相当で導入 (Skill 実行自体は install 不要)。手動: `make install`。
- **Checks**: `make check` (= validate + lint + typecheck + test) · `make check-docs` (lint-md + spell) · `make validate` (plugin 構造検証)。
- **Skill 追加規則**: `CONTRIBUTING.md`。命名・frontmatter 規約はそこが正本。

## Claude Code on the web
A cloud session auto-installs dev tooling (SessionStart hook) and loads this `AGENTS.md` +
`.claude/skills/`. The skill packs themselves ship via the `.claude-plugin/` marketplace.
MCP is local-only. See `thinkyou0714/.github` → `docs/claude-code-web-readiness.md`.
