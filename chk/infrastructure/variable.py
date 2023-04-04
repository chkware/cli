"""
Variable manipulation utils module
"""
import json
import typing
import dataclasses


@dataclasses.dataclass
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
