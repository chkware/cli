"""
test global helper functions
"""
from chk.console.helper import dict_set, data_set


def test_dict_set_pass_when_key_one_dimensional():
    dct = {"a": 1, "b": 2}

    assert dict_set(dct, "a", 21)
    assert dct['a'] == 21


def test_dict_set_pass_when_key_multi_dimensional():
    dct = {"a": {"aa": 1}, "b": 2}
    to_set = [1, 2]

    assert dict_set(dct, "a.aa", to_set)
    assert dct['a']['aa'] == to_set


def test_dict_set_fail_when_key_do_not_exists():
    dct = {"a": 1, "b": 2}

    assert dict_set(dct, "v", 21)


