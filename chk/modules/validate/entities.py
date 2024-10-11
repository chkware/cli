"""
Validate module entities
"""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, UUID4


class AssertionEntry(BaseModel):
    """AssertionEntry holds one assertion operation
    TODO: implement __iter__ for this class
    """

    assert_type: str
    actual: Any
    expected: Any
    msg_pass: str = Field(default_factory=str)
    msg_fail: str = Field(default_factory=str)
    cast_actual_to: str = Field(default_factory=str)
    actual_given: Any = Field(default=NotImplemented)
    actual_b4_cast: Any = Field(default=NotImplemented)
    extra_fields: dict = Field(default_factory=dict)

    def __iter__(self):
        yield "assert_type", self.assert_type
        yield "actual", self.actual
        yield "expected", "" if self.expected == NotImplemented else self.expected
        yield "msg_pass", self.msg_pass
        yield "msg_fail", self.msg_fail
        yield "cast_actual_to", self.cast_actual_to
        yield "actual_given", (
            "" if self.actual_given == NotImplemented else self.actual_given
        )
        yield "actual_b4_cast", (
            "" if self.actual_b4_cast == NotImplemented else self.actual_b4_cast
        )
        yield "extra_fields", self.extra_fields

    @property
    def as_dict(self) -> dict:
        """Return dict representation"""

        if self.actual_given == NotImplemented:
            self.actual_given = ""
        if self.actual_b4_cast == NotImplemented:
            self.actual_b4_cast = ""
        if self.expected == NotImplemented:
            self.expected = ""

        return self.model_dump()


class TestRunDetail(BaseModel):
    """TestRunDetail stores one single run result"""

    assert_entry: AssertionEntry = Field(default=NotImplemented)
    is_pass: bool = Field(default=False)
    message: str = Field(default_factory=str)

    def as_fmt_str(self) -> str:
        """String representation of ApiResponse

        Returns:
            str: String representation
        """

        if self.assert_entry == NotImplemented:
            raise NotImplementedError("AssertionEntry not set.")

        return (
            "\n"
            f"{'+' if self.is_pass else '-'} {self.assert_entry.assert_type} "
            + f"{'PASSED' if self.is_pass else 'FAILED'}, {self.message}"
        )

    def get_message_values(self) -> dict:
        """Get tokens for template messages"""

        if self.assert_entry == NotImplemented:
            raise NotImplementedError("AssertionEntry not set.")

        return {
            "assert_type": self.assert_entry.assert_type,
            "type_actual": self.assert_entry.actual.__class__.__name__,
            "type_expected": self.assert_entry.expected.__class__.__name__,
            "value_actual": self.assert_entry.actual,
            "value_expected": self.assert_entry.expected,
            "value_actual_given": self.assert_entry.actual_given,
            "value_actual_b4_cast": self.assert_entry.actual_b4_cast,
            "extra_fields": self.assert_entry.extra_fields,
        }


class TestRunReport(BaseModel):
    """TestRunReport stores overall test run report"""

    id: UUID4 = Field(default_factory=uuid.uuid4)
    time_start: datetime = Field(default_factory=datetime.now)
    time_end: datetime = Field(default_factory=datetime.now)
    count_all: int = Field(default=0)
    count_fail: int = Field(default=0)
    details: list[TestRunDetail] = Field(default_factory=list)

    def __iter__(self):
        """Implement __iter__"""

        yield "id", str(self.id)
        yield "time_start", self.time_start.timestamp()
        yield "time_end", self.time_end.timestamp()
        yield "count_all", self.count_all
        yield "count_fail", self.count_fail
        yield "details", [detail.model_dump() for detail in self.details]

    def add_run_detail(self, run_dtl: TestRunDetail) -> None:
        """Append a TestRunDetail"""

        if not isinstance(run_dtl, TestRunDetail):
            raise TypeError("TestRunDetail expected.")

        self.details.append(run_dtl)

        if run_dtl.is_pass:
            self.count_fail += 1

    def as_fmt_str(self, only_incl_errors: bool = False) -> str:
        """String representation of ApiResponse

        Returns:
            str: String representation
        """

        _display = (
            f"Test run id: {self.id}, time taken {self.time_end - self.time_start}\n"
            + f"Total tests: {self.count_all}, "
            + f"Total tests failed: {self.count_fail}\n"
        )
        _display += "\n> Test run result(s):"

        if only_incl_errors:
            for detail in self.details:
                if not detail.is_pass:
                    _display += detail.as_fmt_str()
        else:
            for detail in self.details:
                _display += detail.as_fmt_str()

        return _display


class ValidationTask(BaseModel):
    """Parsed FetchTask"""

    name: str
    uses: str
    file: str
    variables: dict = Field(default_factory=dict)
    arguments: dict = Field(default_factory=dict)
