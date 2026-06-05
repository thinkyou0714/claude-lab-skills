"""search.py のユニットテスト。"""

from pathlib import Path

import search

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"


# --- normalize_extensions ---------------------------------------------------

def test_normalize_extensions_adds_dot_and_lowercases():
    assert search.normalize_extensions(["md", ".MD", "CSV"]) == [".md", ".md", ".csv"]


def test_normalize_extensions_skips_empty():
    assert search.normalize_extensions(["", "  ", ".md"]) == [".md"]


# --- search_files -----------------------------------------------------------

def _seed(tmp_path: Path):
    (tmp_path / "a.md").write_text("hello WORLD\nsecond line\n", encoding="utf-8")
    (tmp_path / "b.md").write_text("nothing here\n", encoding="utf-8")
    (tmp_path / "c.txt").write_text("world but txt\n", encoding="utf-8")
    sub = tmp_path / "rules"
    sub.mkdir()
    (sub / "d.md").write_text("world in rules\n", encoding="utf-8")


def test_search_finds_keyword_case_insensitive(tmp_path):
    _seed(tmp_path)
    res = search.search_files(tmp_path, "world", [".md"], None)
    paths = {r["path"] for r in res}
    # a.md と rules/d.md がヒット、b.md はヒットしない
    assert any(p.endswith("a.md") for p in paths)
    assert any("d.md" in p for p in paths)
    assert not any(p.endswith("b.md") for p in paths)


def test_search_respects_extension_filter(tmp_path):
    _seed(tmp_path)
    res = search.search_files(tmp_path, "world", [".md"], None)
    # .txt は対象外
    assert not any(r["path"].endswith("c.txt") for r in res)
    res_txt = search.search_files(tmp_path, "world", [".txt"], None)
    assert any(r["path"].endswith("c.txt") for r in res_txt)


def test_search_tag_filter(tmp_path):
    _seed(tmp_path)
    res = search.search_files(tmp_path, "world", [".md"], tag="rules")
    assert res
    assert all("rules" in r["path"] for r in res)


def test_search_max_results(tmp_path):
    _seed(tmp_path)
    res = search.search_files(tmp_path, "world", [".md"], None, max_results=1)
    assert len(res) == 1


def test_search_max_zero_means_unlimited(tmp_path):
    # max_results=0/負値は「制限なし」として扱う（CLI 側では --max>=1 を要求）
    _seed(tmp_path)
    full = search.search_files(tmp_path, "world", [".md"], None)
    assert search.search_files(tmp_path, "world", [".md"], None, max_results=0) == full


def test_search_single_file_root(tmp_path):
    _seed(tmp_path)
    res = search.search_files(tmp_path / "a.md", "world", [".md"], None)
    assert len(res) == 1


def test_search_no_match_returns_empty(tmp_path):
    _seed(tmp_path)
    assert search.search_files(tmp_path, "no-such-token", [".md"], None) == []


# --- display_path（ValueError 耐性）----------------------------------------

def test_display_path_does_not_crash(tmp_path):
    # 無関係なパス同士でも例外を出さず文字列を返す
    out = search.display_path(tmp_path / "x.md", Path("/totally/unrelated"))
    assert isinstance(out, str)


# --- 統合: 実 src/ を検索 ---------------------------------------------------

def test_search_real_src_glossary():
    res = search.search_files(SRC_ROOT, "判断ゲート", [".md"], None)
    assert any("glossary.md" in r["path"] for r in res)
