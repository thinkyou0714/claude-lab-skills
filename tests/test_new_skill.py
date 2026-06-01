"""new_skill.py（スキャフォルダ）のユニットテスト。"""

import io

import new_skill

import validate_plugins as vp


def test_build_has_all_required_sections():
    text = new_skill.build_skill("foo")
    sections = vp.extract_sections(text)
    for s in vp.REQUIRED_SECTIONS:
        assert s in sections, f"missing section: {s}"


def test_build_frontmatter_name_and_description():
    fm = vp.parse_frontmatter(new_skill.build_skill("foo-bar"))
    assert fm["name"] == "foo-bar"
    assert fm["description"]  # 非空（プレースホルダ）


def test_required_sections_match_validator():
    # スキャフォルダと検証器の必須セクションが一致していること（ドリフト防止）
    assert new_skill.REQUIRED_SECTIONS == vp.REQUIRED_SECTIONS


def test_invalid_name_rejected():
    assert not new_skill.SKILL_NAME_RE.match("Foo_Bar")
    assert not new_skill.SKILL_NAME_RE.match("foo bar")
    assert new_skill.SKILL_NAME_RE.match("foo-bar")


def test_generated_skill_passes_schema(tmp_path):
    # 生成した雛形が必須セクション・frontmatter・name 検証を通る（schema 的に妥当）
    d = tmp_path / "lab-test" / "skills" / "foo"
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(new_skill.build_skill("foo"), encoding="utf-8")
    v = vp.Validator(root=tmp_path.resolve(), out=io.StringIO())
    v.run()
    assert not any(
        "foo" in e and ("セクション" in e or "frontmatter" in e or "name" in e)
        for e in v.errors
    ), f"unexpected errors: {v.errors}"
