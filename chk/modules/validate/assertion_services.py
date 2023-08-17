"""
Assertion services
"""

import typing
import uuid
from collections import UserDict
from collections.abc import Callable
from datetime import datetime

import chk.modules.validate.assertion_function as asrt_f
from chk.modules.validate.assertion_message import (
    get_fail_assert_msg_for,
    get_pass_assert_msg_for,
)
from chk.infrastructure.symbol_table import linear_replace

MAP_TYPE_TO_FN: dict[str, Callable] = {
    "Accepted": asrt_f.accepted,
    "Declined": asrt_f.declined,
    "Equal": asrt_f.equal,
    "NotEqual": asrt_f.not_equal,
    "Empty": asrt_f.empty,
    "NotEmpty": asrt_f.not_empty,
}


class AssertionEntry(typing.NamedTuple):
    """AssertionEntry holds one assertion operation"""

    assert_type: str
    cast_actual_to: str
    actual: typing.Any
    actual_given: typing.Any
    expected: typing.Any
    msg_pass: str
    msg_fail: str

    def __copy__(self) -> "AssertionEntry":
        """Copy protocol

        Returns:
            AssertionEntry
        """

        members = self._asdict()
        return AssertionEntry(**members)


class SingleTestRunResult(UserDict):
    """Result of an assertion run

    keys: is_pass, message, assert_used
    """

    @property
    def as_dict(self) -> dict:
        """Convert SingleTestRunResult to a dict"""

        return {
            key: value._asdict() if key == "assert_used" else value
            for key, value in self.items()
        }

    @property
    def as_fmt_str(self) -> str:
        """String representation of ApiResponse

        Returns:
            str: String representation
        """

        return (
            "\n"
            f"{'+' if self['is_pass'] else '-'} {self['assert_used'].assert_type} "
            + f"{'PASSED' if self['is_pass'] else 'FAILED'} with message: {self['message']}"
        )


class AllTestRunResult(UserDict):
    """Result of a test run

    keys: id, time_start, time_end, count_all, results, count_fail
    """

    @property
    def as_dict(self) -> dict:
        """Convert AllTestRunResult to a dict"""
        _as_dict: dict = {
            key: value for key, value in self.items() if not key.startswith("time_")
        }

        _as_dict |= {
            key: value.timestamp()
            for key, value in self.items()
            if key.startswith("time_")
        }

        if len(self["results"]) > 0:
            _as_dict["results"] = [
                test_result.as_dict
                for test_result in self["results"]
                if isinstance(test_result, SingleTestRunResult)
            ]

        return _as_dict

    @property
    def as_fmt_str(self) -> str:
        """String representation of ApiResponse

        Returns:
            str: String representation
        """

        _display = (
            f"Test run id: {self['id']}, time taken {self['time_end'] - self['time_start']}\n"
            + f"Total tests: {self['count_all']}, "
            + f"Total tests failed: {self['count_fail']}\n"
        )
        _display += "\n> Test run result(s):"

        for one_result in self["results"]:
            _display += one_result.as_fmt_str

        return _display


class AssertionEntryListRunner:
    """AssertionAntiquary is service class that run assertion"""

    @staticmethod
    def _replace_assertion_values(
        assert_item: AssertionEntry, variable_d: dict
    ) -> AssertionEntry:
        """Replace value for actual and expected data

        Args:
            assert_item: AssertionEntry
            variable_d: dict
        Returns:
            AssertionEntry
        """

        if (
            isinstance(assert_item.actual, str)
            and "{{" in assert_item.actual
            and "}}" in assert_item.actual
        ):
            return assert_item._replace(
                actual=linear_replace(assert_item.actual_given, variable_d),
                expected=linear_replace(assert_item.expected, variable_d),
            )

        return assert_item

    @staticmethod
    def _prepare_test_run_result(
        resp: SingleTestRunResult,
        assert_item: AssertionEntry,
        asrt_resp: ValueError | bool,
    ) -> None:
        asrt_fn_name = MAP_TYPE_TO_FN[assert_item.assert_type].__name__
        actual = assert_item._asdict().get("actual")
        expected = assert_item._asdict().get("expected")

        if isinstance(asrt_resp, ValueError):
            resp["is_pass"] = False
            asrt_fn_name = str(asrt_resp)
            resp["message"] = get_fail_assert_msg_for(asrt_fn_name).format(
                actual.__class__.__name__,
                actual,
                expected.__class__.__name__,
                expected,
            )
        else:
            resp["is_pass"] = asrt_resp

            message = (
                get_pass_assert_msg_for(asrt_fn_name)
                if asrt_resp
                else get_fail_assert_msg_for(asrt_fn_name)
            )
            resp["message"] = message.format(
                actual.__class__.__name__,
                actual,
                expected.__class__.__name__,
                expected,
            )

    @staticmethod
    def _call_assertion_method(
        assert_item: AssertionEntry,
    ) -> ValueError | bool:
        """Call assertion method

        Args:
            assert_item: AssertionEntry
        Returns:
            ValueError | bool
        """

        asrt_fn = MAP_TYPE_TO_FN[assert_item.assert_type]
        return asrt_fn(**assert_item._asdict())

    @staticmethod
    def test_run(
        assert_list: list[AssertionEntry], variables: dict
    ) -> AllTestRunResult:
        """Run the tests

        Args:
            assert_list: list[AssertionEntry]
            variables: dict

        Returns:
            AllTestRunResult: Test run result
        """

        test_run_result = AllTestRunResult(
            id=str(uuid.uuid4()),
            time_start=datetime.now(),
            count_all=len(assert_list),
            count_fail=0,
        )

        results: list[SingleTestRunResult] = []

        for assert_item in assert_list:
            assert_item = AssertionEntryListRunner._replace_assertion_values(
                assert_item, variables
            )

            resp = SingleTestRunResult(assert_used=assert_item)
            asrt_resp = AssertionEntryListRunner._call_assertion_method(assert_item)

            AssertionEntryListRunner._prepare_test_run_result(
                resp, assert_item, asrt_resp
            )

            if resp["is_pass"] is False:
                test_run_result["count_fail"] += 1

            results.append(resp)

        test_run_result["time_end"] = datetime.now()
        test_run_result["results"] = results

        return test_run_result
