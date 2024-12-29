"""
Fetch module
"""

import sys
from collections import abc

from chk.infrastructure.document import VersionedDocumentSupport
from chk.infrastructure.file_loader import ExecuteContext, FileContext
from chk.infrastructure.logging import debug, error_trace, with_catch_log
from chk.infrastructure.symbol_table import (
    ExecResponse,
    ExposeManager,
    VariableTableManager,
    Variables,
)
from chk.infrastructure.view import PresentationService, die_with_error
from chk.modules.fetch.entities import FetchTask
from chk.modules.fetch.services import FetchPresenter, HttpDocumentSupport


@with_catch_log
def call(file_ctx: FileContext, exec_ctx: ExecuteContext) -> ExecResponse:
    """Call a http document"""

    debug(file_ctx)
    debug(exec_ctx)

    try:
        http_doc = HttpDocumentSupport.from_file_context(file_ctx)
        debug(http_doc.model_dump_json())

        VersionedDocumentSupport.validate_with_schema(
            HttpDocumentSupport.build_schema(), http_doc
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
    VariableTableManager.handle(variable_doc, http_doc, exec_ctx)
    debug(variable_doc.data)

    try:
        HttpDocumentSupport.process_request_template(http_doc, variable_doc)
        debug(http_doc.model_dump())

        response = HttpDocumentSupport.execute_request(http_doc)
    except Exception as ex:
        error_trace(exception=sys.exc_info()).error(ex)
        return ExecResponse(
            file_ctx=file_ctx,
            exec_ctx=exec_ctx,
            exception=ex,
            report={"is_success": False},
        )

    output_data = Variables({"_response": response.model_dump()})
    debug(output_data.data)

    exposed_data = ExposeManager.get_exposed_replaced_data(
        http_doc,
        {**variable_doc.data, **output_data.data},
    )
    debug(exposed_data)

    # TODO: instead if sending specific report items, and making presentable in other
    #       module, we should prepare and long and short form of presentable that can be
    #       loaded via other module

    request_method, request_url = "", ""

    if "request" in file_ctx.document:
        if "method" in file_ctx.document["request"]:
            request_method = file_ctx.document["request"]["method"]
        if "url" in file_ctx.document["request"]:
            request_url = file_ctx.document["request"]["url"]

    return ExecResponse(
        file_ctx=file_ctx,
        exec_ctx=exec_ctx,
        variables_exec=output_data,
        variables=variable_doc,
        exposed=exposed_data,
        report={
            "is_success": True,
            "request_method": request_method,
            "request_url": request_url,
        },
    )


@with_catch_log
def execute(
    ctx: FileContext, exec_ctx: ExecuteContext, cb: abc.Callable = lambda *args: ...
) -> None:
    """Call with a http document

    Args:
        ctx: FileContext object to handle
        exec_ctx: ExecuteContext
        cb: Callable
    """

    try:
        exr = call(file_ctx=ctx, exec_ctx=exec_ctx)
        cb({ctx.filepath_hash: exr.variables_exec.data})
        PresentationService.display(exr, exec_ctx, FetchPresenter)
    except Exception as ex:
        error_trace(exception=sys.exc_info()).error(ex)
        die_with_error(ex, FetchPresenter, exec_ctx.options["format"])


@with_catch_log
def task_fetch(**kwargs: dict) -> ExecResponse:
    """Task impl"""

    if not (doc := kwargs.get("task", {})):
        raise ValueError("Wrong task format given.")

    _task = FetchTask(**doc)

    return call(
        FileContext.from_file(_task.file),
        ExecuteContext(
            options={"dump": True, "format": True},
            arguments=_task.arguments | {"variables": _task.variables},
        ),
    )
