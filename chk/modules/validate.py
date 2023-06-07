"""
Validate module
"""

import dataclasses
import enum
from collections import abc

from chk.infrastructure.document import VersionedDocument, VersionedDocumentSupport
from chk.infrastructure.file_loader import FileContext, ExecuteContext
from chk.infrastructure.helper import data_get
from chk.infrastructure.version import DocumentVersionMaker, SCHEMA as VER_SCHEMA

from chk.infrastructure.symbol_table import (
    VARIABLE_SCHEMA as VAR_SCHEMA,
    EXPOSE_SCHEMA as EXP_SCHEMA,
)

VERSION_SCOPE = ["validation"]


class ValidationConfigNode(enum.StrEnum):
    """represent request config section"""

    ASSERTS = enum.auto()
    DATA = enum.auto()


DATA_SCHEMA = {
    ValidationConfigNode.DATA: {
        "required": False,
        "empty": True,
        "nullable": True,
        "type": "dict",
    }
}

ASSERTS_SCHEMA = {
    ValidationConfigNode.ASSERTS: {
        "required": True,
        "empty": False,
        "type": "list",
        "valuesrules": {"type": "dict"},
    }
}


@dataclasses.dataclass(slots=True)
class ValidationDocument(VersionedDocument):
    """
    Http document entity
    """

    data: dict = dataclasses.field(default_factory=dict)
    asserts: dict = dataclasses.field(default_factory=dict)

    @staticmethod
    def from_file_context(ctx: FileContext) -> "ValidationDocument":
        """Create a ValidationDocument from FileContext
        :param ctx: FileContext to create the ValidationDocument from
        """

        if not (version_str := data_get(ctx.document, "version")):
            raise RuntimeError("`version:` not found.")

        if not (
            asserts_dct := data_get(ctx.document, ValidationConfigNode.ASSERTS, {})
        ):
            raise RuntimeError(f"`{ValidationConfigNode.ASSERTS}:` not found.")

        data_dct = data_get(ctx.document, ValidationConfigNode.DATA, {})

        return ValidationDocument(
            context=tuple(ctx),
            version=version_str,
            asserts=asserts_dct,
            data=data_dct,
        )

    @property
    def as_dict(self) -> dict:
        """Return a dict of the data"""

        return dataclasses.asdict(self)


class ValidationDocumentSupport:
    """Service class for ValidationDocument"""

    @staticmethod
    def build_schema() -> dict:
        """Validate a validation document with given json-schema

        Returns:
            dict: Containing validation document schema
        """

        return {
            **VER_SCHEMA,
            **ASSERTS_SCHEMA,
            **DATA_SCHEMA,
            **VAR_SCHEMA,
            **EXP_SCHEMA,
        }


def execute(
    ctx: FileContext, exec_ctx: ExecuteContext, cb: abc.Callable = lambda *args: ...
) -> None:
    """Run a validation document

    Args:
        ctx: FileContext object to handle
        exec_ctx: ExecuteContext
        cb: Callable
    """

    validate_doc = ValidationDocument.from_file_context(ctx)

    DocumentVersionMaker.verify_if_allowed(
        DocumentVersionMaker.from_dict(validate_doc.as_dict), VERSION_SCOPE
    )

    VersionedDocumentSupport.validate_with_schema(
        ValidationDocumentSupport.build_schema(), validate_doc
    )
