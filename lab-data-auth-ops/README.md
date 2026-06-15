# lab-data-auth-ops

> English: [README.en.md](./README.en.md)

データ設計・認証/認可境界・PII・監査ログ・アクセス制御・データ層ロールバックを点検するプラグイン。
「誰が・何に・どの条件でアクセスでき、後から追跡・復旧できるか」を判断材料として整える。

## Command

- [`/data-review`](./.claude/commands/data-review.md) — `data-model-review` から `rollback-readiness` まで、対象に応じて Skill を適用する

## Skills（8）

| Skill | 責務 |
|---|---|
| [`data-model-review`](./skills/data-model-review/SKILL.md) | スキーマ設計の正規化・整合性・拡張性・権限境界をレビューする |
| [`auth-system-design`](./skills/auth-system-design/SKILL.md) | 認証・アイデンティティの仕組み（方式・セッション・本人確認・回復）を設計する |
| [`auth-boundary-check`](./skills/auth-boundary-check/SKILL.md) | 認証・認可の境界（誰が何にアクセスできるか）の漏れ・過剰を点検する |
| [`access-control-matrix`](./skills/access-control-matrix/SKILL.md) | ロール × リソース × 操作のアクセス制御を一覧で体系設計する |
| [`secret-management-review`](./skills/secret-management-review/SKILL.md) | APIキー・トークン・鍵の保管・スコープ・ローテーション・漏洩対策を点検する |
| [`pii-handling-review`](./skills/pii-handling-review/SKILL.md) | 個人情報の収集〜削除を最小化・保護の原則でレビューする |
| [`audit-log-design`](./skills/audit-log-design/SKILL.md) | 「誰が・いつ・何をしたか」を追跡できる監査ログを設計する |
| [`rollback-readiness`](./skills/rollback-readiness/SKILL.md) | データ層変更を失敗時に安全に戻せる状態かを確認する |

## インストール

```text
/plugin marketplace add thinkyou0714/claude-lab-skills
/plugin install lab-data-auth-ops@lab-skills
```

詳細は [リポジトリ README](../README.md) / [CONTRIBUTING](../CONTRIBUTING.md) を参照。
