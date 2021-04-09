import ast

import pytest

from pandas_dev_flaker.__main__ import Plugin


def results(s):
    return {"{}:{}: {}".format(*r) for r in Plugin(ast.parse(s)).run()}


@pytest.mark.parametrize(
    "source",
    (
        pytest.param(
            "with pytest.raises(ValueError, match='foo'):\n" "   pass",
            id="pytest.raises used in context manager",
        ),
        pytest.param(
            "from foo import raises\n" "raises(ValueError, match='foo')",
            id="raises not imported",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "pytest.raises(ValueError, match='foo')",
            "1:0: PDF005 'pytest.raises' used outside of context manager",
            id="pytest.raises used without context manager",
        ),
        pytest.param(
            "from pytest import raises\n" "raises(ValueError, match='foo')",
            "2:0: PDF005 'pytest.raises' used outside of context manager",
            id="raises imported from pytest",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
