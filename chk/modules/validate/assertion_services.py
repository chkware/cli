"""
Assertion services
"""
import typing
import uuid
from collections import UserDict
from datetime import datetime

import chk.modules.validate.assertion_function as asrt_f
from chk.infrastructure.exception import ValidationError
from chk.infrastructure.symbol_table import linear_replace

MAP_TYPE_TO_FN = {
    "Equal": asrt_f.equal,
    "NotEqual": asrt_f.not_equal,
}


class AssertionEntry(typing.NamedTuple):
    """AssertionEntry holds one assertion operation"""

    assert_type: str
    type_of_actual: str
    actual: typing.Any
    actual_given: typing.Any
    type_of_expected: str
    expected: typing.Any
    msg_pass: str
    msg_fail: str
    assert_id: str = ""


class SingleTestRunResult(UserDict):
    """Result of an assertion run"""

    __slots__ = (
        "is_pass",
        "time_start",
        "time_end",
        "message",
    )

    is_pass: bool
    message: str
    assert_used: AssertionEntry

    @property
    def as_dict(self) -> dict:
        """Convert SingleTestRunResult to a dict"""

        _as_dict: dict = {
            key: value for key, value in self.items() if not key.startswith("time_")
        }

        _as_dict |= {
            key: value.timestamp()
            for key, value in self.items()
            if key.startswith("time_")
        }

        _as_dict["assert_used"] = self["assert_used"]._asdict()

        return _as_dict

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
    """Result of a test run"""

    __slots__ = (
        "id",
        "time_start",
        "time_end",
        "count_all",
        "results",
        "count_fail",
    )

    id: str
    time_start: datetime
    time_end: datetime
    count_all: int
    results: list[SingleTestRunResult]
    count_fail: int

    @property
    def is_all_pass(self) -> bool:
        """Have all assertion passed for this test run"""

        return self.count_fail == 0

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
            asrt_fn = MAP_TYPE_TO_FN[assert_item.assert_type]

            resp = SingleTestRunResult()

            if (
                isinstance(assert_item.actual, str)
                and "{{" in assert_item.actual
                and "}}" in assert_item.actual
            ):
                assert_item = assert_item._replace(
                    actual=linear_replace(assert_item.actual_given, variables)
                )

            asrt_resp = asrt_fn(**assert_item._asdict())

            if isinstance(asrt_resp, ValidationError):
                test_run_result["count_fail"] += 1
                resp["message"] = str(asrt_resp)
            else:
                resp["is_pass"] = True
                resp["message"] = str(asrt_resp)

            results.append(resp)

        test_run_result["time_end"] = datetime.now()
        test_run_result["results"] = results

        return test_run_result


# @TODO:
# - add more use-case oriented named such as laravel validation
# - adjust existing asserts name; aligned name with new validator func
