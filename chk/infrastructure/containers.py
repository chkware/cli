"""
Global application functionality
"""

from dataclasses import dataclass, asdict
from collections.abc import Callable
from enum import Enum
from typing import NamedTuple, Self

import click

from chk.infrastructure.file_loader import FileContext, ChkFileLoader
from chk.infrastructure.helper import dict_get, data_set, data_get


@dataclass
class CompiledOptions:
    result: bool = True
    dump: bool = True
    format: bool = True

    @staticmethod
    def from_file_context(file_context: FileContext) -> Self:
        return CompiledOptions(
            file_context.options.get("result", True),
            file_context.options.get("dump", True),
            file_context.options.get("format", True),
        )

    dict = asdict


class CompiledDocBlockType(Enum):
    """Support compiled doc blocks"""

    SPEC = "spec"
    REQUEST = "request"
    VERSION = "version"
    VARIABLES = "variables"
    EXPOSE = "expose"
    LOCAL = "__local"
    OUTER = "__outer"

    @staticmethod
    def allowed_keys() -> set:
        return {
            e.value for e in CompiledDocBlockType if not str(e.value).startswith("__")
        }

    @staticmethod
    def all_keys() -> set:
        return {e.value for e in CompiledDocBlockType}

    @staticmethod
    def default() -> dict:
        return {item: {} for item in CompiledDocBlockType.all_keys()}


class App(NamedTuple):
    """Global app container"""

    original_doc: dict = {}
    compiled_doc: dict = {}

    environment_ctx: dict = {
        "config": {},
    }

    def __str__(self) -> str:
        return (
            f"original_doc: {str(self.original_doc)}\r\n\r\n"
            + f"compiled_doc: {str(self.compiled_doc)}\r\n\r\n"
        )

    def set_original_doc(self, key: str, value: dict) -> None:
        """Set original file doc"""

        if not isinstance(value, dict):
            raise RuntimeError("Unsupported format for original doc")

        self.original_doc[key] = value

    def get_original_doc(self, key: str) -> dict:
        """Get original file doc"""

        return self.original_doc.get(key, {})

    def set_compiled_doc(
        self, key: str, value: object, part: str | None = None
    ) -> None:
        """Set compiled file doc"""

        allowed_keys = CompiledDocBlockType.all_keys()

        if key not in self.compiled_doc:
            self.compiled_doc[key] = CompiledDocBlockType.default()

        if part is not None:
            if part.split(".")[:1][0] not in allowed_keys:
                raise RuntimeError("Unsupported key for compiled doc")

            data_set(self.compiled_doc[key], part, value)
        else:
            allowed_keys = CompiledDocBlockType.allowed_keys()

            # Match against all key given and allowed
            if not isinstance(value, dict):
                raise RuntimeError("error: Only dictionary value allowed")

            if len({val for val in value.keys() if val not in allowed_keys}) > 0:
                raise RuntimeError("error: Unmatched allowed keys for compiled doc")

            self.compiled_doc[key] = value

    def get_compiled_doc(self, key: str, part: str | None = None) -> object:
        """Get compiled file doc"""

        allowed_keys = CompiledDocBlockType.all_keys()

        if part is not None:
            if part.split(".")[:1][0] not in allowed_keys:
                raise RuntimeError("Unsupported key for compiled doc")

            return dict_get(self.compiled_doc[key], part)

        return self.compiled_doc[key]

    def load_original_doc_from_file_context(self, file_ctx: FileContext) -> None:
        """Load original doc from a given file context"""

        document = ChkFileLoader.to_dict(file_ctx.filepath)
        self.set_original_doc(file_ctx.filepath_hash, document)

        # add outer replaceable variables
        outer_vars = file_ctx.arguments.get(CompiledDocBlockType.VARIABLES.value)

        if isinstance(outer_vars, dict):
            self.set_outer(
                file_ctx.filepath_hash,
                outer_vars,
                CompiledDocBlockType.VARIABLES.value,
            )

        co = CompiledOptions.from_file_context(file_ctx)
        data_set(self.environment_ctx, f"{file_ctx.filepath_hash}.config", co.dict())

    def config(self, key: str, part: str, val: object = None) -> object:
        """Set and retrieve config"""

        if len(part) == 0:
            raise ValueError("part can't be zero-length")

        loc = f"{key}.config.{part}"

        if val is not None:
            data_set(self.environment_ctx, loc, val)

        return dict_get(self.environment_ctx, loc, None)

    def set_local(self, key: str, val: object, part: str) -> bool:
        """Set local variable values in compiled_doc dict"""
        if key not in self.compiled_doc:
            self.compiled_doc[key] = CompiledDocBlockType.default()
        return data_set(
            self.compiled_doc[key], f"{CompiledDocBlockType.LOCAL.value}.{part}", val
        )

    def get_local(self, key: str, part: str) -> object:
        """Set local variable values in compiled_doc dict"""
        return dict_get(
            self.compiled_doc[key], f"{CompiledDocBlockType.LOCAL.value}.{part}"
        )

    def set_outer(self, key: str, val: object, part: str) -> bool:
        """Set local variable values in original_doc dict"""
        if key not in self.original_doc:
            self.original_doc[key] = CompiledDocBlockType.default()
        return data_set(
            self.original_doc[key], f"{CompiledDocBlockType.OUTER.value}.{part}", val
        )

    def get_outer(self, key: str, part: str) -> object:
        """Set local variable values in original_doc dict"""
        return data_get(
            self.original_doc[key], f"{CompiledDocBlockType.OUTER.value}.{part}"
        )

    @staticmethod
    def print_fmt(
        message: object, callback: Callable = str, ret_s: bool = False
    ) -> str | None:
        """Print message to screen when buffer is off"""
        if ret_s is True:
            return str(callback(message))

        click.echo(str(callback(message)))
        return None
