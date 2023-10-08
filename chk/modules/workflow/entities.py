"""
Entities for workflow
"""
import enum
import typing

from pydantic import BaseModel, Field


class ChkwareTask(BaseModel):
    """Chkware task"""

    uses: str
    file: str
    variables: dict = Field(default_factory=dict)

    @staticmethod
    def from_dict(data: dict) -> "ChkwareTask":
        """constractor"""

        if not data:
            raise AttributeError("ChkwareTask:from_dict Empty data given")

        return ChkwareTask(**data)


class ChkwareValidateTask(ChkwareTask):
    """Chkware validation task"""

    class ChkwareTaskDataArgument(BaseModel):
        """Chkware task data argument"""

        data: dict

    arguments: typing.Optional[ChkwareTaskDataArgument] = Field(default=None)

    @staticmethod
    def from_dict(data: dict) -> "ChkwareValidateTask":
        """constractor"""

        if not data:
            raise AttributeError("ChkwareValidateTask:from_dict Empty data given")

        return ChkwareValidateTask(**data)
