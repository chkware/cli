# type: ignore
"""
test global chk functions
"""
import sys
from io import TextIOWrapper, BytesIO

import pytest

from chk.infrastructure.helper import (
    dict_set,
    data_set,
    dict_get,
    data_get,
    is_scalar,
    Cast,
    parse_args,
    formatter,
)


class TestParseArgs:
    def test_parse_args_pass_for_unique(self):
        argv_s = ["Var1=Val1", "Var2=Val2", "Var3=Val3", "Var=Val"]
        response = parse_args(argv_s)

        assert isinstance(response, dict)
        assert len(response) == 4

    def test_parse_args_pass_for_override(self):
        argv_s = ["Var1=Val1", "Var2=Val2", "Var3=Val3", "Var1=Val4"]
        response = parse_args(argv_s)

        assert isinstance(response, dict)
        assert len(response) == 3


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


def test_data_set_fail_when_keymap_starts_as_list_mixed():
    dct = {}
    to_set = [1, 2]
    keymap = "0.aa.0.aaa"

    with pytest.raises(IndexError):
        data_set(dct, keymap, to_set)


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


class TestCast:
    def test_to_auto_int_pass(self):
        a = "21"
        assert Cast.to_auto(a) == 21

    def test_to_auto_int_return_same(self):
        a = "ab"
        assert Cast.to_auto(a) == a

    def test_to_auto_float_pass(self):
        a = "21.40000000009"
        assert Cast.to_auto(a) == 21.40000000009

    def test_to_auto_truth_pass(self):
        a = "true"
        assert Cast.to_auto(a) is True

        a = "True"
        assert Cast.to_auto(a) is True

    def test_to_auto_false_pass(self):
        a = "false"
        assert Cast.to_auto(a) is False

        a = "False"
        assert Cast.to_auto(a) is False

    def test_to_auto_null_pass(self):
        a = "null"
        assert Cast.to_auto(a) is None

        a = "None"
        assert Cast.to_auto(a) is None

    def test_to_auto_list_pass(self):
        a = "['g', 1, 3]"
        assert Cast.to_auto(a) == ["g", 1, 3]

        a = "['a', 1, 3, [3, 4]]"
        assert Cast.to_auto(a) == ["a", 1, 3, [3, 4]]

    def test_to_auto_dict_pass(self):
        a = "{'g': 23, 'f': 3}"
        assert Cast.to_auto(a) == {"g": 23, "f": 3}

        a = "{'g': 23, 'f': 3, 't': [1, 2]}"
        assert Cast.to_auto(a) == {"g": 23, "f": 3, "t": [1, 2]}

        a = "{'g': 23, 'f': 3, 't': [1, {'a': 2}]}"
        assert Cast.to_auto(a) == {"g": 23, "f": 3, "t": [1, {"a": 2}]}


def test_formatter_pass_get_string():
    assert formatter("Some", dump=False) == "Some"


def test_formatter_pass_get_string_with_cb():
    def cb(val):
        return f"1:{val}"

    assert formatter("Some", cb, False) == "1:Some"


def test_formatter_pass_print():
    # setup the environment
    old_stdout = sys.stdout
    sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

    formatter("Some")

    # get output
    sys.stdout.seek(0)  # jump to the start
    out = sys.stdout.read()  # read output

    # restore stdout
    sys.stdout.close()
    sys.stdout = old_stdout

    # assert
    assert out == "Some\n"


def test_formatter_pass_print_with_cb():
    def fmt(val):
        return f"1:{val}"

    # setup the environment
    old_stdout = sys.stdout
    sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

    formatter("Some", fmt)

    # get output
    sys.stdout.seek(0)  # jump to the start
    out = sys.stdout.read()  # read output

    # restore stdout
    sys.stdout.close()
    sys.stdout = old_stdout

    # assert
    assert out == "1:Some\n"


def test_formatter_pass_print_with_cb_dict():
    def fmt(val):
        return f"Hello, I am {val['name']}. I am {val['age']} years old."

    # setup the environment
    old_stdout = sys.stdout
    sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

    formatter({"name": "Some One", "age": 43}, fmt)

    # get output
    sys.stdout.seek(0)  # jump to the start
    out = sys.stdout.read()  # read output

    # restore stdout
    sys.stdout.close()
    sys.stdout = old_stdout

    # assert
    assert out == "Hello, I am Some One. I am 43 years old.\n"
