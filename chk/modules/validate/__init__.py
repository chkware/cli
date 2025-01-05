"""
Validate module
"""

from __future__ import annotations

import enum
import sys
from collections import abc

import cerberus
from pydantic import BaseModel, Field

from chk.infrastructure.document import (
    VersionedDocumentSupport,
    VersionedDocumentV2,
)
from chk.infrastructure.file_loader import ExecuteContext, FileContext
from chk.infrastructure.helper import data_get
from chk.infrastructure.logging import debug, error_trace, with_catch_log
from chk.infrastructure.symbol_table import (
    EXPOSE_SCHEMA as EXP_SCHEMA,
    ExecResponse,
    ExposeManager,
    VARIABLE_SCHEMA as VAR_SCHEMA,
    VariableTableManager,
    Variables,
    replace_value,
)
from chk.infrastructure.version import DocumentVersionMaker, SCHEMA as VER_SCHEMA
from chk.infrastructure.view import PresentationService, die_with_error
from chk.modules.validate.assertion_services import (
    AssertionEntry,
    AssertionEntryListRunner,
    MAP_TYPE_TO_FN,
)
from chk.modules.validate.assertion_validation import (
    AssertionEntityProperty,
    get_schema_map,
)
from chk.modules.validate.entities import ValidationTask
from chk.modules.validate.services import ValidatePresenter

VERSION_SCOPE = ["validate"]


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


class ValidationDocument(VersionedDocumentV2, BaseModel):
    """
    Http document entity
    """

    data: dict = Field(default_factory=dict)
    asserts: list = Field(default_factory=list)

    @staticmethod
    def from_file_context(ctx: FileContext) -> ValidationDocument:
        """Create a ValidationDocument from FileContext
        :param ctx: FileContext to create the ValidationDocument from
        """

        doc_ver = DocumentVersionMaker.from_dict(ctx.document)
        DocumentVersionMaker.verify_if_allowed(doc_ver, VERSION_SCOPE)

        if not (_asserts := data_get(ctx.document, ValidationConfigNode.ASSERTS, [])):
            raise RuntimeError(f"`{ValidationConfigNode.ASSERTS}:` not found.")

        _data = data_get(ctx.document, ValidationConfigNode.DATA, {})

        # @TODO keep `context`, `version` as object
        # @TODO implement __repr__ for WorkflowDocument
        return ValidationDocument(
            context=tuple(ctx),
            version=str(doc_ver),
            asserts=_asserts,
            data=_data,
        )


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
        variables[ValidationConfigNode.VAR_NODE.value] = (
            data if data else validate_doc.data
        )

    @staticmethod
    def process_data_template(variables: Variables) -> None:
        """process data or template before assertion"""
        data = variables[ValidationConfigNode.VAR_NODE.value]
        tmp_variables = {
            key: val
            for key, val in variables.data.items()
            if key != ValidationConfigNode.VAR_NODE.value
        }

        variables[ValidationConfigNode.VAR_NODE.value] = replace_value(
            data, tmp_variables
        )

    @staticmethod
    def make_assertion_entry_list(assert_lst: list[dict]) -> list[AssertionEntry]:
        new_assertion_lst: list[AssertionEntry] = []

        for each_assert in assert_lst:
            if not (_assert_type := each_assert.get("type", None)):
                raise RuntimeError("key: `type` not found in one of the asserts.")

            try:
                validator = cerberus.Validator(get_schema_map(_assert_type))
            except KeyError as ex:
                raise KeyError(
                    f"`{_assert_type}` key not found. in {repr(each_assert)}"
                ) from ex

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
            ae = AssertionEntry(
                assert_type=_assert_type,
                actual=_actual,
                expected=_expected,
                cast_actual_to=_cast_actual_to,
                extra_fields=_extra_fld,
                msg_pass=_msg_pass,
                msg_fail=_msg_fail,
            )
            debug(ae)

            new_assertion_lst.append(ae)

        return new_assertion_lst


@with_catch_log
def call(file_ctx: FileContext, exec_ctx: ExecuteContext) -> ExecResponse:
    """Call a validation document"""

    debug(file_ctx)
    debug(exec_ctx)

    try:
        validate_doc = ValidationDocument.from_file_context(file_ctx)
        debug(validate_doc.model_dump_json())

        VersionedDocumentSupport.validate_with_schema(
            ValidationDocumentSupport.build_schema(), validate_doc
        )
    except Exception as ex:
        error_trace(exception=sys.exc_info()).error(ex)
        return ExecResponse(
            file_ctx=file_ctx,
            exec_ctx=exec_ctx,
            exception=ex,
            report={"is_success": False},
        )

    variable_doc = Variables()
    VariableTableManager.handle(variable_doc, validate_doc, exec_ctx)
    debug(variable_doc.data)

    # handle passed data in asserts
    ValidationDocumentSupport.set_data_template(validate_doc, variable_doc, exec_ctx)

    ValidationDocumentSupport.process_data_template(variable_doc)
    debug(variable_doc.data)

    try:
        assert_list = ValidationDocumentSupport.make_assertion_entry_list(
            validate_doc.asserts
        )

        run_rpt = AssertionEntryListRunner.test_run(assert_list, variable_doc.data)
    except Exception as ex:
        error_trace(exception=sys.exc_info()).error(ex)
        return ExecResponse(
            file_ctx=file_ctx,
            exec_ctx=exec_ctx,
            exception=ex,
            report={"is_success": False},
        )

    output_data = Variables(
        {
            "_asserts_response": run_rpt,
            "_data": variable_doc["_data"],
        }
    )
    debug(output_data.data)

    exposed_data = ExposeManager.get_exposed_replaced_data(
        validate_doc,
        {
            **variable_doc.data,
            **{"_asserts_response": run_rpt},
        },
    )
    debug(exposed_data)

    # TODO: this is needed only when the request is true
    #       > ExecResponse.__bool__() needed to see if the object is ok OR
    #       > add "variables_exec", "extra", "exposed", "report" only when call() is
    #           successful

    return ExecResponse(
        file_ctx=file_ctx,
        exec_ctx=exec_ctx,
        variables_exec=output_data,
        variables=variable_doc,
        extra=run_rpt,
        exposed=exposed_data,
        report={
            "is_success": run_rpt.count_fail == 0,
            "count_all": len(validate_doc.asserts),
            "count_fail": run_rpt.count_fail,
            "exceptions": [dtl.message for dtl in run_rpt.details if not dtl.is_pass],
        },
    )


@with_catch_log
def execute(
    ctx: FileContext, exec_ctx: ExecuteContext, cb: abc.Callable = lambda *args: ...
) -> None:
    """Run a validation document

    Args:
        ctx: FileContext object to handle
        exec_ctx: ExecuteContext
        cb: Callable
    """
    try:
        exr = call(file_ctx=ctx, exec_ctx=exec_ctx)

        cb({ctx.filepath_hash: exr.variables_exec.data})
        PresentationService.display(exr, exec_ctx, ValidatePresenter)
    except Exception as ex:
        error_trace(exception=sys.exc_info()).error(ex)
        die_with_error(ex, ValidatePresenter, exec_ctx.options["format"])


@with_catch_log
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
