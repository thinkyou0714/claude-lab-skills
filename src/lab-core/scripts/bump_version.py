#!/usr/bin/env python3
"""
bump_version.py — marketplace.json と全 plugin.json の version を一括更新する。

単一バージョン方針（ADR-010）に従い、`.claude-plugin/marketplace.json` と
全 `lab-*/.claude-plugin/plugin.json` の `version` を同一の SemVer に揃える。
version 行のみを置換し、JSON の整形は変更しない（差分を最小化する）。

使い方:
  python src/lab-core/scripts/bump_version.py <new-version>   # 例: 1.1.0

終了コード: 0 = 成功 / 2 = 入力エラー
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VERSION = "1.0.0"

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
_VERSION_LINE_RE = re.compile(r'("version"\s*:\s*")\d+\.\d+\.\d+(")')

PLUGIN_PREFIX = "lab-"
SKIP_DIRS = {".git", "__pycache__", ".claude", "src", "node_modules"}


def bump_text(content: str, new_version: str) -> str:
    """JSON テキスト中の最初の version 行を new_version へ置換する。"""
    return _VERSION_LINE_RE.sub(rf"\g<1>{new_version}\g<2>", content, count=1)


def _manifest_paths(root: Path) -> list[Path]:
    paths = [root / ".claude-plugin" / "marketplace.json"]
    for d in sorted(root.iterdir()):
        if d.is_dir() and d.name.startswith(PLUGIN_PREFIX) and d.name not in SKIP_DIRS:
            pj = d / ".claude-plugin" / "plugin.json"
            if pj.exists():
                paths.append(pj)
    return [p for p in paths if p.exists()]


def main() -> None:
    parser = argparse.ArgumentParser(description="全マニフェストの version を一括更新する")
    parser.add_argument("--version", action="version", version=f"bump_version {VERSION}")
    parser.add_argument("new_version", help="新しいバージョン（SemVer, 例: 1.1.0）")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3],
                        help="リポジトリルート（デフォルト: 推定）")
    args = parser.parse_args()

    if not SEMVER_RE.match(args.new_version):
        print(f"[エラー] SemVer で指定してください（例: 1.1.0）: '{args.new_version}'", file=sys.stderr)
        sys.exit(2)

    paths = _manifest_paths(args.root)
    if not paths:
        print(f"[エラー] マニフェストが見つかりません: {args.root}", file=sys.stderr)
        sys.exit(2)

    changed = 0
    for p in paths:
        original = p.read_text(encoding="utf-8")
        updated = bump_text(original, args.new_version)
        if updated != original:
            p.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"更新: {p.relative_to(args.root)} -> {args.new_version}")
        else:
            print(f"変更なし: {p.relative_to(args.root)}")

    print(f"\n完了: {changed}/{len(paths)} ファイルを {args.new_version} に更新しました。")
    print("次: `python validate_plugins.py --strict` で版の整合を確認してください。")


if __name__ == "__main__":
    main()
