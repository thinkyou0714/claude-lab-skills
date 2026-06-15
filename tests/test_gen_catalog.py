"""gen_catalog.py（Skill カタログ生成）のユニットテスト。"""

from pathlib import Path

import gen_catalog as gc

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_catalog_in_sync():
    """docs/SKILLS.md が生成結果と一致していること（ドリフトガード）。"""
    expected = gc.build_catalog(REPO_ROOT)
    actual = (REPO_ROOT / "docs" / "SKILLS.md").read_text(encoding="utf-8")
    assert actual == expected, (
        "docs/SKILLS.md が古い。`python src/lab-core/scripts/gen_catalog.py` で再生成すること。"
    )


def test_catalog_lists_all_skills():
    catalog = gc.build_catalog(REPO_ROOT)
    plugins = gc._find_plugins(REPO_ROOT)
    total = sum(len(gc._find_skill_dirs(p)) for p in plugins)
    # 各スキルへのリンク行数 == 実体のスキル総数
    link_rows = [ln for ln in catalog.splitlines() if ln.startswith("| [`")]
    assert len(link_rows) == total
    assert f"{len(plugins)} プラグイン / {total} スキル" in catalog


def test_cell_escapes_pipe():
    assert gc._cell("a|b") == "a\\|b"
    assert "\n" not in gc._cell("a\nb")


def test_build_catalog_deterministic():
    assert gc.build_catalog(REPO_ROOT) == gc.build_catalog(REPO_ROOT)
