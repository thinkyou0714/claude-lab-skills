#!/usr/bin/env python3
"""
validate_plugins.py — lab-skills 整合性検証スクリプト

検証内容:
  1. 各 plugin に skills/ ディレクトリが存在する
  2. 各 skill ディレクトリに SKILL.md が存在する（空ディレクトリ検出）
  3. SKILL.md の frontmatter に name: / description: が存在する
  4. frontmatter の name: がディレクトリ名と一致する
  5. SKILL.md に必須セクションが存在する
  6. command ファイルが参照する SKILL.md が実際に存在する

使い方:
  python validate_plugins.py [--root <lab-skills のパス>] [--verbose]
"""

import os
import re
import sys
import argparse
from pathlib import Path

# 必須セクション（## で始まる見出し）
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

# plugin ディレクトリのプレフィックス（検出対象）
PLUGIN_PREFIX = "lab-"

# スキップするディレクトリ名
SKIP_DIRS = {".git", "__pycache__", ".claude", "src"}


def find_plugins(root: Path) -> list[Path]:
    return sorted(
        d for d in root.iterdir()
        if d.is_dir() and d.name.startswith(PLUGIN_PREFIX) and d.name not in SKIP_DIRS
    )


def find_skill_dirs(plugin: Path) -> list[Path]:
    skills_dir = plugin / "skills"
    if not skills_dir.exists():
        return []
    return sorted(d for d in skills_dir.iterdir() if d.is_dir())


def find_command_files(plugin: Path) -> list[Path]:
    commands_dir = plugin / ".claude" / "commands"
    if not commands_dir.exists():
        return []
    return sorted(f for f in commands_dir.iterdir() if f.suffix == ".md")


def parse_frontmatter(content: str) -> dict:
    """--- ... --- ブロックから key: value を抽出する（簡易パーサー）"""
    result = {}
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return result
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip().strip('"')
    return result


def extract_sections(content: str) -> set[str]:
    """## セクション見出しを抽出する"""
    return {m.group(1).strip() for m in re.finditer(r"^## (.+)$", content, re.MULTILINE)}


def extract_command_skill_refs(content: str) -> list[str]:
    """command ファイルから '- skill-name: <path>' 形式のパスを抽出する"""
    return re.findall(r"^- \S+:\s+(\S+\.md)\s*$", content, re.MULTILINE)


class Validator:
    def __init__(self, root: Path, verbose: bool = False):
        self.root = root
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.ok_count = 0

    def err(self, msg: str):
        self.errors.append(f"  [ERROR] {msg}")

    def warn(self, msg: str):
        self.warnings.append(f"  [WARN]  {msg}")

    def ok(self, msg: str):
        self.ok_count += 1
        if self.verbose:
            print(f"  [OK]    {msg}")

    def validate_skill(self, skill_dir: Path):
        skill_md = skill_dir / "SKILL.md"

        # 2. SKILL.md 存在確認
        if not skill_md.exists():
            self.err(f"{skill_dir.relative_to(self.root)}: SKILL.md が存在しない（空ディレクトリ）")
            return

        content = skill_md.read_text(encoding="utf-8")

        # 3. frontmatter 確認
        fm = parse_frontmatter(content)
        if "name" not in fm:
            self.err(f"{skill_md.relative_to(self.root)}: frontmatter に name: がない")
        if "description" not in fm:
            self.err(f"{skill_md.relative_to(self.root)}: frontmatter に description: がない")

        # 4. name: とディレクトリ名の一致確認
        if "name" in fm and fm["name"] != skill_dir.name:
            self.err(
                f"{skill_md.relative_to(self.root)}: name: '{fm['name']}' が"
                f"ディレクトリ名 '{skill_dir.name}' と不一致"
            )

        # 5. 必須セクション確認
        sections = extract_sections(content)
        for required in REQUIRED_SECTIONS:
            if required not in sections:
                self.err(f"{skill_md.relative_to(self.root)}: 必須セクション '## {required}' がない")
            else:
                self.ok(f"{skill_md.relative_to(self.root)}: ## {required}")

    def validate_command(self, command_file: Path, plugin: Path):
        content = command_file.read_text(encoding="utf-8")
        refs = extract_command_skill_refs(content)

        # 6. 参照先 SKILL.md の存在確認
        for ref_path in refs:
            # command ファイルからの相対パスを解決
            resolved = (command_file.parent / ref_path).resolve()
            if not resolved.exists():
                self.err(
                    f"{command_file.relative_to(self.root)}: "
                    f"参照先 '{ref_path}' が存在しない"
                )
            else:
                self.ok(f"{command_file.relative_to(self.root)}: 参照先 '{ref_path}' 確認済み")

    def validate_plugin(self, plugin: Path):
        print(f"\nPlugin: {plugin.name}")

        # 1. skills/ ディレクトリ存在確認
        skills_dir = plugin / "skills"
        if not skills_dir.exists():
            self.err(f"{plugin.name}: skills/ ディレクトリが存在しない")
            return

        skill_dirs = find_skill_dirs(plugin)
        if not skill_dirs:
            self.warn(f"{plugin.name}: skills/ ディレクトリが空")
        else:
            for skill_dir in skill_dirs:
                self.validate_skill(skill_dir)

        # command 検証
        command_files = find_command_files(plugin)
        for cmd in command_files:
            self.validate_command(cmd, plugin)

    def run(self) -> bool:
        plugins = find_plugins(self.root)
        if not plugins:
            print(f"[ERROR] {self.root} に plugin が見つかりません（'{PLUGIN_PREFIX}*' ディレクトリ）")
            return False

        print(f"lab-skills 検証開始: {self.root}")
        print(f"対象 plugin 数: {len(plugins)}")

        for plugin in plugins:
            self.validate_plugin(plugin)

        # 結果サマリー
        print(f"\n{'='*60}")
        print(f"結果サマリー")
        print(f"  OK:      {self.ok_count} 件")
        print(f"  WARN:    {len(self.warnings)} 件")
        print(f"  ERROR:   {len(self.errors)} 件")

        if self.warnings:
            print("\nWARNINGS:")
            for w in self.warnings:
                print(w)

        if self.errors:
            print("\nERRORS:")
            for e in self.errors:
                print(e)
            print(f"\n検証失敗: {len(self.errors)} 件のエラーがあります")
            return False

        print("\n検証成功: すべてのチェックをパスしました")
        return True


def main():
    parser = argparse.ArgumentParser(description="lab-skills 整合性検証スクリプト")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).parent,
        help="lab-skills ディレクトリのパス（デフォルト: スクリプトと同じディレクトリ）",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="OK 判定も出力する",
    )
    args = parser.parse_args()

    validator = Validator(root=args.root.resolve(), verbose=args.verbose)
    success = validator.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
