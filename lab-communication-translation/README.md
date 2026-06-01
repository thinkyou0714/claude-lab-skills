# lab-communication-translation

非エンジニア翻訳・要約構造化・ドキュメント再利用性・他LLM移植性・知識記録変換を担うプラグイン。
技術内容を「受け手に応じた形」へ変換し、判断と引き継ぎを滑らかにする。

## Command

- [`/translate`](./.claude/commands/translate.md) — 入力の目的（非エンジニア説明 / 要約 / 品質チェック / 他LLM移植）に応じて Skill を適用する

## Skills（6）

| Skill | 責務 |
|---|---|
| [`stakeholder-translation`](./skills/stakeholder-translation/SKILL.md) | 技術内容を非エンジニアが理解できる言葉（What / Impact / Need / Deadline）に変換する |
| [`summary-structuring`](./skills/summary-structuring/SKILL.md) | 長文を目的（判断用 / 引き継ぎ用 / 記録用）に応じた構造で要約する |
| [`onboarding-readability`](./skills/onboarding-readability/SKILL.md) | 初見の読み手にとっての可読性（前提・用語・構造・導線）を評価する |
| [`reusable-doc-structure`](./skills/reusable-doc-structure/SKILL.md) | 目的・読み手・更新頻度の変化に耐える再利用可能なドキュメント構造を設計する |
| [`llm-portability-review`](./skills/llm-portability-review/SKILL.md) | Claude 固有依存を検出し、他LLMへの移植耐性を評価する |
| [`knowledge-capture`](./skills/knowledge-capture/SKILL.md) | 判断・却下理由・前提変化・学びを DECISIONS / CONTEXT へ書ける構造化草稿に変換する |

## インストール

```text
/plugin marketplace add thinkyou0714/claude-lab-skills
/plugin install lab-communication-translation@lab-skills
```

詳細は [リポジトリ README](../README.md) / [CONTRIBUTING](../CONTRIBUTING.md) を参照。
