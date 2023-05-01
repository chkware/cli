"""
Version string management
"""

import dataclasses
import re
from enum import StrEnum, auto

from chk.infrastructure.helper import data_get

VERSION_FORMAT_REGEX = r"^([A-Za-z0-9-\.:]+){3}$"


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

        self.validate(True)
        self.parse()

    def parse(self) -> None:
        """
        Parse provider, doc_type, doc_type_ver from original_version_str
        """

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

    def validate(self, throw: bool = False) -> bool:
        """
        Validate version string
        params:
            throw: bool Should raise exception, defaults to False
        throws:
            ValueError If throw is set to True
        """

        if not self.original_version_str:
            raise ValueError("version is empty")

        if re.search(VERSION_FORMAT_REGEX, self.original_version_str):
            return True

        if throw:
            raise ValueError("Invalid version string format")

        return False


class DocumentVersionMaker:
    """Create document version object"""

    @staticmethod
    def from_dict(document: dict) -> DocumentVersion:
        """Create a DocumentVersion from given dict"""

        version_str = data_get(document, VersionConfigNode.VERSION, None)
        return DocumentVersion(version_str)
