"""
Http module helpers
"""
from types import MappingProxyType
from urllib.parse import unquote, urlparse

from requests import (
    request,
    TooManyRedirects,
    ConnectionError,
    ConnectTimeout,
    ReadTimeout,
    RequestException,
)
from requests.auth import HTTPBasicAuth

from chk.modules.http.constants import RequestConfigNode as ConfElem
from chk.modules.http.validation_rules import allowed_method, allowed_url


class RequestProcessorPyRequests:
    """Request class that use python requests"""

    @staticmethod
    def perform(request_data: dict) -> dict:
        """Make external api call"""

        request_args: dict = {}

        HttpRequestArgCompiler.add_generic_args(
            MappingProxyType(request_data),
            request_args,
        )

        try:
            response = request(**request_args)
        except ConnectTimeout as err:
            raise RuntimeError("Connection time out") from err
        except ConnectionError as err:
            raise RuntimeError("Connection error") from err
        except ReadTimeout as err:
            raise RuntimeError("Read time out") from err
        except TooManyRedirects as err:
            raise RuntimeError("Too many redirects") from err
        except RequestException as err:
            raise RuntimeError("Request error") from err

        def version(proto_ver: int) -> str:
            """parse version"""
            return "HTTP/1.0" if proto_ver == 10 else "HTTP/1.1"

        return dict(
            version=version(response.raw.version),
            code=response.status_code,
            reason=response.reason,
            headers=dict(response.headers),
            body=response.text,
        )


class HttpRequestArgCompiler:
    """HttpRequestArgCompiler"""

    @staticmethod
    def add_url_and_method(request_data: MappingProxyType, request_arg: dict) -> None:
        """add default request url and request method"""
        if allowed_method(request_data.get(ConfElem.METHOD)):
            request_arg["method"] = request_data.get(ConfElem.METHOD)

        if allowed_url(request_data.get(ConfElem.URL)):
            request_arg["url"] = request_data.get(ConfElem.URL)

    @staticmethod
    def add_query_string(request_data: MappingProxyType, request_arg: dict) -> None:
        """add query string"""
        if (params := request_data.get(ConfElem.PARAMS)) is not None:
            request_arg["params"] = params

    @staticmethod
    def add_headers(request_data: MappingProxyType, request_arg: dict) -> None:
        """add custom header"""
        if (headers := request_data.get(ConfElem.HEADERS)) is not None:
            request_arg["headers"] = headers

    @staticmethod
    def add_authorization(request_data: MappingProxyType, request_arg: dict) -> None:
        """handle authorization header"""
        # handle basic auth
        if (tag_ba := request_data.get(ConfElem.AUTH_BA)) is not None:
            request_arg["auth"] = HTTPBasicAuth(
                tag_ba.get(ConfElem.AUTH_BA_USR), tag_ba.get(ConfElem.AUTH_BA_PAS)
            )

        # handle bearer auth
        if (tag_be := request_data.get(ConfElem.AUTH_BE)) is not None:
            request_arg["headers"]["authorization"] = "Bearer " + tag_be.get(
                ConfElem.AUTH_BE_TOK
            )

    @staticmethod
    def add_body(request_data: MappingProxyType, request_arg: dict) -> None:
        """add body"""
        if (body := request_data.get(ConfElem.BODY_FRM)) is not None:
            request_arg["data"] = dict(body)
        elif (body := request_data.get(ConfElem.BODY_FRM_DAT)) is not None:
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

        elif (body := request_data.get(ConfElem.BODY_JSN)) is not None:
            request_arg["json"] = dict(body)
        elif (body := request_data.get(ConfElem.BODY_XML)) is not None:
            if request_arg["headers"].get("content-type") is None:
                request_arg["headers"]["content-type"] = "application/xml"
            request_arg["data"] = body
        elif (body := request_data.get(ConfElem.BODY_TXT)) is not None:
            if request_arg["headers"].get("content-type") is None:
                request_arg["headers"]["content-type"] = "text/plain"
            request_arg["data"] = str(body)

    @staticmethod
    def add_generic_args(request_data: MappingProxyType, request_arg: dict) -> None:
        """add default request parameters regardless of method"""
        HttpRequestArgCompiler.add_url_and_method(request_data, request_arg)
        HttpRequestArgCompiler.add_query_string(request_data, request_arg)
        HttpRequestArgCompiler.add_headers(request_data, request_arg)
        HttpRequestArgCompiler.add_authorization(request_data, request_arg)
        HttpRequestArgCompiler.add_body(request_data, request_arg)
