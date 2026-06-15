#!/usr/bin/env python3
"""
export_skill.py — SKILL.md を他ツール向けの可搬フォーマットへ書き出す。

このリポジトリは「思考OS資産は Claude 専用ではなく、他ツール（Cursor / ChatGPT /
Codex 等）へ移植できる」ことを設計原則に掲げている（ADR-003）。本スクリプトは、その
原則を**実際に動く機構**として提供する。SKILL.md は元々ツール中立に書かれているため、
変換は「frontmatter の取り外し」と「各ツールが期待する薄い容れ物への詰め替え」に限定する。
判断本文（Output Contract 等）は改変しない。

使い方:
  python src/lab-core/scripts/export_skill.py <SKILL.md> [--format prompt|cursor|chatgpt]
                                              [--out <file>]

フォーマット:
  prompt   ツール非依存のシステムプロンプト（既定）。任意の LLM の system 欄に貼れる。
  cursor   Cursor の Project Rule（`.mdc`、frontmatter 付き）。
  chatgpt  ChatGPT のカスタム指示 / system メッセージ向けプレーンテキスト。

終了コード: 0 = 成功 / 1 = 入力エラー
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VERSION = "1.0.0"

_FM_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


def normalize_newlines(content: str) -> str:
    """CRLF / CR を LF に正規化する。"""
    return content.replace("\r\n", "\n").replace("\r", "\n")


def split_frontmatter(content: str) -> tuple[dict[str, str], str]:
    """先頭の `--- ... ---` を frontmatter(dict) と本文(str) に分離する。"""
    content = normalize_newlines(content)
    fm: dict[str, str] = {}
    match = _FM_RE.match(content)
    if not match:
        return fm, content.strip()
    for raw in match.group(1).splitlines():
        line = raw.rstrip()
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fm[key.strip()] = value
    body = content[match.end():].strip()
    return fm, body


def to_prompt(name: str, description: str, body: str) -> str:
    """ツール非依存のシステムプロンプトに変換する。"""
    header = (
        f"# 思考スキル: {name}\n\n"
        f"{description}\n\n"
        "あなたは上記スキルを適用する。以下の契約（特に Output Contract と Guardrails）を"
        "厳密に守り、推測で仕様を埋めず、最終判断は人間に委ねること。\n"
    )
    return f"{header}\n---\n\n{body}\n"


def to_cursor(name: str, description: str, body: str) -> str:
    """Cursor の Project Rule（.mdc）に変換する。

    Cursor のルールは frontmatter（description / globs / alwaysApply）を持つ。
    手動適用（@ruleで呼び出す）を想定し alwaysApply は false にする。
    """
    fm = (
        "---\n"
        f"description: {description}\n"
        "globs:\n"
        "alwaysApply: false\n"
        "---\n\n"
    )
    intro = (
        f"# {name}\n\n"
        "このルールを適用するときは、以下の契約に従うこと"
        "（推測で仕様を埋めない / 最終判断は人間）。\n\n"
    )
    return f"{fm}{intro}{body}\n"


def to_chatgpt(name: str, description: str, body: str) -> str:
    """ChatGPT のカスタム指示 / system メッセージ向けプレーンテキストに変換する。"""
    header = (
        f"[Skill: {name}]\n"
        f"{description}\n\n"
        "Apply this skill. Follow the Output Contract and Guardrails exactly. "
        "Do not fill specs by guessing; leave the final decision to the human.\n"
    )
    return f"{header}\n{body}\n"


FORMATTERS = {
    "prompt": to_prompt,
    "cursor": to_cursor,
    "chatgpt": to_chatgpt,
}


def export_skill(skill_md: Path, fmt: str) -> str:
    """SKILL.md を読み、指定フォーマットの文字列を返す。"""
    if fmt not in FORMATTERS:
        raise ValueError(f"未知のフォーマット: {fmt}")
    content = skill_md.read_text(encoding="utf-8-sig")
    fm, body = split_frontmatter(content)
    name = fm.get("name") or skill_md.parent.name
    description = fm.get("description", "")
    if not body:
        raise ValueError(f"本文が空です: {skill_md}")
    return FORMATTERS[fmt](name, description, body)


def main() -> None:
    parser = argparse.ArgumentParser(description="SKILL.md を可搬フォーマットへ書き出す")
    parser.add_argument("--version", action="version", version=f"export_skill {VERSION}")
    parser.add_argument("skill", type=Path, help="SKILL.md のパス")
    parser.add_argument(
        "--format",
        choices=sorted(FORMATTERS),
        default="prompt",
        help="出力フォーマット（既定: prompt）",
    )
    parser.add_argument("--out", type=Path, help="出力先ファイル（省略時は標準出力）")
    args = parser.parse_args()

    if not args.skill.is_file():
        print(f"[エラー] SKILL.md が見つかりません: {args.skill}", file=sys.stderr)
        sys.exit(1)

    try:
        result = export_skill(args.skill, args.format)
    except (ValueError, OSError) as e:
        print(f"[エラー] {e}", file=sys.stderr)
        sys.exit(1)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(result, encoding="utf-8")
        print(f"書き出しました（{args.format}）: {args.out}")
    else:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
