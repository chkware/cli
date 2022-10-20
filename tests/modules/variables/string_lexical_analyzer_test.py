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
