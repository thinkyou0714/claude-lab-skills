#!/usr/bin/env python3
"""
gen_catalog.py — 全 Skill の発見性インデックス（docs/SKILLS.md）を生成する。

各 SKILL.md の frontmatter（name / description）を走査し、プラグイン別の一覧表を
決定論的に組み立てる。手書き一覧のドリフトを避けるための「生成 + --check」方式。

使い方:
  python src/lab-core/scripts/gen_catalog.py            # docs/SKILLS.md を生成・更新
  python src/lab-core/scripts/gen_catalog.py --check    # 生成結果と既存が一致するか検査（CI 用）

終了コード: 0 = 成功 / 1 = --check で不一致 / 2 = 入力エラー
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VERSION = "1.0.0"

PLUGIN_PREFIX = "lab-"
SKIP_DIRS = {".git", "__pycache__", ".claude", "src", "node_modules"}
_FM_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

CATALOG_REL = Path("docs/SKILLS.md")


def _parse_fm(content: str) -> dict[str, str]:
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    match = _FM_RE.match(content)
    fm: dict[str, str] = {}
    if not match:
        return fm
    for raw in match.group(1).splitlines():
        line = raw.rstrip()
        if not line.lstrip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fm[key.strip()] = value
    return fm


def _find_plugins(root: Path) -> list[Path]:
    return sorted(
        d for d in root.iterdir()
        if d.is_dir() and d.name.startswith(PLUGIN_PREFIX) and d.name not in SKIP_DIRS
    )


def _find_skill_dirs(plugin: Path) -> list[Path]:
    skills_dir = plugin / "skills"
    if not skills_dir.exists():
        return []
    return sorted(
        d for d in skills_dir.iterdir()
        if d.is_dir() and not d.name.startswith((".", "__"))
    )


def _cell(text: str) -> str:
    """テーブルセル用にパイプを退避し改行を畳む。"""
    return text.replace("|", "\\|").replace("\n", " ").strip()


def build_catalog(root: Path) -> str:
    """docs/SKILLS.md の内容文字列を生成する。"""
    plugins = _find_plugins(root)
    total = sum(len(_find_skill_dirs(p)) for p in plugins)
    lines: list[str] = [
        "# Skill カタログ — 全スキル索引",
        "",
        "_このファイルは自動生成です。直接編集しないでください。_",
        "_更新: `python src/lab-core/scripts/gen_catalog.py` / 検査: `--check`（CI）。_",
        "",
        f"収録: **{len(plugins)} プラグイン / {total} スキル**",
    ]
    for plugin in plugins:
        skill_dirs = _find_skill_dirs(plugin)
        lines += ["", f"## {plugin.name}（{len(skill_dirs)}）", "", "| Skill | 説明 |", "|---|---|"]
        for sd in skill_dirs:
            md = sd / "SKILL.md"
            fm = _parse_fm(md.read_text(encoding="utf-8-sig")) if md.exists() else {}
            name = fm.get("name", sd.name)
            desc = fm.get("description", "")
            rel = f"../{plugin.name}/skills/{sd.name}/SKILL.md"
            lines.append(f"| [`{_cell(name)}`]({rel}) | {_cell(desc)} |")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Skill カタログ（docs/SKILLS.md）を生成する")
    parser.add_argument("--version", action="version", version=f"gen_catalog {VERSION}")
    parser.add_argument("--check", action="store_true", help="生成結果と既存ファイルの一致を検査する")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3],
                        help="リポジトリルート（デフォルト: 推定）")
    args = parser.parse_args()

    if not args.root.is_dir():
        print(f"[エラー] ルートが存在しません: {args.root}", file=sys.stderr)
        sys.exit(2)

    content = build_catalog(args.root)
    target = args.root / CATALOG_REL

    if args.check:
        existing = target.read_text(encoding="utf-8") if target.exists() else ""
        if existing != content:
            print(
                f"[不一致] {CATALOG_REL} が最新ではありません。"
                "`python src/lab-core/scripts/gen_catalog.py` で再生成してください。",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"{CATALOG_REL} は最新です。")
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print(f"生成しました: {CATALOG_REL}")


if __name__ == "__main__":
    main()
