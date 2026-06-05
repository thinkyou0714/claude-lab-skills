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

TEMPLATE = """---
name: {name}
description: "（1〜2文で責務を説明。使う場面のトリガーを含めること）"
---

## Purpose

（このスキルが解決する問題を1〜2文で。「〜のリスクを防ぐ」「〜を判断できる状態にする」）

## Use When

- （使う場面・具体的なトリガー）

## Inputs

以下を準備すること。不足している場合は推測せず、不足を明示する。

- **（必須項目）**: （説明）

## Output Contract

以下の順で出力すること。順序を変えない。

1. **論点**: （）
2. **根拠**: その論点をそう判断した理由
3. **判断材料**: 次のアクションを選ぶために人間が確認すべき情報

## Review Lens

- **目的妥当性**: （）
- **範囲の過不足**: （）
- **中長期リスク**: （）
- **LAB全体との整合性**: LMS / 自動化 / B2B 展開と整合しているか
- **非エンジニア理解可能性**: 非エンジニアの関係者に説明できるか
- **他LLM移植耐性**: Claude 固有の解釈に依存していないか

## Instructions

1. （ステップ）
2. 不明な前提は推測せず、仮定を明示する

## Guardrails

- 推測で仕様を埋めない。前提が不明な場合は明示する
- 選択肢を1つに閉じない
- コスト比較を省略しない
- 最終判断は人間に委ねる

## LAB Cross-Check

| 観点 | 状態 | 備考 |
|---|---|---|
| 自動化フロー | — | （） |
| データ / 認証 / ログ | — | （） |
| 実装 / 運用フロー | — | （） |
| 非エンジニア理解可能性 | — | （） |
| 会員共有 / 再利用耐性 | — | （） |
| 他LLM移植耐性 | — | （） |

状態は OK / 注意 / NG / 対象外 で記入すること。

## Handoff Notes

施工AI（Claude Code / Cursor 等）へ渡す前に以下を確定させること。

- **要件**: （）
- **成功条件**: （）
- **失敗条件**: （）
- **実行範囲**: （）
- **影響範囲**: （）
- **ロールバック方針**: （）
- **コスト比較**: （）

## Further Reading

- （関連スキル / src の正本へのリンク）
"""


def build_skill(name: str) -> str:
    """skill 名から SKILL.md の雛形テキストを生成する。"""
    return TEMPLATE.format(name=name)


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
