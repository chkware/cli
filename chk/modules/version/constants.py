from enum import Enum

from typing import Any
from dataclasses import dataclass


class DocumentType(Enum):
    HTTP = "http"
    TESTCASE = "testcase"

    @classmethod
    def from_value(cls, value: Any) -> "DocumentType":
        for _, val in cls.__members__.items():
            if val.value == value:
                return val

        raise ValueError("Value do not match")


@dataclass
class VersionConfigNode:
    """represent the base of all kind of documents"""

    VERSION = "version"


class VersionStore:
    """VersionStore lists all version strings."""

    request_versions: list = [
        "default:http:0.7.2",
    ]

    testcase_versions: list = [
        "default:testcase:0.7.2",
    ]
