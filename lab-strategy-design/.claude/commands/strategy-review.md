---
description: "実行中の戦略・施策を査定する。当初前提と実績の差分から、継続・転換（ピボット）・撤退の判断材料を整える。"
argument-hint: "<査定したい施策・当初前提・現在の実績>"
allowed-tools: Read,Grep
---

この command が使う skills:

- strategy-assessment: ../../skills/strategy-assessment/SKILL.md
- goal-validation: ../../skills/goal-validation/SKILL.md

## 手順

1. `strategy-assessment` を読み込み、当初前提と実績の差分を整理する
2. 必要に応じて `goal-validation` を読み込み、当初目標が今も妥当かを再検証する
3. 継続・転換・撤退それぞれの将来コストと期待値を整理する
4. サンクコストを判断から切り離す
5. 最終判断は人間に委ねる

## 出力の優先度

- 「どの Skill を適用したか / しなかったか」を冒頭に明示する
- 継続 / 転換 / 撤退の「推奨 / 条件付き / 非推奨」を判断材料として出力する

## Guardrails

- サンクコストを継続理由にしない
- 撤退・転換の発動基準を曖昧にしない（数値で）
- 最終判断は人間に委ねる
