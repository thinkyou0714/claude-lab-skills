# lab-strategy-design

> English: [README.en.md](./README.en.md)

目標検証・代替案比較・スコープ設計・提供価値/価格/差別化・実行中戦略の査定を行う事業設計プラグイン。
「どこに集中し、何を捨て、どう差別化するか」を、判断材料として整える。

## Command

- [`/strategy`](./.claude/commands/strategy.md) — `goal-validation` から `alternative-comparison` まで、戦略設計の Skill を順に適用する
- [`/strategy-review`](./.claude/commands/strategy-review.md) — `strategy-assessment` で実行中の戦略を査定し、継続/転換/撤退の判断材料を整える

## Skills（7）

| Skill | 責務 |
|---|---|
| [`goal-validation`](./skills/goal-validation/SKILL.md) | 目標（KGI/KPI）が上位目的と整合し測定可能かを検証する |
| [`alternative-comparison`](./skills/alternative-comparison/SKILL.md) | 複数の選択肢を多軸（コスト・リスク・撤退容易性）で比較する |
| [`scope-design`](./skills/scope-design/SKILL.md) | 戦略的スコープ（集中する領域と捨てる領域）を設計する |
| [`value-proposition-check`](./skills/value-proposition-check/SKILL.md) | 提供価値が顧客課題・代替手段に対して刺さるか検証する |
| [`pricing-rationale`](./skills/pricing-rationale/SKILL.md) | 価値・コスト・競合の3基準で価格の根拠を整理する |
| [`competitive-avoidance`](./skills/competitive-avoidance/SKILL.md) | 正面競争を避け、模倣されにくい差別化を設計する |
| [`strategy-assessment`](./skills/strategy-assessment/SKILL.md) | 実行中戦略を前提-実績差分から査定し継続/転換/撤退を判断する |

## インストール

```text
/plugin marketplace add thinkyou0714/claude-lab-skills
/plugin install lab-strategy-design@lab-skills
```

詳細は [リポジトリ README](../README.md) / [CONTRIBUTING](../CONTRIBUTING.md) を参照。
