"""View related utility mod"""

import abc
import typing

from pydantic import BaseModel

from chk.infrastructure.file_loader import ExecuteContext
from chk.infrastructure.helper import formatter
from chk.infrastructure.symbol_table import ExecResponse


class PresentationBuilder(BaseModel, abc.ABC):
    """Presentable signature"""

    data: typing.Any

    @abc.abstractmethod
    def dump_fmt(self) -> str:
        """Signature to dump formatted string"""

        raise NotImplementedError("Signature to dump formatted string")

    @abc.abstractmethod
    def dump_json(self) -> str:
        """Signature to dump json"""

        raise NotImplementedError("Signature to dump json")


class PresentationService:
    """Comment service for presentation"""

    @classmethod
    def display(
        cls,
        ex_resp: ExecResponse,
        exec_ctx: ExecuteContext,
        presenter: type[PresentationBuilder],
    ) -> None:
        wfp = presenter(data=ex_resp)
        if exec_ctx.options["format"]:
            formatter(wfp.dump_fmt(), dump=exec_ctx.options["dump"])
        else:
            formatter(wfp.dump_json(), dump=exec_ctx.options["dump"])
