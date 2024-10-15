"""
Entities for workflow
"""

from __future__ import annotations

import enum
from typing import NamedTuple

from pydantic import BaseModel, ConfigDict, Field

from chk.infrastructure.file_loader import ExecuteContext, generate_abs_path


class WorkflowConfigNode(enum.StrEnum):
    """WorkflowConfigNode"""

    NODE = "_steps"


class TaskExecParam(NamedTuple):
    """TaskExecParams"""

    task: ChkwareTask
    exec_ctx: ExecuteContext

    def as_dict(self) -> dict:
        """Convert to dict"""

        return {"task": self.task.model_dump(), "execution_context": self.exec_ctx}


class WorkflowUses(enum.StrEnum):
    """Types of Workflow Uses"""

    fetch = enum.auto()
    validate = enum.auto()


class ChkwareTask(BaseModel):
    """Chkware task"""

    model_config = ConfigDict(extra="forbid")

    name: str
    uses: str
    file: str
    variables: dict = Field(default_factory=dict)

    def __init__(self, basepath: str, /, **kwargs: dict) -> None:
        """Constructor"""

        if (
            "file" in kwargs
            and isinstance(kwargs["file"], str)
            and len(kwargs["file"]) != 0
        ):
            kwargs["file"] = generate_abs_path(basepath, kwargs["file"])

        super().__init__(**kwargs)


class ChkwareValidateTask(ChkwareTask):
    """Chkware validation task"""

    class ChkwareTaskDataArgument(BaseModel):
        """Chkware task data argument"""

        model_config = ConfigDict(extra="forbid")

        data: dict = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")

    arguments: ChkwareTaskDataArgument = Field(default_factory=ChkwareTaskDataArgument)

    def __init__(self, basepath: str, /, **kwargs: dict) -> None:
        """Constructor"""

        super().__init__(basepath, **kwargs)


class StepResult(BaseModel):
    """StepResult"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    task: ChkwareTask | ChkwareValidateTask
    is_success: bool
    others: dict = Field(default_factory=dict)
    exposed: dict = Field(default_factory=list)
    exception: Exception | None = Field(default=None)
