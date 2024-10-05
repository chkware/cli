# type: ignore
"""
Tests for symbol table
"""
import json

from chk.console.main import combine_initial_variables
from chk.infrastructure.file_loader import ExecuteContext, FileContext
from chk.infrastructure.symbol_table import (
    ExposeManager,
    VariableConfigNode,
    VariableTableManager,
    Variables,
    replace_value,
)
from chk.modules.fetch import HttpDocument


class TestVariableTableManager:
    @staticmethod
    def test_handle_pass():
        document = {
            "version": "default:http:0.7.2",
            "request": {
                "url": "https://httpbin<% extension %>/<% method | lower %>",
                "method": "<% method %>",
            },
            VariableConfigNode.VARIABLES: {
                "method": "GET",
            },
        }

        file_ctx = FileContext(filepath_hash="ab12", document=document)
        exc = ExecuteContext(
            arguments={
                VariableConfigNode.VARIABLES: combine_initial_variables(
                    json.dumps({"extension": ".org"})
                )
            }
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
                "var_3": "ajax<%var_1%>",
                "var_4": "ajax <% Var_1 %>",
                "var_5": "  <% var_2 %>",
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
                "var_3": "ajax_<%var_1%>",
                "var_5": "  <% var_2 %>",
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

        assert len(variable_doc.data) == 4
        assert variable_doc.data == {
            "var_1": "bar",
            "var_2": 2,
            "var_3": "ajax_bar",
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
                "var_3": "ajax_<%var_1%>",
                "var_5": "  <% var_2 %>",
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

        assert len(variable_doc.data) == 5
        assert variable_doc.data == {
            "var_1": "bar",
            "var_2": 2,
            "var_3": "ajax_bar",
            "var_5": "  2",
            "Var_1": "_ccc",
        }


class TestReplaceValue:
    @staticmethod
    def test_replace_value_pass():
        document = {
            "version": "default:http:0.7.2",
            "request": {
                "url": "https://httpbin.org/get",
                "method": "GET",
                "auth .scm=bearer": {"token": "<% token %>"},
            },
        }

        variables = {
            "method": "GET",
            "token": "asdf123",
        }

        assert replace_value(document["request"], variables) == {
            "url": "https://httpbin.org/get",
            "method": "GET",
            "auth .scm=bearer": {"token": "asdf123"},
        }


class TestReplaceValueInTraversable:
    @staticmethod
    def test_replace_value_dict_pass():
        vals = {
            "va": 1,
            "vb": {"x": "y"},
            "vc": {"p": "1", "q": {"x": "y"}},
            "vd": ["a", "b"],
        }

        var1 = {
            "a": "a <% va %>",
            "b": "a <% vd %>",
            "c": "<% vc %>",
            "d": "a <% vc.q.x %>",
        }

        assert replace_value(var1, vals) == {
            "a": "a 1",
            "b": "a ['a', 'b']",
            "c": {"p": "1", "q": {"x": "y"}},
            "d": "a y",
        }

    @staticmethod
    def test_replace_value_list_pass():
        vals = {
            "va": 1,
            "vb": {"x": "y"},
            "vc": {"p": "1", "q": {"x": "y"}},
            "vd": ["a", "b"],
        }

        var2 = [
            "a <% va %>",
            "a <% vd %>",
            "<% vc %>",
            "a <% vc.q.x %>",
        ]

        assert replace_value(var2, vals) == [
            "a 1",
            "a ['a', 'b']",
            {"p": "1", "q": {"x": "y"}},
            "a y",
        ]


class TestExposeManager:
    @staticmethod
    def test_get_expose_doc_always_pass():
        document = {
            "version": "default:http:0.7.2",
            "request": {
                "url": "https://httpbin.org/get",
                "method": "GET",
                "auth .scm=bearer": {"token": "1234"},
            },
        }

        expose_block = {
            "expose": ["<% _response %>", "<% _response.code %>"],
        }

        expose_doc = ExposeManager.get_expose_doc(document | expose_block)

        assert isinstance(expose_doc, list)
        assert len(expose_doc) == 2

        expose_doc = ExposeManager.get_expose_doc(document)

        assert isinstance(expose_doc, list)
        assert len(expose_doc) == 0

    @staticmethod
    def test_replace_values_pass():
        expose_block = ["<% _response %>", "<% _response.code %>"]
        response = {
            "A": "https://httpbin.org/get",
            "_response": {"code": 201},
        }

        replaced = ExposeManager.replace_values(expose_block, response)

        assert len(replaced) == 2
        assert replaced[1] == 201

    @staticmethod
    def test_get_exposed_replaced_data_pass_returns_empty_list():
        document = {
            "version": "default:http:0.7.2",
            "request": {
                "url": "https://httpbin.org/get",
                "method": "GET",
            },
        }

        file_ctx = FileContext(filepath_hash="ab12", document=document)

        http_doc = HttpDocument.from_file_context(file_ctx)

        exposed_data = ExposeManager.get_exposed_replaced_data(
            http_doc, {"a": 1, "b": 2}
        )

        assert isinstance(exposed_data, dict)
        assert len(exposed_data) == 0

    @staticmethod
    def test_get_exposed_replaced_data_pass_returns_nonempty_list():
        document = {
            "version": "default:http:0.7.2",
            "request": {
                "url": "https://httpbin.org/get",
                "method": "GET",
            },
            "expose": ["<% _response %>"],
        }

        file_ctx = FileContext(filepath_hash="ab12", document=document)
        exec_ctx = ExecuteContext(
            arguments={VariableConfigNode.VARIABLES: {"extension": ".org"}}
        )

        http_doc = HttpDocument.from_file_context(file_ctx)

        variable_doc = Variables()
        VariableTableManager.handle(variable_doc, http_doc, exec_ctx)

        exposed_data = ExposeManager.get_exposed_replaced_data(
            http_doc, {**variable_doc.data, **{"_response": {"a": 1, "b": 2}}}
        )

        assert isinstance(exposed_data, dict)
        assert len(exposed_data) == 1
        assert isinstance(exposed_data["_response"], dict)
        assert len(exposed_data["_response"]) == 2
