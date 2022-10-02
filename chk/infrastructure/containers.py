"""
Global application functionality
"""
from enum import Enum
from typing import NamedTuple


class CompiledDocBlockType(Enum):
    REQUEST = "request"
    VERSION = "version"
    VARIABLES = "variables"

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

    def set_compiled_doc(self, key: str, value: dict, part: str | None = None) -> None:
        """Set compiled file doc"""

        if not isinstance(value, dict):
            raise SystemExit("Unsupported format for compiled doc")

        allowed_keys = set(e.value for e in CompiledDocBlockType)

        if part is not None:
            if part not in allowed_keys:
                raise SystemExit("Unsupported key for compiled doc")

            self.compiled_doc[key][part] = value
        else:
            # Match against all key given and allowed
            if len(value.keys()) != len(allowed_keys):
                raise SystemExit("Unmatched key length for compiled doc")

            if set(value.keys()) != allowed_keys:
                raise SystemExit("Unmatched allowed keys for compiled doc")

            self.compiled_doc[key] = value
