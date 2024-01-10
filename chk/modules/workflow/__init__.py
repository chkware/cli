"""
Workflow module
"""

from __future__ import annotations
from collections import abc
import pathlib

from pydantic import Field, ConfigDict
from icecream import ic

from chk.infrastructure.document import VersionedDocumentV2 as VersionedDocument
from chk.modules import validate, fetch
from chk.modules.workflow.entities import (
    ChkwareTask,
    ChkwareValidateTask,
    ParsedTask,
    WorkflowUses,
)
from chk.infrastructure.file_loader import FileContext, ExecuteContext, PathFrom
from chk.infrastructure.helper import data_get, formatter, slugify
from chk.infrastructure.symbol_table import Variables, VariableTableManager


VERSION_SCOPE = ["workflow"]


class WorkflowDocument(VersionedDocument):
    """WorkflowDocument"""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(default_factory=str)
    id: str = Field(default_factory=str)
    tasks: list[ChkwareTask | ChkwareValidateTask]

    @staticmethod
    def from_file_context(ctx: FileContext) -> WorkflowDocument:
        """Create a WorkflowDocument from FileContext"""

        # version
        if not (version_str := data_get(ctx.document, "version")):
            raise RuntimeError("`version:` not found.")

        # id, name
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

        tasks = []
        for task in tasks_lst:
            if not isinstance(task, dict):
                raise RuntimeError("`tasks.*.item` should be map.")

            parsed_task = ParsedTask(**task)

            match parsed_task.uses:
                case "fetch":
                    tasks.append(ChkwareTask.from_parsed_task(parsed_task))
                case "validate":
                    tasks.append(ChkwareValidateTask.from_parsed_task(parsed_task))

        return WorkflowDocument(
            context=tuple(ctx),
            version=version_str,
            name=name_str,
            id=id_str,
            tasks=tasks,
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
    def process_task_template(
        cls, document: WorkflowDocument, variables: Variables
    ) -> None:
        formatter(f"\n\nExecuting: {document.name}")
        formatter("-" * len(f"Executing: {document.name}"))

        for task in document.tasks:
            fcx = FileContext(*document.context)
            file_path = PathFrom(pathlib.Path(fcx.filepath))
            file_ctx: FileContext = FileContext.from_file(file_path.absolute(task.file))

            del fcx, file_path

            execution_ctx = ExecuteContext(
                {"dump": True, "format": True},
                {
                    # "variables": combine_initial_variables(
                    #     variables,
                    #     except_msg="-V, --variables accept values as JSON object",
                    # ),
                },
            )
            formatter(f"\nTask: {task.name}")

            match task.uses:
                case WorkflowUses.fetch.value:
                    exec_resp = fetch.call(file_ctx, execution_ctx)

                    __method = data_get(exec_resp.file_ctx.document, "request.method")
                    __url = data_get(exec_resp.file_ctx.document, "request.url")

                    formatter(f"-> {__method} {__url}")

                case WorkflowUses.validate.value:
                    execution_ctx.arguments[
                        "data"
                    ] = cls._prepare_validate_task_argument_data_(task)

                    exec_resp = validate.call(file_ctx, execution_ctx)

                    __count_all = data_get(
                        exec_resp.variables_exec.data, "_asserts_response.count_all"
                    )
                    __count_fail = data_get(
                        exec_resp.variables_exec.data, "_asserts_response.count_fail"
                    )

                    formatter(f"-> Total tests: {__count_all}, Failed: {__count_fail}")


def execute(
    ctx: FileContext, exec_ctx: ExecuteContext, cb: abc.Callable = lambda *args: ...
) -> None:
    """Run a workflow document

    Args:
        ctx: FileContext object to handle
        exec_ctx: ExecuteContext
        cb: Callable
    """

    wflow_doc = WorkflowDocument.from_file_context(ctx)
    ic(wflow_doc)

    variable_doc = Variables()
    VariableTableManager.handle(variable_doc, wflow_doc, exec_ctx)

    service = WorkflowDocumentSupport()
    service.process_task_template(wflow_doc, variable_doc)

    # DocumentVersionMaker.verify_if_allowed(
    #     DocumentVersionMaker.from_dict(wflow_doc.as_dict), VERSION_SCOPE
    # )

    # VersionedDocumentSupport.validate_with_schema(
    #     HttpDocumentSupport.build_schema(), http_doc
    # )
