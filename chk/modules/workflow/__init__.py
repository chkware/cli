"""
Workflow module
"""

from __future__ import annotations
from collections import abc
import pathlib

from hence import run_tasks, hence_config
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
            _task_params = {
                "task": _task_d,
                "execution_context": execution_ctx,
            }

            formatter(f"\nTask: {task.name}")

            match task.uses:
                case WorkflowUses.fetch.value:
                    task_executable_lst.append((task_fetch, _task_params))
                case WorkflowUses.validate.value:
                    task_executable_lst.append((task_validation, _task_params))

        run_tasks(task_executable_lst)
        ic(hence_config.context)


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
