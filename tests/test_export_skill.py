"""export_skill.py（SKILL.md → 可搬フォーマット）のユニットテスト。"""

from pathlib import Path

import export_skill as ex
import pytest

SAMPLE = (
    '---\n'
    'name: issue-framing\n'
    'description: "曖昧な相談を論点に分解する。要件定義前に使う。"\n'
    '---\n\n'
    '## Purpose\n\n本文\n\n## Output Contract\n\n1. 論点\n'
)


def test_split_frontmatter():
    fm, body = ex.split_frontmatter(SAMPLE)
    assert fm["name"] == "issue-framing"
    assert "曖昧な相談" in fm["description"]
    assert body.startswith("## Purpose")
    assert "---" not in body.splitlines()[0]


def test_split_frontmatter_crlf():
    fm, _ = ex.split_frontmatter(SAMPLE.replace("\n", "\r\n"))
    assert fm["name"] == "issue-framing"


def test_split_frontmatter_absent():
    fm, body = ex.split_frontmatter("## Purpose\n\nx")
    assert fm == {}
    assert body.startswith("## Purpose")


@pytest.mark.parametrize("fmt", ["prompt", "cursor", "chatgpt"])
def test_export_contains_name_and_body(tmp_path, fmt):
    p = tmp_path / "SKILL.md"
    p.write_text(SAMPLE, encoding="utf-8")
    out = ex.export_skill(p, fmt)
    assert "issue-framing" in out
    assert "Output Contract" in out  # 判断本文が保持される
    assert "name: issue-framing" not in out  # 元の frontmatter は剥がれる


def test_cursor_has_mdc_frontmatter(tmp_path):
    p = tmp_path / "SKILL.md"
    p.write_text(SAMPLE, encoding="utf-8")
    out = ex.export_skill(p, "cursor")
    assert out.startswith("---\n")
    assert "alwaysApply: false" in out
    assert "globs:" in out


def test_unknown_format_raises(tmp_path):
    p = tmp_path / "SKILL.md"
    p.write_text(SAMPLE, encoding="utf-8")
    with pytest.raises(ValueError):
        ex.export_skill(p, "nope")


def test_empty_body_raises(tmp_path):
    p = tmp_path / "SKILL.md"
    p.write_text('---\nname: x\ndescription: "d"\n---\n', encoding="utf-8")
    with pytest.raises(ValueError):
        ex.export_skill(p, "prompt")


def test_name_falls_back_to_dir(tmp_path):
    d = tmp_path / "my-skill"
    d.mkdir()
    p = d / "SKILL.md"
    p.write_text("## Purpose\n\nbody\n", encoding="utf-8")
    out = ex.export_skill(p, "prompt")
    assert "my-skill" in out


def test_real_skill_exports(tmp_path):
    # 実スキルが全フォーマットで例外なく書き出せること
    repo = Path(__file__).resolve().parents[1]
    skill = repo / "lab-thinking-core" / "skills" / "issue-framing" / "SKILL.md"
    for fmt in ("prompt", "cursor", "chatgpt"):
        out = ex.export_skill(skill, fmt)
        assert "issue-framing" in out
        assert len(out) > 200
