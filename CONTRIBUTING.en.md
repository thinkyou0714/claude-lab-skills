# CONTRIBUTING — adding/changing lab-skills

> 日本語: [CONTRIBUTING.md](./CONTRIBUTING.md)

## Stance

- Build skills that **assemble decision materials**, not ones that "give the answer".
- Never fill specs by guessing; state missing inputs explicitly.
- 1 Skill = 1 responsibility; minimize cross-plugin references.
- Keep Claude-specific concerns in commands or supporting docs, not in `SKILL.md`.
- The final decision is left to a human.

## Naming

- **Skill** = noun phrase, kebab-case (`issue-framing`, `risk-scan`). The `name:` field must match the directory name and the pattern `^[a-z0-9]+(-[a-z0-9]+)*$`.
- **Command** = verb phrase (`/think`, `/automation-review`).
- **Plugin** = `lab-<domain>` prefix.

## Adding a skill

1. Scaffold from the template:

   ```text
   python src/lab-core/scripts/new_skill.py <plugin> <skill-name>
   ```

2. Fill in `description` (responsibility + when-to-use trigger) and every section.
   The 10 required sections are: Purpose, Use When, Inputs, Output Contract, Review Lens,
   Instructions, Guardrails, LAB Cross-Check, Handoff Notes, Further Reading.
3. Reference the relevant Source of Truth under `src/` from "Further Reading".
4. Update the plugin `README.md` (and `README.en.md`) skill table.

## Command format

```text
---
description: "<one-line summary>"
argument-hint: "<argument hint>"
allowed-tools: Read,Grep
---

skills used by this command:
- <skill-name>: <relative path to SKILL.md>
```

## Quality gates

A change is accepted only when the following are green:

- `python validate_plugins.py --strict` (schema, internal links, skill cross-references, naming, manifests)
- `pytest`, `ruff check .`, `markdownlint`, `codespell`

No personal names or internal code names (GATE-3). See [docs/DECISIONS.md](./docs/DECISIONS.md) for design decisions.
