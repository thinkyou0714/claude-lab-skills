# Changelog

本プロジェクトの主要な変更を記録する。
書式は [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に準拠し、
バージョニングは [Semantic Versioning](https://semver.org/lang/ja/) に従う。

> バージョニング・リリース手順は [RELEASING.md](./RELEASING.md)（方針は ADR-010）を参照。
> MAJOR=構造の破壊的変更 / MINOR=スキル・プラグイン追加 / PATCH=既存の修正。

## [Unreleased]

### Fixed（不具合修正）

- **README / docs のカウントドリフトを是正**: `agmsg` 追加（40→41）が未反映だった `README.md`（実装状態・導入可能プラグイン一覧）/ `README.en.md`（合計・automation の 6→7・CI Python 3.9–3.14）/ `docs/CONTEXT.md`（合計・automation・SoT 収録状況）/ `docs/TASKS.md` を実体（6 プラグイン / 41 スキル）に統一。`docs/architecture.md` の「3層 / 4層」表記の食い違いを補足で明示。
- **カウント整合チェックを `validate_plugins.py` に追加**: README の「N プラグイン / M スキル」表記を実体（プラグイン数・スキル総数）と突き合わせ、数値ドリフトを CI で検出（日本語・英語表記対応、コードフェンス内は除外）。

- **コードの入出力を堅牢化（エッジケース）**: BOM 付きファイルの frontmatter 解析（`utf-8-sig`）、存在しない `--root` のクラッシュをクリーンエラー化、タイトル付き / `<url>` 形式リンクの正規化、`skills/__pycache__`・隠しディレクトリの除外。
- **コード抽出のフェンス処理を統一（根本原因修正）**: `extract_sections` / `extract_command_skill_refs` がコードフェンス内の見出し・参照を誤検出していた問題を修正（必須セクションがフェンス内にだけある場合に検証をすり抜ける潜在バグを解消）。`SKILL_REF_RE` に語境界を追加し "skilled" / "skills" の誤マッチを防止。`search.py --max` は 1 以上を要求するよう検証。
- **`new_skill.py` の `--force` を廃止**（Codex 自動レビュー対応）: 既存 SKILL.md を決して上書きしないようにし、ADR-006（手作り内容の保護）の保証と整合させた。
- `docs/TASKS.md` の DoD の古い数値（4プラグイン27スキル）を実体（6プラグイン40スキル）に是正。
- モノレポ切り出し時に発生した内部リンク切れ **31 件** を解消（`docs/CONTEXT.md` / `DECISIONS.md` / `TASKS.md` への過剰な `../`、幻プラグインへのリンク）。
- 公開リポジトリに漏出していた私的仕様 `slack-notification-spec.md` への参照を除去。
- **プライバシー / 内部情報のスクラブ（GATE-3）**: 公開リポジトリに残っていた個人名 5 箇所を非個人化（「非エンジニアの関係者」等）、内部コードネーム 8 箇所を一般語（「主力プロダクト（LMS）」等）へ置換。
- **未収録スキルへの宙ぶらりん参照 3 件**を修正（`scope-design` / `rollback-readiness` / `auth-boundary-check`）。実在しない forward-reference を `Roadmap: …、本リポジトリ未収録` と明示し、誤認を防止。
- 残存ドリフト 2 件を修正: README 実装状態テーブルの Phase 2 が未収録の `lab-data-auth-ops` を「完了」と記載していた点、`rollback-plan` の `plugin/skill` 修飾形式（`lab-data-auth-ops/rollback-readiness`）の宙ぶらりん参照。あわせてスキル相互参照検査を `plugin/skill` 修飾形式にも対応させ、検証ギャップを解消。
- README / `docs/architecture.md` / `CONTRIBUTING.md` の記述を実体（4 プラグイン / 27 スキル）に整合。未収録の `lab-strategy-design` / `lab-data-auth-ops` は Roadmap 節へ分離。
- `skill-template.md` の frontmatter（`src` / `version`）を実スキル（`name` / `description`）に整合。

### Added（追加）

- **新規スキル2件を `lab-data-auth-ops` に追加（6→8スキル / リポジトリ計 41→43）**: `auth-system-design`（認証・アイデンティティの仕組みを上流で設計。既存の reactive な `auth-boundary-check` の proactive 対）と `secret-management-review`（APIキー・トークン・鍵の保管・スコープ・ローテーション・漏洩対策）。いずれも事業固有情報を含まない汎用フレームワーク。
- **リリース運用を整備（ADR-010）**: 単一バージョン方針（`marketplace.json` を正本に全 `plugin.json` を一致）。版整合を `validate_plugins.py` が検査、一括更新スクリプト `bump_version.py`、タグ `v*` 起点の `release.yml`（GitHub Release 自動生成）、手順書 [RELEASING.md](./RELEASING.md) を追加。
- **全スキル索引 `docs/SKILLS.md` を自動生成（ADR-009）**: `src/lab-core/scripts/gen_catalog.py` が各 SKILL.md の frontmatter から 41 スキルの一覧を生成。`--check` と `tests/test_gen_catalog.py` で「生成結果＝コミット内容」を CI が保証し、一覧ドリフトを構造的に解消。`make catalog` で再生成。
- **プラグイン別スキル数の検査を拡張**: 各プラグイン自身の `README.md` / `README.en.md` の「Skills (N)」見出し（半角・全角括弧）を実体と突き合わせ（automation EN の 6→7 のような取りこぼしを自動検出）。
- **行動規範 `CODE_OF_CONDUCT.md`**（Contributor Covenant v2.1）を追加し CONTRIBUTING（日英）からリンク。
- **カバレッジ計測**: `pytest-cov` と `[tool.coverage]` 設定・`make cov` を追加（CI マトリクスには載せず、ローカル/任意実行）。
- **移植機構 `export_skill.py` を実装（ADR-008）**: SKILL.md を可搬フォーマット（`prompt` / Cursor `.mdc` / `chatgpt`）へ書き出すスクリプトと手順書 [docs/PORTING.md](./docs/PORTING.md) を追加。ADR-003 の「他ツール移植前提」を主張から動く機構へ前進させた。frontmatter を外し各ツールの薄い容れ物へ詰め替えるのみで、判断本文は改変しない。`tests/test_export_skill.py` を追加。
- **検証器の堅牢化**: 必須セクションの **順序**（テンプレートの「順序を変えない」）と **空本文** を検査。`plugin.json` の **version（SemVer）/ description** を検証し keywords 欠落を警告。README の **プラグイン別スキル数カラム** を実体と突き合わせ（automation 6→7 のような表内ドリフトを検出）。`new_skill.load_template` を破損テンプレート（フェンス欠落・name プレースホルダ欠落・必須セクション不足・ファイル不在）に対し早期失敗させた。
- **GitHub Actions ハードニング**: 全ワークフローに per-job `permissions`・`timeout-minutes`・checkout の `persist-credentials: false` を付与し、`actions/checkout` を SHA ピン（actionlint と統一）。PR トリガーに `types: [opened, synchronize, reopened]` を明示。
- **ADR 索引**を `docs/DECISIONS.md` 冒頭に追加（分類・状態・相互参照）。
- **mypy 型チェック**を CI ゲートに追加（`[tool.mypy]`、Python 3.9 基準、4スクリプト対象。`make typecheck` でも実行可）。
- **Roadmap プラグインを本実装**: `lab-strategy-design`（7スキル, `/strategy` `/strategy-review`）と `lab-data-auth-ops`（6スキル, `/data-review`）を追加。収録は 4→6 プラグイン / 27→40 スキルに拡大。既存の forward-reference（`scope-design` / `auth-boundary-check` / `rollback-readiness`）を実体化し、Roadmap 明記を解除。
- **国際化（i18n）**: 英語版 README（ルート + 全6プラグインの `README.en.md`）と `CONTRIBUTING.en.md` を追加し、日本語版と相互リンク。
- **スキャフォルダ `src/lab-core/scripts/new_skill.py`**: テンプレートから新規スキルの雛形を生成（既存は上書きしない）。SKILL.md は手作りを正とし機械的な全文再生成はしない方針を **ADR-006** に記録。「SoT → SKILL」ループを安全な形（雛形生成 + 双方向リンク整合の検証）で実現。
- **`src/` 領域別 Source of Truth 層を実体化**: `src/lab-strategy/`（`strategy-principles.md` / `positioning-reference.md`）と `src/lab-data-auth/`（`data-auth-principles.md` / `pii-classification.md`）を追加。スキルと双方向に参照リンクし、「SoT → SKILL」の依存を明示。
- **`agmsg` スキル**を `lab-automation-architecture` に追加（自動化プラグインは 6 → 7 スキル、リポジトリ合計 40 → 41 スキル）。Claude Code ↔ Codex を共有 SQLite メールボックスで直接メッセージ連携させ、AI 間のコピペ往復を消す導入・運用 skill（upstream: [fujibee/agmsg](https://github.com/fujibee/agmsg), MIT）。
- 欠落していた正本ドキュメントを作成: `docs/CONTEXT.md`, `docs/DECISIONS.md`, `docs/TASKS.md`, `src/lab-core/data/glossary.md`。
- 各プラグインの `README.md`（×4、スキル表 + Command + インストール手順）。`validate_plugins.py` で plugin README の存在と command frontmatter（`description` / `allowed-tools`）も検査。
- CI に pip キャッシュを追加。CONTRIBUTING の品質ゲートに「個人名・内部コードネームを含めない（GATE-3）」「plugin README 更新」を追加。
- `validate_plugins.py` に **スキル相互参照検査**を追加（'`name` skill' 形式の参照は実在するか、未収録なら Roadmap 明記があるかを検査。宙ぶらりん参照の再発を防止）。
- **Markdown / 表記の自動整形**: `markdownlint-cli2`（`.markdownlint-cli2.jsonc`）と `codespell`（`.codespellrc`）を導入し、CI・pre-commit・Makefile に統合。コードフェンスの言語指定・リスト/見出し前後の空行などを正規化。
- `validate_plugins.py` に **内部リンク切れ検出**・skill name の kebab-case 検証・重複 name 検出・description 検証・CRLF 耐性・`--strict` / `--json` / `--version` を追加（ドリフト再発防止）。
- `search.py` に `--json` / `--max` / `--version`・拡張子正規化・`relative_to` の例外保護・ファイル直接指定対応を追加。
- pytest テストスイート（`tests/`、49 ケース）と GitHub Actions CI（ruff + 検証 + テスト、Python 3.9–3.12 マトリクス、docs lint）。
- Claude Code プラグイン化: `.claude-plugin/marketplace.json` と各プラグインの `.claude-plugin/plugin.json`（`/plugin install` で導入可能に）。
- リポジトリ衛生: `.gitattributes`（LF 固定）, `.editorconfig`, `.pre-commit-config.yaml`, `pyproject.toml`, `Makefile`, `SECURITY.md`, PR / Issue テンプレート, `CODEOWNERS`, Dependabot。

### Changed（変更）

- **英語ドキュメントの拡充（i18n パリティ）**: `README.en.md` に「How commands work / Why this structure / AI tool roles / What this repo does not contain」を追加。`CONTRIBUTING.en.md` にテンプレート正本の参照・スキル品質チェックリスト・禁止事項を追加。`README.md`（日）にも「含まれないもの」節を追加。
- **CONTRIBUTING のテンプレート重複を解消（ADR-007 徹底）**: `CONTRIBUTING.md` に埋め込まれていた3つ目のテンプレート複製（LAB Cross-Check が箇条書きで正本の表形式と乖離）を撤去し、正本 `skill-template.md` と `new_skill.py` への参照＋必須セクション表に置換。
- **3層/4層モデルの補足を README（日英）にも反映**。`docs/architecture.md` の `.cursor/rules/` は例示であり実体は持たない旨を明示し、移植の実機構（PORTING.md / export_skill.py）へ誘導。
- `lab-automation-architecture/README.en.md` を 7 スキルへ更新（`agmsg` 行を追加）。
- **雛形テンプレートを単一正本化（重複解消）**: `src/lab-core/templates/skill-template.md` と `new_skill.py` に分裂していた雛形を、`skill-template.md` の ```markdown フェンス1か所に集約。`new_skill.py` はそれを読み取り frontmatter の `name` のみ差し替える（全文再生成はしない / ADR-006 踏襲）。判断は **ADR-007** に記録。
- `.gitignore` を LF 化し、`.pytest_cache` / `.ruff_cache` / `node_modules` 等を追加。
- **スキル description の発見性最適化**: トリガー句（「〜のとき/前に使う」）が無かった 14 スキルの `description` に簡潔な利用トリガーを追記し、AI のスキル自動選択での発見性を改善（意味は不変）。
- 全 Markdown を markdownlint 基準で整形（コードフェンス言語付与・空行整形）。

---

[Unreleased]: https://github.com/thinkyou0714/claude-lab-skills/compare/main...HEAD
