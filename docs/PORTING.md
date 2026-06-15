# PORTING — Skill を他ツール（Cursor / ChatGPT / Codex 等）へ移植する

_このリポジトリの Skill は Claude Code 専用ではありません（ADR-003）。_
_本書は SKILL.md を他ツールへ移す具体手順と、移植時の注意点をまとめます。_

> 関連: [architecture.md](./architecture.md)（層モデル）/ [DECISIONS.md](./DECISIONS.md)（ADR-003）

---

## なぜ移植できるのか

SKILL.md は最初から**ツール中立**に書かれています（Claude 固有の都合は command 層に隔離）。
そのため移植とは「frontmatter を外し、各ツールが期待する薄い容れ物へ詰め替える」だけで済み、
判断本文（Output Contract・Guardrails 等）は改変しません。

---

## 書き出しスクリプト

```bash
# 既定: ツール非依存のシステムプロンプト（任意の LLM の system 欄に貼れる）
python src/lab-core/scripts/export_skill.py lab-thinking-core/skills/issue-framing/SKILL.md

# Cursor の Project Rule（.mdc）として保存
python src/lab-core/scripts/export_skill.py \
  lab-thinking-core/skills/issue-framing/SKILL.md \
  --format cursor --out .cursor/rules/issue-framing.mdc

# ChatGPT のカスタム指示 / system メッセージ向けプレーンテキスト
python src/lab-core/scripts/export_skill.py \
  lab-thinking-core/skills/issue-framing/SKILL.md \
  --format chatgpt
```

| `--format` | 用途 | 貼り先 |
|---|---|---|
| `prompt`（既定） | ツール非依存のシステムプロンプト | 任意の LLM の system / 開発者メッセージ |
| `cursor` | Cursor Project Rule（frontmatter 付き `.mdc`） | `.cursor/rules/<name>.mdc` |
| `chatgpt` | プレーンな system / カスタム指示 | ChatGPT「カスタム指示」, API の system |

---

## ツール別の置き場所

| ツール | 置き場所 | 補足 |
|---|---|---|
| Claude Code | `lab-*/skills/<name>/SKILL.md`（このまま） | Plugin として install、または手動コピー |
| Cursor | `.cursor/rules/<name>.mdc` | `--format cursor`。`alwaysApply: false`（手動 @ 呼び出し） |
| ChatGPT | カスタム指示 / API の `system` | `--format chatgpt` |
| Codex / その他 CLI | `system` プロンプト | `--format prompt` |

---

## 移植時のチェックリスト

- [ ] frontmatter（`name` / `description`）が剥がれ、本文が保持されているか（スクリプトが担保）
- [ ] 本文に Claude / Cursor 固有の記法（`@参照`、ツール名のハードコード）が残っていないか
      → 残っていれば一般語へ置換（例: 「Slack」→「通知先（メール / チャット等）」）
- [ ] `Output Contract` の順序が保たれているか
- [ ] 移植先で「推測で仕様を埋めない / 最終判断は人間」の Guardrails が機能するか
- [ ] 移植結果を `llm-portability-review` skill で点検したか

---

## よくある落とし穴

- **完全移植を断言しない**: 出力フォーマットの再現性はツールにより差が出る。
  `llm-portability-review` skill の Guardrails に従い「完全移植可能」と断定しない。
- **frontmatter を二重に持たせない**: `--format cursor` は `.mdc` 用 frontmatter を新規生成する。
  元の SKILL.md frontmatter は剥がれているので重複しない。
- **正本はあくまで SKILL.md**: 書き出した `.mdc` 等は派生物。内容を直したいときは
  SKILL.md（さらに上流は `src/` の正本）を直し、再書き出しする。
