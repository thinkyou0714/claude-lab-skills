# lab-skills — THINK YOU LAB 思考OS スキルリポジトリ

## 概要

`lab-skills` は THINK YOU LAB の「思考OS」を構成する再利用可能な判断資産のリポジトリです。

AI への丸投げではなく、**意思決定品質を高める論点整理・レビュー観点・判断材料**を再利用可能な単位（Skill）として蓄積します。

---

## 全体構造（4層モデル）

```
src/        ─── Source of Truth（正本データ層）
  └─ lab-core/, lab-strategy/, ... ← 言語非依存の知識資産

Plugin      ─── 領域別パッケージ（例: lab-thinking-core）
  └─ Skill  ─── 判断品質を上げる再利用単位（src/ を参照して記述）
       └─ Command ─ AI固有の薄い入口（Claude Code / Cursor 等向け）
```

### 原則

- **正本は src/**: AI固有フォルダ（`.claude/`, `.cursor/`）を真実源にしない
- **Skill は名詞句**: `issue-framing`, `risk-scan` など、責務を表す名詞
- **Command は動詞句**: `/think`, `/automation-review` など、動作を表す動詞
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

## src/ — 知識の正本（Source of Truth）層

> **なぜ単一巨大スキルにしないか**
> 1責務1スキルの原則により、知識の再利用・差し替え・移植が可能になる。
> 巨大スキルは保守不能になり、ツール変更時に知識ごと失われる。

> **Source of Truth を src/ に分ける理由**
> `.claude/` や `.cursor/` はツール固有の入口であり、仕様変更で消えうる。
> `src/` に言語非依存の正本を置くことで、AIツールが変わっても知識は残る。

```
src/
  lab-core/           ← 全スキル共通の基盤知識（用語・ゲート・アンチパターン）
    data/glossary.md
    rules/judgment-gates.md
    rules/antipatterns.md
    rules/cost-comparison.md
    templates/skill-template.md
    scripts/search.py  ← src/ 内の知識をキーワード検索する最小スクリプト
  lab-strategy/       ← 事業設計の知識（顧客課題・価値・競争回避・価格）
    data/
    rules/
    templates/
    scripts/
  lab-system-design/  ← n8n前提の自動化設計（将来実装）
  lab-data-auth/      ← Supabase前提の認証・データ設計（将来実装）
  lab-implementation-ops/  ← 実装運用規律（将来実装）
  lab-frontend-design/     ← LP・会員画面・CTA設計（将来実装）
```

### AIツールの役割分担

| AIツール | 役割 |
|---------|------|
| ChatGPT | 構造設計・論点整理（設計OS）|
| Claude Code | 実装・ファイル操作（施工AI）|
| Cursor | 差分実装（施工AI補助）|
| **src/** | **知識の正本（SoT）** ← ここが唯一の真実源 |

### 手動運用 vs 自動化

- 最初は手動。ボトルネックを観察してから自動化を検討する
- 手動境界（人間が必ず判断する操作）を明示する
- 詳細: `src/lab-core/rules/cost-comparison.md`

### 改善ループ（将来接続の前提構造）

```
src/data/ に記録 → 採否ログに追記 → 定期査定 → src/rules/ 更新 → SKILL.md 再生成
```

現時点では手動。将来 n8n 等と接続できる構造のみ整えている。

### src/ を検索する

```powershell
# lab-skills/ ディレクトリで実行
python src/lab-core/scripts/search.py "判断ゲート"
python src/lab-core/scripts/search.py "BtoB" --path src/lab-strategy
```

詳細: [examples/search-example.md](./examples/search-example.md)

---

## 関連ドキュメント

- [docs/architecture.md](./docs/architecture.md) — src/ アーキテクチャの設計思想
- [docs/CONTEXT.md](../docs/CONTEXT.md) — プロジェクト背景・現フェーズ
- [docs/DECISIONS.md](../docs/DECISIONS.md) — 設計決定記録（ADR）
- [CONTRIBUTING.md](./CONTRIBUTING.md) — Skill 追加ルール・命名規則
