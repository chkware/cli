"""
Variable entities
"""
from json import loads, decoder
from dataclasses import dataclass, asdict


@dataclass
class ApiResponse:
    """
    Generic class to hold API response data and parsing
    """

    code: int
    version: str
    reason: str
    headers: list
    body: dict

    dict = asdict

    @staticmethod
    def from_dict(response: dict) -> "ApiResponse":
        """
        Convert response dict to ApiResponse
        """

        if code := response.get("code"):
            response["code"] = int(code)

        try:
            if body := response.get("body"):
                response["body"] = loads(body)
        except decoder.JSONDecodeError:
            SystemExit('`json` data not found')

        return ApiResponse(**response)
