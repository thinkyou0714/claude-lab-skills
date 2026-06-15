# DECISIONS — 設計決定記録（ADR）

_過去の設計決定と前提を記録する。一度決めたことを再議論しないための参照先。_
_新しい決定は末尾に追記する（既存エントリは改変しない）。_

書式: 各決定は `ADR-<番号>` で識別し、**Context / Decision / Consequences** を記載する。
状態は `採用 (Accepted)` / `置換 (Superseded by ADR-x)` / `撤回 (Deprecated)` のいずれか。

## 索引

| ADR | タイトル | 分類 | 状態 |
|---|---|---|---|
| [ADR-001](#adr-001-知識の正本を-src-に置く) | 知識の正本を `src/` に置く | アーキテクチャ | 採用 |
| [ADR-002](#adr-002-1-skill--1-責務) | 1 Skill = 1 責務 | アーキテクチャ | 採用 |
| [ADR-003](#adr-003-skill-はツール移植を前提に設計する) | Skill はツール移植を前提に設計する | アーキテクチャ | 採用 |
| [ADR-004](#adr-004-manual-first手動を恥じない) | manual-first（手動を恥じない） | プロセス | 採用 |
| [ADR-005](#adr-005-公開用に標準リポジトリ構成へ切り出す) | 公開用に標準リポジトリ構成へ切り出す | プロセス | 採用 |
| [ADR-006](#adr-006-skillmd-は手作りを正とし機械的な再生成はしない) | SKILL.md は手作りを正とする | プロセス | 採用 |
| [ADR-007](#adr-007-雛形テンプレートを単一正本化しカウント整合を-ci-で保証する) | テンプレート単一正本化・カウント整合 CI | プロセス | 採用 |
| [ADR-008](#adr-008-移植性を主張ではなく機構で提供する) | 移植性を機構（export_skill）で提供 | アーキテクチャ | 採用 |
| [ADR-009](#adr-009-発見性インデックスは手書きせず生成物とする) | 発見性インデックスは生成物とする | プロセス | 採用 |
| [ADR-010](#adr-010-単一バージョン方針でリリースする) | 単一バージョン方針でリリース | プロセス | 採用 |

> ADR-006 と ADR-007 は密接に関連する（テンプレート/再生成ループの方針）。
> ADR-008 は ADR-003（移植前提の設計）を「主張」から「動く機構」へ前進させる。
> ADR-009 は ADR-007（カウント整合）の延長で、一覧そのものを生成物にしてドリフトを消す。

---

## ADR-001: 知識の正本を `src/` に置く

- **状態**: 採用
- **Context**: AIツール（Claude Code / Cursor / ChatGPT）は頻繁に更新され、ツール固有の
  指示ファイル（`.claude/`, `.cursor/`）だけを真実源にすると、ツール変更のたびに知識が失われる。
- **Decision**: 言語・ツール非依存の正本を `src/` に置き、AI向けは薄いアダプター層（SKILL.md / command）として記述する。
- **Consequences**: 移植性が上がる。一方で「正本」と「アダプター」の二重管理が生じるため、整合性検証（`validate_plugins.py`）が必須になる。

---

## ADR-002: 1 Skill = 1 責務

- **状態**: 採用
- **Context**: 単一巨大スキル（[antipatterns](../src/lab-core/rules/antipatterns.md) AP-D1）は保守不能になり、再利用・差し替え・移植ができない。
- **Decision**: 1スキル1責務を原則とし、cross-plugin 参照は最小化する。責務が1文で説明できない場合は分割する。
- **Consequences**: スキル数は増えるが、各スキルが独立して再利用・移植できる。

---

## ADR-003: Skill はツール移植を前提に設計する

- **状態**: 採用
- **Context**: 思考OS資産は Claude Code 専用ではなく、Cursor / Codex / ChatGPT へ移植して使う想定。
- **Decision**: SKILL.md に Claude 固有の都合を書かない。ツール固有の入口は command 側へ隔離する。各スキルに「他LLM移植耐性」のレビュー観点を持たせる。
- **Consequences**: 表現がツール中立になる。Claude 固有の最適化は command 層でのみ行う。

---

## ADR-004: manual-first（手動を恥じない）

- **状態**: 採用
- **Context**: 初手で完全自動化を目指すと、障害時に人間が介入できず連鎖障害を招く（antipatterns AP-A1）。
- **Decision**: 最初は手動。ボトルネックを観察し、「月10回以上」「失敗影響が小さい」が確認できてから自動化を検討する（[judgment-gates](../src/lab-core/rules/judgment-gates.md) GATE-2）。
- **Consequences**: 自動化の着手は遅れるが、手動境界が明示され、失敗影響を制御できる。

---

## ADR-005: 公開用に標準リポジトリ構成へ切り出す

- **状態**: 採用
- **Context**: lab-skills は親モノレポのサブディレクトリとして開発されていた。公開（MIT License）にあたり単独リポジトリへ切り出した。
- **Decision**: `docs/`（CONTEXT / DECISIONS / TASKS）・`glossary` をリポジトリ内に正本として持ち、相対参照はリポジトリルート基準で解決する。整合性検証に内部リンク切れ検出を組み込み、ドリフトを防ぐ。
- **Consequences**: 切り出し時に発生した「親階層 `docs/` への過剰な `../`」リンク切れを解消。以後は CI（`validate_plugins.py`、リンク検査は既定で有効。`--no-check-links` で無効化）でリンク健全性を継続的に保証する。

---

## ADR-006: SKILL.md は手作りを正とし、機械的な「再生成」はしない

- **状態**: 採用
- **Context**: アーキテクチャは「`src/` 正本 → SKILL.md 再生成」の改善ループを将来像として描く。しかし SKILL.md は Output Contract・Instructions 等の手作り部分が価値の中心であり、`src/` のルールから機械的に全文再生成すると、その手作り内容を破壊する。
- **Decision**: SKILL.md は手作りを正本とする。`src/` の SoT はスキルが「参照」する原則・データであり、スキル本文を全文生成する元ではない。生成方向は「テンプレート → 新規スキルの雛形」に限定し、`src/lab-core/scripts/new_skill.py` で安全に scaffold する（既存は上書きしない）。SoT とスキルの整合は双方向リンクと `validate_plugins.py`（リンク・相互参照検査）で担保する。
- **Consequences**: 「再生成ループ」は全文自動生成ではなく、(1) 新規スキルの雛形生成、(2) SoT↔スキルのリンク整合検証、という安全な形で実現する。手作りの判断品質を保全できる。

---

## ADR-007: 雛形テンプレートを単一正本化し、カウント整合を CI で保証する

- **状態**: 採用
- **Context**: 雛形テンプレートが2か所（`src/lab-core/templates/skill-template.md` と
  `new_skill.py` のハードコード文字列）に分裂し、内容が乖離していた（Output Contract /
  Review Lens / LAB Cross-Check の形式が不一致）。また README / docs の「N プラグイン /
  M スキル」が手書きで、実体（agmsg 追加で 40→41）と繰り返しドリフトしていた。
- **Decision**: (1) 雛形の正本を `skill-template.md` の ```markdown フェンス1か所に集約し、
  `new_skill.py` はそれを読み取って frontmatter の `name` のみ差し替える。
  全文再生成はしない（ADR-006 を踏襲）。(2) `validate_plugins.py` に README カウント
  整合チェックを追加し、プラグイン数・スキル総数を実体から数えて README 表記と突き合わせる。
- **Consequences**: テンプレートの二重管理が解消し、ドリフトは CI（`validate_plugins.py
  --strict`）で機械的に検出される。「SoT → 雛形生成」ループは、全文生成ではなく
  「単一正本テンプレート → 新規スキル雛形」＋「カウント・リンク・相互参照の整合検証」
  という安全な形で実体化した。領域別 SoT（`src/lab-system-design/` 等）の本文は、
  推測で仕様を埋めない原則（ADR-006）に従い、実コンテキストが確定するまで Roadmap に留める。

---

## ADR-008: 移植性を「主張」ではなく「機構」で提供する

- **状態**: 採用
- **Context**: ADR-003 は「Skill は他ツール（Cursor / ChatGPT / Codex）へ移植できる」ことを
  設計原則に掲げ、各スキルに「他LLM移植耐性」のレビュー観点も持たせてきた。しかし実際に
  移植するための**動く成果物**（変換スクリプトや手順書）は無く、原則が主張に留まっていた。
- **Decision**: SKILL.md を可搬フォーマットへ書き出す `src/lab-core/scripts/export_skill.py`
  （`prompt` / `cursor` (.mdc) / `chatgpt`）と、手順書 [PORTING.md](./PORTING.md) を追加する。
  変換は frontmatter の取り外しと各ツールの薄い容れ物への詰め替えに限定し、判断本文
  （Output Contract / Guardrails 等）は改変しない。SKILL.md を正本とし、書き出した成果物は派生物とする。
- **Consequences**: 「他LLM移植耐性」が検証可能な機構として裏づけられる。`.cursor/rules/` 等の
  ツール固有エントリーポイントは、リポジトリに常設するのではなく必要時に書き出す運用とする
  （正本の二重管理を避ける）。移植の完全性はツール差により限界があるため、`llm-portability-review`
  skill の Guardrails（「完全移植可能」と断定しない）と併用する。

---

## ADR-009: 発見性インデックスは手書きせず生成物とする

- **状態**: 採用
- **Context**: 41 スキルの一覧（プラグイン / 名前 / 説明）を手書きで持つと、スキル追加・
  description 変更のたびにドリフトする。ADR-007 でカウントは検査できるようになったが、
  一覧本文そのものは依然として手書きドリフトの温床だった。
- **Decision**: 全スキル索引 [docs/SKILLS.md](./SKILLS.md) を各 SKILL.md の frontmatter から
  `src/lab-core/scripts/gen_catalog.py` で生成する。`--check` と pytest（`test_gen_catalog`）で
  「生成結果＝コミット内容」を CI が保証する。SKILL.md を正本、カタログを派生物とする
  （ADR-006 / ADR-008 と同じ「正本→派生」原則）。
- **Consequences**: 一覧のドリフトが構造的に消える。スキル追加時は `make catalog` で再生成する
  運用になる（CONTRIBUTING に明記）。export_skill（ADR-008）と同様、派生物は手で編集しない。

---

## ADR-010: 単一バージョン方針でリリースする

- **状態**: 採用
- **Context**: マーケットプレイスに 6 プラグインを同梱しており、プラグインごとに独立した版を
  振ると、利用者・CHANGELOG・タグの対応が複雑化する。一方でリリース手順・版上げ基準が
  明文化されておらず、`marketplace.json` と `plugin.json` の版がドリフトしうる状態だった。
- **Decision**: **単一バージョン方針**を採る。`marketplace.json` の `version` をリリースの正本とし、
  全 `plugin.json` の `version` をそれに一致させる（`validate_plugins.py --strict` が不一致を検出）。
  版上げは SemVer（MAJOR=構造の破壊的変更 / MINOR=スキル・プラグイン追加 / PATCH=既存修正）。
  一括更新は `src/lab-core/scripts/bump_version.py`、公開はタグ `v*` 起点の
  `release.yml`（GitHub Release 自動生成）で行う。手順は [RELEASING.md](../RELEASING.md)。
- **Consequences**: 版の対応が単純になり、ドリフトが CI で防がれる。プラグインを個別に
  バージョニングしたくなった場合は、本 ADR を置換する新 ADR で方針を改める。

---

## 追記方法

新しい決定は `ADR-00N` として上に倣って追記する。
既存の決定を覆す場合は、新しい ADR を追加し、古い ADR の状態を
`置換 (Superseded by ADR-N)` に更新する（本文は残す）。
