# Changelog

本プロジェクトの主要な変更を記録する。
書式は [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に準拠し、
バージョニングは [Semantic Versioning](https://semver.org/lang/ja/) に従う。

## [Unreleased]

### Fixed（不具合修正）
- モノレポ切り出し時に発生した内部リンク切れ **31 件** を解消（`docs/CONTEXT.md` / `DECISIONS.md` / `TASKS.md` への過剰な `../`、幻プラグインへのリンク）。
- 公開リポジトリに漏出していた私的仕様 `slack-notification-spec.md` への参照を除去。
- **プライバシー / 内部情報のスクラブ（GATE-3）**: 公開リポジトリに残っていた個人名 5 箇所を非個人化（「非エンジニアの関係者」等）、内部コードネーム 8 箇所を一般語（「主力プロダクト（LMS）」等）へ置換。
- README / `docs/architecture.md` / `CONTRIBUTING.md` の記述を実体（4 プラグイン / 27 スキル）に整合。未収録の `lab-strategy-design` / `lab-data-auth-ops` は Roadmap 節へ分離。
- `skill-template.md` の frontmatter（`src` / `version`）を実スキル（`name` / `description`）に整合。

### Added（追加）
- 欠落していた正本ドキュメントを作成: `docs/CONTEXT.md`, `docs/DECISIONS.md`, `docs/TASKS.md`, `src/lab-core/data/glossary.md`。
- 各プラグインの `README.md`（×4、スキル表 + Command + インストール手順）。`validate_plugins.py` で plugin README の存在と command frontmatter（`description` / `allowed-tools`）も検査。
- CI に pip キャッシュを追加。CONTRIBUTING の品質ゲートに「個人名・内部コードネームを含めない（GATE-3）」「plugin README 更新」を追加。
- `validate_plugins.py` に **内部リンク切れ検出**・skill name の kebab-case 検証・重複 name 検出・description 検証・CRLF 耐性・`--strict` / `--json` / `--version` を追加（ドリフト再発防止）。
- `search.py` に `--json` / `--max` / `--version`・拡張子正規化・`relative_to` の例外保護・ファイル直接指定対応を追加。
- pytest テストスイート（`tests/`、41 ケース）と GitHub Actions CI（ruff + 検証 + テスト、Python 3.9–3.12 マトリクス）。
- Claude Code プラグイン化: `.claude-plugin/marketplace.json` と各プラグインの `.claude-plugin/plugin.json`（`/plugin install` で導入可能に）。
- リポジトリ衛生: `.gitattributes`（LF 固定）, `.editorconfig`, `.pre-commit-config.yaml`, `pyproject.toml`, `Makefile`, `SECURITY.md`, PR / Issue テンプレート, `CODEOWNERS`, Dependabot。

### Changed（変更）
- `.gitignore` を LF 化し、`.pytest_cache` / `.ruff_cache` 等を追加。

---

[Unreleased]: https://github.com/thinkyou0714/claude-lab-skills/compare/main...HEAD
