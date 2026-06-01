# lab-implementation-flow

> English: [README.en.md](./README.en.md)

実装着手ゲート・影響範囲スキャン・施工AIへの handoff を担うプラグイン。
「実装に入ってよい状態か」を点検し、通過後に実行可能な指示書へ変換する。

## Command

- [`/impl-gate`](./.claude/commands/impl-gate.md) — `implementation-gate` から `cursor-handoff` まで、必要な Skill を順に適用する（ゲートがブロックなら即停止）

## Skills（7）

| Skill | 責務 |
|---|---|
| [`implementation-gate`](./skills/implementation-gate/SKILL.md) | 要件・設計・影響範囲・ロールバック方針が揃っているかを一括チェックする |
| [`change-impact-scan`](./skills/change-impact-scan/SKILL.md) | 変更が波及する範囲（直接・依存・副作用）を洗い出す |
| [`test-scope-definition`](./skills/test-scope-definition/SKILL.md) | 何をどこまでテストするか（種別・対象・合否基準）を定義する |
| [`rollback-plan`](./skills/rollback-plan/SKILL.md) | 失敗時に元へ戻す手順（何を・どの順序で・どこまで）を設計する |
| [`patch-readiness`](./skills/patch-readiness/SKILL.md) | パッチ/ホットフィックスを安全に適用できる状態かを確認する |
| [`repo-structure-review`](./skills/repo-structure-review/SKILL.md) | ディレクトリ構造・命名・配置が設計原則と整合しているかをレビューする |
| [`cursor-handoff`](./skills/cursor-handoff/SKILL.md) | ゲート通過後の情報を施工AIが実行可能な指示書へ変換する |

## インストール

```text
/plugin marketplace add thinkyou0714/claude-lab-skills
/plugin install lab-implementation-flow@lab-skills
```

詳細は [リポジトリ README](../README.md) / [CONTRIBUTING](../CONTRIBUTING.md) を参照。
