# type: ignore
"""
Test assertion_services
"""
import pytest

from chk.infrastructure.file_loader import FileContext, ExecuteContext
from chk.infrastructure.symbol_table import Variables, VariableTableManager
from chk.modules.validate import ValidationDocument, ValidationDocumentSupport
from chk.modules.validate.assertion_services import (
    AssertionEntryListRunner,
    AllTestRunResult,
)


@pytest.fixture
def setup_validation_document_both_pass_assert():
    ctx = FileContext(
        document={
            "version": "default:validation:0.7.2",
            "asserts": [
                {
                    "type": "Equal",
                    "actual": "{{ _data.roll }}",
                    "expected": 39,
                },
                {
                    "type": "Equal",
                    "actual": "{{ _data.year }}",
                    "expected": 2023,
                },
            ],
            "data": {
                "name": "Sadaqat",
                "roll": 39,
                "class": "Nursery",
                "year": 2023,
            },
            "expose": ["$_asserts_response"],
        }
    )

    return ValidationDocument.from_file_context(ctx)


@pytest.fixture
def setup_validation_document_one_fail_assert():
    ctx = FileContext(
        document={
            "version": "default:validation:0.7.2",
            "asserts": [
                {
                    "type": "Equal",
                    "actual": "{{ _data.roll }}",
                    "expected": 39,
                },
                {
                    "type": "Equal",
                    "actual": "{{ _data.year }}",
                    "expected": 2023,
                },
            ],
            "data": {
                "name": "Sadaqat",
                "roll": 39,
                "class": "Nursery",
                "year": 2023,
            },
            "expose": ["$_asserts_response"],
        }
    )

    return ValidationDocument.from_file_context(ctx)


@pytest.fixture
def setup_empty_execution_ctx():
    return ExecuteContext(
        options={
            "dump": True,
            "format": False,
        },
        arguments={},
    )


class TestAssertionEntryListRunner:
    @staticmethod
    def test_test_run_pass(
        setup_validation_document_both_pass_assert, setup_empty_execution_ctx
    ):
        exec_ctx = setup_empty_execution_ctx
        doc = setup_validation_document_both_pass_assert

        variables = Variables()
        VariableTableManager.handle(variables, doc, exec_ctx)
        ValidationDocumentSupport.set_data_template(doc, variables, exec_ctx)
        ValidationDocumentSupport.process_data_template(variables)

        assert_list = ValidationDocumentSupport.make_assertion_entry_list(doc.asserts)

        test_run_result = AssertionEntryListRunner.test_run(assert_list, variables.data)

        assert isinstance(test_run_result, AllTestRunResult)
