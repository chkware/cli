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
        assert StringLexicalAnalyzer.replace(container, replace_with) == "Hasan"

        container = "Hasan "
        assert StringLexicalAnalyzer.replace(container, replace_with) == "Hasan "

    @staticmethod
    def test_replace_pass_when_single_variable():
        replace_with = {"var1": 1, "var_3": "my name"}

        container = "$var1"
        assert StringLexicalAnalyzer.replace(container, replace_with) == "$var1"

        container = "a $var1 b"
        assert StringLexicalAnalyzer.replace(container, replace_with) == "a $var1 b"

        container = "{$var1}"
        assert StringLexicalAnalyzer.replace(container, replace_with) == 1

        replace_with = {"var1": [1, 2], "var_3": "my name"}

        container = "{$var1}"
        assert [1, 2] == StringLexicalAnalyzer.replace(container, replace_with)

        container = "a {$var1} b"
        assert StringLexicalAnalyzer.replace(container, replace_with) == "a [1, 2] b"

        container = "{$var1} Here"
        assert StringLexicalAnalyzer.replace(container, replace_with) == "[1, 2] Here"

        container = "{ $var1    }"
        assert StringLexicalAnalyzer.replace(container, replace_with) == "{ $var1    }"

        container = "{$var2}"
        assert StringLexicalAnalyzer.replace(container, replace_with) == "{$var2}"

    @staticmethod
    def test_replace_pass_when_multiple_variable():
        container = "$var1:$var_3"
        replace_with = {"var1": 2, "var_3": "my_name"}
        assert StringLexicalAnalyzer.replace(container, replace_with) == "$var1:$var_3"

        container = "{$var1}:$var_3"
        replace_with = {"var1": 2, "var_3": "my_name"}
        assert StringLexicalAnalyzer.replace(container, replace_with) == "2:$var_3"

        container = "{$var1}:{$var_3}"
        replace_with = {"var1": 2, "var_3": "my_name"}
        assert StringLexicalAnalyzer.replace(container, replace_with) == "2:my_name"

        replace_with = {"var1": [1, 2], "var_3": "my_name"}
        assert (
            StringLexicalAnalyzer.replace(container, replace_with) == "[1, 2]:my_name"
        )

        container = "$var1:{$var_3}:$var4"
        replace_with = {"var1": [1, 2], "var_3": "my_name", "var4": {"a": 1}}
        assert (
            StringLexicalAnalyzer.replace(container, replace_with)
            == "$var1:my_name:$var4"
        )

        container = "{$var1}:{$var_3}:{$var4}"
        assert (
            StringLexicalAnalyzer.replace(container, replace_with)
            == "[1, 2]:my_name:{'a': 1}"
        )

    @staticmethod
    def test_replace_pass_when_multiple_variable_with_curly_braces():
        replace_with = {"var1": 2, "var_3": "my_name"}

        container = "$var1:{$var_3}"
        assert StringLexicalAnalyzer.replace(container, replace_with) == "$var1:my_name"

        container = "{$var1}:{$var_3}"
        assert StringLexicalAnalyzer.replace(container, replace_with) == "2:my_name"

        container = "{$var1}:{{$var_3}}"
        assert StringLexicalAnalyzer.replace(container, replace_with) == "2:{my_name}"

    @staticmethod
    def test_replace_pass_when_coll():
        st = {"var1": 2, "var_3": {"v3": {"v33": 1}}}

        container = "{$var1}:{$var_3.v3.v33}"
        assert StringLexicalAnalyzer.replace(container, st) == "2:1"

        container = "{$var1}:$var_2.v3.v33"
        assert StringLexicalAnalyzer.replace(container, st) == "2:$var_2.v3.v33"
