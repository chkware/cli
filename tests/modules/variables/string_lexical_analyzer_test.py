# type: ignore
"""
Test StringLexicalAnalyzer
"""

from chk.modules.variables.lexicon import StringLexicalAnalyzer


class TestStringLexicalAnalyzerReplace:
    @staticmethod
    def test_replace_pass_when_value_passed():
        replace_with = {"var1": 1, "var_3": "my name"}

        container = "Hasan"
        assert "Hasan" == StringLexicalAnalyzer.replace(container, replace_with)

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
