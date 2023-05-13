# type: ignore
"""
Tests for symbol table
"""
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.symbol_table import (
    VariableConfigNode,
    Variables,
    VariableTableManager,
    replace_value,
)
from chk.modules.fetch import HttpDocument


class TestVariableTableManager:
    @staticmethod
    def test_handle_pass():
        document = {
            "version": "default:http:0.7.2",
            "request": {
                "url": "https://httpbin.org/get",
                "method": "GET",
            },
            VariableConfigNode.VARIABLES: {
                "var_1": "bar",
                "var_2": 2,
            },
        }

        file_ctx = FileContext(filepath_hash="ab12", document=document)
        http_doc = HttpDocument.from_file_context(file_ctx)

        variable_doc = Variables()
        VariableTableManager.handle(variable_doc, http_doc)

        assert len(variable_doc.data) == 3
        assert VariableConfigNode.ENV in variable_doc.data

    @staticmethod
    def test_handle_absolute_pass():
        document = {
            "version": "default:http:0.7.2",
            "request": {
                "url": "https://httpbin.org/get",
                "method": "GET",
            },
            VariableConfigNode.VARIABLES: {
                "var_1": "bar",
                "var_2": 2,
                "var_3": "ajax{{var_1}}",
                "var_4": "ajax {{ Var_1 }}",
                "var_5": "  {{ var_2 }}",
            },
        }

        file_ctx = FileContext(filepath_hash="ab12", document=document)

        variable_doc = Variables()
        VariableTableManager.handle_absolute(
            variable_doc, file_ctx.document[VariableConfigNode.VARIABLES]
        )

        assert len(variable_doc.data) == 2
        assert variable_doc.data == {"var_1": "bar", "var_2": 2}

    @staticmethod
    def test_handle_environment_pass():
        variable_doc = Variables()
        VariableTableManager.handle_environment(variable_doc)

        assert len(variable_doc.data) == 1
        assert VariableConfigNode.ENV in variable_doc.data

    @staticmethod
    def test_handle_composite_pass():
        document = {
            "version": "default:http:0.7.2",
            "request": {
                "url": "https://httpbin.org/get",
                "method": "GET",
            },
            VariableConfigNode.VARIABLES: {
                "var_1": "bar",
                "var_2": 2,
                "var_3": "ajax_{{var_1}}",
                "var_4": "ajax{{ Var_1|default('_xaja') }}",
                "var_5": "  {{ var_2 }}",
            },
        }

        file_ctx = FileContext(filepath_hash="ab12", document=document)

        variable_doc = Variables()
        VariableTableManager.handle_absolute(
            variable_doc, file_ctx.document[VariableConfigNode.VARIABLES]
        )

        VariableTableManager.handle_composite(
            variable_doc, file_ctx.document[VariableConfigNode.VARIABLES]
        )

        assert len(variable_doc.data) == 5
        assert variable_doc.data == {
            "var_1": "bar",
            "var_2": 2,
            "var_3": "ajax_bar",
            "var_4": "ajax_xaja",
            "var_5": "  2",
        }


class TestReplaceValue:
    @staticmethod
    def test_replace_value_pass():
        document = {
            "version": "default:http:0.7.2",
            "request": {
                "url": "https://httpbin.org/{{ method|lower }}",
                "method": "GET",
                "auth[bearer]": {"token": "{{ token }}"},
            },
        }

        variables = {
            "method": "GET",
            "token": "asdf123",
        }

        assert replace_value(document["request"], variables) == {
            "url": "https://httpbin.org/get",
            "method": "GET",
            "auth[bearer]": {"token": "asdf123"},
        }
