"""
Fetch module entities
"""

from __future__ import annotations

import enum
import json
from collections import abc
from typing import Any

import requests
import xmltodict
from defusedxml.minidom import parseString
from pydantic import BaseModel, Field, model_serializer, computed_field

from chk.infrastructure.document import VersionedDocumentV2
from chk.infrastructure.helper import Cast

VERSION_SCOPE = ["http"]
Http_V10 = "HTTP/1.0"
Http_V11 = "HTTP/1.1"
CTYPE_JSON = "application/json"
CTYPE_XML = "application/xml"


class HttpMethod(enum.StrEnum):
    """Constants of wellknown http methods"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class RequestConfigNode(enum.StrEnum):
    """represent request config section"""

    ROOT = "request"
    LOCAL = "_response"

    # common request
    URL = enum.auto()
    METHOD = enum.auto()
    HEADERS = enum.auto()
    PARAMS = "url_params"

    # Basic
    AUTH_BA = "auth[basic]"
    AUTH_BA_USR = "username"
    AUTH_BA_PAS = "password"

    # Bearer
    AUTH_BE = "auth[bearer]"
    AUTH_BE_TOK = "token"

    # Body
    BODY_FRM = "body[form]"
    BODY_FRM_DAT = "body[form-data]"
    BODY_JSN = "body[json]"
    BODY_XML = "body[xml]"
    BODY_TXT = "body[text]"


SCHEMA = {
    RequestConfigNode.ROOT: {
        "required": True,
        "type": "dict",
        "schema": {
            RequestConfigNode.URL: {
                "required": True,
                "empty": False,
                "type": "string",
            },
            RequestConfigNode.METHOD: {
                "required": True,
                "type": "string",
            },
            RequestConfigNode.PARAMS: {
                "required": False,
                "empty": False,
                "type": "dict",
            },
            RequestConfigNode.HEADERS: {
                "required": False,
                "empty": False,
                "type": "dict",
            },
            RequestConfigNode.AUTH_BA: {
                "required": False,
                "empty": False,
                "type": "dict",
                "excludes": RequestConfigNode.AUTH_BE,
            },
            RequestConfigNode.AUTH_BE: {
                "required": False,
                "empty": False,
                "type": "dict",
                "excludes": RequestConfigNode.AUTH_BA,
            },
            RequestConfigNode.BODY_FRM: {
                "required": False,
                "empty": False,
                "type": "dict",
                "excludes": [
                    RequestConfigNode.BODY_FRM_DAT,
                    RequestConfigNode.BODY_JSN,
                    RequestConfigNode.BODY_XML,
                    RequestConfigNode.BODY_TXT,
                ],
            },
            RequestConfigNode.BODY_FRM_DAT: {
                "required": False,
                "empty": False,
                "type": "dict",
                "excludes": [
                    RequestConfigNode.BODY_FRM,
                    RequestConfigNode.BODY_JSN,
                    RequestConfigNode.BODY_XML,
                    RequestConfigNode.BODY_TXT,
                ],
            },
            RequestConfigNode.BODY_JSN: {
                "required": False,
                "empty": False,
                "type": "dict",
                "excludes": [
                    RequestConfigNode.BODY_FRM,
                    RequestConfigNode.BODY_FRM_DAT,
                    RequestConfigNode.BODY_XML,
                    RequestConfigNode.BODY_TXT,
                ],
            },
            RequestConfigNode.BODY_XML: {
                "required": False,
                "empty": False,
                "type": "string",
                "excludes": [
                    RequestConfigNode.BODY_FRM,
                    RequestConfigNode.BODY_FRM_DAT,
                    RequestConfigNode.BODY_JSN,
                    RequestConfigNode.BODY_TXT,
                ],
            },
            RequestConfigNode.BODY_TXT: {
                "required": False,
                "empty": False,
                "type": "string",
                "excludes": [
                    RequestConfigNode.BODY_FRM,
                    RequestConfigNode.BODY_FRM_DAT,
                    RequestConfigNode.BODY_JSN,
                    RequestConfigNode.BODY_XML,
                ],
            },
        },
    }
}


class ApiResponseModel(BaseModel):
    """ApiResponseModel"""

    code: int = Field(default=0)
    version: int = Field(default_factory=int)
    reason: str = Field(default_factory=str)
    headers: dict[str, str] = Field(default_factory=dict)
    body: str = Field(default_factory=str)

    def __bool__(self) -> bool:
        """implement __bool__"""
        return self.code != 0 and self.version in (10, 11) and len(self.reason) > 0

    @computed_field  # type: ignore
    @property
    def info(self) -> str:
        return (
            f"{Http_V10 if self.version == 10 else Http_V11} {self.code} {self.reason}"
        )

    @computed_field  # type: ignore
    @property
    def body_content_type(self) -> str:
        if "Content-Type" in self.headers:
            content_type = self.headers["Content-Type"]
        elif "content-type" in self.headers:
            content_type = self.headers["content-type"]

        if CTYPE_JSON in content_type:
            return CTYPE_JSON
        elif CTYPE_XML in content_type:
            return CTYPE_XML
        else:
            raise ValueError("Non-convertable body found")

    @info.setter  # type: ignore
    def set_info(self, sinfo: str) -> None:
        """set info"""

        if not sinfo:
            raise ValueError("Info can not be empty.")

        _version, _, _reason = sinfo.split()

        if Http_V10 == _version:
            self.version = 10
        elif Http_V11 == _version:
            self.version = 11
        else:
            raise ValueError("Unsupported protocol.")

        self.reason = _reason

    def body_as_dict(self) -> abc.Iterable:
        if CTYPE_JSON == self.body_content_type:
            return json.loads(self.body)
        elif CTYPE_XML == self.body_content_type:
            return xmltodict.parse(parseString(self.body).toxml())
        else:
            raise ValueError("Non-convertable body found")

    @model_serializer
    def mdl_serializer(self) -> dict[str, Any]:
        _dict = {
            "code": self.code,
            "info": self.info,
            "headers": self.headers,
        }

        try:
            _dict["body"] = self.body_as_dict()
        except (TypeError, ValueError):
            _dict["body"] = self.body

        return _dict

    @staticmethod
    def from_response(response: requests.Response) -> ApiResponseModel:
        """Create a ApiResponseModel object from requests.Response object

        Args:
            response (requests.Response): _description_

        Returns:
            ApiResponseModel: _description_
        """

        arm = ApiResponseModel(
            code=response.status_code,
            version=11 if response.raw.version == 0 else response.raw.version,
            reason=response.reason,
            headers=dict(response.headers),
            body=response.text,
        )

        if arm:
            arm.body_content_type

        return arm

    @staticmethod
    def from_dict(**kwargs: dict) -> ApiResponseModel:
        """Construct from dict"""

        if not all(
            [item in kwargs.keys() for item in ["code", "info", "headers", "body"]]
        ):
            raise KeyError("Expected keys to make ApiResponseModel not found")

        if not isinstance(kwargs["code"], int):
            raise ValueError("Invalid code.")

        if not isinstance(kwargs["headers"], dict):
            raise ValueError("Invalid headers.")

        if "Content-Type" in kwargs["headers"]:
            content_type = kwargs["headers"]["Content-Type"]
        elif "content-type" in kwargs["headers"]:
            content_type = kwargs["headers"]["content-type"]

        if CTYPE_JSON in content_type:
            _body = json.dumps(kwargs["body"])
        elif CTYPE_XML in content_type:
            _body = parseString(kwargs["body"]).toxml()
        else:
            raise ValueError("Non-convertable body found")

        model = ApiResponseModel(
            code=Cast.to_int(kwargs["code"]),
            headers=kwargs["headers"],
            body=_body,
        )
        model.info = kwargs["info"]

        return model

    def as_fmt_str(self) -> str:
        """String representation of ApiResponseModel

        Returns:
            str: String representation
        """

        # set info
        presentation = f"{self.info}\r\n\r\n"

        # set headers
        presentation += "\r\n".join(f"{k}: {v}" for k, v in self.headers.items())
        presentation += "\r\n\r\n"

        presentation += (
            json.dumps(self.body_as_dict())
            if self.body_content_type == CTYPE_JSON
            else self.body
        )

        return presentation


class BearerAuthentication(requests.auth.AuthBase):
    """Authentication: Bearer ... support"""

    def __init__(self, token: str) -> None:
        """Construct BearerAuthentication"""

        self.token = token

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        """Add the actual header on call"""

        r.headers["authorization"] = "Bearer " + self.token
        return r


class HttpDocument(VersionedDocumentV2, BaseModel):
    """
    Http document entity
    """

    request: dict = Field(default_factory=dict)

    def __bool__(self) -> bool:
        """Check is the document is empty"""

        return len(self.request) > 0


class FetchTask(BaseModel):
    """Parsed FetchTask"""

    name: str
    uses: str
    file: str
    variables: dict = Field(default_factory=dict)
    arguments: dict = Field(default_factory=dict)
