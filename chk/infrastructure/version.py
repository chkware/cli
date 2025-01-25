"""
Version string management
"""

import dataclasses
import re
from enum import StrEnum, auto

from chk.infrastructure.helper import data_get

VERSION_FORMAT_REGEX = r"^([A-Za-z0-9-\.:]+){3}$"

# VERSION_STORE lists all version strings.
VERSION_STORE = {
    "http": [
        "0.7.2",
    ],
    "validate": [
        "0.7.2",
    ],
    "workflow": [
        "0.8.0",
    ],
}

# validation schema
SCHEMA = {
    "version": {
        "required": True,
        "type": "string",
        "empty": False,
    }
}


class VersionConfigNode(StrEnum):
    """represent the base of all kind of documents"""

    VERSION = auto()


@dataclasses.dataclass(slots=True)
class DocumentVersion:
    """DocumentVersion class to hold version"""

    original_version_str: str
    provider: str = dataclasses.field(default_factory=str)
    doc_type: str = dataclasses.field(default_factory=str)
    doc_type_ver: str = dataclasses.field(default_factory=str)

    def __post_init__(self) -> None:
        """Validate after class initiated"""

        self.validate()
        self.parse()
        self.verify_doc_type_ver()

    def parse(self) -> None:
        """Parse provider, doc_type, doc_type_ver from original_version_str"""

        ver_l = self.original_version_str.split(":")
        if len(ver_l) < 3:
            raise ValueError("version format not supported")

        self.provider, self.doc_type, self.doc_type_ver = (
            ver_l[0],
            ":".join(ver_l[1:-1]),
            ver_l[-1],
        )

        if (
            len(self.provider) == 0
            or len(self.doc_type) == 0
            or len(self.doc_type_ver) == 0
        ):
            raise ValueError("Invalid version string")

    def validate(self) -> bool:
        """Validate version string

        Raises:
            ValueError: If throw is set to True
        """

        if not self.original_version_str:
            raise ValueError("version is empty")

        if not re.search(VERSION_FORMAT_REGEX, self.original_version_str):
            raise ValueError("Invalid version string format")

        return True

    def verify_doc_type_ver(self) -> bool:
        """Verify that doc_type_ver is supported

        Raises:
            ValueError: When doc_type is not supported

        Returns:
            bool: True if verification complete
        """

        if self.doc_type not in VERSION_STORE:
            raise ValueError("Invalid doc_type in version string")

        if self.doc_type_ver not in VERSION_STORE[self.doc_type]:
            raise ValueError("Invalid doc_type_ver in version string")

        return True

    def __str__(self) -> str:
        """str dunder"""

        return self.original_version_str


class DocumentVersionMaker:
    """Create document version object"""

    @staticmethod
    def from_dict(document: dict) -> DocumentVersion:
        """Create a DocumentVersion from given dict"""

        version_str = data_get(document, VersionConfigNode.VERSION, None)
        if not version_str:
            raise RuntimeError("`version:` not found.")

        return DocumentVersion(version_str)

    @staticmethod
    def verify_if_allowed(version: DocumentVersion, scopes: list[str]) -> bool:
        """Verify if a version is allowed with given scopes

        Args:
            version: DocumentVersion under test
            scopes: list[str] of string containing supported DocumentVersion.doc_type

        Raises:
            RuntimeError: Unsupported document exception
        """

        if version.doc_type not in scopes:
            raise RuntimeError("Unsupported document exception")

        return True
