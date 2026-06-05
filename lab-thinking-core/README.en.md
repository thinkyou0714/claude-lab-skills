# lab-thinking-core

> 日本語: [README.md](./README.md)

Thinking-core plugin for issue framing, assumption auditing, and decision support.
Breaks down vague problems into decision materials so a **human can make the final call**.

## Command

- [`/think`](./.claude/commands/think.md) — applies skills from `issue-framing` to `decision-materials` as needed

## Skills (8)

| Skill | Responsibility |
|---|---|
| [`issue-framing`](./skills/issue-framing/SKILL.md) | Decompose a vague request into issue / goal / success & failure criteria / constraints |
| [`assumption-audit`](./skills/assumption-audit/SKILL.md) | Surface embedded assumptions and check for unverified premises |
| [`boundary-check`](./skills/boundary-check/SKILL.md) | Clarify scope boundaries (in / out / deferred) and prevent scope creep |
| [`risk-scan`](./skills/risk-scan/SKILL.md) | Systematically scan for overlooked risks |
| [`tradeoff-analysis`](./skills/tradeoff-analysis/SKILL.md) | Compare options across axes; make gains and losses explicit |
| [`critique-panel`](./skills/critique-panel/SKILL.md) | Apply multiple critical viewpoints to expose blind spots |
| [`success-failure-criteria`](./skills/success-failure-criteria/SKILL.md) | Define measurable success and failure criteria |
| [`decision-materials`](./skills/decision-materials/SKILL.md) | Assemble issues / options / cost / risk into one decision sheet |

## Install

```text
/plugin marketplace add thinkyou0714/claude-lab-skills
/plugin install lab-thinking-core@lab-skills
```

See [repository README](../README.en.md) / [CONTRIBUTING](../CONTRIBUTING.md).
