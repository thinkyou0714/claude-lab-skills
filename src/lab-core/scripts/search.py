#!/usr/bin/env python3
"""
search.py — lab-skills src/ 内の知識資産を検索するスクリプト

使い方:
  python src/lab-core/scripts/search.py <キーワード>
  python src/lab-core/scripts/search.py <キーワード> --path src/lab-core
  python src/lab-core/scripts/search.py <キーワード> --ext .md .csv
  python src/lab-core/scripts/search.py <キーワード> --tag rules
  python src/lab-core/scripts/search.py <キーワード> --json --max 20

説明:
  src/ 配下のファイルをキーワードで全文検索し、
  マッチしたファイルと該当行を出力します。
  外部ライブラリ不要（stdlib のみ）。

終了コード:
  0 = 正常（マッチ有無に関わらず）
  1 = 検索対象パスが存在しない等のエラー
  2 = 引数エラー（argparse）
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VERSION = "1.0.0"

DEFAULT_EXTENSIONS = [".md", ".csv", ".json"]


def normalize_extensions(exts: list[str]) -> list[str]:
    """'md' のような拡張子に先頭ドットを補い、小文字化する。"""
    out = []
    for e in exts:
        e = e.strip().lower()
        if not e:
            continue
        if not e.startswith("."):
            e = "." + e
        out.append(e)
    return out


def iter_target_files(root: Path):
    """検索対象ファイルを列挙する（root がファイルならそれ自身）。"""
    if root.is_file():
        yield root
        return
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path


def display_path(path: Path, root: Path) -> str:
    """表示用の相対パスを安全に算出する（失敗時は絶対パス文字列）。"""
    for base in (Path.cwd(), root if root.is_dir() else root.parent, root.parent):
        try:
            return str(path.resolve().relative_to(base.resolve()))
        except ValueError:
            continue
    return str(path.resolve())


def search_files(
    root: Path,
    keyword: str,
    extensions: list[str],
    tag: str | None,
    context_lines: int = 2,
    max_results: int | None = None,
) -> list[dict]:
    """root 以下のファイルをキーワード検索する。"""
    results: list[dict] = []
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)

    for path in iter_target_files(root):
        if path.suffix.lower() not in extensions:
            continue
        if tag and tag not in str(path):
            continue

        try:
            lines = path.read_text(encoding="utf-8-sig").splitlines()
        except (UnicodeDecodeError, PermissionError, OSError):
            continue

        file_hits = []
        for i, line in enumerate(lines):
            if pattern.search(line):
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                file_hits.append({
                    "line_no": i + 1,
                    "match": line.strip(),
                    "snippet": lines[start:end],
                    "start_line": start + 1,
                })

        if file_hits:
            results.append({
                "path": display_path(path, root),
                "hits": file_hits,
            })
            if max_results is not None and max_results >= 1 and len(results) >= max_results:
                break

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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="lab-skills src/ 内の知識資産を検索する")
    parser.add_argument("--version", action="version", version=f"search {VERSION}")
    parser.add_argument("keyword", help="検索キーワード")
    parser.add_argument(
        "--path",
        type=Path,
        default=None,
        help="検索対象ディレクトリまたはファイル（デフォルト: src/）",
    )
    parser.add_argument(
        "--ext",
        nargs="+",
        default=DEFAULT_EXTENSIONS,
        help="対象ファイル拡張子（デフォルト: .md .csv .json）",
    )
    parser.add_argument(
        "--tag",
        default=None,
        help="パスに含まれる文字列でフィルタ（例: rules, data, lab-core）",
    )
    parser.add_argument(
        "--context",
        type=int,
        default=2,
        help="マッチ行の前後に表示する行数（デフォルト: 2）",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=None,
        help="最大マッチファイル数（デフォルト: 無制限）",
    )
    parser.add_argument("--json", action="store_true", help="結果を JSON で出力する")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    # デフォルトの検索ルートはスクリプトから2階層上の src/
    script_dir = Path(__file__).resolve().parent
    default_root = script_dir.parent.parent  # src/
    root = args.path if args.path else default_root

    if not root.exists():
        print(f"[エラー] 検索対象が存在しません: {root}", file=sys.stderr)
        sys.exit(1)

    if args.context < 0:
        print("[エラー] --context は 0 以上で指定してください", file=sys.stderr)
        sys.exit(1)

    if args.max is not None and args.max < 1:
        print("[エラー] --max は 1 以上で指定してください", file=sys.stderr)
        sys.exit(1)

    results = search_files(
        root=root,
        keyword=args.keyword,
        extensions=normalize_extensions(args.ext),
        tag=args.tag,
        context_lines=args.context,
        max_results=args.max,
    )

    if args.json:
        print(json.dumps(
            {"keyword": args.keyword, "count": len(results), "results": results},
            ensure_ascii=False,
            indent=2,
        ))
    else:
        print_results(results, args.keyword)


if __name__ == "__main__":
    main()
