"""View related utility mod"""

import abc
import sys
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

    @abc.abstractmethod
    def dump_error_fmt(self, err: object = None) -> str:
        """Signature to dump formatted error string"""

        raise NotImplementedError("Signature to dump formatted error string")

    @abc.abstractmethod
    def dump_error_json(self, err: object = None) -> str:
        """Signature to dump error json"""

        raise NotImplementedError("Signature to dump error json")


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
            if ex_resp.exception:
                formatter(wfp.dump_error_fmt(), dump=exec_ctx.options["dump"])
            else:
                formatter(wfp.dump_fmt(), dump=exec_ctx.options["dump"])
        else:
            if ex_resp.exception:
                formatter(wfp.dump_error_json(), dump=exec_ctx.options["dump"])
            else:
                formatter(wfp.dump_json(), dump=exec_ctx.options["dump"])


def die_with_error(
    err: Exception, Presenter: type[PresentationBuilder], is_fmt: bool
) -> None:
    """die_with_error"""

    prs = Presenter(data=None)

    formatter(
        prs.dump_error_fmt(err) if is_fmt else prs.dump_error_json(err),
        dump=True,
        is_err=True,
    )

    sys.exit(1)
