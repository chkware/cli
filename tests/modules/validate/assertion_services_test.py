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
def setup_assertion_entry_list_pass_assert():
    ctx = FileContext(
        document={
            "version": "default:validation:0.7.2",
            "asserts": [
                {
                    "type": "Equal",
                    "actual": "{{ _data.roll }}",
                    "expected": 39,
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

    doc = ValidationDocument.from_file_context(ctx)

    exec_ctx = ExecuteContext(
        options={
            "dump": True,
            "format": False,
        },
        arguments={},
    )

    variables = Variables()
    VariableTableManager.handle(variables, doc, exec_ctx)
    ValidationDocumentSupport.set_data_template(doc, variables, exec_ctx)
    ValidationDocumentSupport.process_data_template(variables)

    assert_list = ValidationDocumentSupport.make_assertion_entry_list(doc.asserts)

    return assert_list, variables


class TestAssertionEntryListRunner:
    @staticmethod
    def test_test_run_pass(setup_assertion_entry_list_pass_assert):
        assert_list, variables = setup_assertion_entry_list_pass_assert
        test_run_result = AssertionEntryListRunner.test_run(assert_list, variables.data)

        assert isinstance(test_run_result, AllTestRunResult)

    @staticmethod
    def test__replace_assertion_values_pass(setup_assertion_entry_list_pass_assert):
        assert_list, variables = setup_assertion_entry_list_pass_assert
        assert_item = AssertionEntryListRunner._replace_assertion_values(
            assert_list[0], variables.data
        )

        assert assert_item.actual == assert_item.expected
