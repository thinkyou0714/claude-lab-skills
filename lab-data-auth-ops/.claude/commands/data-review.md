---
description: "データ設計・認証境界・PII・監査ログ・ロールバック準備をレビューする。データ/認証に関わる設計や変更を渡すと、必要な Skill を順に適用して点検する。"
argument-hint: "<レビューしたいデータ設計・認証/権限・変更内容>"
allowed-tools: Read,Grep
---

この command が使う skills:

- data-model-review: ../../skills/data-model-review/SKILL.md
- auth-boundary-check: ../../skills/auth-boundary-check/SKILL.md
- access-control-matrix: ../../skills/access-control-matrix/SKILL.md
- pii-handling-review: ../../skills/pii-handling-review/SKILL.md
- audit-log-design: ../../skills/audit-log-design/SKILL.md
- rollback-readiness: ../../skills/rollback-readiness/SKILL.md

## 手順

1. スキーマ・データ構造が対象なら `data-model-review` を読み込み、設計を点検する
2. 認証・認可が対象なら `auth-boundary-check` を読み込み、権限境界を確認する
3. ロールが複雑な場合は `access-control-matrix` を読み込み、権限を一覧で点検する
4. 個人情報を扱う場合は `pii-handling-review` を読み込み、最小化・保護を確認する
5. 重要操作を扱う場合は `audit-log-design` を読み込み、監査ログを設計する
6. データ変更を伴う場合は `rollback-readiness` を読み込み、戻せる状態かを確認する
7. 最終判断は人間に委ねる

## 出力の優先度

- 全 Skill を機械的に適用しない。対象に応じて必要な Skill のみ適用する
- 「どの Skill を適用したか / しなかったか」を冒頭に明示する
- 公開・共有を伴う場合は PII 点検（GATE-3）を必ず含める

## Guardrails

- 推測でデータ要件・権限要件を埋めない。不足は明示して止まる
- 最小権限・最小収集の原則からの逸脱を見逃さない
- データ変更はロールバック準備の確認なしに勧めない
- 最終判断は人間に委ねる
