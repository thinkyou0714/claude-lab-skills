# lab-communication-translation

> 日本語: [README.md](./README.md)

Non-engineer translation, summary structuring, doc reusability, LLM portability, and knowledge capture plugin.
Converts technical content into a form fit for the audience to smooth decisions and handoffs.

## Command

- [`/translate`](./.claude/commands/translate.md) — applies skills based on intent (non-engineer explanation / summary / quality check / LLM portability)

## Skills (6)

| Skill | Responsibility |
|---|---|
| [`stakeholder-translation`](./skills/stakeholder-translation/SKILL.md) | Translate technical content for non-engineers (What / Impact / Need / Deadline) |
| [`summary-structuring`](./skills/summary-structuring/SKILL.md) | Summarize long text by purpose (decision / handoff / record) |
| [`onboarding-readability`](./skills/onboarding-readability/SKILL.md) | Evaluate readability for first-time readers (premises / terms / structure / flow) |
| [`reusable-doc-structure`](./skills/reusable-doc-structure/SKILL.md) | Design reusable doc structures that withstand changing purpose / audience |
| [`llm-portability-review`](./skills/llm-portability-review/SKILL.md) | Detect Claude-specific dependencies; assess portability to other LLMs |
| [`knowledge-capture`](./skills/knowledge-capture/SKILL.md) | Turn decisions / rejections / learnings into structured drafts for DECISIONS / CONTEXT |

## Install

```text
/plugin marketplace add thinkyou0714/claude-lab-skills
/plugin install lab-communication-translation@lab-skills
```

See [repository README](../README.en.md) / [CONTRIBUTING](../CONTRIBUTING.md).
