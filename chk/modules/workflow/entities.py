"""
Entities for workflow
"""

from __future__ import annotations

import enum
import typing
from uuid import uuid4

from pydantic import BaseModel, Field, ConfigDict


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

    @staticmethod
    def from_dict(data: dict) -> ChkwareTask:
        """constractor"""

        if not data:
            raise AttributeError("ChkwareTask:from_dict Empty data given")

        return ChkwareTask(**data)


class ChkwareValidateTask(ChkwareTask):
    """Chkware validation task"""

    class ChkwareTaskDataArgument(BaseModel):
        """Chkware task data argument"""

        model_config = ConfigDict(extra="forbid")

        data: dict = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")

    arguments: ChkwareTaskDataArgument = Field(default_factory=ChkwareTaskDataArgument)

    @staticmethod
    def from_dict(data: dict) -> ChkwareValidateTask:
        """constructor"""

        if not data:
            raise AttributeError("ChkwareValidateTask:from_dict Empty data given")

        return ChkwareValidateTask(**data)
