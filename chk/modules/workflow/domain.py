"""
Domain logics for workflow module
"""

import typing
from os.path import splitext

from pydantic import BaseModel, Field

from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import data_get

VERSION_SCOPE = ["workflow"]


class VersionedDocument(BaseModel):
    context: tuple = Field(default_factory=tuple)
    version: str = Field(default_factory=str)


class WorkflowDocument(VersionedDocument):
    """WorkflowDocument"""

    id: str = Field(default_factory=str)

    @staticmethod
    def from_file_context(ctx: FileContext) -> "WorkflowDocument":
        """Create a WorkflowDocument from FileContext"""

        if not (version_str := data_get(ctx.document, "version")):
            raise RuntimeError("`version:` not found.")

        id_str = data_get(ctx.document, "id", splitext(ctx.filepath)[0])

        if not (tasks_dct := data_get(ctx.document, "tasks")):
            raise RuntimeError("`tasks:` not found.")

        return WorkflowDocument(context=tuple(ctx), version=version_str, id=id_str)
