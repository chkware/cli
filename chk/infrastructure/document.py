"""
Module for all the core entities
"""
import abc
import dataclasses
import json
import typing

from chk.infrastructure.variable import Variable
from chk.infrastructure.version import DocumentVersion


@typing.runtime_checkable
class JsonSerializable(typing.Protocol):
    """
    Document protocol
    """

    def from_json(self, json_string: str) -> None:
        """Signature to converts json string to document"""

    def as_json(self) -> str:
        """Signature to converts document to json string"""


@typing.runtime_checkable
class DictionarySerializable(typing.Protocol):
    """
    Document protocol
    """

    def from_dict(self, dict_obj: dict) -> None:
        """Signature to converts dictionary to document"""

    def as_dict(self) -> dict:
        """Signature to converts document to dictionary"""


@dataclasses.dataclass(slots=True)
class BaseDocument(abc.ABC):
    """
    Base of all specification document
    """

    version: DocumentVersion | str = dataclasses.field(default_factory=str)
    exposables: list[Variable] = dataclasses.field(default_factory=list)
    variables: list[Variable] = dataclasses.field(default_factory=list)

    def as_dict(self) -> dict:
        return dataclasses.asdict(self)

    def as_json(self) -> str:
        """Default overloaded implementation"""
        return json.dumps(self.as_dict)


@dataclasses.dataclass(slots=True)
class CallingContextData:
    """Representation of context object"""

    document: BaseDocument
    behaviour: dict = dataclasses.field(default_factory=dict)
    attribute: dict = dataclasses.field(default_factory=dict)
