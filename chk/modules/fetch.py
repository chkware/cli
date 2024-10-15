"""
Fetch module
"""

from __future__ import annotations

import enum
import json
import pathlib
from collections import UserDict, abc
from urllib.parse import unquote, urlparse

import requests
import xmltodict
from defusedxml.minidom import parseString
from pydantic import BaseModel, Field
from requests.auth import HTTPBasicAuth

from chk.infrastructure.document import (
    VersionedDocumentSupport,
    VersionedDocumentV2,
)
from chk.infrastructure.file_loader import ExecuteContext, FileContext
from chk.infrastructure.helper import data_get
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
                request_arg["headers"]["content-type"] = "application/xml"

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


class ApiResponseDict(UserDict):
    """Represents a API response with body in dict representation"""

    api_resp: dict
    body_as_dict: dict

    @staticmethod
    def from_api_response(resp: ApiResponse) -> ApiResponseDict:
        """Create JsonApiResponse from ApiResponse

        Args:
            resp (ApiResponse): ApiResponse object

        Raises:
            RuntimeError: if response format not supported

        Returns:
            ApiResponseDict: new ApiResponseDict object
        """

        body = None

        try:
            if "headers" in resp:
                content_type = ""
                if "Content-Type" in resp["headers"]:
                    content_type = resp["headers"]["Content-Type"]
                elif "content-type" in resp["headers"]:
                    content_type = resp["headers"]["content-type"]

                if content_type and "application/json" in content_type:
                    body = json.loads(resp["body"])
                elif content_type and "application/xml" in content_type:
                    body = xmltodict.parse(parseString(resp["body"]).toxml())

            if not body:
                body = dict(resp["body"])

            return ApiResponseDict(api_resp=resp.data, body_as_dict=body)

        except Exception:
            raise RuntimeError("Unsupported response format.")

    @property
    def as_json(self) -> str:
        """Converts to JSON string

        Returns:
            str: JSON object as string representation
        """

        return json.dumps(self.as_dict)

    @property
    def as_dict(self) -> dict:
        """Converts to JSON string

        Returns:
            str: JSON object as string representation
        """

        return {**self["api_resp"], **{"body": self["body_as_dict"]}}


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


def call(file_ctx: FileContext, exec_ctx: ExecuteContext) -> ExecResponse:
    """Call a http document"""

    r_exception: Exception | None = None

    http_doc = HttpDocument.from_file_context(file_ctx)

    DocumentVersionMaker.verify_if_allowed(
        DocumentVersionMaker.from_dict(http_doc.model_dump()), VERSION_SCOPE
    )

    VersionedDocumentSupport.validate_with_schema(
        HttpDocumentSupport.build_schema(), http_doc
    )

    variable_doc = Variables()
    VariableTableManager.handle(variable_doc, http_doc, exec_ctx)
    HttpDocumentSupport.process_request_template(http_doc, variable_doc)

    response = ApiResponse()

    try:
        response = HttpDocumentSupport.execute_request(http_doc)
    except Exception as ex:
        r_exception = ex

    output_data = Variables({"_response": response.data})

    exposed_data = ExposeManager.get_exposed_replaced_data(
        http_doc,
        {**variable_doc.data, **output_data.data},
    )

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
    if exr.exception is not None:
        raise exr.exception

    cb({ctx.filepath_hash: exr.variables_exec.data})
    PresentationService.display(exr, exec_ctx, FetchPresenter)


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
