"""
Workflow module
"""

from __future__ import annotations

import json
import pathlib
from collections import abc
from collections.abc import Callable

from pydantic import BaseModel, ConfigDict, Field

from chk.infrastructure.document import (
    VersionedDocumentV2,
)
from chk.infrastructure.file_loader import ExecuteContext, FileContext
from chk.infrastructure.helper import data_get, slugify
from chk.infrastructure.symbol_table import (
    ExecResponse,
    ExposeManager,
    VariableTableManager,
    Variables,
    replace_value,
)
from chk.infrastructure.version import DocumentVersionMaker
from chk.infrastructure.view import PresentationService
from chk.modules.fetch import task_fetch
from chk.modules.validate import task_validation
from chk.modules.workflow.entities import (
    ChkwareTask,
    ChkwareValidateTask,
    StepResult,
    TaskExecParam,
    WorkflowConfigNode,
    WorkflowUses,
)
from chk.modules.workflow.services import ChkwareTaskSupport, WorkflowPresenter

VERSION_SCOPE = ["workflow"]


class WorkflowDocument(VersionedDocumentV2, BaseModel):
    """WorkflowDocument"""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(default_factory=str)
    id: str = Field(default_factory=str)
    tasks: list[dict] = Field(default="")

    @staticmethod
    def from_file_context(ctx: FileContext) -> WorkflowDocument:
        """Create a WorkflowDocument from FileContext"""

        # version
        doc_ver = DocumentVersionMaker.from_dict(ctx.document)
        DocumentVersionMaker.verify_if_allowed(doc_ver, VERSION_SCOPE)

        # id, name
        # @TODO Name and ID processing should have separate func
        if name_str := data_get(ctx.document, "name"):
            name_str = str(name_str).strip()

        if id_str := data_get(ctx.document, "id"):
            id_str = slugify(str(id_str).strip())
        else:
            id_str = (
                slugify(name_str)
                if name_str and len(name_str) > 0
                else pathlib.Path(ctx.filepath).stem
            )

        if not name_str:
            name_str = id_str

        # tasks
        if not (tasks_lst := data_get(ctx.document, "tasks")):
            raise RuntimeError("`tasks:` not found.")

        if not isinstance(tasks_lst, list):
            raise RuntimeError("`tasks:` is not list.")

        # @TODO keep `context`, `version` as object
        # @TODO implement __repr__ for WorkflowDocument
        return WorkflowDocument(
            context=tuple(ctx),
            version=str(doc_ver),
            name=name_str,
            id=id_str,
            tasks=tasks_lst,
        )


class WorkflowDocumentSupport:
    """Workflow document support"""

    @classmethod
    def _prepare_validate_task_argument_data_(cls, task: ChkwareTask) -> dict:
        """Prepare data for ChkwareValidateTask.arguments.data"""

        if isinstance(task, ChkwareValidateTask) and task.arguments:
            return task.arguments.data

        return {}

    @classmethod
    def set_step_template(cls, variables: Variables) -> None:
        """sets data or template"""

        # @TODO implement data set functionality with validation for variables
        variables[WorkflowConfigNode.NODE.value] = []

    @classmethod
    def process_task_template(
        cls, document: WorkflowDocument, variables: Variables
    ) -> list:
        """Process task block of document"""

        base_fpath: str = FileContext(*document.context).filepath
        exec_report: list[StepResult] = []

        for task in document.tasks:
            if not isinstance(task, dict):
                raise RuntimeError("`tasks.*.item` should be map.")

            # replace values in tasks
            task_d_: dict = replace_value(task, variables.data)
            task_o_ = ChkwareTaskSupport.make_task(
                task_d_, **dict(base_file_path=base_fpath)
            )

            exctx_args = {"variables": json.dumps(task_o_.variables)}

            if isinstance(task_o_, ChkwareValidateTask):
                exctx_args["arguments"] = task_o_.arguments.model_dump_json()

            execution_ctx = ExecuteContext({"dump": True, "format": True}, exctx_args)

            task_fn = None

            match task_o_.uses:
                case WorkflowUses.fetch.value:
                    task_fn = task_fetch
                case WorkflowUses.validate.value:
                    task_fn = task_validation

            if task_fn:
                te_param = TaskExecParam(task=task_o_, exec_ctx=execution_ctx)
                task_resp: ExecResponse = cls.execute_task(task_fn, te_param, variables)

                exec_report.append(
                    StepResult(
                        task=task_o_,
                        is_success=task_resp.report.pop("is_success"),
                        others=task_resp.report,
                        exposed=task_resp.exposed,
                    )
                )

        return exec_report

    @classmethod
    def execute_task(
        cls, task_fn: Callable, task_params: TaskExecParam, variables: Variables
    ) -> ExecResponse:
        """execute_task"""

        _task_res: ExecResponse = task_fn(**task_params.as_dict())
        variables[WorkflowConfigNode.NODE.value].append(_task_res.exposed)

        return _task_res


def call(file_ctx: FileContext, exec_ctx: ExecuteContext) -> ExecResponse:
    """Call a workflow document"""

    wflow_doc = WorkflowDocument.from_file_context(file_ctx)

    variable_doc = Variables()
    VariableTableManager.handle(variable_doc, wflow_doc, exec_ctx)

    service = WorkflowDocumentSupport()
    # @TODO make sure the document do not call self making it repeating
    service.set_step_template(variable_doc)

    r_exception: Exception | None = None
    try:
        exec_report = service.process_task_template(wflow_doc, variable_doc)
    except Exception as ex:
        r_exception = ex

    output_data = Variables({"_steps": variable_doc[WorkflowConfigNode.NODE.value]})

    exposed_data: dict = ExposeManager.get_exposed_replaced_data(
        wflow_doc, variable_doc.data
    )

    # TODO also send failed_details (fail code, message, stacktrace, etc)
    return ExecResponse(
        file_ctx=file_ctx,
        exec_ctx=exec_ctx,
        variables=variable_doc,
        variables_exec=output_data,
        extra=exec_report,
        exposed=exposed_data,
        exception=r_exception,
    )


def execute(
    ctx: FileContext, exec_ctx: ExecuteContext, cb: abc.Callable = lambda *args: ...
) -> None:
    """Run a workflow document

    Args:
        ctx: FileContext object to handle
        exec_ctx: ExecuteContext
        cb: Callable
    """

    exr = call(file_ctx=ctx, exec_ctx=exec_ctx)

    cb({ctx.filepath_hash: exr.variables_exec.data})
    PresentationService.display(exr, exec_ctx, WorkflowPresenter)
