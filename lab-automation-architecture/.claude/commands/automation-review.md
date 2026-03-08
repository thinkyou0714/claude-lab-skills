---
description: "自動化の可否判断・フロー設計・障害設計を行う。自動化したい処理・フローを渡すと、feasibility から monitoring まで必要な Skill を順に適用する。"
argument-hint: "<自動化したい処理・フロー・現在の課題>"
allowed-tools: Read,Grep
---

この command が使う skills:
- automation-feasibility: ../../skills/automation-feasibility/SKILL.md
- manual-vs-automation-cost: ../../skills/manual-vs-automation-cost/SKILL.md
- trigger-action-map: ../../skills/trigger-action-map/SKILL.md
- failure-point-review: ../../skills/failure-point-review/SKILL.md
- retry-idempotency-check: ../../skills/retry-idempotency-check/SKILL.md
- monitoring-alert-design: ../../skills/monitoring-alert-design/SKILL.md

## 手順

1. `automation-feasibility` を読み込み、自動化の可否を評価する（技術・コスト・リスク）
2. `manual-vs-automation-cost` を読み込み、手動対応と自動化のコストを比較する
3. 自動化が妥当と判断された場合: `trigger-action-map` を読み込み、トリガー・アクション・条件を整理する
4. `failure-point-review` を読み込み、フローの障害ポイントと影響を洗い出す
5. `retry-idempotency-check` を読み込み、リトライ・冪等性の設計を確認する
6. `monitoring-alert-design` を読み込み、監視・アラートの設計を確認する
7. 最終判断は人間に委ねる

## 出力の優先度

- 自動化が不適切と判断された場合は Step 1-2 で止めて理由を明示する
- 「どの Skill を適用したか / しなかったか」を冒頭に明示する
- 自動化の「推奨 / 条件付き推奨 / 非推奨」を判断材料として出力する

## Guardrails

- 自動化を推奨する方向に評価を歪めない
- コスト比較を省略しない
- 障害時の手動復旧手順が定義できない場合は非推奨を明示する
