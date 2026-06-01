# lab-data-auth-ops

> 日本語: [README.md](./README.md)

Data design, auth boundaries, PII, audit logging, access control, and data-layer rollback plugin.
Frames "who can access what under which conditions, and can it be traced and recovered afterward."

## Command

- [`/data-review`](./.claude/commands/data-review.md) — applies skills from `data-model-review` to `rollback-readiness` as needed

## Skills (6)

| Skill | Responsibility |
|---|---|
| [`data-model-review`](./skills/data-model-review/SKILL.md) | Review schema for normalization / integrity / extensibility / permission boundaries |
| [`auth-boundary-check`](./skills/auth-boundary-check/SKILL.md) | Check authn/authz boundaries for gaps and over-grants |
| [`access-control-matrix`](./skills/access-control-matrix/SKILL.md) | Design role × resource × operation access control as a matrix |
| [`pii-handling-review`](./skills/pii-handling-review/SKILL.md) | Review PII collection-to-deletion against minimization and protection |
| [`audit-log-design`](./skills/audit-log-design/SKILL.md) | Design audit logs that trace who did what, when |
| [`rollback-readiness`](./skills/rollback-readiness/SKILL.md) | Confirm data-layer changes can be safely rolled back on failure |

## Install

```text
/plugin marketplace add thinkyou0714/claude-lab-skills
/plugin install lab-data-auth-ops@lab-skills
```

See [repository README](../README.en.md) / [CONTRIBUTING](../CONTRIBUTING.md).
