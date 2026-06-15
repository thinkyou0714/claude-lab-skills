# CONTRIBUTING — adding/changing lab-skills

> 日本語: [CONTRIBUTING.md](./CONTRIBUTING.md)
> Code of Conduct: [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) (Contributor Covenant v2.1)
> Releasing & versioning: [RELEASING.md](./RELEASING.md)

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

2. Fill in `description` (responsibility + when-to-use trigger, e.g. *"Decompose a vague
   request into issues / goals / success criteria. Use at the requirements/design phase."*)
   and every section. The single source of truth for the template is
   [`src/lab-core/templates/skill-template.md`](./src/lab-core/templates/skill-template.md)
   (ADR-007); `new_skill.py` generates from it. The 10 required sections (do not reorder —
   the validator checks order and empty bodies) are: Purpose, Use When, Inputs, Output Contract,
   Review Lens, Instructions, Guardrails, LAB Cross-Check, Handoff Notes, Further Reading.
3. Reference the relevant Source of Truth under `src/` from "Further Reading".
4. Update the plugin `README.md` (and `README.en.md`) skill table, then regenerate the catalog
   with `make catalog` (or `python src/lab-core/scripts/gen_catalog.py`).

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

- `python validate_plugins.py --strict` (schema, internal links, skill cross-references, naming,
  manifests, section order/non-empty bodies, README count consistency)
- `pytest`, `ruff check .`, `mypy`, `markdownlint`, `codespell`

Skill quality checklist (do not add a skill that fails these):

- [ ] Clear issue, explicit rationale, articulated risks
- [ ] Realistic improvement options; decision materials assembled
- [ ] LAB-wide consistency explained; human decision room preserved
- [ ] `Guardrails` and `LAB Cross-Check` sections present (not dropped)
- [ ] No personal names / internal code names / private paths (GATE-3)
- [ ] Updated the plugin `README.md`; `validate_plugins.py --strict` is green

## Prohibited

- Do not copy an existing skill and stop there (no real specialization).
- Do not mass-produce commands (skills come first).
- Do not write Claude-specific details into `SKILL.md` (isolate them in the command layer).
- Do not drop `Guardrails` / `LAB Cross-Check`.
- Do not mass-produce skills without a `README.md`.

See [docs/DECISIONS.md](./docs/DECISIONS.md) for design decisions and
[docs/PORTING.md](./docs/PORTING.md) for porting skills to other tools.
