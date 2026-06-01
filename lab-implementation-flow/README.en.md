# lab-implementation-flow

> 日本語: [README.md](./README.md)

Implementation gate, impact scan, and handoff-to-builder-AI plugin.
Checks "are we ready to implement?" and converts the result into an executable instruction set.

## Command

- [`/impl-gate`](./.claude/commands/impl-gate.md) — applies skills from `implementation-gate` to `cursor-handoff` (stops immediately if the gate blocks)

## Skills (7)

| Skill | Responsibility |
|---|---|
| [`implementation-gate`](./skills/implementation-gate/SKILL.md) | Check requirements / design / impact / rollback are ready in one pass |
| [`change-impact-scan`](./skills/change-impact-scan/SKILL.md) | Surface the blast radius (direct / dependency / side-effect) |
| [`test-scope-definition`](./skills/test-scope-definition/SKILL.md) | Define what to test and to what extent (type / target / pass criteria) |
| [`rollback-plan`](./skills/rollback-plan/SKILL.md) | Design how to revert on failure (what / order / how far) |
| [`patch-readiness`](./skills/patch-readiness/SKILL.md) | Confirm a patch/hotfix can be applied safely |
| [`repo-structure-review`](./skills/repo-structure-review/SKILL.md) | Review directory structure / naming / placement against design principles |
| [`cursor-handoff`](./skills/cursor-handoff/SKILL.md) | Convert gate-passed info into an executable instruction set for a builder AI |

## Install

```text
/plugin marketplace add thinkyou0714/claude-lab-skills
/plugin install lab-implementation-flow@lab-skills
```

See [repository README](../README.en.md) / [CONTRIBUTING](../CONTRIBUTING.md).
