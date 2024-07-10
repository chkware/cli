"""
Validate module
"""

from __future__ import annotations
import dataclasses
import enum
import json
from collections import abc

import cerberus
from hence import task

from chk.infrastructure.document import VersionedDocument, VersionedDocumentSupport
from chk.infrastructure.file_loader import FileContext, ExecuteContext
from chk.infrastructure.helper import data_get, formatter
from chk.infrastructure.version import DocumentVersionMaker, SCHEMA as VER_SCHEMA

from chk.infrastructure.symbol_table import (
    VARIABLE_SCHEMA as VAR_SCHEMA,
    EXPOSE_SCHEMA as EXP_SCHEMA,
    Variables,
    VariableTableManager,
    replace_value,
    ExposeManager,
    ExposableVariables,
    ExecResponse,
)
from chk.modules.validate.assertion_services import (
    AssertionEntry,
    AssertionEntryListRunner,
    AllTestRunResult,
    ValidationTask,
    MAP_TYPE_TO_FN,
)
from chk.modules.validate.assertion_validation import (
    get_schema_map,
    AssertionEntityProperty,
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


@dataclasses.dataclass(slots=True)
class ValidationDocument(VersionedDocument):
    """
    Http document entity
    """

    data: dict = dataclasses.field(default_factory=dict)
    asserts: list = dataclasses.field(default_factory=list)

    @staticmethod
    def from_file_context(ctx: FileContext) -> ValidationDocument:
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

            validator = cerberus.Validator(get_schema_map(_assert_type))

            if not validator.validate(each_assert):
                raise RuntimeError(
                    f"key: Unsupported structure for `{each_assert}`. {validator.errors}"
                )

            if _assert_type not in MAP_TYPE_TO_FN:
                raise RuntimeError(f"type: `{_assert_type}` not supported.")

            if "actual" not in each_assert:
                raise RuntimeError("key: `actual` not found in one of the asserts.")
            _actual = each_assert["actual"]

            _expected = (
                each_assert["expected"] if "expected" in each_assert else NotImplemented
            )

            _cast_actual_to = each_assert.get("cast_actual_to", "")
            _msg_pass = each_assert.get("msg_pass", "")
            _msg_fail = each_assert.get("msg_fail", "")

            only = tuple(set(each_assert.keys()) - set(AssertionEntityProperty))
            _extra_fld = {}

            if len(only) > 0:
                _extra_fld = {
                    key: val for key, val in each_assert.items() if key in only
                }

            new_assertion_lst.append(
                AssertionEntry(
                    assert_type=_assert_type,
                    actual=_actual,
                    expected=_expected,
                    cast_actual_to=_cast_actual_to,
                    extra_fields=_extra_fld,
                    msg_pass=_msg_pass,
                    msg_fail=_msg_fail,
                )
            )

        return new_assertion_lst

    @staticmethod
    def display(expose_list: list, exec_ctx: ExecuteContext) -> None:
        """Displays the response based on the command response format

        Args:
            expose_list: list
            exec_ctx: ExecuteContext
        """

        if not expose_list:
            return

        display_item_list: list[object] = []

        for expose_item in expose_list:
            if isinstance(expose_item, AllTestRunResult):
                if exec_ctx.options["format"]:
                    display_item_list.append(expose_item.as_fmt_str)
                else:
                    display_item_list.append(expose_item.as_dict)
            else:
                display_item_list.append(expose_item)

        if exec_ctx.options["format"]:
            formatter(
                (
                    "\n---\n".join([str(item) for item in display_item_list])
                    if len(display_item_list) > 1
                    else display_item_list.pop()
                ),
                dump=exec_ctx.options["dump"],
            )
        else:
            formatter(
                (
                    json.dumps(display_item_list)
                    if len(display_item_list) > 1
                    else json.dumps(display_item_list.pop())
                ),
                dump=exec_ctx.options["dump"],
            )


def call(file_ctx: FileContext, exec_ctx: ExecuteContext) -> ExecResponse:
    """Call a validation document"""

    validate_doc = ValidationDocument.from_file_context(file_ctx)

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

    test_run_result = AssertionEntryListRunner.test_run(assert_list, variable_doc.data)
    output_data = ExposableVariables(
        {
            "_asserts_response": test_run_result.as_dict,
            "_data": variable_doc["_data"],
        }
    )

    return ExecResponse(
        file_ctx=file_ctx,
        exec_ctx=exec_ctx,
        variables_exec=output_data,
        variables=variable_doc,
        extra=test_run_result,
    )


def execute(
    ctx: FileContext, exec_ctx: ExecuteContext, cb: abc.Callable = lambda *args: ...
) -> None:
    """Run a validation document

    Args:
        ctx: FileContext object to handle
        exec_ctx: ExecuteContext
        cb: Callable
    """

    exec_response = call(file_ctx=ctx, exec_ctx=exec_ctx)

    validate_doc = ValidationDocument.from_file_context(ctx)
    exposed_data = ExposeManager.get_exposed_replaced_data(
        validate_doc,
        {
            **exec_response.variables.data,
            **{"_asserts_response": exec_response.extra},
        },
    )

    cb({ctx.filepath_hash: exec_response.variables_exec.data})
    ValidationDocumentSupport.display(exposed_data, exec_ctx)


@task(title="Validate task")
def task_validation(**kwargs: dict) -> ExecResponse:
    """Task impl"""

    if not (doc := kwargs.get("task", {})):
        raise ValueError("Wrong task format given.")

    _task = ValidationTask(**doc)

    return call(
        FileContext.from_file(_task.file),
        ExecuteContext(
            options={"dump": True, "format": True},
            arguments=_task.arguments | {"variables": _task.variables},
        ),
    )
