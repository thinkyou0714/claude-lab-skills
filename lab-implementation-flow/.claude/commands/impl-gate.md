---
description: "実装着手前のゲートチェックから handoff までを一貫して実行する。タスク概要・要件・対象ファイルを渡すと、implementation-gate から rollback-plan まで必要な Skill を順に適用する。"
argument-hint: "<タスク概要・要件・対象ファイル・影響範囲>"
allowed-tools: Read,Grep
---

この command が使う skills:
- implementation-gate: ../../skills/implementation-gate/SKILL.md
- change-impact-scan: ../../skills/change-impact-scan/SKILL.md
- test-scope-definition: ../../skills/test-scope-definition/SKILL.md
- rollback-plan: ../../skills/rollback-plan/SKILL.md
- patch-readiness: ../../skills/patch-readiness/SKILL.md
- repo-structure-review: ../../skills/repo-structure-review/SKILL.md

## 手順

1. `implementation-gate` を読み込み、実装着手前のゲートチェックを実行する（要件・影響・ロールバック方針の確認）
2. ゲートが「ブロック」の場合: 不足情報を明示して終了する（Step 3 以降に進まない）
3. `change-impact-scan` を読み込み、変更の波及範囲を洗い出す（直接・依存・副作用の3分類）
4. `test-scope-definition` を読み込み、テストスコープ・合否基準を定義する
5. `rollback-plan` を読み込み、失敗時のロールバック手順を設計する
6. 必要に応じて `patch-readiness` を読み込み、パッチ適用前の準備を確認する
7. 必要に応じて `repo-structure-review` を読み込み、実装対象のディレクトリ構造を確認する
8. 最終判断は人間に委ねる

## 出力の優先度

- `implementation-gate` でブロックが宣言された場合は即座に止まる
- 「どの Skill を適用したか / しなかったか」を冒頭に明示する
- 施工AI への handoff に必要な情報（要件・範囲・ロールバック方針）をまとめて出力する

## Guardrails

- ゲートを通過させるために評価を甘くしない
- ロールバック方針が未定義のまま実装を推奨しない
- 影響範囲が「不明」の場合は必ず注意/NG として指摘する
