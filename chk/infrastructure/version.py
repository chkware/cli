"""
Version management
"""
import dataclasses
import re

VERSION_FORMAT_REGEX = r"^([\w-]+:[\w-]+){2}$"


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
