# lab-strategy-design

> 日本語: [README.md](./README.md)

Business strategy design plugin: goal validation, alternatives comparison, scope design,
value / pricing / differentiation, and assessment of in-flight strategy.
Frames "where to focus, what to drop, how to differentiate" as decision materials.

## Command

- [`/strategy`](./.claude/commands/strategy.md) — applies strategy-design skills from `goal-validation` to `alternative-comparison`
- [`/strategy-review`](./.claude/commands/strategy-review.md) — assesses in-flight strategy (continue / pivot / exit) via `strategy-assessment`

## Skills (7)

| Skill | Responsibility |
|---|---|
| [`goal-validation`](./skills/goal-validation/SKILL.md) | Verify goals (KGI/KPI) align with higher purpose and are measurable |
| [`alternative-comparison`](./skills/alternative-comparison/SKILL.md) | Compare options across cost / risk / exit-ease |
| [`scope-design`](./skills/scope-design/SKILL.md) | Design strategic scope: where to concentrate and what to drop |
| [`value-proposition-check`](./skills/value-proposition-check/SKILL.md) | Verify the value proposition lands against customer problems and alternatives |
| [`pricing-rationale`](./skills/pricing-rationale/SKILL.md) | Ground pricing in value / cost / competitor bases |
| [`competitive-avoidance`](./skills/competitive-avoidance/SKILL.md) | Avoid head-on competition; design hard-to-imitate differentiation |
| [`strategy-assessment`](./skills/strategy-assessment/SKILL.md) | Assess in-flight strategy from premise-vs-actual gaps |

## Install

```text
/plugin marketplace add thinkyou0714/claude-lab-skills
/plugin install lab-strategy-design@lab-skills
```

See [repository README](../README.en.md) / [CONTRIBUTING](../CONTRIBUTING.md).
