"""
Variable manipulation utils module
"""
import dataclasses
import json
import re
import typing

LOCAL_VARIABLE_NAME_FORMAT_REGEX = r"^([a-zA-Z]\w*)$"


@typing.runtime_checkable
class Variable(typing.Protocol):
    """Variable protocol"""

    def as_json(self) -> str:
        """Returns json representation of a variable"""

    value_type: typing.Any
    """Returns type of the variable's value"""


@dataclasses.dataclass(slots=True)
class LocalVariable:
    name: str
    value: typing.Any

    def __post_init__(self) -> None:
        self._validate_name(True)

    @property
    def as_dict(self) -> dict:
        """
        Dictionary impl
        """

        return dataclasses.asdict(self)

    def as_json(self) -> str:
        """
        Overloaded protocol impl
        """

        return json.dumps(self.as_dict)

    @property
    def value_type(self) -> typing.Any:
        """
        Override type of value impl
        """

        return type(self.value)

    def _validate_name(self, throw: bool = False) -> bool:
        """
        Validate local variable name

        params:
            throw: bool Should raise exception, defaults to False
        throws:
            ValueError If throw is set to True
        """
        if re.search(LOCAL_VARIABLE_NAME_FORMAT_REGEX, self.name):
            return True

        if throw:
            raise ValueError(f"Invalid local variable name: `{self.name}`")

        return False
