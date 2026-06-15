"""validate_plugins.py のユニットテスト。"""

import io
import json
from pathlib import Path

import pytest

import validate_plugins as vp

REPO_ROOT = Path(__file__).resolve().parents[1]


# --- ヘルパー ---------------------------------------------------------------

def make_skill_md(name="foo", description="責務の説明。使う場面を含む。", sections=None, extra=""):
    if sections is None:
        sections = vp.REQUIRED_SECTIONS
    fm = f'---\nname: {name}\ndescription: "{description}"\n---\n\n'
    body = "\n".join(f"## {s}\n\n本文\n" for s in sections)
    return fm + body + extra


def make_plugin(root: Path, plugin="lab-test", skills=None):
    if skills is None:
        skills = {"foo": make_skill_md("foo")}
    for skill, content in skills.items():
        d = root / plugin / "skills" / skill
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(content, encoding="utf-8")


def run_validator(root: Path, **kw) -> vp.Validator:
    v = vp.Validator(root=root.resolve(), out=io.StringIO(), **kw)
    v.run()
    return v


# --- parse_frontmatter ------------------------------------------------------

def test_parse_frontmatter_basic():
    fm = vp.parse_frontmatter('---\nname: foo\ndescription: "bar"\n---\nbody')
    assert fm == {"name": "foo", "description": "bar"}


def test_parse_frontmatter_crlf():
    fm = vp.parse_frontmatter('---\r\nname: foo\r\ndescription: "bar"\r\n---\r\nbody')
    assert fm["name"] == "foo"
    assert fm["description"] == "bar"


def test_parse_frontmatter_single_quotes_and_comments():
    fm = vp.parse_frontmatter("---\nname: foo\n# comment\ndescription: 'bar'\n---\n")
    assert fm["name"] == "foo"
    assert fm["description"] == "bar"
    assert "# comment" not in fm


def test_parse_frontmatter_missing():
    assert vp.parse_frontmatter("no frontmatter here") == {}


# --- extract_* --------------------------------------------------------------

def test_extract_sections():
    secs = vp.extract_sections("## A\ntext\n## B\n### C\n")
    assert secs == {"A", "B"}


def test_extract_command_skill_refs():
    text = "- foo: ../../skills/foo/SKILL.md\n- bar: ../../skills/bar/SKILL.md\n"
    assert vp.extract_command_skill_refs(text) == [
        "../../skills/foo/SKILL.md",
        "../../skills/bar/SKILL.md",
    ]


def test_extract_md_links_ignores_fences_and_inline_code():
    # extract_md_links はリンク抽出のみ担当（http 等の除外は validate_links 側）。
    # コードフェンス内・インラインコード内のリンクは抽出されないこと。
    text = (
        "[a](./a.md) and [ext](https://example.com)\n"
        "```\n[infence](./should-be-ignored.md)\n```\n"
        "`[inline](./also-ignored.md)`\n"
    )
    links = vp.extract_md_links(text)
    assert "./a.md" in links
    assert "https://example.com" in links  # 抽出はされる（除外は後段）
    assert "./should-be-ignored.md" not in links
    assert "./also-ignored.md" not in links


# --- skill name 正規表現 ----------------------------------------------------

@pytest.mark.parametrize("name", ["foo", "foo-bar", "a1-b2-c3", "x"])
def test_skill_name_valid(name):
    assert vp.SKILL_NAME_RE.match(name)


@pytest.mark.parametrize(
    "name", ["Foo", "foo_bar", "foo--bar", "-foo", "foo-", "foo bar", "", "1foo", "123"]
)
def test_skill_name_invalid(name):
    assert not vp.SKILL_NAME_RE.match(name)


# --- Validator: 正常系 ------------------------------------------------------

def test_valid_plugin_passes(tmp_path):
    make_plugin(tmp_path)
    v = run_validator(tmp_path)
    assert not v.errors
    assert v.ok_count > 0


# --- Validator: 異常系 ------------------------------------------------------

def test_missing_skill_md(tmp_path):
    (tmp_path / "lab-test" / "skills" / "empty").mkdir(parents=True)
    v = run_validator(tmp_path)
    assert any("SKILL.md が存在しない" in e for e in v.errors)


def test_missing_frontmatter_name(tmp_path):
    md = "---\ndescription: \"x\"\n---\n" + "\n".join(f"## {s}\n\nx\n" for s in vp.REQUIRED_SECTIONS)
    make_plugin(tmp_path, skills={"foo": md})
    v = run_validator(tmp_path)
    assert any("name: がない" in e for e in v.errors)


def test_name_dir_mismatch(tmp_path):
    make_plugin(tmp_path, skills={"foo": make_skill_md(name="bar")})
    v = run_validator(tmp_path)
    assert any("不一致" in e for e in v.errors)


def test_bad_name_format(tmp_path):
    # ディレクトリ名も不正にして「不一致」ではなく「形式」エラーを出させる
    md = make_skill_md(name="Foo_Bar")
    d = tmp_path / "lab-test" / "skills" / "Foo_Bar"
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(md, encoding="utf-8")
    v = run_validator(tmp_path)
    assert any("kebab-case" in e for e in v.errors)


def test_duplicate_name(tmp_path):
    # 2 つの plugin に同じ skill 名 -> 重複検出
    make_plugin(tmp_path, plugin="lab-a", skills={"dup": make_skill_md("dup")})
    make_plugin(tmp_path, plugin="lab-b", skills={"dup": make_skill_md("dup")})
    v = run_validator(tmp_path)
    assert any("重複" in e for e in v.errors)


def test_missing_section(tmp_path):
    md = make_skill_md(sections=["Purpose", "Use When"])  # 大半が欠落
    make_plugin(tmp_path, skills={"foo": md})
    v = run_validator(tmp_path)
    assert any("必須セクション" in e for e in v.errors)


def test_empty_description(tmp_path):
    md = make_skill_md(description="")
    make_plugin(tmp_path, skills={"foo": md})
    v = run_validator(tmp_path)
    assert any("description: が空" in e for e in v.errors)


def test_broken_internal_link(tmp_path):
    md = make_skill_md(extra="\n[broken](./does-not-exist.md)\n")
    make_plugin(tmp_path, skills={"foo": md})
    v = run_validator(tmp_path)
    assert any("が存在しない" in e for e in v.errors)


def test_outside_repo_link(tmp_path):
    md = make_skill_md(extra="\n[outside](../../../../../../etc/passwd)\n")
    make_plugin(tmp_path, skills={"foo": md})
    v = run_validator(tmp_path)
    assert any("リポジトリ外" in e for e in v.errors)


def test_no_plugins(tmp_path):
    v = vp.Validator(root=tmp_path.resolve(), out=io.StringIO())
    assert v.run() is False  # plugin が無ければ False


# --- 統合: 実リポジトリがグリーンであること --------------------------------

def test_real_repo_passes():
    """実リポジトリは error 0・warning 0 でなければならない（回帰ガード）。"""
    v = vp.Validator(root=REPO_ROOT, out=io.StringIO())
    success = v.run()
    assert success, f"errors={v.errors}\nwarnings={v.warnings}"
    assert not v.warnings, f"warnings={v.warnings}"


# --- マニフェスト検査 -------------------------------------------------------

def _write_manifests(root: Path, plugin: str, plugin_name: str, list_in_market: bool = True):
    market_dir = root / ".claude-plugin"
    market_dir.mkdir(parents=True, exist_ok=True)
    plugins = [{"name": plugin, "source": f"./{plugin}"}] if list_in_market else []
    (market_dir / "marketplace.json").write_text(
        json.dumps({"name": "m", "owner": {"name": "o"}, "plugins": plugins}),
        encoding="utf-8",
    )
    pj_dir = root / plugin / ".claude-plugin"
    pj_dir.mkdir(parents=True, exist_ok=True)
    (pj_dir / "plugin.json").write_text(
        json.dumps({
            "name": plugin_name,
            "version": "1.0.0",
            "description": "テスト用プラグイン",
            "keywords": ["test"],
        }),
        encoding="utf-8",
    )


def test_manifest_valid(tmp_path):
    make_plugin(tmp_path, plugin="lab-test")
    _write_manifests(tmp_path, "lab-test", "lab-test")
    v = run_validator(tmp_path)
    assert not v.errors
    assert not any("plugin.json が存在しない" in w for w in v.warnings)


def test_manifest_name_mismatch(tmp_path):
    make_plugin(tmp_path, plugin="lab-test")
    _write_manifests(tmp_path, "lab-test", "wrong-name")
    v = run_validator(tmp_path)
    assert any("不一致" in e for e in v.errors)


def test_manifest_unlisted_plugin(tmp_path):
    make_plugin(tmp_path, plugin="lab-test")
    _write_manifests(tmp_path, "lab-test", "lab-test", list_in_market=False)
    v = run_validator(tmp_path)
    assert any("未登録" in e for e in v.errors)


# --- command frontmatter / plugin README -----------------------------------

def _add_command(root: Path, plugin: str, name="cmd", frontmatter='description: "x"\nallowed-tools: Read'):
    d = root / plugin / ".claude" / "commands"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{name}.md").write_text(f"---\n{frontmatter}\n---\n\n## 手順\n", encoding="utf-8")


def test_command_requires_description(tmp_path):
    make_plugin(tmp_path, plugin="lab-test")
    _add_command(tmp_path, "lab-test", frontmatter="allowed-tools: Read")  # description なし
    v = run_validator(tmp_path)
    assert any("command frontmatter に description" in e for e in v.errors)


def test_command_missing_allowed_tools_warns(tmp_path):
    make_plugin(tmp_path, plugin="lab-test")
    _add_command(tmp_path, "lab-test", frontmatter='description: "x"')  # allowed-tools なし
    v = run_validator(tmp_path)
    assert any("allowed-tools" in w for w in v.warnings)


def test_plugin_missing_readme_warns(tmp_path):
    make_plugin(tmp_path, plugin="lab-test")  # README を作らない
    v = run_validator(tmp_path)
    assert any("README.md がない" in w for w in v.warnings)


# --- スキル相互参照 ---------------------------------------------------------

def test_skill_ref_to_nonexistent_errors(tmp_path):
    md = make_skill_md(name="foo", extra="\n## 参照\n- `nonexistent-skill` skill — x\n")
    make_plugin(tmp_path, skills={"foo": md})
    v = run_validator(tmp_path)
    assert any("参照スキル 'nonexistent-skill' が存在しない" in e for e in v.errors)


def test_skill_ref_roadmap_marker_ok(tmp_path):
    md = make_skill_md(name="foo", extra="\n## 参照\n- `future-skill` skill（Roadmap: 未収録）— x\n")
    make_plugin(tmp_path, skills={"foo": md})
    v = run_validator(tmp_path)
    assert not any("future-skill" in e for e in v.errors)


def test_skill_ref_valid_ok(tmp_path):
    foo = make_skill_md(name="foo", extra="\n## 参照\n- `bar` skill — x\n")
    bar = make_skill_md(name="bar")
    make_plugin(tmp_path, plugin="lab-test", skills={"foo": foo, "bar": bar})
    v = run_validator(tmp_path)
    assert not any("bar" in e and "存在しない" in e for e in v.errors)


def test_skill_ref_qualified_dangling_errors(tmp_path):
    # `plugin/skill` 修飾形式の宙ぶらりん参照も検出されること（R5 で塞いだギャップ）
    md = make_skill_md(name="foo", extra="\n## 参照\n- `other-plugin/missing-skill` skill — x\n")
    make_plugin(tmp_path, skills={"foo": md})
    v = run_validator(tmp_path)
    assert any("other-plugin/missing-skill" in e for e in v.errors)


# --- フェンス処理の統一（コード抽出のバグ修正） -----------------------------

def test_extract_sections_ignores_fenced_headings():
    secs = vp.extract_sections("## Real\n\n```text\n## Fenced\n```\n\n## Real2\n")
    assert "Real" in secs and "Real2" in secs
    assert "Fenced" not in secs


def test_section_inside_fence_does_not_satisfy_requirement(tmp_path):
    # 必須セクションをフェンス内にだけ置いても「欠落」として検出されること（潜在バグの回帰）
    body = [s for s in vp.REQUIRED_SECTIONS if s != "Guardrails"]
    md = make_skill_md(name="foo", sections=body, extra="\n```text\n## Guardrails\n（fence 内）\n```\n")
    make_plugin(tmp_path, skills={"foo": md})
    v = run_validator(tmp_path)
    assert any("## Guardrails" in e for e in v.errors)


def test_extract_command_refs_ignores_fenced():
    text = "- real: ../../skills/real/SKILL.md\n```text\n- fenced: ../../skills/fenced/SKILL.md\n```\n"
    refs = vp.extract_command_skill_refs(text)
    assert "../../skills/real/SKILL.md" in refs
    assert "../../skills/fenced/SKILL.md" not in refs


def test_skill_ref_re_word_boundary():
    assert vp.SKILL_REF_RE.search("`foo` skill —")
    assert vp.SKILL_REF_RE.search("`foo` skill")
    assert not vp.SKILL_REF_RE.search("`foo` skilled developer")
    assert not vp.SKILL_REF_RE.search("`foo` skills are")


# --- 入出力の堅牢化（エッジケース修正） -------------------------------------

def test_read_text_strips_bom(tmp_path):
    p = tmp_path / "x.md"
    p.write_bytes("﻿---\nname: foo\ndescription: \"x\"\n---\n".encode())
    content = vp.read_text(p)
    assert content is not None
    assert vp.parse_frontmatter(content)["name"] == "foo"


def test_nonexistent_root_no_crash(tmp_path):
    v = vp.Validator(root=tmp_path / "does-not-exist", out=io.StringIO())
    assert v.run() is False  # クラッシュせず False を返す


def test_find_skill_dirs_skips_dunder_and_dot(tmp_path):
    base = tmp_path / "lab-x" / "skills"
    (base / "__pycache__").mkdir(parents=True)
    (base / ".hidden").mkdir()
    (base / "real").mkdir()
    names = {d.name for d in vp.find_skill_dirs(tmp_path / "lab-x")}
    assert "real" in names
    assert "__pycache__" not in names and ".hidden" not in names


def test_link_with_title_not_flagged(tmp_path):
    # `[text](./SKILL.md "title")` のタイトル付きリンクを誤って壊れリンク扱いしない
    md = make_skill_md(name="foo", extra='\n## 参照\n[self](./SKILL.md "title")\n')
    make_plugin(tmp_path, skills={"foo": md})
    v = run_validator(tmp_path)
    assert not any("SKILL.md" in e and "存在しない" in e for e in v.errors)


# --- README カウント整合性チェック ------------------------------------------

def _write_readme(root: Path, text: str, fname="README.md"):
    (root / fname).write_text(text, encoding="utf-8")


def test_readme_count_matches_actual(tmp_path):
    # 実体（1 プラグイン / 1 スキル）と一致する README はエラーを出さない
    make_plugin(tmp_path, plugin="lab-x", skills={"foo": make_skill_md("foo")})
    _write_readme(tmp_path, "# t\n\n本リポジトリ収録: 1 プラグイン / 1 スキル\n")
    v = run_validator(tmp_path)
    assert not any("カウント" in e for e in v.errors)


def test_readme_count_drift_flagged(tmp_path):
    # 実体（1/1）と乖離した手書きカウント（6 プラグイン / 40 スキル）はエラー
    make_plugin(tmp_path, plugin="lab-x", skills={"foo": make_skill_md("foo")})
    _write_readme(tmp_path, "# t\n\n収録: 6 プラグイン / 40 スキル\n")
    v = run_validator(tmp_path)
    assert any("カウント" in e and "不一致" in e for e in v.errors)


def test_readme_count_english_pattern(tmp_path):
    # 英語表記（plugins / skills）も検出する
    make_plugin(tmp_path, plugin="lab-x", skills={"foo": make_skill_md("foo")})
    _write_readme(tmp_path, "# t\n\n6 plugins / 40 skills\n", fname="README.en.md")
    v = run_validator(tmp_path)
    assert any("README.en.md" in e and "不一致" in e for e in v.errors)


def test_readme_count_ignores_code_fence(tmp_path):
    # コードフェンス内の「N プラグイン / M スキル」はカウント検査の対象外
    make_plugin(tmp_path, plugin="lab-x", skills={"foo": make_skill_md("foo")})
    _write_readme(tmp_path, "# t\n\n```text\n6 プラグイン / 40 スキル\n```\n")
    v = run_validator(tmp_path)
    assert not any("カウント" in e for e in v.errors)


# --- セクション順序・空本文・plugin.json・プラグイン別カウント -----------------

def test_section_order_enforced(tmp_path):
    # 必須セクションの順序が崩れているとエラー
    reordered = list(vp.REQUIRED_SECTIONS)
    reordered[0], reordered[1] = reordered[1], reordered[0]  # Purpose と Use When を入れ替え
    make_plugin(tmp_path, skills={"foo": make_skill_md("foo", sections=reordered)})
    v = run_validator(tmp_path)
    assert any("順序" in e for e in v.errors)


def test_section_order_ok_in_canonical(tmp_path):
    make_plugin(tmp_path, skills={"foo": make_skill_md("foo")})
    v = run_validator(tmp_path)
    assert not any("順序" in e for e in v.errors)


def test_empty_section_body_flagged(tmp_path):
    fm = '---\nname: foo\ndescription: "責務の説明。使う場面を含む。"\n---\n\n'
    # Purpose を空本文にする
    parts = []
    for s in vp.REQUIRED_SECTIONS:
        body = "" if s == "Purpose" else "本文"
        parts.append(f"## {s}\n\n{body}\n")
    make_plugin(tmp_path, skills={"foo": fm + "\n".join(parts)})
    v = run_validator(tmp_path)
    assert any("本文が空" in e and "Purpose" in e for e in v.errors)


def test_plugin_json_requires_semver(tmp_path):
    make_plugin(tmp_path, plugin="lab-x", skills={"foo": make_skill_md("foo")})
    _write_manifests(tmp_path, "lab-x", "lab-x")
    # version を壊す
    pj = tmp_path / "lab-x" / ".claude-plugin" / "plugin.json"
    import json as _json
    data = _json.loads(pj.read_text(encoding="utf-8"))
    data["version"] = "v1"
    pj.write_text(_json.dumps(data), encoding="utf-8")
    v = run_validator(tmp_path)
    assert any("SemVer" in e for e in v.errors)


def test_per_plugin_count_drift_flagged(tmp_path):
    # README のプラグイン表のスキル数が実体（1）と乖離（9）するとエラー
    make_plugin(tmp_path, plugin="lab-x", skills={"foo": make_skill_md("foo")})
    _write_readme(
        tmp_path,
        "# t\n\n1 プラグイン / 1 スキル\n\n"
        "| Plugin | 責務 | Skill | Cmd |\n|---|---|---|---|\n"
        "| [lab-x](./lab-x/) | r | 9 | `/x` |\n",
    )
    v = run_validator(tmp_path)
    assert any("lab-x" in e and "不一致" in e for e in v.errors)


def test_per_plugin_count_ok(tmp_path):
    make_plugin(tmp_path, plugin="lab-x", skills={"foo": make_skill_md("foo")})
    _write_readme(
        tmp_path,
        "# t\n\n1 プラグイン / 1 スキル\n\n"
        "| Plugin | 責務 | Skill | Cmd |\n|---|---|---|---|\n"
        "| [lab-x](./lab-x/) | r | 1 | `/x` |\n",
    )
    v = run_validator(tmp_path)
    assert not any("lab-x" in e and "不一致" in e for e in v.errors)


def test_plugin_readme_skills_header_drift(tmp_path):
    # プラグイン README の「Skills (N)」見出しが実体（1）と乖離（5）するとエラー
    make_plugin(tmp_path, plugin="lab-x", skills={"foo": make_skill_md("foo")})
    (tmp_path / "lab-x" / "README.md").write_text("# lab-x\n\n## Skills （5）\n", encoding="utf-8")
    v = run_validator(tmp_path)
    assert any("lab-x/README.md" in e and "不一致" in e for e in v.errors)


def test_plugin_readme_skills_header_ok(tmp_path):
    make_plugin(tmp_path, plugin="lab-x", skills={"foo": make_skill_md("foo")})
    (tmp_path / "lab-x" / "README.md").write_text("# lab-x\n\n## Skills (1)\n", encoding="utf-8")
    v = run_validator(tmp_path)
    assert not any("lab-x/README.md" in e and "不一致" in e for e in v.errors)


def test_plugin_version_must_match_marketplace(tmp_path):
    # marketplace に version があるとき plugin.json の version 不一致はエラー（ADR-010）
    make_plugin(tmp_path, plugin="lab-x", skills={"foo": make_skill_md("foo")})
    market_dir = tmp_path / ".claude-plugin"
    market_dir.mkdir(parents=True)
    (market_dir / "marketplace.json").write_text(
        json.dumps({"name": "m", "owner": {"name": "o"}, "version": "1.2.0",
                    "plugins": [{"name": "lab-x", "source": "./lab-x"}]}),
        encoding="utf-8",
    )
    pj_dir = tmp_path / "lab-x" / ".claude-plugin"
    pj_dir.mkdir(parents=True)
    (pj_dir / "plugin.json").write_text(
        json.dumps({"name": "lab-x", "version": "1.0.0", "description": "d", "keywords": ["t"]}),
        encoding="utf-8",
    )
    v = run_validator(tmp_path)
    assert any("marketplace.json の '1.2.0' と不一致" in e for e in v.errors)


def test_parse_frontmatter_skips_empty_key():
    fm = vp.parse_frontmatter("---\n: orphan\nname: foo\n---\n")
    assert fm == {"name": "foo"}
    assert "" not in fm
