# lab-thinking-core

論点整理・前提検証・意思決定支援を行う思考コアプラグイン。
曖昧な相談を判断材料へ分解し、**最終判断を人間が下せる状態**にする。

## Command

- [`/think`](./.claude/commands/think.md) — `issue-framing` から `decision-materials` まで、問いに応じて必要な Skill を順に適用する

## Skills（8）

| Skill | 責務 |
|---|---|
| [`issue-framing`](./skills/issue-framing/SKILL.md) | 曖昧な相談を論点・目的・成功条件・失敗条件・制約に分解して判断材料を揃える |
| [`assumption-audit`](./skills/assumption-audit/SKILL.md) | 設計・計画に埋め込まれた前提を洗い出し、未検証の前提が判断を歪めていないか確認する |
| [`boundary-check`](./skills/boundary-check/SKILL.md) | スコープの境界（やる/やらない/後回し）を明確にし、スコープクリープを防ぐ |
| [`risk-scan`](./skills/risk-scan/SKILL.md) | 見落としがちなリスクを体系的にスキャンする |
| [`tradeoff-analysis`](./skills/tradeoff-analysis/SKILL.md) | 複数の選択肢のトレードオフを多軸で比較し、得るもの・失うものを明示する |
| [`critique-panel`](./skills/critique-panel/SKILL.md) | 複数の視点から批判的検討を行い、死角と改善余地を可視化する |
| [`success-failure-criteria`](./skills/success-failure-criteria/SKILL.md) | 成功条件・失敗条件を測定可能な形で定義する |
| [`decision-materials`](./skills/decision-materials/SKILL.md) | 論点・選択肢・コスト・リスクを一枚の判断シートに整理する |

## インストール

```
/plugin marketplace add thinkyou0714/claude-lab-skills
/plugin install lab-thinking-core@lab-skills
```

詳細は [リポジトリ README](../README.md) / [CONTRIBUTING](../CONTRIBUTING.md) を参照。
