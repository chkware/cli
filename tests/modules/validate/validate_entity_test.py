# type: ignore
"""
Validation entity test
"""

import pytest

from chk.infrastructure.file_loader import FileContext, ExecuteContext
from chk.infrastructure.symbol_table import Variables, VariableTableManager
from chk.modules.validate import (
    ValidationDocument,
    ValidationDocumentSupport,
    ValidationConfigNode,
)
from chk.modules.validate.assertion_services import AssertionEntry


class TestValidationDocument:
    @staticmethod
    def test_from_file_context_pass_when_no_data():
        ctx = FileContext(
            document={
                "version": "default:validation:0.7.2",
                "asserts": [
                    {
                        "type": "Equal",
                        "actual": "<% _data.roll %>",
                        "expected": 39,
                    }
                ],
                "expose": ["<% _asserts_response %>"],
            }
        )

        doc = ValidationDocument.from_file_context(ctx)

        assert isinstance(doc.context, tuple)
        assert isinstance(doc.version, str)

        assert isinstance(doc.asserts, list)
        assert len(doc.asserts) == 1

        assert isinstance(doc.data, dict)
        assert not doc.data

    @staticmethod
    def test_from_file_context_pass_when_data():
        ctx = FileContext(
            document={
                "version": "default:validation:0.7.2",
                "asserts": [
                    {
                        "type": "Equal",
                        "actual": "<% _data.roll %>",
                        "expected": 39,
                    }
                ],
                "data": {
                    "name": "Sadaqat",
                    "roll": 39,
                    "class": "Nursery",
                    "year": 2023,
                },
                "expose": ["<% _asserts_response %>"],
            }
        )

        doc = ValidationDocument.from_file_context(ctx)

        assert isinstance(doc.context, tuple)
        assert isinstance(doc.version, str)

        assert isinstance(doc.asserts, list)
        assert len(doc.asserts) == 1

        assert isinstance(doc.data, dict)
        assert len(doc.data) == 4

    @staticmethod
    def test_from_file_context_fail_when_no_asserts():
        ctx = FileContext(
            document={
                "version": "default:validation:0.7.2",
                "data": {
                    "name": "Sadaqat",
                    "roll": 39,
                    "class": "Nursery",
                    "year": 2023,
                },
                "expose": ["<% _asserts_response %>"],
            }
        )

        with pytest.raises(RuntimeError):
            ValidationDocument.from_file_context(ctx)

    @staticmethod
    def test_as_dict_pass():
        ctx = FileContext(
            document={
                "version": "default:validation:0.7.2",
                "asserts": [
                    {
                        "type": "Equal",
                        "actual": "<% _data.roll %>",
                        "expected": 39,
                    }
                ],
                "data": {
                    "name": "Sadaqat",
                    "roll": 39,
                    "class": "Nursery",
                    "year": 2023,
                },
                "expose": ["<% _asserts_response %>"],
            }
        )

        doc = ValidationDocument.from_file_context(ctx)

        assert isinstance(doc.model_dump(), dict)
        assert len(doc.model_dump()) == 4


class TestValidationDocumentSupport:
    @staticmethod
    def test_build_schema_pass():
        schema = ValidationDocumentSupport.build_schema()

        assert isinstance(schema, dict)
        assert len(schema) == 5

    def test_set_data_template_pass_when_set_from_exec_ctx(self):
        ctx = FileContext(
            document={
                "version": "default:validation:0.7.2",
                "asserts": [
                    {
                        "type": "Equal",
                        "actual": "<% _data.roll %>",
                        "expected": 39,
                    }
                ],
                "expose": ["<% _asserts_response %>"],
            }
        )

        exec_ctx = ExecuteContext(
            options={
                "dump": True,
                "format": False,
            },
            arguments={"data": {"name": "Some Name"}},
        )

        doc = ValidationDocument.from_file_context(ctx)
        variables = Variables()
        ValidationDocumentSupport.set_data_template(doc, variables, exec_ctx)

        assert bool(variables[ValidationConfigNode.VAR_NODE.value])

    def test_set_data_template_pass_when_set_from_doc(self):
        ctx = FileContext(
            document={
                "version": "default:validation:0.7.2",
                "asserts": [
                    {
                        "type": "Equal",
                        "actual": "<% _data.roll %>",
                        "expected": 39,
                    }
                ],
                "data": {"name": "Some Name"},
                "expose": ["<% _asserts_response %>"],
            }
        )

        exec_ctx = ExecuteContext(
            options={
                "dump": True,
                "format": False,
            }
        )

        doc = ValidationDocument.from_file_context(ctx)
        variables = Variables()
        ValidationDocumentSupport.set_data_template(doc, variables, exec_ctx)

        assert bool(variables[ValidationConfigNode.VAR_NODE.value])

    def test_set_data_template_pass_exec_ctx_prioritise(self):
        ctx = FileContext(
            document={
                "version": "default:validation:0.7.2",
                "asserts": [
                    {
                        "type": "Equal",
                        "actual": "<% _data.roll %>",
                        "expected": 39,
                    }
                ],
                "data": {"name": "Some Name One"},
                "expose": ["<% _asserts_response %>"],
            }
        )

        exec_ctx = ExecuteContext(
            options={
                "dump": True,
                "format": False,
            },
            arguments={"data": {"name": "Some Name Two"}},
        )

        doc = ValidationDocument.from_file_context(ctx)
        variables = Variables()
        ValidationDocumentSupport.set_data_template(doc, variables, exec_ctx)

        assert bool(variables[ValidationConfigNode.VAR_NODE.value])
        assert (
            variables[ValidationConfigNode.VAR_NODE.value].get("name")
            == "Some Name Two"
        )

    @staticmethod
    def test_process_data_template_pass():
        ctx = FileContext(
            document={
                "version": "default:validation:0.7.2",
                "asserts": [
                    {
                        "type": "Equal",
                        "actual": "<% _data.roll %>",
                        "expected": 39,
                    }
                ],
                "data": {"greet": "Hello <% name %>"},
                "expose": ["<% _asserts_response %>"],
            }
        )

        exec_ctx = ExecuteContext(
            options={
                "dump": True,
                "format": False,
            },
            arguments={"variables": {"name": "Somebody"}},
        )

        doc = ValidationDocument.from_file_context(ctx)

        variables = Variables()
        VariableTableManager.handle(variables, doc, exec_ctx)

        ValidationDocumentSupport.set_data_template(doc, variables, exec_ctx)
        ValidationDocumentSupport.process_data_template(variables)

        assert bool(variables[ValidationConfigNode.VAR_NODE.value])
        assert (
            variables[ValidationConfigNode.VAR_NODE.value].get("greet")
            == "Hello Somebody"
        )

    @staticmethod
    def test_make_assertion_entry_list_pass():
        ctx = FileContext(
            document={
                "version": "default:validation:0.7.2",
                "asserts": [
                    {
                        "type": "Equal",
                        "actual": "<% _data.roll %>",
                        "expected": 39,
                    },
                    {
                        "type": "Equal",
                        "actual": "<% _data.name %>",
                        "expected": "Some one",
                    },
                ],
                "data": {"roll": 39, "name": "Some one"},
                "expose": ["<% _asserts_response %>"],
            }
        )

        doc = ValidationDocument.from_file_context(ctx)
        resp = ValidationDocumentSupport.make_assertion_entry_list(doc.asserts)

        assert all(list(isinstance(a_item, AssertionEntry) for a_item in resp))
