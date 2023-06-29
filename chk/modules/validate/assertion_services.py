"""
Assertion services
"""
import typing
import uuid
from collections import UserDict
from datetime import datetime

import chk.modules.validate.assertion_function as asrt_f

MAP_TYPE_TO_FN = {
    "AssertEquals": asrt_f.assert_equals,
}


class AssertionEntry(typing.NamedTuple):
    """AssertionEntry holds one assertion operation"""

    assert_type: str
    type_of_actual: str
    actual: typing.Any
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
    time_start: datetime
    time_end: datetime
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
            f"{'+' if self['is_pass'] else '-'} Test {self['assert_used'].assert_type} "
            + f"[{'Pass' if self['is_pass'] else 'Fail'}] with message: {self['message']}\n"
            + f"  Test started at: {str(self['time_start'])}, and "
            + f"finished at: {str(self['time_end'])}\n"
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
            "\n"
            f"Test run id: {self['id']}\n"
            + f"Test run started at: {str(self['time_start'])}, and "
            + f"finished at: {str(self['time_end'])}\n"
            + f"Total tests: {self['count_all']}, "
            + f"Total tests failed: {self['count_fail']}\n"
        )
        _display += f"Test run result(s):\n"

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

            resp = SingleTestRunResult(time_start=datetime.now())
            is_pass, asrt_resp = asrt_fn(
                **{**assert_item._asdict(), **{"variables": variables}}
            )

            if isinstance(asrt_resp, Exception):
                test_run_result["count_fail"] += 1

            resp["is_pass"] = is_pass
            resp["message"] = str(asrt_resp)
            resp["time_end"] = datetime.now()
            resp["assert_used"] = assert_item

            results.append(resp)

        test_run_result["time_end"] = datetime.now()
        test_run_result["results"] = results

        return test_run_result


# @TODO:
# - add more use-case oriented named such as laravel validation
# - adjust existing asserts name; aligned name with new validator func
