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


class AssertionEntryListRunner:
    """AssertionAntiquary is service class that run assertion"""

    @staticmethod
    def test_run(
        assert_list: list[AssertionEntry], variable_doc: dict
    ) -> AllTestRunResult:
        """Run the tests

        Args:
            assert_list: list[AssertionEntry]
            variable_doc: dict

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
            is_pass, asrt_resp = asrt_fn(**assert_item._asdict())

            if isinstance(asrt_resp, Exception):
                test_run_result["count_fail"] += 1

            resp["is_pass"] = is_pass
            resp["message"] = str(asrt_resp)
            resp["time_end"] = datetime.now()

            results.append(resp)

        test_run_result["time_end"] = datetime.now()
        test_run_result["results"] = results

        return test_run_result


# @TODO:
# - add more use-case oriented named such as laravel validation
# - adjust existing asserts name; aligned name with new validator func
