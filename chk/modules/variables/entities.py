"""
Variable entities
"""
import json
from dataclasses import dataclass, asdict
from typing import NamedTuple, Self, Any

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

    def merged(self, doc: dict) -> dict:
        """Merge given doc with default one"""
        if not doc:
            doc = {}

        if doc == DefaultExposableDoc().doc:
            doc = {}

        return self.doc | doc


@dataclass
class ApiResponse:
    """Generic class to hold API response data and parsing"""

    code: int
    version: str
    reason: str
    headers: list
    body: dict

    @staticmethod
    def from_dict(response: dict) -> Self:
        """Convert response dict to ApiResponse"""

        def convert_json(string: str) -> Any:
            try:
                return json.loads(string)
            except json.decoder.JSONDecodeError as jde:
                raise TypeError("Not `json` data") from jde

        if (code := response["code"]) and not isinstance(code, int):
            response["code"] = int(code)

        try:
            if body := response.get("body"):
                if (
                    "Content-Type" in response["headers"]
                    and "application/json" in response["headers"]["Content-Type"]
                    and isinstance(body, str)
                ):
                    body = convert_json(body)

            response["body"] = body
        except TypeError as ex:
            raise RuntimeError(ex) from ex

        return ApiResponse(**response)

    dict = asdict
