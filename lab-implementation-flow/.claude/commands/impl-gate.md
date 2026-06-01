---
description: "実装着手前のゲートチェックから施工AI への handoff までを一貫して実行する。タスク概要・要件・対象ファイルを渡すと、implementation-gate から cursor-handoff まで必要な Skill を順に適用する。"
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
- cursor-handoff: ../../skills/cursor-handoff/SKILL.md

## 手順

1. `implementation-gate` を読み込み、実装着手前のゲートチェックを実行する（要件・影響・ロールバック方針の確認）
2. ゲートが「ブロック」の場合: 不足情報を明示して終了する（Step 3 以降に進まない）
3. `change-impact-scan` を読み込み、変更の波及範囲を洗い出す（直接・依存・副作用の3分類）
4. `test-scope-definition` を読み込み、テストスコープ・合否基準を定義する
5. `rollback-plan` を読み込み、失敗時のロールバック手順を設計する
6. 必要に応じて `patch-readiness` を読み込み、パッチ適用前の準備を確認する
7. 必要に応じて `repo-structure-review` を読み込み、実装対象のディレクトリ構造を確認する
8. ゲートが「着手可」の場合: `cursor-handoff` を読み込み、施工AI向けの実行可能な指示書を生成する
9. 最終判断は人間に委ねる

## 出力の優先度

- `implementation-gate` でブロックが宣言された場合は即座に止まる（Step 3 以降に進まない）
- 「どの Skill を適用したか / しなかったか」を冒頭に明示する
- 最終出力として `cursor-handoff` が生成した指示書を末尾に提示する

## Guardrails

- ゲートを通過させるために評価を甘くしない
- ロールバック方針が未定義のまま `cursor-handoff` に進まない
- 影響範囲が「不明」の場合は必ず注意/NG として指摘する
- `cursor-handoff` の指示書を確認せずに施工AIに委譲することを推奨しない
