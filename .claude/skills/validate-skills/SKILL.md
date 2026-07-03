---
name: validate-skills
description: Validate the skill packs and run repo checks (structure, lint, types, tests). Use when asked to validate skills, check the repo, or verify a new/edited SKILL.md.
---

Validate this skills repository and report results concisely.

1. Ensure dev tooling is present (the SessionStart bootstrap installs `[dev]` extras; else `make install`).
2. Run `make validate` first (plugin/skill structure + SKILL.md frontmatter). For the full gate: `make check` (validate + lint + typecheck + test) and `make check-docs` (markdown lint + spell).
3. Summarize: which checks passed/failed, and for each failure the offending skill/file + the first error line.
4. Do not edit skill content unless asked; when adding/fixing a SKILL.md, follow `CONTRIBUTING.md` naming + frontmatter rules.
