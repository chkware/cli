# type: ignore
"""
test templating
"""

import sys
from io import TextIOWrapper, BytesIO

import pytest

from chk.infrastructure.templating import StrTemplate


class TestStrTemplate:
    @staticmethod
    def test_create_str_templates_pass():
        tpl = StrTemplate()
        assert tpl.template == ""

        tpl = StrTemplate("Random string")
        assert tpl.template == "Random string"

    @staticmethod
    def test_create_str_templates_fails():
        with pytest.raises(ValueError):
            StrTemplate({})

    @staticmethod
    def test_substitute_fails():
        tpl = StrTemplate("Hello <% name")
        assert tpl.substitute({"name": "Nobody"}) == "Hello <% name"

        tpl = StrTemplate("Hello name %>")
        assert tpl.substitute({"name": "Nobody"}) == "Hello name %>"

    @staticmethod
    def test_substitute_fails_if_mapping_not_dict():
        tpl = StrTemplate("Hello <% name")

        with pytest.raises(ValueError):
            assert tpl.substitute("name")

    @staticmethod
    def test_substitute_pass_with_scaler():
        tpl = StrTemplate("Hello <% name %>")
        assert tpl.substitute({"name": "Nobody"}) == "Hello Nobody"

    @staticmethod
    def test_substitute_pass_with_dict():
        tpl = StrTemplate("Hello <% name.last %>, <% name.first %>")
        assert (
            tpl.substitute({"name": {"first": "John", "last": "Doe"}})
            == "Hello Doe, John"
        )


class TestGetFromStrTemplate:
    @staticmethod
    def test_get_pass_when_key_found():
        dct = {"a": {"aa": {"aaa": 1}}}
        keymap = "a.aa.aaa"

        assert StrTemplate._get(dct, keymap) == 1

    @staticmethod
    def test_get_pass_return_none_when_key_not_found():
        dct = {"a": {"aa": {"aaa": 1}}}
        keymap = "a.aa.aaaa"

        assert not StrTemplate._get(dct, keymap)

    @staticmethod
    def test_get_pass_for_non_existent_key():
        dct = {"a": {"aa": {"aaa": 1}}}
        keymap = "a.aa.aaa.aaaa"

        assert not StrTemplate._get(dct, keymap)

    @staticmethod
    def test_get_pass_for_list():
        dct = {"a": {"aa": {"aaa": [1, 2]}}}
        keymap = "a.aa.aaa.1"

        assert StrTemplate._get(dct, keymap) == 2

    @staticmethod
    def test_get_pass_for_list_stating_index():
        dct = [{"aa": {"aaa": [1, 2]}}, 2]
        keymap = "0.aa.aaa.1"

        assert StrTemplate._get(dct, keymap) == 2


class TestReplaceFromStrTemplate:
    vals = {
        "va": 1,
        "vb": {"x": "y"},
        "vc": {"p": "1", "q": {"x": "y"}},
        "vd": ["a", "b"],
    }

    @classmethod
    def test_replace_ret_same_when_nothing_to_replace(cls):
        v1 = "a"  # "a"
        assert StrTemplate._replace(v1, cls.vals) == "a"

    @classmethod
    def test_replace_pass_when_scalar(cls):
        v2 = "a <% va %>"  # "a 1"
        assert StrTemplate._replace(v2, cls.vals) == "a 1"

    @classmethod
    def test_replace_pass_when_dict_with_str(cls):
        v3 = "a <% vb %>"  # "a {'x': 'y'}"
        assert StrTemplate._replace(v3, cls.vals) == "a {'x': 'y'}"

    @classmethod
    def test_replace_pass_when_list_with_str(cls):
        v4 = "a <% vd %>"  # "a ['a', 'b']"
        assert StrTemplate._replace(v4, cls.vals) == "a ['a', 'b']"

    @classmethod
    def test_replace_pass_when_dict_scalar_value_with_str(cls):
        v5 = "a <% vc.p %>"  # "a 1"
        assert StrTemplate._replace(v5, cls.vals) == "a 1"

    @classmethod
    def test_replace_pass_when_dict_deep_scalar_value_with_str(cls):
        v6 = "a <% vc.q.x %>"  # "a y"
        assert StrTemplate._replace(v6, cls.vals) == "a y"

    @classmethod
    def test_replace_pass_when_dict_deep_scalar_value(cls):
        v7 = "<% vc.q.x %>"  # y
        assert StrTemplate._replace(v7, cls.vals) == "y"

    @classmethod
    def test_replace_pass_when_dict(cls):
        v8 = "<% vc %>"  # {'p': '1', 'q': {'x': 'y'}}
        assert StrTemplate._replace(v8, cls.vals) == {"p": "1", "q": {"x": "y"}}

    @classmethod
    def test_replace_pass_when_list(cls):
        v9 = "<% vd %>"
        assert StrTemplate._replace(v9, cls.vals) == ["a", "b"]


class TestIsTplFromStrTemplate:
    @staticmethod
    def test_is_tpl_pass():
        assert StrTemplate.is_tpl("<% some %>")

    @staticmethod
    def test_is_tpl_fail():
        assert not StrTemplate.is_tpl("some time")

    @staticmethod
    def test_is_tpl_fail_with_only_start_delimiter():
        assert not StrTemplate.is_tpl("some <% time")

    @staticmethod
    def test_is_tpl_fail_with_only_end_delimiter():
        assert not StrTemplate.is_tpl("some time %>")


class TestParseFromStrTemplate:
    @classmethod
    def test_return_empty_list_when_container_not_str(cls):
        assert StrTemplate._parse(11) == []
        assert StrTemplate._parse((11,)) == []
        assert StrTemplate._parse({"a": 11}) == []
        assert StrTemplate._parse([11]) == []

    @classmethod
    def test_return_list_with_container_when_not_parsable(cls):
        v2 = "a"
        assert StrTemplate._parse(v2) == ["a"]

    @classmethod
    def test_return_list_with_parsable(cls):
        assert StrTemplate._parse("a <% vb %>") == ["a ", "<% vb %>"]
