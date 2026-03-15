# lab-skills — THINK YOU LAB 思考OS スキルリポジトリ

## 概要

`lab-skills` は THINK YOU LAB の「思考OS」を構成する再利用可能な判断資産のリポジトリです。

AI への丸投げではなく、**意思決定品質を高める論点整理・レビュー観点・判断材料**を再利用可能な単位（Skill）として蓄積します。

---

## 三層構造

```
Plugin  ─── 領域別パッケージ（例: lab-thinking-core）
  └─ Skill  ─ 判断品質を上げる再利用単位。正本は SKILL.md
       └─ Command ─ 複数 skill を束ねる最小導線（Claude 固有の薄い入口）
```

### 原則

- **Skill は名詞句**: `issue-framing`, `risk-scan` など、責務を表す名詞
- **Command は動詞句**: `/think`, `/automation-review` など、動作を表す動詞
- **正本は SKILL.md**: Claude 固有の表現・手順は command 側に隔離する
- **1 Skill = 1責務**: cross-plugin 参照は最小化
- **推測で仕様を埋めない**: 入力が不足している場合は明示する

---

## Plugin 一覧

| Plugin | 責務 | Skill 数 | Command |
|---|---|---|---|
| [lab-thinking-core](./lab-thinking-core/) | 論点整理・前提検証・意思決定支援 | 8 | `/think` |
| [lab-strategy-design](./lab-strategy-design/) | 目標検証・代替案比較・スコープ設計・実行中戦略の査定 | 7 | `/strategy` `/strategy-review` |
| [lab-automation-architecture](./lab-automation-architecture/) | 自動化可否判断・フロー設計・障害設計 | 6 | `/automation-review` |
| [lab-data-auth-ops](./lab-data-auth-ops/) | データ設計・認証境界・ログ・PII | 6 | `/data-review` |
| [lab-implementation-flow](./lab-implementation-flow/) | 実装ゲート・影響範囲・施工AIへの handoff | 7 | `/impl-gate` |
| [lab-communication-translation](./lab-communication-translation/) | 非エンジニア翻訳・ドキュメント再利用性・知識記録変換 | 6 | `/translate` |

---

## 既存 `.claude/skills/` との分離

| ディレクトリ | 役割 |
|---|---|
| `.claude/skills/` | Claude Code 実装ツール（code-reviewer, debugger 等） |
| `lab-skills/` | 思考OS資産（論点整理・判断支援 Skill） |

両者は役割が異なります。`lab-skills/` の Skill は Claude Code 専用ではなく、Cursor / Codex / ChatGPT 他への移植を前提に設計されています。

---

## Skill の使い方

### 直接参照

```
# 例: issue-framing skill を使って論点を整理する
cat lab-skills/lab-thinking-core/skills/issue-framing/SKILL.md
```

### Command 経由（Claude Code）

```
# Plugin の .claude/commands/ からインストールして使う
cp lab-skills/lab-thinking-core/.claude/commands/think.md .claude/commands/think.md
# → /think コマンドが使えるようになる
```

Command のインストール手順は [CONTRIBUTING.md](./CONTRIBUTING.md) を参照。

---

## 実装状態

| Phase | 内容 | 状態 |
|---|---|---|
| Phase 1 | lab-thinking-core 中核5 skills | 完了 |
| Phase 2 | lab-automation-architecture / lab-data-auth-ops 骨組み | 完了 |
| Phase 3 | lab-implementation-flow | 完了 |
| Phase 4 | lab-communication-translation | 完了 |
| Phase 5 | 最小 command 群（plugin ごとに1 command） | 完了 |
| Phase 6 | 戦略ライフサイクル完結・施工AI handoff・知識記録変換 | 完了 |

---

## 関連ドキュメント

- [docs/CONTEXT.md](../docs/CONTEXT.md) — プロジェクト背景・現フェーズ
- [docs/DECISIONS.md](../docs/DECISIONS.md) — 設計決定記録（ADR）
- [CONTRIBUTING.md](./CONTRIBUTING.md) — Skill 追加ルール・命名規則
