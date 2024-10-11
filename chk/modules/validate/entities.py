from typing import Any
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
