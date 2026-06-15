# RELEASING — リリース手順とバージョニング方針

> English summary below. 設計判断は [docs/DECISIONS.md](./docs/DECISIONS.md) ADR-010 を参照。

## バージョニング方針（Semantic Versioning）

本リポジトリは **単一バージョン方針** を採る。`.claude-plugin/marketplace.json` の `version` を
リリースの正本とし、全 `lab-*/.claude-plugin/plugin.json` の `version` をそれに一致させる
（`validate_plugins.py --strict` が不一致を検出する）。

スキル資産リポジトリとしての版上げ基準:

| 種別 | いつ上げるか | 例 |
|---|---|---|
| **MAJOR** (`X.0.0`) | スキル構造・出力契約の破壊的変更、プラグインの削除/改名 | 必須セクションの変更、`name` 変更 |
| **MINOR** (`0.X.0`) | スキル / プラグインの追加、後方互換な機能追加 | `auth-system-design` 追加 |
| **PATCH** (`0.0.X`) | 既存スキルの文言・整合性・ツールの修正（互換性に影響なし） | 説明の改善、リンク修正 |

## リリース手順

1. `CHANGELOG.md` の `## [Unreleased]` を新バージョン見出しへ繰り下げ、日付を付ける。
2. 版を一括更新する（marketplace.json と全 plugin.json を同じ版に）:

   ```bash
   python3 src/lab-core/scripts/bump_version.py <new-version>   # 例: 1.1.0
   python3 validate_plugins.py --strict            # 版の整合とカウントを確認
   ```

3. 変更を main にマージする。
4. タグを打って push する（`release.yml` が GitHub Release を作成する）:

   ```bash
   git tag v<new-version>
   git push origin v<new-version>
   ```

5. GitHub Actions の `release` ワークフローが Release を作成する。失敗時は手動で
   `gh release create v<new-version> --notes-file <notes>` を実行する。

## English (summary)

Single-version policy: `marketplace.json` `version` is the source of truth; every
`plugin.json` `version` must match it (enforced by `validate_plugins.py --strict`).
SemVer: MAJOR = breaking skill/structure change, MINOR = new skill/plugin, PATCH = fixes.
Bump with `src/lab-core/scripts/bump_version.py <ver>`, then tag `v<ver>` — `release.yml` publishes the
GitHub Release from `CHANGELOG.md`.
