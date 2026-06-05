# Changelog

本プロジェクトの主要な変更を記録する。
書式は [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に準拠し、
バージョニングは [Semantic Versioning](https://semver.org/lang/ja/) に従う。

## [Unreleased]

### Fixed（不具合修正）

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

- **Roadmap プラグインを本実装**: `lab-strategy-design`（7スキル, `/strategy` `/strategy-review`）と `lab-data-auth-ops`（6スキル, `/data-review`）を追加。収録は 4→6 プラグイン / 27→40 スキルに拡大。既存の forward-reference（`scope-design` / `auth-boundary-check` / `rollback-readiness`）を実体化し、Roadmap 明記を解除。
- **国際化（i18n）**: 英語版 README（ルート + 全6プラグインの `README.en.md`）と `CONTRIBUTING.en.md` を追加し、日本語版と相互リンク。
- **スキャフォルダ `src/lab-core/scripts/new_skill.py`**: テンプレートから新規スキルの雛形を生成（既存は上書きしない）。SKILL.md は手作りを正とし機械的な全文再生成はしない方針を **ADR-006** に記録。「SoT → SKILL」ループを安全な形（雛形生成 + 双方向リンク整合の検証）で実現。
- **`src/` 領域別 Source of Truth 層を実体化**: `src/lab-strategy/`（`strategy-principles.md` / `positioning-reference.md`）と `src/lab-data-auth/`（`data-auth-principles.md` / `pii-classification.md`）を追加。スキルと双方向に参照リンクし、「SoT → SKILL」の依存を明示。
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

- `.gitignore` を LF 化し、`.pytest_cache` / `.ruff_cache` / `node_modules` 等を追加。
- **スキル description の発見性最適化**: トリガー句（「〜のとき/前に使う」）が無かった 14 スキルの `description` に簡潔な利用トリガーを追記し、AI のスキル自動選択での発見性を改善（意味は不変）。
- 全 Markdown を markdownlint 基準で整形（コードフェンス言語付与・空行整形）。

---

[Unreleased]: https://github.com/thinkyou0714/claude-lab-skills/compare/main...HEAD
