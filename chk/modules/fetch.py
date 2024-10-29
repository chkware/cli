"""
Fetch module
"""

from __future__ import annotations

import enum
import json
import pathlib
from collections import abc
from typing import Any
from urllib.parse import unquote, urlparse

import requests
import xmltodict
from defusedxml.minidom import parseString
from pydantic import BaseModel, Field, computed_field, model_serializer
from requests.auth import HTTPBasicAuth

from chk.infrastructure.document import (
    VersionedDocumentSupport,
    VersionedDocumentV2,
)
from chk.infrastructure.file_loader import ExecuteContext, FileContext
from chk.infrastructure.helper import Cast, data_get
from chk.infrastructure.logging import debug, error, with_catch_log
from chk.infrastructure.symbol_table import (
    EXPOSE_SCHEMA as EXP_SCHEMA,
    ExecResponse,
    ExposeManager,
    VARIABLE_SCHEMA as VAR_SCHEMA,
    VariableTableManager,
    Variables,
    replace_value,
)
from chk.infrastructure.version import DocumentVersionMaker, SCHEMA as VER_SCHEMA
from chk.infrastructure.view import PresentationBuilder, PresentationService

VERSION_SCOPE = ["http"]
Http_V10 = "HTTP/1.0"
Http_V11 = "HTTP/1.1"
CTYPE_JSON = "application/json"
CTYPE_XML = "application/xml"


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

    @computed_field  # type: ignore[prop-decorator]
    @property
    def info(self) -> str:
        return (
            f"{Http_V10 if self.version == 10 else Http_V11} {self.code} {self.reason}"
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def body_content_type(self) -> str:
        if "Content-Type" in self.headers:
            content_type = self.headers["Content-Type"]
        elif "content-type" in self.headers:
            content_type = self.headers["content-type"]
        else:
            raise TypeError("Unsupported content type.")

        if CTYPE_JSON in content_type:
            return CTYPE_JSON
        elif CTYPE_XML in content_type:
            return CTYPE_XML
        else:
            raise ValueError("Non-convertable body found")

    @info.setter
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

        return ApiResponseModel(
            code=response.status_code,
            version=11 if response.raw.version == 0 else response.raw.version,
            reason=response.reason,
            headers=dict(response.headers),
            body=response.text,
        )

    @staticmethod
    def from_dict(**kwargs: dict) -> ApiResponseModel:
        """Construct from dict"""

        if not all(
            [item in kwargs.keys() for item in ["code", "info", "headers", "body"]]
        ):
            raise KeyError("Expected keys to make ApiResponseModel not found")

        if not isinstance(kwargs["code"], str):
            raise ValueError("Invalid code.")

        if not isinstance(kwargs["headers"], dict):
            raise ValueError("Invalid headers.")

        if "Content-Type" in kwargs["headers"]:
            content_type = kwargs["headers"]["Content-Type"]
        elif "content-type" in kwargs["headers"]:
            content_type = kwargs["headers"]["content-type"]
        else:
            raise TypeError("Unsupported content type.")

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
    AUTH_BA = "auth .scm=basic"
    AUTH_BA_USR = "username"
    AUTH_BA_PAS = "password"

    # Bearer
    AUTH_BE = "auth .scm=bearer"
    AUTH_BE_TOK = "token"

    # Body
    BODY_FRM = "body .enc=form"
    BODY_FRM_DAT = "body .enc=form-data"
    BODY_JSN = "body .enc=json"
    BODY_XML = "body .enc=xml"
    BODY_TXT = "body .enc=text"


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


def allowed_method(value: str) -> bool:
    """Validate if given method is allowed

    Raises:
        ValueError: When unsupported method found
    """

    if value not in set(method for method in HttpMethod):
        raise ValueError("Unsupported method")

    return True


def allowed_url(value: str) -> bool:
    """Validate if given URL is allowed"""

    parsed_url = urlparse(value)

    if all([parsed_url.scheme, parsed_url.netloc]) is False:
        raise ValueError("Invalid `url`")

    if parsed_url.scheme not in ["http", "https"]:
        raise ValueError("Invalid `url` scheme. http and https allowed")

    return True


class FetchTask(BaseModel):
    """Parsed FetchTask"""

    name: str
    uses: str
    file: str
    variables: dict = Field(default_factory=dict)
    arguments: dict = Field(default_factory=dict)


class HttpRequestArgCompiler:
    """HttpRequestArgCompiler"""

    @staticmethod
    def add_url_and_method(request_data: dict, request_arg: dict) -> None:
        """add default request url and request method"""
        if RequestConfigNode.METHOD not in request_data:
            raise KeyError("required key `method:` not found")

        if allowed_method(request_data[RequestConfigNode.METHOD]):
            request_arg["method"] = request_data.get(RequestConfigNode.METHOD)

        if RequestConfigNode.URL not in request_data:
            raise KeyError("required key `url:` not found")

        if allowed_url(request_data[RequestConfigNode.URL]):
            request_arg["url"] = request_data.get(RequestConfigNode.URL)

    @staticmethod
    def add_query_string(request_data: dict, request_arg: dict) -> None:
        """add query string"""
        if (params := request_data.get(RequestConfigNode.PARAMS)) is not None:
            request_arg["params"] = params

    @staticmethod
    def add_headers(request_data: dict, request_arg: dict) -> None:
        """add custom header"""
        if (headers := request_data.get(RequestConfigNode.HEADERS)) is not None:
            request_arg["headers"] = headers

    @staticmethod
    def add_authorization(request_data: dict, request_arg: dict) -> None:
        """handle authorization header"""
        # handle basic auth
        if (tag_ba := request_data.get(RequestConfigNode.AUTH_BA)) is not None:
            request_arg["auth"] = HTTPBasicAuth(
                tag_ba.get(RequestConfigNode.AUTH_BA_USR),
                tag_ba.get(RequestConfigNode.AUTH_BA_PAS),
            )

        # handle bearer auth
        if (tag_be := request_data.get(RequestConfigNode.AUTH_BE)) is not None:
            request_arg["auth"] = BearerAuthentication(
                tag_be.get(RequestConfigNode.AUTH_BE_TOK)
            )

    @staticmethod
    def add_body(request_data: dict, request_arg: dict) -> None:
        """add body"""
        if (body := request_data.get(RequestConfigNode.BODY_FRM)) is not None:
            request_arg["data"] = dict(body)
        elif (body := request_data.get(RequestConfigNode.BODY_FRM_DAT)) is not None:
            data = {}
            files = {}

            for key, val in dict(body).items():
                if isinstance(val, str) and val.startswith("file://"):
                    path_parsed = urlparse(val)
                    path = unquote(path_parsed.path)
                    netloc = unquote(path_parsed.netloc)

                    filepath = pathlib.Path(f"{netloc}{path}")
                    if not filepath.expanduser().exists():
                        raise FileNotFoundError(f"path `{val}` do not exists")

                    files[key] = str(filepath.expanduser().resolve())
                else:
                    data[key] = val

            request_arg["data"] = data
            request_arg["files"] = files

        elif (body := request_data.get(RequestConfigNode.BODY_JSN)) is not None:
            request_arg["json"] = dict(body)
        elif (body := request_data.get(RequestConfigNode.BODY_XML)) is not None:
            if "headers" not in request_arg:
                request_arg["headers"] = {}

            if (
                "content-type" not in request_arg["headers"]
                and "Content-Type" not in request_arg["headers"]
            ):
                request_arg["headers"]["content-type"] = CTYPE_XML

            request_arg["data"] = body
        elif (body := request_data.get(RequestConfigNode.BODY_TXT)) is not None:
            if "headers" not in request_arg:
                request_arg["headers"] = {}

            if (
                "content-type" not in request_arg["headers"]
                and "Content-Type" not in request_arg["headers"]
            ):
                request_arg["headers"]["content-type"] = "text/plain"

            request_arg["data"] = str(body)

    @staticmethod
    def add_generic_args(request_data: dict, request_arg: dict) -> None:
        """add default request parameters regardless of method"""
        HttpRequestArgCompiler.add_url_and_method(request_data, request_arg)
        HttpRequestArgCompiler.add_query_string(request_data, request_arg)
        HttpRequestArgCompiler.add_headers(request_data, request_arg)
        HttpRequestArgCompiler.add_authorization(request_data, request_arg)
        HttpRequestArgCompiler.add_body(request_data, request_arg)


class HttpDocument(VersionedDocumentV2, BaseModel):
    """
    Http document entity
    """

    request: dict = Field(default_factory=dict)

    @staticmethod
    def from_file_context(ctx: FileContext) -> HttpDocument:
        """Create a HttpDocument from FileContext
        :param ctx: FileContext to create the HttpDocument from
        """

        if not (version_str := data_get(ctx.document, "version")):
            raise RuntimeError("`version:` not found.")

        if not (request_dct := data_get(ctx.document, "request")):
            raise RuntimeError("`request:` not found.")

        # @TODO keep `context`, `version` as object
        # @TODO implement __repr__ for WorkflowDocument
        return HttpDocument(
            context=tuple(ctx),
            version=version_str,
            request=request_dct,
        )


class HttpDocumentSupport:
    """Service class for HttpDocument"""

    @staticmethod
    def execute_request(http_doc: HttpDocument) -> ApiResponse:
        """Execute http request from given HttpDocument

        Args:
            http_doc (HttpDocument): Http request document object

        Returns:
            dict: Returns response for http request
        """

        request_args: dict = {}

        HttpRequestArgCompiler.add_generic_args(http_doc.request, request_args)

        return ApiResponse.from_response(requests.request(**request_args))

    @staticmethod
    def process_request_template(http_doc: HttpDocument, variables: Variables) -> None:
        """Replace variables in request body

        Args:
            http_doc: HttpDocument, for the request body
            variables: Variables, variable base
        """

        http_doc.request = replace_value(http_doc.request, variables.data)

    @staticmethod
    def build_schema() -> dict:
        """Validate a http document with given json-schema

        Returns:
            dict: Containing http document schema
        """

        return {**VER_SCHEMA, **SCHEMA, **VAR_SCHEMA, **EXP_SCHEMA}


class FetchPresenter(PresentationBuilder):
    """FetchPresenter"""

    def dump_error_json(self) -> str:
        return json.dumps(
            {
                "error": (
                    repr(self.data.exception)
                    if self.data.exception
                    else "Unspecified error"
                )
            }
        )

    def dump_error_fmt(self) -> str:
        """dump fmt error str"""

        return (
            f"Fetch error\n------\n{repr(self.data.exception)}"
            if self.data.exception
            else "Fetch error\n------\nUnspecified error"
        )

    def dump_json(self) -> str:
        """dump json"""

        displayables: list[object] = []

        for key, expose_item in self.data.exposed.items():
            if key == RequestConfigNode.LOCAL:
                resp = ApiResponse(expose_item)
                displayables.append(ApiResponseDict.from_api_response(resp).as_dict)
            else:
                displayables.append(expose_item)

        return json.dumps(displayables)

    def dump_fmt(self) -> str:
        """dump fmt string"""

        displayables: list[str] = []

        for key, expose_item in self.data.exposed.items():
            if key == RequestConfigNode.LOCAL:
                resp = ApiResponse(expose_item)
                displayables.append(resp.as_fmt_str)
            else:
                displayables.append(json.dumps(expose_item))

        return "\n======\n".join(displayables)


@with_catch_log
def call(file_ctx: FileContext, exec_ctx: ExecuteContext) -> ExecResponse:
    """Call a http document"""

    debug(file_ctx)
    debug(exec_ctx)

    http_doc = HttpDocument.from_file_context(file_ctx)
    debug(http_doc.model_dump_json())

    DocumentVersionMaker.verify_if_allowed(
        DocumentVersionMaker.from_dict(http_doc.model_dump()), VERSION_SCOPE
    )

    VersionedDocumentSupport.validate_with_schema(
        HttpDocumentSupport.build_schema(), http_doc
    )

    variable_doc = Variables()
    VariableTableManager.handle(variable_doc, http_doc, exec_ctx)
    debug(variable_doc.data)

    HttpDocumentSupport.process_request_template(http_doc, variable_doc)
    debug(http_doc.model_dump_json())

    r_exception: Exception | None = None
    response = ApiResponse()

    try:
        response = HttpDocumentSupport.execute_request(http_doc)
    except Exception as ex:
        r_exception = ex
        error(ex)

    output_data = Variables({"_response": response.as_dict()})
    debug(output_data.data)

    exposed_data = ExposeManager.get_exposed_replaced_data(
        http_doc,
        {**variable_doc.data, **output_data.data},
    )
    debug(exposed_data)

    # TODO: instead if sending specific report items, and making presentable in other
    #       module, we should prepare and long and short form of presentable that can be
    #       loaded via other module

    return ExecResponse(
        file_ctx=file_ctx,
        exec_ctx=exec_ctx,
        variables_exec=output_data,
        variables=variable_doc,
        exception=r_exception,
        exposed=exposed_data,
        report={
            "is_success": r_exception is None,
            "request_method": file_ctx.document["request"]["method"],
            "request_url": file_ctx.document["request"]["url"],
        },
    )


@with_catch_log
def execute(
    ctx: FileContext, exec_ctx: ExecuteContext, cb: abc.Callable = lambda *args: ...
) -> None:
    """Call with a http document

    Args:
        ctx: FileContext object to handle
        exec_ctx: ExecuteContext
        cb: Callable
    """

    exr = call(file_ctx=ctx, exec_ctx=exec_ctx)

    cb({ctx.filepath_hash: exr.variables_exec.data})
    PresentationService.display(exr, exec_ctx, FetchPresenter)


@with_catch_log
def task_fetch(**kwargs: dict) -> ExecResponse:
    """Task impl"""

    if not (doc := kwargs.get("task", {})):
        raise ValueError("Wrong task format given.")

    _task = FetchTask(**doc)

    return call(
        FileContext.from_file(_task.file),
        ExecuteContext(
            options={"dump": True, "format": True},
            arguments=_task.arguments | {"variables": _task.variables},
        ),
    )
