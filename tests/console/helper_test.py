# type: ignore

"""Test global helper functions"""

import pytest

from chk.infrastructure.helper import (
    dict_set,
    data_set,
    dict_get,
    data_get,
    is_scalar,
    type_converter,
)


def test_dict_set_pass_when_key_one_dimensional():
    dct = {"a": 1, "b": 2}

    assert dict_set(dct, "a", 21)
    assert dct["a"] == 21


def test_dict_set_pass_when_key_multi_dimensional():
    dct = {"a": {"aa": 1}, "b": 2}
    to_set = [1, 2]

    assert dict_set(dct, "a.aa", to_set)
    assert dct["a"]["aa"] == to_set


def test_dict_set_fail_when_key_do_not_exists():
    dct = {"a": 1, "b": 2}
    with pytest.raises(Exception):
        assert dict_set(dct, "v", 21)


def test_data_set_pass_when_key_one_dimensional():
    dct = {"a": 1, "b": 2}

    assert data_set(dct, "a", 21)
    assert dct["a"] == 21


def test_data_set_pass_when_key_multi_dimensional():
    dct = {"a": {"aa": 1}, "b": 2}
    to_set = [1, 2]

    assert data_set(dct, "a.aa", to_set)
    assert dct["a"]["aa"] == to_set


def test_data_set_pass_when_key_do_not_exists():
    dct = {"a": 1, "b": 2}

    assert data_set(dct, "v", 21)


def test_data_set_pass_when_keymap_deep_dict():
    dct = {}
    to_set = [1, 2]
    keymap = "a.aa.aaa"

    assert data_set(dct, keymap, to_set)
    assert dct["a"]["aa"]["aaa"] == to_set


def test_data_set_fail_when_keymap_deep_dict_but_var_is_list():
    dct = []
    to_set = [1, 2]
    keymap = "a.aa.aaa"

    with pytest.raises(Exception):
        assert data_set(dct, keymap, to_set)
        assert dct["a"]["aa"]["aaa"] == to_set


def test_data_set_pass_when_keymap_deep_dict_or_list_mixed():
    dct = {}
    to_set = [1, 2]
    keymap = "a.0.aa.0.aaa"

    assert data_set(dct, keymap, to_set)
    assert dct["a"][0]["aa"][0]["aaa"] == to_set


def test_data_set_pass_when_keymap_starts_as_list_mixed():
    dct = {}
    to_set = [1, 2]
    keymap = "0.aa.0.aaa"

    assert data_set(dct, keymap, to_set)
    assert dct[0]["aa"][0]["aaa"] == to_set


def test_data_set_pass_when_keymap_starts_as_list_mixed_var_is_list():
    dct = []
    to_set = [1, 2]
    keymap = "0.aa.0.aaa"

    assert data_set(dct, keymap, to_set)
    assert dct[0]["aa"][0]["aaa"] == to_set


def test_data_set_fail_when_incompatible_type_found():
    dct = {"a": [1, {"aa": 1}]}
    to_set = [1, 2]
    keymap = "a.0.aa"

    with pytest.raises(Exception):
        assert data_set(dct, keymap, to_set)


def test_data_set_pass_when_key_found():
    dct = {"a": [1, {"aa": 1}]}
    to_set = [1, 2]
    keymap = "a.1.aa"

    assert data_set(dct, keymap, to_set)
    assert dct["a"][1]["aa"] == to_set


def test_dict_get_pass_when_key_found():
    dct = {"a": {"aa": {"aaa": 1}}}
    keymap = "a.aa.aaa"

    assert dict_get(dct, keymap) == 1


def test_dict_get_pass_return_none_when_key_not_found():
    dct = {"a": {"aa": {"aaa": 1}}}
    keymap = "a.aa.aaaa"

    assert not dict_get(dct, keymap)


def test_dict_get_fail_for_incompatible_type():
    dct = {"a": {"aa": {"aaa": 1}}}
    keymap = "a.aa.aaa.aaaa"

    with pytest.raises(Exception):
        assert not dict_get(dct, keymap)


def test_data_get_pass_when_key_found():
    dct = {"a": {"aa": {"aaa": 1}}}
    keymap = "a.aa.aaa"

    assert data_get(dct, keymap) == 1


def test_data_get_pass_return_none_when_key_not_found():
    dct = {"a": {"aa": {"aaa": 1}}}
    keymap = "a.aa.aaaa"

    assert not data_get(dct, keymap)


def test_data_get_pass_for_non_existent_key():
    dct = {"a": {"aa": {"aaa": 1}}}
    keymap = "a.aa.aaa.aaaa"

    assert not data_get(dct, keymap)


def test_data_get_pass_for_list():
    dct = {"a": {"aa": {"aaa": [1, 2]}}}
    keymap = "a.aa.aaa.1"

    assert data_get(dct, keymap) == 2


def test_data_get_pass_for_list_stating_index():
    dct = [{"aa": {"aaa": [1, 2]}}, 2]
    keymap = "0.aa.aaa.1"

    assert data_get(dct, keymap) == 2


def test_is_scalar_pass():
    lst = [{"aa": {"aaa": [1, 2]}}, 2]
    dct = {"a": 1, "b": 2}
    s = "jo"
    i = 2000000000
    f = 2000000000.222222222

    assert not is_scalar(lst)
    assert not is_scalar(dct)
    assert is_scalar(s)
    assert is_scalar(i)
    assert is_scalar(f)


class TestTypeConverter:
    def test_type_converter_int_pass(self):
        a = "21"
        assert type_converter(a) == 21

    def test_type_converter_int_return_same(self):
        a = "ab"
        assert type_converter(a) == a

    def test_type_converter_float_pass(self):
        a = "21.40000000009"
        assert type_converter(a) == 21.40000000009

    def test_type_converter_truth_pass(self):
        a = "true"
        assert type_converter(a) is True

        a = "True"
        assert type_converter(a) is True

    def test_type_converter_false_pass(self):
        a = "false"
        assert type_converter(a) is False

        a = "False"
        assert type_converter(a) is False

    def test_type_converter_null_pass(self):
        a = "null"
        assert type_converter(a) is None

        a = "None"
        assert type_converter(a) is None

    def test_type_converter_list_pass(self):
        a = "['g', 1, 3]"
        assert type_converter(a) == ["g", 1, 3]

        a = "['a', 1, 3, [3, 4]]"
        assert type_converter(a) == ["a", 1, 3, [3, 4]]

    def test_type_converter_dict_pass(self):
        a = "{'g': 23, 'f': 3}"
        assert type_converter(a) == {"g": 23, "f": 3}

        a = "{'g': 23, 'f': 3, 't': [1, 2]}"
        assert type_converter(a) == {"g": 23, "f": 3, "t": [1, 2]}
