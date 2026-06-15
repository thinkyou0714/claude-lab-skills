#!/usr/bin/env python3
"""
new_skill.py — テンプレートから新しい SKILL.md の雛形を生成する。

「SoT/テンプレート → SKILL」方向の生成を安全に行うためのスキャフォルダ。
既存スキルの内容を機械的に「再生成」はしない（手作りの Output Contract 等を保護するため。
ADR-006 を参照）。生成するのは未着手の雛形のみで、既存ファイルは上書きしない。

使い方:
  python src/lab-core/scripts/new_skill.py <plugin> <skill-name>

既存の SKILL.md は決して上書きしない（手作りの内容を保護するため。ADR-006）。
作り直したい場合は対象ファイルを手動で削除してから再実行する。

生成後:
  - description を埋める（責務 + 使う場面のトリガーを含める）
  - 各セクションを埋める
  - python validate_plugins.py --strict で検証する
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VERSION = "1.0.0"

SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# 必須セクション（validate_plugins.REQUIRED_SECTIONS と一致させること）
REQUIRED_SECTIONS = [
    "Purpose",
    "Use When",
    "Inputs",
    "Output Contract",
    "Review Lens",
    "Instructions",
    "Guardrails",
    "LAB Cross-Check",
    "Handoff Notes",
    "Further Reading",
]

# 雛形の正本（テンプレート本文）はこのファイルではなく
# src/lab-core/templates/skill-template.md の ```markdown フェンス内に置く。
# 生成スクリプトとドキュメントの二重管理を避けるため（ADR-006 / ADR-007）。
TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "skill-template.md"

# テンプレート内の skill 名プレースホルダ（frontmatter の name 行のみ置換する）
_NAME_PLACEHOLDER_RE = re.compile(r"^name:\s*<skill-name>\s*$", re.MULTILINE)
_TEMPLATE_FENCE_RE = re.compile(r"```markdown\n(.*?)\n```", re.DOTALL)


def load_template() -> str:
    """skill-template.md の ```markdown フェンス内の雛形本文を取り出す。

    テンプレート破損を早期に検出するため、フェンスの存在・name プレースホルダ・
    必須セクションの揃いを検証してから返す。
    """
    if not TEMPLATE_PATH.exists():
        raise RuntimeError(f"テンプレートが見つかりません: {TEMPLATE_PATH}")
    text = TEMPLATE_PATH.read_text(encoding="utf-8")
    match = _TEMPLATE_FENCE_RE.search(text)
    if not match:
        raise RuntimeError(
            f"テンプレート本文（```markdown フェンス）が見つかりません: {TEMPLATE_PATH}"
        )
    body = match.group(1).rstrip() + "\n"
    if not _NAME_PLACEHOLDER_RE.search(body):
        raise RuntimeError(
            f"テンプレートに name プレースホルダ（name: <skill-name>）がありません: {TEMPLATE_PATH}"
        )
    headings = {m.group(1).strip() for m in re.finditer(r"^## (.+)$", body, re.MULTILINE)}
    missing = [s for s in REQUIRED_SECTIONS if s not in headings]
    if missing:
        raise RuntimeError(
            f"テンプレートに必須セクションが不足しています {missing}: {TEMPLATE_PATH}"
        )
    return body


def build_skill(name: str) -> str:
    """skill 名から SKILL.md の雛形テキストを生成する（正本: skill-template.md）。"""
    template = load_template()
    return _NAME_PLACEHOLDER_RE.sub(f"name: {name}", template, count=1)


def main() -> None:
    parser = argparse.ArgumentParser(description="新しい SKILL.md の雛形を生成する")
    parser.add_argument("--version", action="version", version=f"new_skill {VERSION}")
    parser.add_argument("plugin", help="プラグインディレクトリ名（例: lab-strategy-design）")
    parser.add_argument("skill", help="スキル名（kebab-case）")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3],
                        help="リポジトリルート（デフォルト: 推定）")
    args = parser.parse_args()

    if not SKILL_NAME_RE.match(args.skill):
        print(f"[エラー] skill 名は kebab-case で指定してください: '{args.skill}'", file=sys.stderr)
        sys.exit(2)

    plugin_dir = args.root / args.plugin
    if not plugin_dir.is_dir():
        print(f"[エラー] プラグインが存在しません: {plugin_dir}", file=sys.stderr)
        sys.exit(1)

    dest = plugin_dir / "skills" / args.skill / "SKILL.md"
    if dest.exists():
        # 既存は決して上書きしない（手作りの Output Contract / Instructions を保護。ADR-006）
        print(
            f"[エラー] 既に存在するため生成しません（作り直すなら手動削除してから）: {dest}",
            file=sys.stderr,
        )
        sys.exit(1)

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(build_skill(args.skill), encoding="utf-8")
    print(f"生成しました: {dest}")
    print("次: description と各セクションを埋め、`python validate_plugins.py --strict` で検証してください。")


if __name__ == "__main__":
    main()
