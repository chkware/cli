"""
Version management
"""
import dataclasses
import re


@dataclasses.dataclass
class DocumentVersion:
    _version: str
    _version_format_regex = r"^([\w-]+:[\w-]+){2}$"

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

        if re.search(self._version_format_regex, self._version):
            return True

        if throw:
            raise ValueError("Invalid version string format")

        return False
