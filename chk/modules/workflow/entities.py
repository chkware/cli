"""
Entities for workflow
"""
from __future__ import annotations
import typing

from pydantic import BaseModel, Field, ConfigDict


class ParsedTask(BaseModel):
    """Parsed tasks"""

    name: str
    uses: str
    file: str
    variables: dict = Field(default_factory=dict)
    arguments: dict = Field(default=None)


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

    @staticmethod
    def from_parsed_task(task: ParsedTask) -> ChkwareTask:
        """Create new instance from ParsedTask"""

        return ChkwareTask(
            name=task.name, uses=task.uses, file=task.file, variables=task.variables
        )


class ChkwareValidateTask(ChkwareTask):
    """Chkware validation task"""

    class ChkwareTaskDataArgument(BaseModel):
        """Chkware task data argument"""

        model_config = ConfigDict(extra="forbid")

        data: dict

    model_config = ConfigDict(extra="forbid")

    arguments: typing.Optional[ChkwareTaskDataArgument] = Field(default=None)

    @staticmethod
    def from_dict(data: dict) -> ChkwareValidateTask:
        """constractor"""

        if not data:
            raise AttributeError("ChkwareValidateTask:from_dict Empty data given")

        return ChkwareValidateTask(**data)

    @staticmethod
    def from_parsed_task(task: ParsedTask) -> ChkwareValidateTask:
        """Create new instance from ParsedTask"""

        return ChkwareValidateTask.from_dict(task.model_dump())