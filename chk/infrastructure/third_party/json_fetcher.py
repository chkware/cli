"""
JSON data fetcher
"""
import json
from collections import UserDict

from chk.infrastructure.third_party.http_fetcher import ApiResponse, fetch


class JsonApiResponse(UserDict):
    """JsonApiResponse"""

    __slots__ = ("code", "info", "headers", "body")

    code: int
    info: str
    headers: dict
    body: str

    @staticmethod
    def from_api_response(resp: ApiResponse) -> "JsonApiResponse":
        """Create JsonApiResponse from ApiResponse
        Args:
            resp (ApiResponse): ApiResponse object
        """
        try:
            return JsonApiResponse(
                code=resp["code"],
                info=resp["info"],
                headers=resp["headers"],
                body=json.loads(resp["body"]),
            )
        except Exception as ex:
            raise RuntimeError("response not json") from ex


def fetch_json(params: dict) -> JsonApiResponse:
    return JsonApiResponse.from_api_response(fetch(params))
