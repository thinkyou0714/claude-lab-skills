# CONTRIBUTING — lab-skills への追加・変更ルール

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
- 例: `/think`, `/automation-review`, `/handoff-impl`
- Command は複数の Skill を束ねる入口として設計する

### Plugin 名

- 形式: `lab-<領域>` プレフィックス必須
- 例: `lab-thinking-core`, `lab-data-auth-ops`

---

## Skill 追加手順

### 1. 対象 plugin の確認

既存 plugin に収まる場合はそこへ追加する。
新 plugin が必要な場合は、README.md の Plugin 一覧更新を含めて提案する。

### 2. ディレクトリ作成

```
lab-skills/
└─ <plugin-name>/
   └─ skills/
      └─ <skill-name>/
         └─ SKILL.md
```

### 3. SKILL.md 作成

以下のテンプレートを使用する。各セクションの削除・省略は禁止。

```markdown
---
name: <skill-name>
description: "<1〜2文で責務を説明。使う場面を含めること>"
---

## Purpose
この skill の目的（1〜3文）

## Use When
この skill を使う状況（箇条書き）

## Inputs
必要な入力情報
不足している場合は推測せず明示すること

## Output Contract
必ず以下の順で出力すること
1. 論点
2. 根拠
3. リスク
4. 含意
5. 改善案
6. 代替案
7. 判断材料

## Review Lens
最低限確認する観点
- 目的妥当性
- 範囲の過不足
- 中長期リスク
- LAB全体との整合性
- 非エンジニア理解可能性
- 他LLM移植耐性

## Instructions
実行手順（箇条書き）

## Guardrails
- 推測で仕様を埋めない
- 実装を勝手に確定しない
- 選択肢を1つに閉じない
- コスト比較を省略しない
- ユーザーの意思決定余地を消さない

## LAB Cross-Check
以下を OK / 注意 / NG で確認すること
- 自動化フロー
- データ / 認証 / ログ
- 実装 / 運用フロー
- 非エンジニア理解可能性
- 会員共有 / 再利用耐性
- 他LLM移植耐性

## Handoff Notes
施工AIへ渡す前に必要な情報
- 要件
- 成功条件
- 失敗条件
- 実行範囲
- 影響範囲
- ロールバック方針
- コスト比較

## Further Reading
関連ドキュメントや参照先
```

### 4. README.md の更新

追加した Skill は plugin ディレクトリの README（存在する場合）または lab-skills/README.md の Plugin 一覧に反映する。

---

## Command 追加手順

Command は Skill の薄いアダプタです。Command 自体に判断ロジックを書かない。

### 配置

```
lab-skills/<plugin-name>/.claude/commands/<command-name>.md
```

### インストール（Claude Code で使う場合）

```bash
# リポジトリルートから実行
cp lab-skills/<plugin-name>/.claude/commands/<command-name>.md .claude/commands/<command-name>.md
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

---

## 禁止事項

- pm-skills をそのままコピーして終わりにしない
- Command を大量作成しない（Skill が先）
- Claude 固有仕様を SKILL.md に書き込まない
- Guardrails / LAB Cross-Check を削らない
- README なしで Skill を量産しない
