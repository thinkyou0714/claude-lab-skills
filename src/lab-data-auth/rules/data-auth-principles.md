# データ・認証設計の原則 — lab-data-auth

_`lab-data-auth-ops` プラグインの6スキルが derive する正本（Source of Truth）。_
_スキル本文で原則がぶれたらここを正とする。_

---

## 中核原則

1. **最小権限（least privilege）**: 役割には業務に必要な最小の権限だけを与える。「とりあえず管理者」を許容しない（`auth-boundary-check` / `access-control-matrix`）。
2. **最小収集（data minimization）**: 個人情報は目的に必要な項目だけ集める。「念のため」を許容しない（`pii-handling-review`）。
3. **サーバ側で境界を担保**: 認可を UI 制御だけに頼らない。サーバ・行レベルで強制する（`auth-boundary-check`）。
4. **監査は 5W1H・追記専用**: 重要操作は「誰が・いつ・何を」を改ざんできない形で記録する（`audit-log-design`）。
5. **PII をログ・URL・通知に出さない**: ログや例外通知に生の個人情報・秘密情報を残さない。
6. **データ変更は可逆性を確認してから**: バックアップ・後方互換手順・ロールバック基準なしに本番データを変えない（`rollback-readiness`）。
7. **整合性は制約で守る**: 一意・外部キー・NOT NULL を「今動くから」で省略しない（`data-model-review`）。

---

## 判断の前提

- 不明なデータ要件・権限要件は推測で埋めず、確認事項として明示する。
- 公開・共有の前に PII の混入を点検する（[judgment-gates.md](../../lab-core/rules/judgment-gates.md) GATE-3）。
- 設計の最終確定・データ変更の実行可否は人間が判断する。

---

## このルールを参照するスキル

- [auth-boundary-check](../../../lab-data-auth-ops/skills/auth-boundary-check/SKILL.md)
- [pii-handling-review](../../../lab-data-auth-ops/skills/pii-handling-review/SKILL.md)
- [audit-log-design](../../../lab-data-auth-ops/skills/audit-log-design/SKILL.md)
- [rollback-readiness](../../../lab-data-auth-ops/skills/rollback-readiness/SKILL.md)

## 参照

- [pii-classification.md](../data/pii-classification.md) — PII 機微度の分類
- [judgment-gates.md](../../lab-core/rules/judgment-gates.md) — 共通の判断ゲート
