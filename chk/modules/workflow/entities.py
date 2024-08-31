"""
Entities for workflow
"""

from __future__ import annotations

import enum
from pydantic import BaseModel, Field, ConfigDict

from chk.infrastructure.file_loader import generate_abs_path


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

        if isinstance(kwargs["file"], str) and len(kwargs["file"]) != 0:
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
