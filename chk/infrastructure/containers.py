"""
Global application functionality
"""
from enum import Enum
from typing import NamedTuple

from chk.infrastructure.file_loader import FileContext, ChkFileLoader
from chk.infrastructure.helper import dict_get, dict_set


class CompiledDocBlockType(Enum):
    """Support compiled doc blocks"""

    REQUEST = "request"
    VERSION = "version"
    VARIABLES = "variables"
    EXPOSE = "expose"
    LOCAL = "__local"

    @staticmethod
    def allowed_keys() -> set:
        return {
            e.value for e in CompiledDocBlockType if not str(e.value).startswith("__")
        }

    @staticmethod
    def all_keys() -> set:
        return {e.value for e in CompiledDocBlockType}


class App(NamedTuple):
    """Global app container"""

    original_doc: dict = {}
    compiled_doc: dict = {}

    environment_ctx: dict = {
        "config": {
            "buffer_access_off": True
        },
    }

    def __str__(self) -> str:
        return (
            f"original_doc: {str(self.original_doc)}\r\n\r\n"
            + f"compiled_doc: {str(self.compiled_doc)}\r\n\r\n"
        )

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

        allowed_keys = CompiledDocBlockType.all_keys()

        if key not in self.compiled_doc:
            self.compiled_doc[key] = {item: {} for item in allowed_keys}

        if part is not None:
            if part not in allowed_keys:
                raise SystemExit("Unsupported key for compiled doc")

            self.compiled_doc[key][part] = value
        else:
            allowed_keys = CompiledDocBlockType.allowed_keys()

            # Match against all key given and allowed
            if len(value.keys()) != len(allowed_keys):
                raise SystemExit("Unmatched key length for compiled doc")

            if set(value.keys()) != allowed_keys:
                raise SystemExit("Unmatched allowed keys for compiled doc")

            self.compiled_doc[key] = value

    def get_compiled_doc(self, key: str, part: str | None = None) -> object:
        """Get compiled file doc"""

        allowed_keys = CompiledDocBlockType.all_keys()

        if part is not None:
            if part not in allowed_keys:
                raise SystemExit("Unsupported key for compiled doc")

            return self.compiled_doc[key][part]

        return self.original_doc.get(key)

    def load_original_doc_from_file_context(self, file_ctx: FileContext) -> None:
        """Load original doc from a given file context"""

        document = ChkFileLoader.to_dict(file_ctx.filepath)
        self.set_original_doc(file_ctx.filepath_hash, document)

    def config(self, key: str, val: object = None) -> object:
        if val is not None:
            dict_set(self.environment_ctx, f"config.{key}", val)

        return dict_get(self.environment_ctx, f"config.{key}", None)
