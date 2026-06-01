# lab-automation-architecture

自動化の可否判断・フロー設計・障害設計を行うプラグイン。
「自動化すべきか」「止まったら気づけるか」を、実装前に判断できる状態にする。

## Command

- [`/automation-review`](./.claude/commands/automation-review.md) — `automation-feasibility` から `monitoring-alert-design` まで、必要な Skill を順に適用する

## Skills（6）

| Skill | 責務 |
|---|---|
| [`automation-feasibility`](./skills/automation-feasibility/SKILL.md) | 自動化できるか・すべきかを、コスト/ROI/リスク/依存性から判断する |
| [`manual-vs-automation-cost`](./skills/manual-vs-automation-cost/SKILL.md) | 手動と自動化の総コストを比較し、回収期間・損益分岐点を算出する |
| [`trigger-action-map`](./skills/trigger-action-map/SKILL.md) | トリガー・アクション・条件分岐・エラー処理を可視化し、抜け漏れを確認する |
| [`failure-point-review`](./skills/failure-point-review/SKILL.md) | 障害点を体系的に列挙し、影響度・検知可能性・対応方針を整理する |
| [`retry-idempotency-check`](./skills/retry-idempotency-check/SKILL.md) | リトライ設計とべき等性を確認し、二重実行による破損を防ぐ |
| [`monitoring-alert-design`](./skills/monitoring-alert-design/SKILL.md) | 監視項目・アラート条件・通知先・初動手順を設計する |

## インストール

```text
/plugin marketplace add thinkyou0714/claude-lab-skills
/plugin install lab-automation-architecture@lab-skills
```

詳細は [リポジトリ README](../README.md) / [CONTRIBUTING](../CONTRIBUTING.md) を参照。
