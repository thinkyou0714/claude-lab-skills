#!/usr/bin/env python3
"""
search.py — lab-skills src/ 内の知識資産を検索するスクリプト

使い方:
  python src/lab-core/scripts/search.py <キーワード>
  python src/lab-core/scripts/search.py <キーワード> --path src/lab-strategy
  python src/lab-core/scripts/search.py <キーワード> --ext .md .csv
  python src/lab-core/scripts/search.py <キーワード> --tag rules

説明:
  src/ 配下のファイルをキーワードで全文検索し、
  マッチしたファイルと該当行を出力します。
  外部ライブラリ不要（stdlib のみ）。
"""

import sys
import re
import argparse
from pathlib import Path


def search_files(
    root: Path,
    keyword: str,
    extensions: list[str],
    tag: str | None,
    context_lines: int = 2,
) -> list[dict]:
    """src/ 以下のファイルをキーワード検索する。"""
    results = []
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix not in extensions:
            continue
        # --tag フィルタ（ディレクトリ名に含まれるかチェック）
        if tag and tag not in str(path):
            continue

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, PermissionError):
            continue

        file_hits = []
        for i, line in enumerate(lines):
            if pattern.search(line):
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                snippet = lines[start:end]
                file_hits.append({
                    "line_no": i + 1,
                    "match": line.strip(),
                    "snippet": snippet,
                    "start_line": start + 1,
                })

        if file_hits:
            results.append({
                "path": str(path.relative_to(root.parent)),
                "hits": file_hits,
            })

    return results


def print_results(results: list[dict], keyword: str) -> None:
    if not results:
        print(f"[検索結果なし] キーワード: '{keyword}'")
        return

    print(f"[検索結果] キーワード: '{keyword}' — {len(results)} ファイルにマッチ\n")
    for r in results:
        print(f"  {r['path']}")
        for hit in r["hits"]:
            print(f"    L{hit['line_no']}: {hit['match']}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="lab-skills src/ 内の知識資産を検索する")
    parser.add_argument("keyword", help="検索キーワード")
    parser.add_argument(
        "--path",
        type=Path,
        default=None,
        help="検索対象ディレクトリ（デフォルト: src/）",
    )
    parser.add_argument(
        "--ext",
        nargs="+",
        default=[".md", ".csv", ".json"],
        help="対象ファイル拡張子（デフォルト: .md .csv .json）",
    )
    parser.add_argument(
        "--tag",
        default=None,
        help="ディレクトリ名でフィルタ（例: rules, data, lab-strategy）",
    )
    parser.add_argument(
        "--context",
        type=int,
        default=2,
        help="マッチ行の前後に表示する行数（デフォルト: 2）",
    )
    args = parser.parse_args()

    # デフォルトの検索ルートはスクリプトから3階層上の src/
    script_dir = Path(__file__).parent
    default_root = script_dir.parent.parent  # src/
    root = args.path if args.path else default_root

    if not root.exists():
        print(f"[エラー] 検索対象ディレクトリが存在しません: {root}", file=sys.stderr)
        sys.exit(1)

    results = search_files(
        root=root,
        keyword=args.keyword,
        extensions=args.ext,
        tag=args.tag,
        context_lines=args.context,
    )
    print_results(results, args.keyword)


if __name__ == "__main__":
    main()
