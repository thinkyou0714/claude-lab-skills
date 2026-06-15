# lab-skills — THINK YOU LAB Thinking-OS Skill Repository

[![CI](https://github.com/thinkyou0714/claude-lab-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/thinkyou0714/claude-lab-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

> 日本語版は [README.md](./README.md) を参照 / Japanese version: [README.md](./README.md)

## Overview

`lab-skills` is a repository of reusable **decision-quality assets** that make up the
"Thinking OS" of THINK YOU LAB.

Instead of offloading thinking to an AI, it accumulates **issue framing, review lenses, and
decision materials** as reusable units (Skills) that are portable across tools
(Claude Code / Cursor / ChatGPT / Codex).

## Structure (4-layer model)

```text
src/        --- Source of Truth (canonical, language-neutral knowledge)
  └─ lab-core/, lab-strategy/, lab-data-auth/ ...

Plugin      --- Domain package (e.g. lab-thinking-core)
  └─ Skill  --- Reusable unit that raises decision quality (references src/)
       └─ Command --- Thin, tool-specific entry point (Claude Code / Cursor)
```

> Note: [docs/architecture.md](./docs/architecture.md) describes the same hierarchy as 3 layers
> (SoT / adapter / tool entry point). It is the same structure at a different granularity
> (the 4-layer Plugin + Skill map to the 3-layer "adapter" layer).

### Principles

- **Source of Truth lives in `src/`**: tool-specific folders (`.claude/`, `.cursor/`) are not the truth.
- **Skills are noun phrases**: `issue-framing`, `risk-scan` — responsibilities.
- **Commands are verb phrases**: `/think`, `/automation-review` — actions.
- **1 Skill = 1 responsibility**; cross-plugin references are minimized.
- **Never fill specs by guessing**: when inputs are missing, say so explicitly.

## Plugins (6 plugins / 41 skills)

| Plugin | Responsibility | Skills | Command |
|---|---|---|---|
| [lab-thinking-core](./lab-thinking-core/) | Issue framing, assumption audit, decision support | 8 | `/think` |
| [lab-strategy-design](./lab-strategy-design/) | Goal validation, alternatives, scope, value/pricing/differentiation, assessment | 7 | `/strategy` `/strategy-review` |
| [lab-automation-architecture](./lab-automation-architecture/) | Automation feasibility, flow & failure design | 7 | `/automation-review` |
| [lab-data-auth-ops](./lab-data-auth-ops/) | Data modeling, auth boundary, PII, audit log, access control | 6 | `/data-review` |
| [lab-implementation-flow](./lab-implementation-flow/) | Implementation gate, impact scan, handoff | 7 | `/impl-gate` |
| [lab-communication-translation](./lab-communication-translation/) | Non-engineer translation, doc reuse, knowledge capture | 6 | `/translate` |

## Install (Claude Code)

```text
# Add this repository as a plugin marketplace
/plugin marketplace add thinkyou0714/claude-lab-skills

# Install a plugin (e.g. the thinking core)
/plugin install lab-thinking-core@lab-skills
```

You can also reference any `SKILL.md` directly, or copy a command from
`<plugin>/.claude/commands/` into your own `.claude/commands/`.

## Source of Truth (`src/`)

- `src/lab-core/` — shared foundation (glossary, judgment gates, anti-patterns, cost comparison)
- `src/lab-strategy/` — strategy design principles & references
- `src/lab-data-auth/` — data & auth design principles, PII classification

Search the knowledge base:

```text
python src/lab-core/scripts/search.py "judgment gate"
```

## Quality gates

Every change is verified by `validate_plugins.py --strict` (schema, internal links, skill
cross-references, naming, manifests) plus `pytest`, `ruff`, `markdownlint`, and `codespell`,
run on CI across Python 3.9–3.14. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Related docs

- [docs/architecture.md](./docs/architecture.md) — design philosophy
- [docs/PORTING.md](./docs/PORTING.md) — port a skill to other tools (Cursor / ChatGPT / Codex)
- [docs/DECISIONS.md](./docs/DECISIONS.md) — architecture decision records
- [CONTRIBUTING.md](./CONTRIBUTING.md) — how to add skills
- [CHANGELOG.md](./CHANGELOG.md)
