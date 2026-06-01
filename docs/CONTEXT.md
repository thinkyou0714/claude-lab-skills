# CONTEXT — プロジェクト背景・現フェーズ

_lab-skills の事業文脈・技術スタック・現在地をまとめた正本。_
_SKILL.md / command から「背景・前提」として参照される。_

> このドキュメントは "なぜ今これをやっているか" の単一の参照先です。
> 個別スキルは判断の「型」だけを持ち、文脈はここに集約します。

---

## プロジェクトの目的

`lab-skills` は THINK YOU LAB の「思考OS」を構成する再利用可能な判断資産です。
AI への丸投げではなく、**意思決定品質を高める論点整理・レビュー観点・判断材料**を
ツール非依存（Claude Code / Cursor / ChatGPT / Codex 等に移植可能）な Skill として蓄積します。

詳細な全体設計思想は [architecture.md](./architecture.md) を参照。

---

## 現フェーズ（本リポジトリの収録範囲）

本リポジトリ（公開版）には **思考OSの中核4プラグイン / 27スキル** を収録しています。

| Plugin | 責務 | Skill 数 | Command |
|---|---|---|---|
| lab-thinking-core | 論点整理・前提検証・意思決定支援 | 8 | `/think` |
| lab-automation-architecture | 自動化可否判断・フロー設計・障害設計 | 6 | `/automation-review` |
| lab-implementation-flow | 実装ゲート・影響範囲・施工AIへの handoff | 7 | `/impl-gate` |
| lab-communication-translation | 非エンジニア翻訳・ドキュメント再利用性・知識記録変換 | 6 | `/translate` |

事業設計（lab-strategy-design）・データ/認証（lab-data-auth-ops）は
**Roadmap（本リポジトリ未収録）** です。README の「Roadmap」節を参照。

---

## 技術スタック文脈

スキルが前提とする運用環境（判断の背景として参照）。

| 領域 | スタック | 備考 |
|---|---|---|
| 自動化基盤 | n8n | トリガー/アクション設計の前提（trigger-action-map 等） |
| 認証・データ | Supabase | 認証境界・PII・監査ログの前提 |
| デプロイ | Vercel | LP・会員画面のホスティング前提 |
| 施工AI | Claude Code / Cursor / Codex CLI | 実装・差分修正の担い手 |
| 設計AI | ChatGPT | 構造設計・論点整理 |

> 注: 上記は判断の前提を示す「文脈」です。具体的な接続仕様・認証情報は
> 本リポジトリには含めません（公開リポジトリのため）。

---

## 成功条件・ロールバック条件の考え方

個別の成功/失敗条件は各タスクの [TASKS.md](./TASKS.md) で定義します。
全体としては以下を基準にします。

- **成功条件**: 測定可能な形で定義する（success-failure-criteria skill を通す）
- **ロールバック条件**: 失敗条件をロールバック発動基準として明文化する
- **手動境界**: 失敗影響が大きい操作は、自動化せず人間判断を残す（[judgment-gates](../src/lab-core/rules/judgment-gates.md) GATE-2）

---

## 運用方針（manual-first）

- 最初は手動。ボトルネックを観察してから自動化を検討する
- 「月10回以上繰り返す」「失敗影響が小さい」が確認できてから自動化する
- 詳細: [cost-comparison.md](../src/lab-core/rules/cost-comparison.md) / [judgment-gates.md](../src/lab-core/rules/judgment-gates.md)

---

## 関連ドキュメント

- [architecture.md](./architecture.md) — 全体設計思想（4層モデル）
- [DECISIONS.md](./DECISIONS.md) — 設計決定記録（ADR）
- [TASKS.md](./TASKS.md) — タスク状態・完了定義・引き継ぎサマリーの参照例
- [glossary.md](../src/lab-core/data/glossary.md) — 用語集
- [../CONTRIBUTING.md](../CONTRIBUTING.md) — Skill 追加ルール・命名規則
