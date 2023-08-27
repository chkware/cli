"""
Assertion services
"""

import dataclasses
import typing
import uuid
from collections import UserDict
from collections.abc import Callable
from datetime import datetime

import chk.modules.validate.assertion_function as asrt_f
from chk.infrastructure.helper import Cast
from chk.modules.validate.assertion_message import get_assert_msg_for
from chk.infrastructure.symbol_table import linear_replace
from chk.modules.validate.assertion_validation import AssertionEntityType

MAP_TYPE_TO_FN: dict[str, Callable] = {
    AssertionEntityType.Accepted: asrt_f.accepted,
    AssertionEntityType.Declined: asrt_f.declined,
    AssertionEntityType.Equal: asrt_f.equal,
    AssertionEntityType.NotEqual: asrt_f.not_equal,
    AssertionEntityType.Empty: asrt_f.empty,
    AssertionEntityType.NotEmpty: asrt_f.not_empty,
    AssertionEntityType.Boolean: asrt_f.boolean,
    AssertionEntityType.Integer: asrt_f.integer,
    AssertionEntityType.IntegerBetween: asrt_f.integer_between,
    AssertionEntityType.IntegerGreater: asrt_f.integer_greater,
    AssertionEntityType.IntegerGreaterOrEqual: asrt_f.integer_greater_or_equal,
    AssertionEntityType.IntegerLess: asrt_f.integer_less,
    AssertionEntityType.IntegerLessOrEqual: asrt_f.integer_less_or_equal,
    AssertionEntityType.Float: asrt_f.float_,
    AssertionEntityType.FloatBetween: asrt_f.float_between,
    AssertionEntityType.FloatGreater: asrt_f.float_greater,
    AssertionEntityType.FloatGreaterOrEqual: asrt_f.float_greater_or_equal,
    AssertionEntityType.FloatLess: asrt_f.float_less,
    AssertionEntityType.FloatLessOrEqual: asrt_f.float_less_or_equal,
    AssertionEntityType.Str: asrt_f.str_,
    AssertionEntityType.StrHave: asrt_f.str_have,
    AssertionEntityType.StrDoNotHave: asrt_f.str_do_not_have,
    AssertionEntityType.StrStartsWith: asrt_f.str_starts_with,
    AssertionEntityType.StrDoNotStartsWith: asrt_f.str_do_not_starts_with,
    AssertionEntityType.StrEndsWith: asrt_f.str_ends_with,
    AssertionEntityType.StrDoNotEndsWith: asrt_f.str_do_not_ends_with,
    AssertionEntityType.Date: asrt_f.date,
    AssertionEntityType.DateAfter: asrt_f.date_after,
    AssertionEntityType.DateAfterOrEqual: asrt_f.date_after_or_equal,
    AssertionEntityType.DateBefore: asrt_f.date_before,
    AssertionEntityType.DateBeforeOrEqual: asrt_f.date_before_or_equal,
    AssertionEntityType.List: asrt_f.list_,
    AssertionEntityType.ListContains: asrt_f.list_contains,
    AssertionEntityType.ListDoNotContains: asrt_f.list_do_not_contains,
    AssertionEntityType.ListHasIndex: asrt_f.list_has_index,
    AssertionEntityType.ListDoNotHasIndex: asrt_f.list_do_not_has_index,
    AssertionEntityType.Map: asrt_f.map_,
}


@dataclasses.dataclass
class AssertionEntry:
    """AssertionEntry holds one assertion operation"""

    assert_type: str
    actual: typing.Any
    expected: typing.Any
    msg_pass: str = dataclasses.field(default_factory=str)
    msg_fail: str = dataclasses.field(default_factory=str)
    cast_actual_to: str = dataclasses.field(default_factory=str)
    actual_given: typing.Any = dataclasses.field(default=NotImplemented)
    actual_b4_cast: typing.Any = dataclasses.field(default=NotImplemented)
    extra_fields: dict = dataclasses.field(default_factory=dict)

    @property
    def as_dict(self) -> dict:
        """Return dict representation"""

        return dataclasses.asdict(self)


class SingleTestRunResult(UserDict):
    """Result of an assertion run

    keys: is_pass, message, assert_used
    """

    @property
    def as_dict(self) -> dict:
        """Convert SingleTestRunResult to a dict"""

        return {
            key: value.as_dict if key == "assert_used" else value
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
            + f"{'PASSED' if self['is_pass'] else 'FAILED'}, {self['message']}"
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

        # replace actual value for template
        if (
            isinstance(assert_item.actual, str)
            and "{{" in assert_item.actual
            and "}}" in assert_item.actual
        ):
            assert_item.actual_given = assert_item.actual
            assert_item.actual = linear_replace(assert_item.actual, variable_d)

        # convert actual value type
        if assert_item.cast_actual_to != "" and isinstance(assert_item.actual, str):
            assert_item.actual_b4_cast = assert_item.actual

            if assert_item.cast_actual_to == "int_or_flot":
                assert_item.actual = Cast.to_int_or_float(assert_item.actual)
            elif assert_item.cast_actual_to == "int":
                assert_item.actual = Cast.to_int(assert_item.actual)
            elif assert_item.cast_actual_to == "float":
                assert_item.actual = Cast.to_float(assert_item.actual)
            elif assert_item.cast_actual_to == "bool":
                assert_item.actual = Cast.to_bool(assert_item.actual)
            elif assert_item.cast_actual_to == "none":
                assert_item.actual = Cast.to_none(assert_item.actual)
            elif assert_item.cast_actual_to in ["map", "list", "str"]:
                assert_item.actual = Cast.to_hashable(assert_item.actual)
            elif assert_item.cast_actual_to == "auto":
                assert_item.actual = Cast.to_auto(assert_item.actual)

        # replace expected value for template
        if (
            isinstance(assert_item.expected, str)
            and "{{" in assert_item.expected
            and "}}" in assert_item.expected
        ):
            assert_item.expected = linear_replace(assert_item.expected, variable_d)

        return assert_item

    @staticmethod
    def _prepare_test_run_result(
        resp: SingleTestRunResult,
        assert_item: AssertionEntry,
        asrt_resp: ValueError | bool,
    ) -> None:
        def _prepare_message_values() -> dict:
            return {
                "assert_type": assert_item.assert_type,
                "type_actual": assert_item.actual.__class__.__name__,
                "type_expected": assert_item.expected.__class__.__name__,
                "value_actual": assert_item.actual,
                "value_expected": assert_item.expected,
                "value_actual_given": assert_item.actual_given,
                "value_actual_b4_cast": assert_item.actual_b4_cast,
                "extra_fields": assert_item.extra_fields,
            }

        asrt_fn_name = MAP_TYPE_TO_FN[assert_item.assert_type].__name__

        if isinstance(asrt_resp, ValueError):
            resp["is_pass"] = False
            resp["message"] = get_assert_msg_for(
                f"{asrt_fn_name}.{str(asrt_resp)}"
            ).format(**_prepare_message_values())
        else:
            resp["is_pass"] = asrt_resp

            message = (
                get_assert_msg_for(f"{asrt_fn_name}.pass")
                if asrt_resp
                else get_assert_msg_for(f"{asrt_fn_name}.fail")
            )
            resp["message"] = message.format(**_prepare_message_values())

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
        return asrt_fn(**assert_item.as_dict)

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
