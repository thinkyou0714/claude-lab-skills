# アーキテクチャ概要 — lab-skills

_このドキュメントは lab-skills の全体設計思想を説明します。_
_非エンジニアでも読めるように書いています。_

---

## なぜこの構造になっているか

### 問題意識

AIツール（Claude Code, ChatGPT, Cursor）は頻繁にアップデートされます。
もし「AIへの指示ファイル」が唯一の知識源になると、ツールが変わるたびに
知識を作り直す必要が生じます。

**解決策**: 知識の本体（Source of Truth）を `src/` に置き、
AIツール向けは「薄いアダプター」として生成する。

---

## 全体構造（3層モデル）

> 補足: README は同じ階層を `src → Plugin → Skill → Command` の **4層**として説明します。
> 本ドキュメントの「Layer 1: AI アダプター」が、その Plugin 層（SKILL.md）と Skill を束ねた粒度です。
> どちらも同一の階層構造を別の粒度で表現したものであり、矛盾しません。

```text
┌─────────────────────────────────────────┐
│  Layer 0: Source of Truth               │
│  src/lab-core/ ほか（領域別は Roadmap）  │
│  → Markdown/CSV/JSON の軽量データ      │
│  → ルール・用語・テンプレートの正本    │
└─────────────────────────────────────────┘
           ↓ 参照・生成
┌─────────────────────────────────────────┐
│  Layer 1: AI アダプター（Plugin 層）    │
│  lab-thinking-core/, lab-automation-architecture/ 等 │
│  → SKILL.md（AI向けに最適化した表現）  │
│  → 既存の Plugin/Skill/Command 構造     │
└─────────────────────────────────────────┘
           ↓ 参照
┌─────────────────────────────────────────┐
│  Layer 2: ツール固有エントリーポイント  │
│  .claude/commands/, .cursor/rules/ 等  │
│  → Claude Code の /think コマンド等    │
│  → 最も薄いレイヤー。SoT ではない     │
└─────────────────────────────────────────┘
```

> 注: 現在リポジトリに実体があるツール固有エントリーポイントは Claude Code 用
> （`.claude/commands/`）のみです。`.cursor/rules/` 等は「同じ Skill を別ツールへ
> 移植できる」という設計意図を示す例示であり、現時点ではディレクトリを持ちません。
> SKILL.md を他ツール形式へ書き出す具体的な手順とスクリプトは
> [PORTING.md](./PORTING.md) と `src/lab-core/scripts/export_skill.py` を参照してください。

---

## src/ ディレクトリの役割

| ディレクトリ | 役割 | 現状 |
|-------------|------|------|
| `src/lab-core/` | 全スキル共通の基盤（用語・ゲート・アンチパターン・コスト比較）| 実装済み |
| `src/lab-strategy/` | 事業設計（顧客課題・提供価値・競争回避・価格）| 実装済み |
| `src/lab-system-design/` | n8n前提の自動化設計 | 予約済み（未実装）|
| `src/lab-data-auth/` | 認証・データ設計（権限境界・PII・監査）| 実装済み |
| `src/lab-implementation-ops/` | 実装運用規律（PR・ロールバック・AI指示）| 予約済み（未実装）|
| `src/lab-frontend-design/` | LP・会員画面・CTA設計 | 予約済み（未実装）|

---

## AIツールの役割分担

| AIツール | 役割 | SoTになるか |
|---------|------|------------|
| ChatGPT | 構造設計・論点整理・戦略査定（設計OS）| ならない |
| Claude Code | 実装・ファイル操作・コードレビュー（施工AI）| ならない |
| Cursor | 差分実装・インライン修正（施工AI補助）| ならない |
| `src/` | 知識の正本 | **なる**（SoT）|

---

## 改善ループの設計思想（将来）

```text
1. 施策・設計を src/ の data/ へ記録（現在は手動）
2. 採否ログを docs/DECISIONS.md に追記
3. 定期査定で src/ のルールを更新
4. AIへの指示（SKILL.md）は src/ から再生成
```

現時点では全て手動。自動化は「月10回以上繰り返す」「失敗影響が小さい」
ことが確認できてから検討する。

---

## 手動運用 vs 自動化 の考え方

- **手動を恥じない**: 最初から自動化しようとしない
- **ボトルネックを観察してから自動化する**: 手動でやってみて、本当に繰り返すことが確認できたら自動化を検討
- **手動境界は明示する**: どこを人間が判断するかを docs に書く

詳細: `src/lab-core/rules/cost-comparison.md`

---

## 参照

- 用語集: `src/lab-core/data/glossary.md`
- 判断ゲート: `src/lab-core/rules/judgment-gates.md`
- アンチパターン: `src/lab-core/rules/antipatterns.md`
- Skill 追加ルール: `CONTRIBUTING.md`
