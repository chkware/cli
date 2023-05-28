# type: ignore
"""
Tests for symbol table
"""
from chk.infrastructure.file_loader import FileContext, ExecuteContext
from chk.infrastructure.symbol_table import (
    VariableConfigNode,
    Variables,
    VariableTableManager,
    replace_value,
    ExposeManager,
)
from chk.modules.fetch import HttpDocument


class TestVariableTableManager:
    @staticmethod
    def test_handle_pass():
        document = {
            "version": "default:http:0.7.2",
            "request": {
                "url": "https://httpbin{{ extension }}/{{ method | lower }}",
                "method": "{{ method }}",
            },
            VariableConfigNode.VARIABLES: {
                "method": "GET",
            },
        }

        file_ctx = FileContext(filepath_hash="ab12", document=document)
        exc = ExecuteContext(
            arguments={VariableConfigNode.VARIABLES: {"extension": ".org"}}
        )

        http_doc = HttpDocument.from_file_context(file_ctx)

        variable_doc = Variables()
        VariableTableManager.handle(variable_doc, http_doc, exc)

        assert len(variable_doc.data) == 3
        assert VariableConfigNode.ENV in variable_doc.data
        assert "extension" in variable_doc.data

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

    @staticmethod
    def test_handle_execute_context_pass():
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

        exc = ExecuteContext(
            arguments={VariableConfigNode.VARIABLES: {"Var_1": "_ccc"}}
        )

        file_ctx = FileContext(filepath_hash="ab12", document=document)

        variable_doc = Variables()

        VariableTableManager.handle_absolute(
            variable_doc, file_ctx.document[VariableConfigNode.VARIABLES]
        )

        VariableTableManager.handle_execute_context(variable_doc, exc)

        VariableTableManager.handle_composite(
            variable_doc, file_ctx.document[VariableConfigNode.VARIABLES]
        )

        assert len(variable_doc.data) == 6
        assert variable_doc.data == {
            "var_1": "bar",
            "var_2": 2,
            "var_3": "ajax_bar",
            "var_4": "ajax_ccc",
            "var_5": "  2",
            "Var_1": "_ccc",
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


class TestExposeManager:
    @staticmethod
    def test_get_expose_doc_always_pass():
        document = {
            "version": "default:http:0.7.2",
            "request": {
                "url": "https://httpbin.org/get",
                "method": "GET",
                "auth[bearer]": {"token": "1234"},
            },
        }

        expose_block = {
            "expose": ["{{ _response }}", "{{ _response.code }}"],
        }

        expose_doc = ExposeManager.get_expose_doc(document | expose_block)

        assert isinstance(expose_doc, list)
        assert len(expose_doc) == 2

        expose_doc = ExposeManager.get_expose_doc(document)

        assert isinstance(expose_doc, list)
        assert len(expose_doc) == 0
