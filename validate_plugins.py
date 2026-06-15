#!/usr/bin/env python3
"""
validate_plugins.py — lab-skills 整合性検証スクリプト

検証内容:
  1. 各 plugin に skills/ ディレクトリが存在する
  2. 各 skill ディレクトリに SKILL.md が存在する（空ディレクトリ検出）
  3. SKILL.md の frontmatter に name: / description: が存在する
  4. frontmatter の name: がディレクトリ名と一致する
  5. name: が kebab-case（^[a-z0-9]+(-[a-z0-9]+)*$）かつ 64 文字以内
  6. name: がリポジトリ全体で一意（重複検出）
  7. description: が空でない / 長すぎない（<= 1024 文字）
  8. SKILL.md に必須セクションが存在する
  9. command ファイルが参照する SKILL.md が実際に存在する
 10. command の frontmatter に description: がある（allowed-tools: は警告）
 11. 各 plugin に README.md がある（警告）
 12. リポジトリ内の全 .md の相対リンクが解決でき、リポジトリ外を指さない
 13. SKILL.md の '`name` skill' 参照が実在する（未収録なら Roadmap 明記を要求）
 14. .claude-plugin マニフェスト（marketplace.json / plugin.json）が整合している
 15. README の「N プラグイン / M スキル」の数値が実体と一致する（数値ドリフト検出）

使い方:
  python validate_plugins.py [--root <lab-skills のパス>] [--verbose]
                             [--strict] [--no-check-links] [--json]

終了コード:
  0 = 成功（--strict 時は warning も無いこと）
  1 = 失敗（error あり、または --strict 時に warning あり）
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VERSION = "1.0.0"

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

# plugin 検出時にスキップするディレクトリ名
SKIP_DIRS = {".git", "__pycache__", ".claude", "src", "node_modules"}

# リンク検査時にスキップするディレクトリ名（VCS・キャッシュのみ）
LINK_SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", ".pytest_cache"}

# skill name の許容形式（kebab-case）と長さ上限
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME_LEN = 64
MAX_DESC_LEN = 1024

# Markdown リンク・コードフェンスのパターン
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`]*`")

# スキル相互参照（`name` skill / `plugin/name` skill 形式）と Roadmap マーカー
# skill の後ろは語境界（\b）を要求し、"skilled" / "skills" 等の誤マッチを防ぐ
SKILL_REF_RE = re.compile(r"`([a-z][a-z0-9-]*(?:/[a-z0-9-]+)*)`\s*skill\b")
ROADMAP_MARKERS = ("Roadmap", "未収録")

# README の「N プラグイン / M スキル」表記（日本語・英語）を検出する。
# 数値ドリフト（実体と乖離した手書きカウント）を検出するために使う。
README_COUNT_RES = (
    re.compile(r"(\d+)\s*プラグイン\s*/\s*(\d+)\s*スキル"),
    re.compile(r"(\d+)\s*plugins?\s*/\s*(\d+)\s*skills?", re.IGNORECASE),
)
# カウント検査の対象 README（リポジトリルート直下）
README_FILES = ("README.md", "README.en.md")


def normalize_newlines(content: str) -> str:
    """CRLF / CR を LF に正規化する。"""
    return content.replace("\r\n", "\n").replace("\r", "\n")


def parse_frontmatter(content: str) -> dict:
    """--- ... --- ブロックから key: value を抽出する（簡易パーサー）。

    - CRLF 耐性あり
    - 行頭 # のコメント行は無視
    - 値を囲む " または ' を1組だけ除去
    """
    result: dict[str, str] = {}
    content = normalize_newlines(content)
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return result
    for raw in match.group(1).splitlines():
        line = raw.rstrip()
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            result[key.strip()] = value
    return result


def extract_sections(content: str) -> set[str]:
    """## セクション見出しを抽出する（コードフェンス内の見出しは無視）。"""
    content = FENCE_RE.sub("", normalize_newlines(content))
    return {m.group(1).strip() for m in re.finditer(r"^## (.+)$", content, re.MULTILINE)}


def extract_command_skill_refs(content: str) -> list[str]:
    """command ファイルから '- skill-name: <path>' 形式のパスを抽出する（フェンス内は無視）。"""
    content = FENCE_RE.sub("", normalize_newlines(content))
    return re.findall(r"^- \S+:\s+(\S+\.md)\s*$", content, re.MULTILINE)


def extract_md_links(content: str) -> list[str]:
    """Markdown リンク先を抽出する（コードフェンス/インラインコード内は無視）。"""
    content = normalize_newlines(content)
    content = FENCE_RE.sub("", content)
    content = INLINE_CODE_RE.sub("", content)
    return MD_LINK_RE.findall(content)


def extract_skill_refs(content: str) -> list[tuple[str, str]]:
    """'`name` skill' / '`plugin/name` skill' 形式のスキル参照を (token, 行テキスト) で返す（コードフェンス内は無視）。"""
    content = normalize_newlines(content)
    content = FENCE_RE.sub("", content)
    out: list[tuple[str, str]] = []
    for line in content.splitlines():
        for m in SKILL_REF_RE.finditer(line):
            out.append((m.group(1), line))
    return out


def find_plugins(root: Path) -> list[Path]:
    return sorted(
        d for d in root.iterdir()
        if d.is_dir() and d.name.startswith(PLUGIN_PREFIX) and d.name not in SKIP_DIRS
    )


def find_skill_dirs(plugin: Path) -> list[Path]:
    skills_dir = plugin / "skills"
    if not skills_dir.exists():
        return []
    # __pycache__ や隠しディレクトリはスキルとして扱わない
    return sorted(
        d for d in skills_dir.iterdir()
        if d.is_dir() and not d.name.startswith((".", "__"))
    )


def find_command_files(plugin: Path) -> list[Path]:
    commands_dir = plugin / ".claude" / "commands"
    if not commands_dir.exists():
        return []
    return sorted(f for f in commands_dir.iterdir() if f.suffix == ".md")


def read_text(path: Path) -> str | None:
    """UTF-8（BOM 許容）として読む。失敗したら None。"""
    try:
        return path.read_text(encoding="utf-8-sig")
    except (UnicodeDecodeError, OSError):
        return None


class Validator:
    def __init__(
        self,
        root: Path,
        verbose: bool = False,
        strict: bool = False,
        check_links: bool = True,
        out=None,
    ):
        self.root = root
        self.verbose = verbose
        self.strict = strict
        self.check_links_enabled = check_links
        self.out = out if out is not None else sys.stdout
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.ok_count = 0
        self.seen_names: dict[str, Path] = {}

    def err(self, msg: str) -> None:
        self.errors.append(f"  [ERROR] {msg}")

    def warn(self, msg: str) -> None:
        self.warnings.append(f"  [WARN]  {msg}")

    def ok(self, msg: str) -> None:
        self.ok_count += 1
        if self.verbose:
            print(f"  [OK]    {msg}", file=self.out)

    def rel(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.root))
        except ValueError:
            return str(path)

    def validate_skill(self, skill_dir: Path) -> None:
        skill_md = skill_dir / "SKILL.md"

        # 2. SKILL.md 存在確認
        if not skill_md.exists():
            self.err(f"{self.rel(skill_dir)}: SKILL.md が存在しない（空ディレクトリ）")
            return

        content = read_text(skill_md)
        if content is None:
            self.err(f"{self.rel(skill_md)}: UTF-8 として読み込めない")
            return

        rel = self.rel(skill_md)

        # 3. frontmatter 確認
        fm = parse_frontmatter(content)
        if "name" not in fm:
            self.err(f"{rel}: frontmatter に name: がない")
        if "description" not in fm:
            self.err(f"{rel}: frontmatter に description: がない")

        # 4-6. name 検証
        if "name" in fm:
            name = fm["name"]
            if name != skill_dir.name:
                self.err(f"{rel}: name: '{name}' がディレクトリ名 '{skill_dir.name}' と不一致")
            if not SKILL_NAME_RE.match(name):
                self.err(f"{rel}: name: '{name}' は kebab-case ではない（^[a-z0-9]+(-[a-z0-9]+)*$）")
            if len(name) > MAX_NAME_LEN:
                self.err(f"{rel}: name: が長すぎる（{len(name)} > {MAX_NAME_LEN} 文字）")
            if name in self.seen_names:
                self.err(f"{rel}: name: '{name}' が重複（既出: {self.rel(self.seen_names[name])}）")
            else:
                self.seen_names[name] = skill_md

        # 7. description 検証
        if "description" in fm:
            desc = fm["description"]
            if not desc:
                self.err(f"{rel}: description: が空")
            elif len(desc) > MAX_DESC_LEN:
                self.warn(f"{rel}: description: が長い（{len(desc)} > {MAX_DESC_LEN} 文字）")
            else:
                self.ok(f"{rel}: description ({len(desc)} 文字)")

        # 8. 必須セクション確認
        sections = extract_sections(content)
        for required in REQUIRED_SECTIONS:
            if required not in sections:
                self.err(f"{rel}: 必須セクション '## {required}' がない")
            else:
                self.ok(f"{rel}: ## {required}")

    def validate_command(self, command_file: Path) -> None:
        content = read_text(command_file)
        if content is None:
            self.err(f"{self.rel(command_file)}: UTF-8 として読み込めない")
            return
        rel = self.rel(command_file)

        # command frontmatter 検査
        fm = parse_frontmatter(content)
        if not fm.get("description"):
            self.err(f"{rel}: command frontmatter に description: がない")
        else:
            self.ok(f"{rel}: command description")
        if "allowed-tools" not in fm:
            self.warn(f"{rel}: command に allowed-tools: の宣言がない")

        for ref_path in extract_command_skill_refs(content):
            resolved = (command_file.parent / ref_path).resolve()
            if not resolved.exists():
                self.err(f"{self.rel(command_file)}: 参照先 '{ref_path}' が存在しない")
            else:
                self.ok(f"{self.rel(command_file)}: 参照先 '{ref_path}' 確認済み")

    def validate_plugin(self, plugin: Path) -> None:
        print(f"\nPlugin: {plugin.name}", file=self.out)

        # 1. skills/ ディレクトリ存在確認
        skills_dir = plugin / "skills"
        if not skills_dir.exists():
            self.err(f"{plugin.name}: skills/ ディレクトリが存在しない")
            return

        # plugin README の存在確認（AP-D4: README なしでファイルを増やさない）
        if (plugin / "README.md").exists():
            self.ok(f"{plugin.name}: README.md")
        else:
            self.warn(f"{plugin.name}: README.md がない")

        skill_dirs = find_skill_dirs(plugin)
        if not skill_dirs:
            self.warn(f"{plugin.name}: skills/ ディレクトリが空")
        else:
            for skill_dir in skill_dirs:
                self.validate_skill(skill_dir)

        for cmd in find_command_files(plugin):
            self.validate_command(cmd)

    def validate_links(self) -> None:
        """リポジトリ内の全 .md の相対リンク健全性を検査する。"""
        print("\nリンク検査: リポジトリ内 .md の相対リンク", file=self.out)
        md_files = [
            p for p in sorted(self.root.rglob("*.md"))
            if not (set(p.relative_to(self.root).parts) & LINK_SKIP_DIRS)
        ]
        for md in md_files:
            content = read_text(md)
            if content is None:
                self.err(f"{self.rel(md)}: UTF-8 として読み込めない")
                continue
            for target in extract_md_links(content):
                t = target.strip()
                # <url> 形式、および `url "title"` のタイトル付き形式を正規化する
                if t.startswith("<") and ">" in t:
                    t = t[1:t.index(">")].strip()
                else:
                    parts = t.split(None, 1)
                    t = parts[0] if parts else ""
                if not t or t.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                path_part = t.split("#", 1)[0].strip()
                if not path_part:
                    continue
                resolved = (md.parent / path_part).resolve()
                try:
                    resolved.relative_to(self.root)
                    inside = True
                except ValueError:
                    inside = False
                if not inside:
                    self.err(f"{self.rel(md)}: リンク '{t}' がリポジトリ外を指す")
                elif not resolved.exists():
                    self.err(f"{self.rel(md)}: リンク先 '{t}' が存在しない")
                else:
                    self.ok(f"{self.rel(md)}: リンク '{t}'")

    def validate_skill_refs(self, plugins: list[Path]) -> None:
        """SKILL.md 内の '`name` skill' 参照が実在するか検査する。

        実在しない場合、同じ行に Roadmap/未収録 の明記があれば許容、なければ error。
        （Round 1 の方針に従い、未収録スキルへの forward-reference は明示する）
        """
        print("\nスキル相互参照チェック: '`name` skill'", file=self.out)
        valid = set(self.seen_names)
        for plugin in plugins:
            for skill_dir in find_skill_dirs(plugin):
                md = skill_dir / "SKILL.md"
                content = read_text(md)
                if content is None:
                    continue
                for token, line in extract_skill_refs(content):
                    # `plugin/skill` 修飾も許容し、末尾セグメントで実在判定する
                    name = token.rsplit("/", 1)[-1]
                    if name in valid:
                        self.ok(f"{self.rel(md)}: skill ref '{token}'")
                    elif any(mk in line for mk in ROADMAP_MARKERS):
                        self.ok(f"{self.rel(md)}: skill ref '{token}'（Roadmap 明記）")
                    else:
                        self.err(
                            f"{self.rel(md)}: 参照スキル '{token}' が存在しない"
                            "（実在しないなら Roadmap/未収録 を明記すること）"
                        )

    def _load_json(self, path: Path):
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError) as e:
            self.err(f"{self.rel(path)}: JSON として読めない（{e}）")
            return None

    def validate_manifests(self, plugins: list[Path]) -> None:
        """.claude-plugin/ の marketplace.json / plugin.json の整合を検査する。"""
        print("\nマニフェスト検査: .claude-plugin/", file=self.out)

        listed_names: set[str] = set()
        market = self.root / ".claude-plugin" / "marketplace.json"
        if not market.exists():
            self.warn(".claude-plugin/marketplace.json が存在しない")
        else:
            data = self._load_json(market)
            if isinstance(data, dict):
                if not data.get("name"):
                    self.err(f"{self.rel(market)}: name がない")
                owner = data.get("owner")
                if not isinstance(owner, dict) or not owner.get("name"):
                    self.err(f"{self.rel(market)}: owner.name がない")
                for entry in data.get("plugins", []):
                    if not isinstance(entry, dict):
                        continue
                    if entry.get("name"):
                        listed_names.add(entry["name"])
                    src = entry.get("source")
                    if src:
                        resolved = (self.root / src).resolve()
                        if not resolved.exists():
                            self.err(f"{self.rel(market)}: source '{src}' が存在しない")
                        else:
                            self.ok(f"marketplace source '{src}'")

        for plugin in plugins:
            pj = plugin / ".claude-plugin" / "plugin.json"
            if not pj.exists():
                self.warn(f"{plugin.name}: .claude-plugin/plugin.json が存在しない")
            else:
                data = self._load_json(pj)
                if isinstance(data, dict):
                    name = data.get("name")
                    if not name:
                        self.err(f"{self.rel(pj)}: name がない")
                    elif name != plugin.name:
                        self.err(
                            f"{self.rel(pj)}: name '{name}' がディレクトリ名 '{plugin.name}' と不一致"
                        )
                    else:
                        self.ok(f"{self.rel(pj)}: name 一致")
            if market.exists() and plugin.name not in listed_names:
                self.err(f"{plugin.name}: marketplace.json の plugins に未登録")

    def validate_readme_counts(self, plugins: list[Path]) -> None:
        """README の「N プラグイン / M スキル」が実体と一致するか検査する。

        手書きのカウントは実体から乖離しやすい（ドリフト）。プラグイン数・スキル総数を
        実体から数え、README 内の表記と突き合わせる。コードフェンス内は無視する。
        """
        print("\nカウント整合性チェック: README の「N プラグイン / M スキル」", file=self.out)
        actual_plugins = len(plugins)
        actual_skills = sum(len(find_skill_dirs(p)) for p in plugins)
        for fname in README_FILES:
            md = self.root / fname
            if not md.exists():
                continue
            content = read_text(md)
            if content is None:
                self.err(f"{fname}: UTF-8 として読み込めない")
                continue
            content = FENCE_RE.sub("", normalize_newlines(content))
            found = False
            for pattern in README_COUNT_RES:
                for m in pattern.finditer(content):
                    found = True
                    p_count, s_count = int(m.group(1)), int(m.group(2))
                    if p_count != actual_plugins or s_count != actual_skills:
                        self.err(
                            f"{fname}: カウント '{m.group(0)}' が実体と不一致"
                            f"（実体: {actual_plugins} プラグイン / {actual_skills} スキル）"
                        )
                    else:
                        self.ok(f"{fname}: カウント '{m.group(0)}'")
            if not found:
                self.warn(f"{fname}: 「N プラグイン / M スキル」表記が見つからない")

    def run(self) -> bool:
        if not self.root.is_dir():
            print(f"[ERROR] ルートディレクトリが存在しません: {self.root}", file=self.out)
            return False
        plugins = find_plugins(self.root)
        if not plugins:
            print(
                f"[ERROR] {self.root} に plugin が見つかりません（'{PLUGIN_PREFIX}*' ディレクトリ）",
                file=self.out,
            )
            return False

        print(f"lab-skills 検証開始: {self.root}", file=self.out)
        print(f"対象 plugin 数: {len(plugins)}", file=self.out)

        for plugin in plugins:
            self.validate_plugin(plugin)

        if self.check_links_enabled:
            self.validate_links()

        self.validate_skill_refs(plugins)
        self.validate_manifests(plugins)
        self.validate_readme_counts(plugins)

        # 結果サマリー
        print(f"\n{'=' * 60}", file=self.out)
        print("結果サマリー", file=self.out)
        print(f"  OK:      {self.ok_count} 件", file=self.out)
        print(f"  WARN:    {len(self.warnings)} 件", file=self.out)
        print(f"  ERROR:   {len(self.errors)} 件", file=self.out)

        if self.warnings:
            print("\nWARNINGS:", file=self.out)
            for w in self.warnings:
                print(w, file=self.out)

        if self.errors:
            print("\nERRORS:", file=self.out)
            for e in self.errors:
                print(e, file=self.out)

        failed = bool(self.errors) or (self.strict and bool(self.warnings))
        if failed:
            reason = f"{len(self.errors)} 件のエラー"
            if self.strict and self.warnings:
                reason += f" / {len(self.warnings)} 件の警告（--strict）"
            print(f"\n検証失敗: {reason} があります", file=self.out)
            return False

        print("\n検証成功: すべてのチェックをパスしました", file=self.out)
        return True

    def summary_dict(self, success: bool) -> dict:
        return {
            "success": success,
            "ok": self.ok_count,
            "warnings": [w.strip() for w in self.warnings],
            "errors": [e.strip() for e in self.errors],
            "root": str(self.root),
            "version": VERSION,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="lab-skills 整合性検証スクリプト")
    parser.add_argument("--version", action="version", version=f"validate_plugins {VERSION}")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).parent,
        help="lab-skills ディレクトリのパス（デフォルト: スクリプトと同じディレクトリ）",
    )
    parser.add_argument("--verbose", action="store_true", help="OK 判定も出力する")
    parser.add_argument("--strict", action="store_true", help="warning も失敗扱いにする")
    parser.add_argument("--no-check-links", action="store_true", help="リンク検査を無効化する")
    parser.add_argument("--json", action="store_true", help="結果を JSON で stdout に出力する")
    args = parser.parse_args()

    # --json 時は進捗ログを stderr へ送り、stdout を純粋な JSON に保つ
    out = sys.stderr if args.json else sys.stdout
    validator = Validator(
        root=args.root.resolve(),
        verbose=args.verbose,
        strict=args.strict,
        check_links=not args.no_check_links,
        out=out,
    )
    success = validator.run()

    if args.json:
        print(json.dumps(validator.summary_dict(success), ensure_ascii=False, indent=2))

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
