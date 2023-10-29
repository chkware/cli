"""
Domain logics for workflow module
"""
from __future__ import annotations
import pathlib

from pydantic import Field

from chk.infrastructure.document import VersionedDocumentV2 as VersionedDocument
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import data_get
from chk.infrastructure.symbol_table import Variables
from chk.modules.workflow.entities import ChkwareTask, ChkwareValidateTask, ParsedTask

VERSION_SCOPE = ["workflow"]


class WorkflowDocument(VersionedDocument):
    """WorkflowDocument"""

    id: str = Field(default_factory=str)
    tasks: list[ChkwareTask | ChkwareValidateTask]

    @staticmethod
    def from_file_context(ctx: FileContext) -> WorkflowDocument:
        """Create a WorkflowDocument from FileContext"""

        if not (version_str := data_get(ctx.document, "version")):
            raise RuntimeError("`version:` not found.")

        id_str = data_get(ctx.document, "id", pathlib.Path(ctx.filepath).stem)

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
            context=tuple(ctx), version=version_str, id=id_str, tasks=tasks
        )


class WorkflowDocumentSupport:
    """Workflow document support"""

    @classmethod
    def process_task_template(
        cls, document: WorkflowDocument, variables: Variables
    ) -> None:
        ...
