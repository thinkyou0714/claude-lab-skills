---
description: "技術内容の翻訳・要約・ドキュメント品質チェックを行う。AI の出力・技術ドキュメント・実装結果を渡すと、受け手に応じた形式で整理して出力する。"
argument-hint: "<翻訳・要約・チェックしたい内容と受け手（非エンジニア / チーム / AI引き継ぎ等）>"
allowed-tools: Read,Grep
---

この command が使う skills:
- stakeholder-translation: ../../skills/stakeholder-translation/SKILL.md
- summary-structuring: ../../skills/summary-structuring/SKILL.md
- onboarding-readability: ../../skills/onboarding-readability/SKILL.md
- reusable-doc-structure: ../../skills/reusable-doc-structure/SKILL.md
- llm-portability-review: ../../skills/llm-portability-review/SKILL.md

## 手順

1. 入力の目的を判定する:
   - 非エンジニアへの説明・報告 → Step 2 へ
   - 長文の要約・構造化 → Step 3 へ
   - ドキュメントの品質チェック → Step 4 へ
   - 他LLMへの移植準備 → Step 5 へ

2. 非エンジニア向け翻訳: `stakeholder-translation` を読み込み、What / Impact / Need / Deadline 形式で出力する
3. 要約・構造化: `summary-structuring` を読み込み、目的（判断用 / 引き継ぎ用 / 記録用）に応じたフォーマットで出力する
4. ドキュメント品質チェック:
   - `onboarding-readability` を読み込み、初見の読み手視点で可読性を評価する
   - 必要に応じて `reusable-doc-structure` を読み込み、構造の再利用性を評価する
5. 他LLM移植準備: `llm-portability-review` を読み込み、Claude 固有依存と移植耐性を評価する
6. 最終判断は人間に委ねる

## 出力の優先度

- 「どの Skill を適用したか / しなかったか」を冒頭に明示する
- 目的が複数ある場合は主目的の Skill を先に適用する
- 翻訳・要約は原文の情報を改変しない（言い換え・構造化のみ）

## Guardrails

- 技術的正確性を犠牲にして分かりやすさを優先しない
- 不都合な情報を省略して「良く見せる」翻訳をしない
- 受け手が不明な場合は確認してから翻訳する
