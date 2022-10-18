"""
Variable entities
"""
from json import loads, decoder
from dataclasses import dataclass, asdict
from typing import NamedTuple

from chk.modules.variables.constants import VariableConfigNode as VConst


class DefaultVariableDoc(NamedTuple):
    """Default variable doc"""

    doc: dict[str, object] = {
        VConst.ROOT: {},
    }

    def merged(self, doc: dict) -> dict:
        """Merge given doc with default one"""
        if not doc:
            doc = {}

        return self.doc | doc


class DefaultReturnableDoc(NamedTuple):
    """Default return-able doc"""

    doc: dict[str, object] = {
        VConst.RETURN: None,
    }


class DefaultExposableDoc(NamedTuple):
    """Default expose-able doc"""

    doc: dict[str, object] = {
        VConst.EXPOSE: None,
    }


@dataclass
class ApiResponse:
    """Generic class to hold API response data and parsing"""

    code: int
    version: str
    reason: str
    headers: list
    body: dict

    @staticmethod
    def from_dict(response: dict) -> "ApiResponse":
        """Convert response dict to ApiResponse"""

        if code := response.get("code"):
            response["code"] = int(code)

        try:
            if body := response.get("body"):
                response["body"] = loads(body)
        except decoder.JSONDecodeError:
            SystemExit("`json` data not found")

        return ApiResponse(**response)

    dict = asdict
