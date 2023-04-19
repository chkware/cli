"""
Version management
"""
import dataclasses
import re
from enum import Enum

from chk.infrastructure.helper import data_get

VERSION_FORMAT_REGEX = r"^([A-Za-z0-9-\.:]+){3}$"


class VersionConfigNode(Enum):
    """represent the base of all kind of documents"""

    VERSION = "version"


@dataclasses.dataclass
class DocumentVersion:
    _version: str

    def __post_init__(self) -> None:
        """
        Validate after class initiated
        """

        self._validate(True)

    @property
    def version(self) -> str:
        """
        Get version string. Validates the string before return
        """

        return self._version

    def _validate(self, throw: bool = False) -> bool:
        """
        Validate version string

        params:
            throw: bool Should raise exception, defaults to False
        throws:
            ValueError If throw is set to True
        """

        if re.search(VERSION_FORMAT_REGEX, self._version):
            return True

        if throw:
            raise ValueError("Invalid version string format")

        return False


class DocumentVersionMaker:
    """Create document version object"""

    @staticmethod
    def from_dict(document: dict) -> DocumentVersion:
        """Create a DocumentVersion from given dict"""

        version_str = data_get(document, VersionConfigNode.VERSION.value, None)
        return DocumentVersion(version_str)
