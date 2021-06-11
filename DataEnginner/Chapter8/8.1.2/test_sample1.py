
from sample1 import add


def test_add():
    result = add(1, 2)
    expected = 3
    assert result == expected
