"""
Http module helpers
"""
from chk.modules.http.constants import HttpDocElements, HttpMethod
from dotmap import DotMap
from requests.auth import HTTPBasicAuth
from requests import request, Response
from typing import Dict
from urllib.parse import unquote, urlparse


def do_http_request(request_args: Dict[str, str]) -> Response:
    """Make external api call"""
    return request(**request_args)


def prepare_request_args(request_data: DotMap) -> dict:
    """Prepare dotmap to dict before making request"""
    request_args: Dict[str, str] = {}
    HttpRequestArgCompiler.add_generic_args(request_data, request_args)
    return request_args


class HttpRequestArgCompiler:
    """
    HttpRequestArgCompiler
    """

    @staticmethod
    def add_url_and_method(request_data: DotMap, request_arg: dict) -> None:
        """add default request url and request method"""
        request_arg["method"] = request_data.method
        request_arg["url"] = request_data.url

    @staticmethod
    def add_query_string(request_data: DotMap, request_arg: dict) -> None:
        """add query string"""
        if (params := request_data.get(HttpDocElements.PARAMS)) is not None:
            request_arg["params"] = params

    @staticmethod
    def add_headers(request_data: DotMap, request_arg: dict) -> None:
        """add custom header"""
        if (headers := request_data.get(HttpDocElements.HEADERS)) is not None:
            request_arg["headers"] = headers

    @staticmethod
    def add_authorization(request_data: DotMap, request_arg: dict) -> None:
        """handle authorization header"""
        # handle basic auth
        if (tag_ba := request_data.get(HttpDocElements.AUTH_BA)) is not None:
            request_arg["auth"] = HTTPBasicAuth(
                tag_ba.get(HttpDocElements.AUTH_BA_USR), tag_ba.get(HttpDocElements.AUTH_BA_PAS))

        # handle bearer auth
        if (tag_be := request_data.get(HttpDocElements.AUTH_BE)) is not None:
            request_arg["headers"]["authorization"] = "Bearer " + tag_be.get(HttpDocElements.AUTH_BE_TOK)

    @staticmethod
    def add_body(request_data: DotMap, request_arg: dict) -> None:
        """add body"""
        if request_data.get(HttpDocElements.BODY_NO):
            pass
        elif (body := request_data.get(HttpDocElements.BODY_FRM)) is not None:
            request_arg["data"] = dict(body)
        elif (body := request_data.get(HttpDocElements.BODY_FRM_DAT)) is not None:
            non_files = {}
            files = {}

            for body_i in dict(body).items():
                (key, val) = body_i
                if val.startswith('file://'):
                    val = unquote(urlparse(val).path)
                    files[key] = open(val, 'rb')
                else:
                    non_files[key] = val

            request_arg["data"] = non_files
            request_arg["files"] = files

        elif (body := request_data.get(HttpDocElements.BODY_JSN)) is not None:
            request_arg["json"] = dict(body)
        elif (body := request_data.get(HttpDocElements.BODY_XML)) is not None:
            request_arg["headers"]["content-type"] = 'application/xml'
            request_arg["data"] = body

    @staticmethod
    def add_generic_args(request_data: DotMap, request_arg: dict) -> None:
        """add default request parameters regardless of method"""
        HttpRequestArgCompiler.add_url_and_method(request_data, request_arg)
        HttpRequestArgCompiler.add_query_string(request_data, request_arg)
        HttpRequestArgCompiler.add_headers(request_data, request_arg)
        HttpRequestArgCompiler.add_authorization(request_data, request_arg)
        HttpRequestArgCompiler.add_body(request_data, request_arg)
