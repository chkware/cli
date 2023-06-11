"""
Validate module
"""

import dataclasses
import datetime
import enum
import typing
from collections import abc, UserDict

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


class SingleTestRunResult(UserDict):
    """Result of an assertion run"""

    is_pass: bool
    time_start: datetime.datetime
    time_end: datetime.datetime
    message: str


class AllTestRunResult(UserDict):
    """Result of a test run"""

    id: str
    time_start: datetime.datetime
    time_end: datetime.datetime
    count_all: int
    results: list[SingleTestRunResult]
    count_fail: int = 0

    @property
    def is_all_pass(self) -> bool:
        """Have all assertion passed for this test run"""

        return self.count_fail == 0


class AssertionEntry(typing.NamedTuple):
    """AssertionEntry holds one assertion operation"""

    assert_id: str
    assert_function: str
    type_of_actual: object
    actual: typing.Any
    type_of_expected: object
    expected: typing.Any
    msg_pass: str
    msg_fail: str


class AssertionAntiquary:
    """AssertionAntiquary is service class that run assertion"""

    @staticmethod
    def test_run():
        pass


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

    import var_dump

    var_dump.var_dump(validate_doc.asserts)

    # handle passed templated data in asserts, with variables
    # handle passed templated data in templated asserts, with variables
    # handle passed in-file data in templated asserts, with variables
