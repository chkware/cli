# type: ignore
"""
Test assertion_services
"""
import copy
import datetime
import types
import uuid

import pytest

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
                    "actual": "<% _data.roll %>",
                    "expected": 39,
                },
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


@pytest.fixture
def setup_assertion_entry_list_many_items_pass_assert():
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
                    "actual": "<% _data.year %>",
                    "expected": "<% _data.year %>",
                },
                {
                    "type": "Equal",
                    "actual": "<% _data.year %>",
                    "cast_actual_to": "int",
                    "expected": 2023,
                },
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
    def test__replace_assertion_values_pass_with_expected_replaced(
        setup_assertion_entry_list_many_items_pass_assert,
    ):
        assert_list, variables = setup_assertion_entry_list_many_items_pass_assert
        assert_item = AssertionEntryListRunner._replace_assertion_values(
            assert_list[1], variables.data
        )

        assert assert_item.actual == assert_item.expected

    @staticmethod
    def test__replace_assertion_values_pass_with_casting(
        setup_assertion_entry_list_many_items_pass_assert,
    ):
        assert_list, variables = setup_assertion_entry_list_many_items_pass_assert
        assert_item = AssertionEntryListRunner._replace_assertion_values(
            assert_list[2], variables.data
        )

        assert assert_item.actual == assert_item.expected
        assert isinstance(assert_item.actual, int)

    @staticmethod
    def test__call_assertion_method_pass(setup_assertion_entry_list_pass_assert):
        assert_list, _ = setup_assertion_entry_list_pass_assert
        assert_resp = AssertionEntryListRunner._call_assertion_method(assert_list[0])

        assert isinstance(assert_resp, bool)

    @staticmethod
    def test__prepare_test_run_result(setup_assertion_entry_list_pass_assert):
        assert_list, _ = setup_assertion_entry_list_pass_assert
        assert_resp = AssertionEntryListRunner._call_assertion_method(assert_list[0])
        assert_item = assert_list[0]

        resp = AssertionEntryListRunner._prepare_test_run_result(
            assert_item, assert_resp
        )

        assert resp.assert_entry == assert_item
        assert not resp.is_pass
        assert resp.message


@pytest.fixture
def setup_new_single_test_run_result():
    s = SingleTestRunResult()

    s["is_pass"] = True
    s["message"] = "Ok"
    s["assert_used"] = AssertionEntry(
        assert_type="Empty",
        actual="39",
        actual_given="<% _data.roll %>",
        expected=39,
    )

    return s


class TestSingleTestRunResult:
    @staticmethod
    def test_create(setup_new_single_test_run_result):
        s = SingleTestRunResult()
        assert len(s) == 0

        s = setup_new_single_test_run_result
        assert len(s) == 3

    @staticmethod
    def test_as_dict(setup_new_single_test_run_result):
        s = setup_new_single_test_run_result
        assert isinstance(s.as_dict, dict)

    @staticmethod
    def test_as_fmt_str(setup_new_single_test_run_result):
        s = setup_new_single_test_run_result

        assert isinstance(s.as_fmt_str, str)
        assert s.as_fmt_str == "\n+ Empty PASSED, Ok"


@pytest.fixture
def setup_new_all_test_run_result(setup_new_single_test_run_result):
    s = AllTestRunResult()

    s["id"] = uuid.uuid4()
    s["time_start"] = datetime.datetime.now()
    s["time_end"] = datetime.datetime.now()
    s["count_all"] = 1
    s["results"] = [setup_new_single_test_run_result]
    s["count_fail"] = 0

    return s


class TestAllTestRunResult:
    @staticmethod
    def test_create(setup_new_all_test_run_result):
        s = AllTestRunResult()
        assert len(s) == 0

        s = setup_new_all_test_run_result
        assert len(s) == 6

    @staticmethod
    def test_as_dict(setup_new_all_test_run_result):
        s = setup_new_all_test_run_result
        assert isinstance(s.as_dict, dict)

    @staticmethod
    def test_as_fmt_str(setup_new_all_test_run_result):
        s = setup_new_all_test_run_result

        assert isinstance(s.as_fmt_str, str)


class TestAssertionEntry:
    @staticmethod
    def test_create():
        ae = AssertionEntry(
            "Empty",
            "10",
            10,
        )

        assert isinstance(ae, AssertionEntry)
        assert isinstance(ae.actual_b4_cast, types.NotImplementedType)
        assert isinstance(ae.actual_given, types.NotImplementedType)

    @staticmethod
    def test_copy():
        ae = AssertionEntry(
            "Empty", "10", 10, cast_actual_to="int", extra_fields={"a": 1}
        )

        ar = copy.copy(ae)
        assert ar.assert_type == ae.assert_type
        assert ar is not ae
        assert "a" in ar.extra_fields
