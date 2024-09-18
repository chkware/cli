"""View related utility mod"""

import abc
import typing

from pydantic import BaseModel


class PresentationBuilder(BaseModel, abc.ABC):
    """Presentable signature"""

    data: typing.Any

    @abc.abstractmethod
    def dump_fmt(self) -> None:
        """Signature to dump formatted string"""

        raise NotImplementedError("Signature to dump formatted string")

    @abc.abstractmethod
    def dump_json(self) -> str:
        """Signature to dump json"""

        raise NotImplementedError("Signature to dump json")
