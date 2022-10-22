from enum import Enum

from typing import List
from dataclasses import dataclass


class DocumentType(Enum):
    HTTP = 'http'
    TESTCASE = 'testcase'

    @classmethod
    def from_value(cls, value=None):
        for key, val in cls.__members__.items():
            if val.value == value:
                return val
        return value


@dataclass
class VersionConfigNode:
    """represent the base of all kind of documents"""
    VERSION = 'version'


class VersionStore:
    """VersionStore lists all version strings."""

    request_versions: List = [
        'default:http:0.7.2',
    ]

    testcase_versions: List = [
        'default:testcase:0.7.2',
    ]
