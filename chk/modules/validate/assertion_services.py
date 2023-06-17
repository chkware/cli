"""
Assertion services
"""
import typing
from collections import UserDict

import datetime


class SingleTestRunResult(UserDict):
    """Result of an assertion run"""

    is_pass: bool
    time_start: datetime.datetime
    time_end: datetime.datetime
    message: str


class AllTestRunResult(UserDict):
    """Result of a test run"""

    id: str
    time_start: datetime.datetime
    time_end: datetime.datetime
    count_all: int
    results: list[SingleTestRunResult]
    count_fail: int = 0

    @property
    def is_all_pass(self) -> bool:
        """Have all assertion passed for this test run"""

        return self.count_fail == 0


class AssertionEntry(typing.NamedTuple):
    """AssertionEntry holds one assertion operation"""

    assert_type: str
    type_of_actual: object
    actual: typing.Any
    type_of_expected: object
    expected: typing.Any
    msg_pass: str
    msg_fail: str
    assert_id: str = ""


class AssertionAntiquary:
    """AssertionAntiquary is service class that run assertion"""

    @staticmethod
    def test_run() -> None:
        """test_run"""


# @TODO:
# - add more use-case oriented named such as laravel validation
# - adjust existing asserts name; aligned name with new validator func
