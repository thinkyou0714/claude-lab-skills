"""bump_version.py（版一括更新）のユニットテスト。"""

import bump_version as bv
import pytest


def test_bump_text_replaces_version():
    src = '{\n  "name": "x",\n  "version": "1.0.0",\n  "keywords": ["a"]\n}\n'
    out = bv.bump_text(src, "1.1.0")
    assert '"version": "1.1.0"' in out
    assert '"version": "1.0.0"' not in out
    # 整形は変えない（version 行以外は不変）
    assert '"keywords": ["a"]' in out


def test_bump_text_only_first_version():
    src = '{"version": "1.0.0", "x": {"version": "9.9.9"}}'
    out = bv.bump_text(src, "2.0.0")
    assert out.count('"version": "2.0.0"') == 1
    assert '"version": "9.9.9"' in out  # ネストは触らない


@pytest.mark.parametrize("bad", ["v1", "1.0", "1.0.0.0", "x"])
def test_semver_re_rejects(bad):
    assert not bv.SEMVER_RE.match(bad)
