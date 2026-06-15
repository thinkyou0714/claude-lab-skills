# CONTRIBUTING — lab-skills への追加・変更ルール

> English: [CONTRIBUTING.en.md](./CONTRIBUTING.en.md)

## 基本姿勢

- 「答えを出す」ではなく「判断材料を揃える」Skill を作る
- 推測で仕様を埋めない。不足情報は明示する
- 1 Skill = 1責務。cross-plugin 参照は最小化
- Claude 固有の都合は command または補助ドキュメントに隔離する
- 最終判断は人間に委ねる

---

## 命名規則

### Skill 名（名詞句）

- 形式: `動詞なし-名詞句`（kebab-case）
- 例: `issue-framing`, `risk-scan`, `auth-boundary-check`
- ディレクトリ名と SKILL.md の `name:` フィールドを一致させること
- 責務が1文で説明できない場合は分割を検討する

### Command 名（動詞句）

- 形式: `動詞` または `動詞-対象`（kebab-case）
- 例: `/think`, `/automation-review`, `/impl-gate`
- Command は複数の Skill を束ねる入口として設計する

### Plugin 名

- 形式: `lab-<領域>` プレフィックス必須
- 例: `lab-thinking-core`, `lab-implementation-flow`

---

## Skill 追加手順

### 1. 対象 plugin の確認

既存 plugin に収まる場合はそこへ追加する。
新 plugin が必要な場合は、README.md の Plugin 一覧更新を含めて提案する。

### 2. ディレクトリ作成

スキャフォルダで雛形を生成する（既存は上書きしない。設計方針は ADR-006 参照）。

```text
python src/lab-core/scripts/new_skill.py <plugin-name> <skill-name>
```

生成される構造:

```text
<plugin-name>/
└─ skills/
   └─ <skill-name>/
      └─ SKILL.md
```

### 3. SKILL.md 作成

テンプレートの**唯一の正本**は [`src/lab-core/templates/skill-template.md`](./src/lab-core/templates/skill-template.md) です（ADR-007）。
`new_skill.py`（手順 2）はこの正本から雛形を生成するため、通常は別途コピーは不要です。
各セクションの削除・省略は禁止。記入例は実スキル
[`lab-thinking-core/skills/issue-framing/SKILL.md`](./lab-thinking-core/skills/issue-framing/SKILL.md) を参照。

必須セクション（この順序を変えない。`validate_plugins.py` が順序・空本文を検査する）:

| セクション | 役割 |
|---|---|
| `## Purpose` | 解決する問題（1〜3文） |
| `## Use When` | 使う状況・トリガー（箇条書き） |
| `## Inputs` | 必要な入力。不足は推測せず明示 |
| `## Output Contract` | 出力の順序（論点 → 根拠 → …（領域別）… → 判断材料） |
| `## Review Lens` | レビュー観点（目的妥当性 / 範囲 / 中長期リスク / LAB整合 / 非エンジニア理解 / 他LLM移植耐性） |
| `## Instructions` | 実行手順（箇条書き） |
| `## Guardrails` | してはいけないこと |
| `## LAB Cross-Check` | クロスチェック表（観点 / 状態 / 備考。状態は OK / 注意 / NG / 対象外） |
| `## Handoff Notes` | 施工AIへの引き継ぎ（要件 / 成功・失敗条件 / 範囲 / 影響 / ロールバック / コスト） |
| `## Further Reading` | 関連スキル・正本（src/）への参照 |

> 表現はテンプレート正本に従うこと。テンプレートを変更する場合は
> `skill-template.md` のみを編集する（CONTRIBUTING・生成スクリプトに本文を複製しない）。

### 4. README.md の更新

追加した Skill は plugin ディレクトリの README（存在する場合）または README.md の Plugin 一覧に反映する。

---

## Command 追加手順

Command は Skill の薄いアダプタです。Command 自体に判断ロジックを書かない。

### 配置

```text
lab-skills/<plugin-name>/.claude/commands/<command-name>.md
```

### インストール（Claude Code で使う場合）

```bash
# リポジトリルートから実行
cp <plugin-name>/.claude/commands/<command-name>.md .claude/commands/<command-name>.md
```

### フォーマット

```markdown
---
description: "<command の一行説明>"
argument-hint: "<引数のヒント（省略可）>"
allowed-tools: Read,Grep
---

この command が使う skills:
- <skill-name>: <SKILL.md への相対パス>

## 手順
1. <skill-name> を読み込む
2. Inputs に合わせて情報を収集する
3. Output Contract に従って出力する
```

---

## 品質ゲート

以下を満たさない Skill は追加しない。

- [ ] 論点が明確
- [ ] 根拠が明示されている
- [ ] リスクが言語化されている
- [ ] 改善策が現実的
- [ ] 判断材料が揃っている
- [ ] LAB全体との整合が説明されている
- [ ] 人間の意思決定余地が残されている
- [ ] Guardrails セクションが省略されていない
- [ ] LAB Cross-Check セクションが省略されていない
- [ ] 個人名・内部コードネーム・私的パスを含まない（GATE-3 / 非エンジニアにも通じる一般語にする）
- [ ] 追加・変更した plugin の `README.md` を更新した
- [ ] `python validate_plugins.py --strict` がグリーン（整合性 + リンク + マニフェスト）

---

## 禁止事項

- pm-skills をそのままコピーして終わりにしない
- Command を大量作成しない（Skill が先）
- Claude 固有仕様を SKILL.md に書き込まない
- Guardrails / LAB Cross-Check を削らない
- README なしで Skill を量産しない
