"""
Fetch module
"""
import dataclasses
import enum
import json

from collections import UserDict
from urllib.parse import unquote, urlparse
from requests.auth import HTTPBasicAuth

from defusedxml.minidom import parseString
import xmltodict

from chk.infrastructure.document import VersionedDocument
from chk.infrastructure.file_loader import ExecuteContext, FileContext
from chk.infrastructure.helper import data_get

from chk.infrastructure.third_party.http_fetcher import ApiResponse, fetch


class HttpMethod(enum.StrEnum):
    """Constants of wellknown http methods"""

    GET = enum.auto()
    POST = enum.auto()
    PUT = enum.auto()
    PATCH = enum.auto()
    DELETE = enum.auto()
    HEAD = enum.auto()
    OPTIONS = enum.auto()


class RequestConfigNode(enum.StrEnum):
    """represent request config section"""

    ROOT = "request"
    LOCAL = "_response"
    RETURN = "return"

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


def allowed_method(value: str) -> bool:
    """Validate if given method is allowed"""

    return value not in set(method for method in HttpMethod)


def allowed_url(value: str) -> bool:
    """Validate if given URL is allowed"""

    parsed_url = urlparse(value)
    ret = all([parsed_url.scheme, parsed_url.netloc])

    if ret is False:
        raise ValueError("Invalid `url`")

    if parsed_url.scheme not in ["http", "https"]:
        raise ValueError("Invalid `url` scheme. http and https allowed")

    return True


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
            request_arg["headers"]["authorization"] = "Bearer " + tag_be.get(
                RequestConfigNode.AUTH_BE_TOK
            )

    @staticmethod
    def add_body(request_data: dict, request_arg: dict) -> None:
        """add body"""
        if (body := request_data.get(RequestConfigNode.BODY_FRM)) is not None:
            request_arg["data"] = dict(body)
        elif (body := request_data.get(RequestConfigNode.BODY_FRM_DAT)) is not None:
            non_files = {}
            files = {}

            for body_i in dict(body).items():
                (key, val) = body_i
                if val.startswith("file://"):
                    val = unquote(urlparse(val).path)
                    files[key] = open(val, "rb")
                else:
                    non_files[key] = val

            request_arg["data"] = non_files
            request_arg["files"] = files

        elif (body := request_data.get(RequestConfigNode.BODY_JSN)) is not None:
            request_arg["json"] = dict(body)
        elif (body := request_data.get(RequestConfigNode.BODY_XML)) is not None:
            if request_arg["headers"].get("content-type") is None:
                request_arg["headers"]["content-type"] = "application/xml"
            request_arg["data"] = body
        elif (body := request_data.get(RequestConfigNode.BODY_TXT)) is not None:
            if request_arg["headers"].get("content-type") is None:
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


@dataclasses.dataclass(slots=True)
class HttpDocument(VersionedDocument):
    """
    Http document entity
    """

    request: dict = dataclasses.field(default_factory=dict)

    @staticmethod
    def from_file_context(ctx: FileContext) -> "HttpDocument":
        """Create a HttpDocument from FileContext
        :param ctx: FileContext to create the HttpDocument from
        """

        if not (version_str := data_get(ctx.document, "version")):
            raise RuntimeError("`version:` not found.")

        if not (request_dct := data_get(ctx.document, "request")):
            raise RuntimeError("`request:` not found.")

        return HttpDocument(
            context=tuple(ctx),
            version=version_str,
            request=request_dct,
        )


class ApiResponseDict(UserDict):
    """Represents a API response with body in dict representation"""

    api_resp: ApiResponse
    body_as_dict: dict

    @staticmethod
    def from_api_response(resp: ApiResponse) -> "ApiResponseDict":
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
            if "headers" in resp and "Content-Type" in resp["headers"]:
                CONTENT_TYPE = resp["headers"]["Content-Type"]

                if "application/json" in CONTENT_TYPE:
                    body = json.loads(resp["body"])
                elif "application/xml" in CONTENT_TYPE:
                    body = xmltodict.parse(parseString(resp["body"]).toxml())

            if not body:
                body = resp["body"]

            return ApiResponseDict(api_resp=resp, body_as_dict=body)

        except Exception as ex:
            raise RuntimeError("Unsupported response format.")

    @property
    def as_json(self) -> str:
        """Converts to JSON string

        Returns:
            str: JSON object as string representation
        """

        return json.dumps({**dict(self["api_resp"]), **dict(body=self["body_as_dict"])})


def execute_request(http_doc: HttpDocument) -> ApiResponse:
    """Execute http request from given HttpDocument

    Args:
        http_doc (HttpDocument): Http request document object

    Returns:
        dict: Returns response for http request
    """

    request_args: dict = {}

    HttpRequestArgCompiler.add_generic_args(http_doc.request, request_args)

    return fetch(request_args)


def execute_context(ctx: FileContext, _: ExecuteContext) -> None:
    """Run a http document
    :param ctx: FileContext object to handle
    """

    http_doc = HttpDocument.from_file_context(ctx)
    response_ = execute_request(http_doc)
    response = ApiResponseDict.from_api_response(response_)

    print(response.as_json, response_)
