"""
Driver to handle requests library (https://pypi.org/project/requests/)
"""
from __future__ import annotations
from collections import UserDict

import requests


class ApiResponse(UserDict):
    """Represent a response"""

    __slots__ = ("code", "info", "headers", "body")

    code: int
    info: str
    headers: dict
    body: str

    @property
    def as_fmt_str(self) -> str:
        """String representation of ApiResponse

        Returns:
            str: String representation
        """
        # set info
        presentation = f"{self['info']}\r\n\r\n"

        # set headers
        presentation += "\r\n".join(f"{k}: {v}" for k, v in self["headers"].items())
        presentation += "\r\n\r\n"

        # set body
        presentation += self["body"]

        return presentation

    @staticmethod
    def from_response(response: requests.Response) -> ApiResponse:
        """Create a ApiResponse object from requests.Response object

        Args:
            response (requests.Response): _description_

        Returns:
            ApiResponse: _description_
        """
        version = "HTTP/1.0" if response.raw.version == 10 else "HTTP/1.1"

        return ApiResponse(
            code=response.status_code,
            info=f"{version} {response.status_code} {response.reason}",
            headers=dict(response.headers),
            body=response.text,
        )


class BearerAuthentication(requests.auth.AuthBase):
    """Authentication: Bearer ... support"""

    def __init__(self, token: str) -> None:
        """Construct BearerAuthentication"""

        self.token = token

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        """Add the actual header on call"""

        r.headers["authorization"] = "Bearer " + self.token
        return r


def fetch(params: dict) -> ApiResponse:
    """Fetch an external resource

    Args:
        params (dict): all supported params from requests.request

    Returns:
        ApiResponse: a new ApiResponse
    """

    try:
        return ApiResponse.from_response(requests.request(**params))
    except requests.ConnectTimeout as err:
        raise RuntimeError("Connection time out") from err
    except requests.ConnectionError as err:
        raise RuntimeError("Connection error") from err
    except requests.ReadTimeout as err:
        raise RuntimeError("Read time out") from err
    except requests.TooManyRedirects as err:
        raise RuntimeError("Too many redirects") from err
    except requests.RequestException as err:
        raise RuntimeError("Request error") from err
