# lab-automation-architecture

> 日本語: [README.md](./README.md)

Automation feasibility, flow design, and failure design plugin.
Lets you decide "should this be automated?" and "would we notice if it broke?" before building.

## Command

- [`/automation-review`](./.claude/commands/automation-review.md) — applies skills from `automation-feasibility` to `monitoring-alert-design`

## Skills (7)

| Skill | Responsibility |
|---|---|
| [`automation-feasibility`](./skills/automation-feasibility/SKILL.md) | Judge whether/when to automate from cost / ROI / risk / dependencies |
| [`manual-vs-automation-cost`](./skills/manual-vs-automation-cost/SKILL.md) | Compare total cost of manual vs automated; compute payback |
| [`trigger-action-map`](./skills/trigger-action-map/SKILL.md) | Map triggers / actions / branches / error handling; find gaps |
| [`failure-point-review`](./skills/failure-point-review/SKILL.md) | Enumerate failure points by impact and detectability |
| [`retry-idempotency-check`](./skills/retry-idempotency-check/SKILL.md) | Verify retry design and idempotency to prevent double-execution damage |
| [`monitoring-alert-design`](./skills/monitoring-alert-design/SKILL.md) | Design monitoring items, alert thresholds, recipients, and first response |
| [`agmsg`](./skills/agmsg/SKILL.md) | Wire Claude Code ↔ Codex via a shared SQLite mailbox to remove human copy-paste between agents (upstream: fujibee/agmsg, MIT) |

## Install

```text
/plugin marketplace add thinkyou0714/claude-lab-skills
/plugin install lab-automation-architecture@lab-skills
```

See [repository README](../README.en.md) / [CONTRIBUTING](../CONTRIBUTING.md).
