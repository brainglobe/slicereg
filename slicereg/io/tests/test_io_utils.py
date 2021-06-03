import pytest

from slicereg.io.utils import split_keyvalue_string


cases = [
    ("a=3&b=6", "&", "=", {'a': 3., 'b': 6.}),
]
@pytest.mark.parametrize("string,sep1,sep2,expected", cases)
def test_string_splitter(string, sep1, sep2, expected):
    assert expected == split_keyvalue_string(string, sep1, sep2)
