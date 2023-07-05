# type: ignore
"""
Test assertion_services
"""
import pytest
import var_dump

from chk.infrastructure.exception import ValidationError
from chk.infrastructure.file_loader import FileContext, ExecuteContext
from chk.infrastructure.symbol_table import Variables, VariableTableManager
from chk.modules.validate import ValidationDocument, ValidationDocumentSupport
from chk.modules.validate.assertion_services import (
    AssertionEntryListRunner,
    AllTestRunResult,
    SingleTestRunResult,
    AssertionEntry,
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

    @staticmethod
    def test__call_assertion_method_pass(setup_assertion_entry_list_pass_assert):
        assert_list, _ = setup_assertion_entry_list_pass_assert
        assert_resp = AssertionEntryListRunner._call_assertion_method(assert_list[0])

        assert isinstance(assert_resp, ValidationError)

    @staticmethod
    def test__prepare_test_run_result(setup_assertion_entry_list_pass_assert):
        assert_list, _ = setup_assertion_entry_list_pass_assert
        assert_resp = AssertionEntryListRunner._call_assertion_method(assert_list[0])
        assert_item = assert_list[0]

        resp = SingleTestRunResult(assert_used=assert_item)
        AssertionEntryListRunner._prepare_test_run_result(
            resp, assert_item, assert_resp
        )

        assert resp["assert_used"] == assert_item
        assert not resp["is_pass"]
        assert resp["message"]


class TestSingleTestRunResult:
    @staticmethod
    def test_create():
        s = SingleTestRunResult()

        assert len(s) == 0

        s["is_pass"] = True
        s["message"] = ""
        s["assert_used"] = object()

        assert len(s) == 3

    @staticmethod
    def test_as_dict():
        s = SingleTestRunResult()

        s["is_pass"] = True
        s["message"] = ""
        s["assert_used"] = AssertionEntry(
            assert_type="Empty",
            actual="39",
            actual_given="{{ _data.roll }}",
            expected=39,
            msg_pass="",
            msg_fail="",
        )

        assert isinstance(s.as_dict, dict)

    @staticmethod
    def test_as_fmt_str():
        s = SingleTestRunResult()

        s["is_pass"] = True
        s["message"] = "Ok"
        s["assert_used"] = AssertionEntry(
            assert_type="Empty",
            actual="39",
            actual_given="{{ _data.roll }}",
            expected=39,
            msg_pass="",
            msg_fail="",
        )

        assert isinstance(s.as_fmt_str, str)
        assert s.as_fmt_str == "\n+ Empty PASSED with message: Ok"
