---
description: "事業・施策の戦略設計を支援する。目標検証からスコープ・価値・差別化・価格・代替案比較まで、必要な Skill を順に適用して判断材料を揃える。"
argument-hint: "<検討したい事業・施策・戦略テーマと現状>"
allowed-tools: Read,Grep
---

この command が使う skills:

- goal-validation: ../../skills/goal-validation/SKILL.md
- scope-design: ../../skills/scope-design/SKILL.md
- value-proposition-check: ../../skills/value-proposition-check/SKILL.md
- competitive-avoidance: ../../skills/competitive-avoidance/SKILL.md
- pricing-rationale: ../../skills/pricing-rationale/SKILL.md
- alternative-comparison: ../../skills/alternative-comparison/SKILL.md

## 手順

1. `goal-validation` を読み込み、目標が上位目的と整合し測定可能かを検証する
2. `scope-design` を読み込み、集中する領域と捨てる領域を設計する
3. `value-proposition-check` を読み込み、集中領域の提供価値が顧客課題に刺さるか検証する
4. `competitive-avoidance` を読み込み、模倣されにくい差別化・独自ポジションを設計する
5. 収益化を扱う場合は `pricing-rationale` を読み込み、価格の根拠を整理する
6. 複数の方向性がある場合は `alternative-comparison` を読み込み、案を多軸で比較する
7. 最終判断は人間に委ねる

## 出力の優先度

- 全 Skill を機械的に適用しない。テーマに応じて必要な Skill のみ適用する
- 「どの Skill を適用したか / しなかったか」を冒頭に明示する
- 適用しなかった Skill の理由を1行で記載する

## Guardrails

- 推測で市場・顧客の前提を埋めない。不足は明示して止まる
- 戦略を1案に閉じない。撤退容易性を含めた選択肢を残す
- コスト比較（機会コスト・撤退コスト）を省略しない
- 最終的な戦略判断は人間に委ねる
