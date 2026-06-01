# Skill テンプレート — lab-core

_新しい Skill を作るときはこのテンプレートをコピーして使う。_
_各セクションの削除・省略は禁止。不明な場合は `(未定)` と書く。_

---

_frontmatter は `name` と `description` の2つを必須とする（`validate_plugins.py` がこの2つを検証する）。_
_`name` はディレクトリ名と一致させ、kebab-case（`^[a-z0-9]+(-[a-z0-9]+)*$`）で書く。_

```markdown
---
name: <skill-name>
description: "<1〜2文で責務を説明。使う場面を含めること>"
---

## Purpose

このスキルが解決する問題を1〜2文で説明する。
「〜のリスクを防ぐ」「〜を判断できる状態にする」の形式で書く。

## Use When

- どんな場面で使うか（箇条書き）
- 具体的なトリガーを書く

## Inputs

以下を準備すること。不足している場合は推測せず、不足を明示する。

- **必須項目1**: 説明
- **必須項目2**: 説明
- **任意項目**: 説明（任意）

## Output Contract

以下の順で出力すること。順序を変えない。

1. **項目1**: 内容
2. **項目2**: 内容
3. **判断材料**: 次のアクションを選ぶために人間が確認すべき情報

## Review Lens

出力をレビューする観点。

- 論点は明確か
- 根拠は明示されているか
- リスクが言語化されているか
- 将来の拡張余地があるか

## Instructions

ステップバイステップの手順（AIへの指示として書く）。

1. まず〜を確認する
2. 次に〜を整理する
3. 最後に〜を出力する

## Guardrails

このスキルを使うときに「してはいけないこと」。

- 推測で仕様を埋めない
- 判断を AI に委ねない（最終判断は人間）
- スコープ外の話題に脱線しない

## LAB Cross-Check

このスキルの出力を他の観点でクロスチェックするとき参照するもの。

- `src/lab-core/rules/judgment-gates.md` — 判断ゲートとの整合性
- `src/lab-core/rules/antipatterns.md` — アンチパターンに該当しないか

## Handoff Notes

このスキルの出力を次のフェーズへ渡すときの注意。

- 渡す先のスキル/ツール: (例: issue-framing → risk-scan → implementation-gate)
- 渡す形式: (例: Markdown / JSON)

## Further Reading

- `src/<plugin-name>/data/<関連データ>.md`
- (外部リンクは公開情報のみ)
```
