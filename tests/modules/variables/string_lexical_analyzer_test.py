# type: ignore
"""
Test StringLexicalAnalyzer
"""

import pytest

from chk.modules.variables.lexicon import StringLexicalAnalyzer


def test_replace_in_str_success():
    container = "https://httpbin.org/put?foo={ $var_1 }&bar={$var_2}"
    replace_with = {"var_1": 1, "var_2": "my name"}

    assert (
        "https://httpbin.org/put?foo=1&bar=my name"
        == StringLexicalAnalyzer.replace_in_str(container, replace_with)
    )


def test_replace_in_str_empty_container_success():
    container = ""
    replace_with = {"var_1": 1, "var_2": "my name"}

    assert "" == StringLexicalAnalyzer.replace_in_str(container, replace_with)


def test_replace_in_str_integer_container_fail():
    with pytest.raises(TypeError):
        assert "" == StringLexicalAnalyzer.replace_in_str(12, {})


def test_replace_in_str_empty_replace_with_fail():
    container = "https://httpbin.org/put?foo={ $var_1 }&bar={$var_2}"
    replace_with = {}

    assert container == StringLexicalAnalyzer.replace_in_str(container, replace_with)


def test_replace_in_str_alter_replace_with_fail():
    container = "https://httpbin.org/put?foo={ $var_1 }&bar={$var_2}"
    replace_with = {"var_1": 1, "var_3": "my name"}

    assert (
        "https://httpbin.org/put?foo=1&bar={$var_2}"
        == StringLexicalAnalyzer.replace_in_str(container, replace_with)
    )


def test_replace_in_str_when_combined_pass():
    container = "$var1:|$var_3"
    replace_with = {"var1": 1, "var_3": "my name"}
    # print(StringLexicalAnalyzer.replace_in_str(container, replace_with))

    assert "1:|my name" == StringLexicalAnalyzer.replace_in_str(container, replace_with)


class TestStringLexicalAnalyzerReplace:
    @staticmethod
    def test_replace_pass_when_single_variable():
        replace_with = {"var1": 1, "var_3": "my name"}

        container = "$var1"
        assert 1 == StringLexicalAnalyzer.replace(container, replace_with)

        container = "$var2"
        assert "{ $var2 }" == StringLexicalAnalyzer.replace(container, replace_with)

        replace_with = {"var1": [1, 2], "var_3": "my name"}

        container = "{$var1}"
        assert [1, 2] == StringLexicalAnalyzer.replace(container, replace_with)

        container = "{ $var1    }"
        assert [1, 2] == StringLexicalAnalyzer.replace(container, replace_with)

        container = "{$var2}"
        assert "{ $var2 }" == StringLexicalAnalyzer.replace(container, replace_with)

    @staticmethod
    def test_replace_pass_when_multiple_variable():
        container = "$var1:$var_3"

        replace_with = {"var1": 2, "var_3": "my_name"}
        assert "2:my_name" == StringLexicalAnalyzer.replace(container, replace_with)

        replace_with = {"var1": [1, 2], "var_3": "my_name"}
        assert "[1, 2]:my_name" == StringLexicalAnalyzer.replace(
            container, replace_with
        )

        container = "$var1:$var_3:$var4"
        replace_with = {"var1": [1, 2], "var_3": "my_name", "var4": {"a": 1}}
        assert "[1, 2]:my_name:{'a': 1}" == StringLexicalAnalyzer.replace(
            container, replace_with
        )

    @staticmethod
    def test_replace_pass_when_multiple_variable_with_curly_braces():
        replace_with = {"var1": 2, "var_3": "my_name"}

        container = "$var1:{$var_3}"
        assert "2:my_name" == StringLexicalAnalyzer.replace(container, replace_with)

        container = "{$var1}:{$var_3}"
        assert "2:my_name" == StringLexicalAnalyzer.replace(container, replace_with)

        container = "{$var1}:{{$var_3}}"
        assert "2:{my_name}" == StringLexicalAnalyzer.replace(container, replace_with)

    @staticmethod
    def test_replace_pass_when_coll():
        st = {"var1": 2, "var_3": {"v3": {"v33": 1}}}

        container = "$var1:{$var_3.v3.v33}"
        assert "2:1" == StringLexicalAnalyzer.replace(container, st)

        container = "$var1:$var_2.v3.v33"
        assert "2:{$var_2.v3.v33}" == StringLexicalAnalyzer.replace(container, st)
