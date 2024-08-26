"""
Workflow module
"""

from __future__ import annotations
from collections import abc
import pathlib
from uuid import uuid4

from hence import run_tasks, _context, Utils
from pydantic import Field, ConfigDict
from icecream import ic

from chk.infrastructure.document import VersionedDocumentV2 as VersionedDocument
from chk.modules.fetch import task_fetch
from chk.modules.validate import task_validation
from chk.modules.workflow.entities import (
    ChkwareTask,
    ChkwareValidateTask,
    WorkflowUses,
)
from chk.infrastructure.file_loader import (
    FileContext,
    ExecuteContext,
    generate_abs_path,
)
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

        # @TODO this should to VersionDoc
        # version
        if not (version_str := data_get(ctx.document, "version")):
            raise RuntimeError("`version:` not found.")

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

        tasks = []
        for task in tasks_lst:
            # @TODO can this be done in ParsedTask class
            if not isinstance(task, dict):
                raise RuntimeError("`tasks.*.item` should be map.")

            if "uses" in task:
                if task["uses"] == "fetch":
                    tasks.append(ChkwareTask.from_dict(task))
                elif task["uses"] == "validate":
                    tasks.append(ChkwareValidateTask.from_dict(task))
            else:
                raise RuntimeError("Malformed task item found.")

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

        base_filepath: str = FileContext(*document.context).filepath
        task_executable_lst = []

        for task in document.tasks:
            ic(task)
            _task_d = task.model_dump()
            _task_d["file"] = generate_abs_path(base_filepath, task.file)

            execution_ctx = ExecuteContext(
                {"dump": True, "format": True},
                {
                    # "variables": combine_initial_variables(
                    #     variables,
                    #     except_msg="-V, --variables accept values as JSON object",
                    # ),
                },
            )
            ic(_task_d)

            formatter(f"\nTask: {_task_d['name']}")

            _task_params = {"task": _task_d, "execution_context": execution_ctx}
            match _task_d["uses"]:
                case WorkflowUses.fetch.value:
                    task_executable_lst.append(
                        (task_fetch, _task_params)
                    )
                case WorkflowUses.validate.value:
                    task_executable_lst.append(
                        (task_validation, _task_params)
                    )

        task_executable_keys = run_tasks(task_executable_lst, str(uuid4()))
        # ic(task_executable_keys)
        # ic(_context.context.get())

        for tx_key in task_executable_keys:
            f_task_ = Utils.get_task(tx_key)
            ic(f_task_.result)

        # match task.uses:
        #     case WorkflowUses.fetch.value:
        #         task_executable_lst.append((task_fetch, {"file": target_file_path, "execution_context": execution_ctx}))
        #         exec_resp = fetch.call(file_ctx, execution_ctx)
        #
        #         __method = data_get(exec_resp.file_ctx.document, "request.method")
        #         __url = data_get(exec_resp.file_ctx.document, "request.url")
        #
        #         formatter(f"-> {__method} {__url}")
        #
        #     case WorkflowUses.validate.value:
        #         execution_ctx.arguments["data"] = (
        #             cls._prepare_validate_task_argument_data_(task)
        #         )
        #
        #         exec_resp = validate.call(file_ctx, execution_ctx)
        #
        #         __count_all = data_get(
        #             exec_resp.variables_exec.data, "_asserts_response.count_all"
        #         )
        #         __count_fail = data_get(
        #             exec_resp.variables_exec.data, "_asserts_response.count_fail"
        #         )
        #
        #         formatter(f"-> Total tests: {__count_all}, Failed: {__count_fail}")


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
