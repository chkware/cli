"""
test global helper functions
"""
import pytest

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
    with pytest.raises(Exception):
        assert dict_set(dct, "v", 21)


def test_data_set_pass_when_key_one_dimensional():
    dct = {"a": 1, "b": 2}

    assert data_set(dct, "a", 21)
    assert dct['a'] == 21


def test_data_set_pass_when_key_multi_dimensional():
    dct = {"a": {"aa": 1}, "b": 2}
    to_set = [1, 2]

    assert data_set(dct, "a.aa", to_set)
    assert dct['a']['aa'] == to_set


def test_data_set_pass_when_key_do_not_exists():
    dct = {"a": 1, "b": 2}

    assert data_set(dct, "v", 21)


def test_data_set_pass_when_keymap_deep_dict():
    dct = {}
    to_set = [1, 2]
    keymap = "a.aa.aaa"

    assert data_set(dct, keymap, to_set)
    assert dct['a']['aa']['aaa'] == to_set


def test_data_set_fail_when_keymap_deep_dict_but_var_is_list():
    dct = []
    to_set = [1, 2]
    keymap = "a.aa.aaa"

    with pytest.raises(Exception):
        assert data_set(dct, keymap, to_set)
        assert dct['a']['aa']['aaa'] == to_set


def test_data_set_pass_when_keymap_deep_dict_or_list_mixed():
    dct = {}
    to_set = [1, 2]
    keymap = "a.0.aa.0.aaa"

    assert data_set(dct, keymap, to_set)
    assert dct['a'][0]['aa'][0]['aaa'] == to_set


def test_data_set_pass_when_keymap_starts_as_list_mixed():
    dct = {}
    to_set = [1, 2]
    keymap = "0.aa.0.aaa"

    assert data_set(dct, keymap, to_set)
    assert dct[0]['aa'][0]['aaa'] == to_set


def test_data_set_pass_when_keymap_starts_as_list_mixed_var_is_list():
    dct = []
    to_set = [1, 2]
    keymap = "0.aa.0.aaa"

    assert data_set(dct, keymap, to_set)
    assert dct[0]['aa'][0]['aaa'] == to_set


def test_data_set_fail_when_incompatible_type_found():
    dct = {'a': [1, {"aa": 1}]}
    to_set = [1, 2]
    keymap = "a.0.aa"

    with pytest.raises(Exception):
        assert data_set(dct, keymap, to_set)


def test_data_set_pass_when_key_found():
    dct = {'a': [1, {"aa": 1}]}
    to_set = [1, 2]
    keymap = "a.1.aa"

    assert data_set(dct, keymap, to_set)
    assert dct['a'][1]['aa'] == to_set
