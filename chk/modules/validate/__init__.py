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
    Variables,
    VariableTableManager,
    replace_value,
)
from chk.modules.validate.assertion_services import AssertionEntry

VERSION_SCOPE = ["validation"]


class ValidationConfigNode(enum.StrEnum):
    """represent request config section"""

    ASSERTS = enum.auto()
    DATA = enum.auto()
    VAR_NODE = "_data"


DATA_SCHEMA = {
    ValidationConfigNode.DATA: {
        "required": False,
        "empty": False,
        "nullable": False,
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
    asserts: list = dataclasses.field(default_factory=list)

    @staticmethod
    def from_file_context(ctx: FileContext) -> "ValidationDocument":
        """Create a ValidationDocument from FileContext
        :param ctx: FileContext to create the ValidationDocument from
        """

        if not (_version := data_get(ctx.document, "version")):
            raise RuntimeError("`version:` not found.")

        if not (_asserts := data_get(ctx.document, ValidationConfigNode.ASSERTS, [])):
            raise RuntimeError(f"`{ValidationConfigNode.ASSERTS}:` not found.")

        _data = data_get(ctx.document, ValidationConfigNode.DATA, {})

        return ValidationDocument(
            context=tuple(ctx),
            version=_version,
            asserts=_asserts,
            data=_data,
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

    @staticmethod
    def set_data_template(
        validate_doc: ValidationDocument,
        variables: Variables,
        exec_ctx: ExecuteContext,
    ) -> None:
        """sets data or template"""

        data = data_get(exec_ctx.arguments, "data", {})
        variables[ValidationConfigNode.VAR_NODE] = data if data else validate_doc.data

    @staticmethod
    def process_data_template(variables: Variables) -> None:
        """process data or template before assertion"""
        data = variables[ValidationConfigNode.VAR_NODE]
        tmp_variables = {
            key: val
            for key, val in variables.data.items()
            if key != ValidationConfigNode.VAR_NODE
        }

        variables[ValidationConfigNode.VAR_NODE] = replace_value(data, tmp_variables)

    @staticmethod
    def make_assertion_entry_list(assert_lst: list[dict]) -> list[AssertionEntry]:
        new_assertion_lst: list[AssertionEntry] = []

        for each_assert in assert_lst:
            if not (_assert_type := each_assert.get("type", None)):
                raise RuntimeError("key: `type` not found in one of the asserts.")

            if not (_actual := each_assert.get("actual", None)):
                raise RuntimeError("key: `actual` not found in one of the asserts.")

            if not (_expected := each_assert.get("expected", None)):
                raise RuntimeError("key: `expected` not found in one of the asserts.")

            new_assertion_lst.append(
                AssertionEntry(
                    assert_type=_assert_type,
                    actual=_actual,
                    type_of_actual=type(_actual),
                    expected=_expected,
                    type_of_expected=type(_expected),
                    msg_pass="",
                    msg_fail="",
                    assert_id="",
                )
            )

        return new_assertion_lst


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

    variable_doc = Variables()
    VariableTableManager.handle(variable_doc, validate_doc, exec_ctx)

    # handle passed data in asserts
    ValidationDocumentSupport.set_data_template(validate_doc, variable_doc, exec_ctx)
    ValidationDocumentSupport.process_data_template(variable_doc)

    assert_list = ValidationDocumentSupport.make_assertion_entry_list(
        validate_doc.asserts
    )

    import var_dump

    var_dump.var_dump(assert_list)

    # handle passed in-file data in templated asserts, with variables