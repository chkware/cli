"""
Global application functionality
"""
from typing import NamedTuple
from copy import deepcopy


class App(NamedTuple):
    """
    Global app container; used to bootstrap global level data structure
    """

    original_doc: dict = {}
    compiled_doc: dict = {}
    display_buffer: dict = {}

    def __str__(self) -> str:
        return format(self.__str__())

    def set_original_doc(self, key: str, value: dict) -> None:
        """Set original file doc"""

        if not isinstance(value, dict):
            raise SystemExit("Unsupported format for original doc")

        self.original_doc[key] = value

    def get_original_doc(self, key: str) -> dict:
        """Get original file doc"""

        return self.original_doc.get(key, {})
