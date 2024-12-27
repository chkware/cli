"""
Fetch module
"""

from __future__ import annotations

import json
import pathlib
from urllib.parse import unquote, urlparse

import requests
from requests.auth import HTTPBasicAuth

from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import data_get
from chk.infrastructure.symbol_table import (
    EXPOSE_SCHEMA as EXP_SCHEMA,
    VARIABLE_SCHEMA as VAR_SCHEMA,
    Variables,
    replace_value,
)
from chk.infrastructure.version import (
    DocumentVersionMaker,
    SCHEMA as VER_SCHEMA,
)
from chk.infrastructure.view import PresentationBuilder
from chk.modules.fetch.entities import (
    ApiResponseModel,
    BearerAuthentication,
    CTYPE_XML,
    HttpDocument,
    HttpMethod,
    RequestConfigNode,
    SCHEMA,
    VERSION_SCOPE,
)


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


class HttpDocumentSupport:
    """Service class for HttpDocument"""

    @staticmethod
    def from_file_context(ctx: FileContext) -> HttpDocument:
        """Create a HttpDocument from FileContext
        :param ctx: FileContext to create the HttpDocument from
        """

        doc_ver = DocumentVersionMaker.from_dict(ctx.document)
        DocumentVersionMaker.verify_if_allowed(doc_ver, VERSION_SCOPE)

        if not (request_dct := data_get(ctx.document, "request")):
            raise RuntimeError("`request:` not found.")

        # @TODO keep `context`, `version` as object
        # @TODO implement __repr__ for WorkflowDocument
        return HttpDocument(
            context=tuple(ctx),
            version=str(doc_ver),
            request=request_dct,
        )

    @staticmethod
    def execute_request(http_doc: HttpDocument) -> ApiResponseModel:
        """Execute http request from given HttpDocument

        Args:
            http_doc (HttpDocument): Http request document object

        Returns:
            dict: Returns response for http request
        """

        if not http_doc:
            raise ValueError("Empty document found.")

        request_args: dict = {}

        HttpRequestArgCompiler.add_generic_args(http_doc.request, request_args)

        return ApiResponseModel.from_response(requests.request(**request_args))

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

    def dump_error_json(self, err: object = None) -> str:
        """dump_error_json"""

        if not err:
            err = self.data.exception

        return json.dumps({"error": (repr(err) if err else "Unspecified error")})

    def dump_error_fmt(self, err: object = None) -> str:
        """dump fmt error str"""

        if not err:
            err = self.data.exception

        return (
            f"Fetch error\n------\n{repr(err)}"
            if err
            else "Fetch error\n------\nUnspecified error"
        )

    def dump_json(self) -> str:
        """dump json"""

        displayables: list[object] = []

        for key, expose_item in self.data.exposed.items():
            if key == RequestConfigNode.LOCAL and all(
                [
                    item in expose_item.keys()
                    for item in ["code", "info", "headers", "body"]
                ]
            ):
                resp = ApiResponseModel.from_dict(**expose_item)
                displayables.append(resp.model_dump())
            else:
                displayables.append(expose_item)

        return json.dumps(displayables)

    def dump_fmt(self) -> str:
        """dump fmt string"""

        displayables: list[str] = []

        for key, expose_item in self.data.exposed.items():
            if key == RequestConfigNode.LOCAL and all(
                [
                    item in expose_item.keys()
                    for item in ["code", "info", "headers", "body"]
                ]
            ):
                resp = ApiResponseModel.from_dict(**expose_item)
                displayables.append(resp.as_fmt_str())
            else:
                displayables.append(json.dumps(expose_item))

        return "\n======\n".join(displayables)
