"""
Http module helpers
"""
from chk.infrastructure.work import RequestProcessorContract
from chk.modules.http.constants import RequestConfigNode as ConfElem
from chk.modules.http.validation_rules import allowed_method, allowed_url
from dotmap import DotMap
from requests.auth import HTTPBasicAuth
from requests import request
from urllib.parse import unquote, urlparse


class RequestProcessorMixin_PyRequests(RequestProcessorContract):
    """ Request class that use python requests """

    def __process__(self) -> dict:
        """Make external api call"""

        if not hasattr(self, 'request_args'):
            raise SystemExit('RequestProcessorContract not inherited.')

        return request(**self.request_args)  # type: ignore

    def __before_process__(self, request_data: dict[str, object]) -> None:
        """Prepare dotmap to dict before making request"""

        if not hasattr(self, 'request_args'):
            raise SystemExit('RequestProcessorContract not inherited.')

        if ConfElem.ROOT not in request_data:
            raise SystemExit('Wrong document format.')

        HttpRequestArgCompiler.add_generic_args(DotMap(request_data[ConfElem.ROOT]), self.request_args)  # type: ignore


class HttpRequestArgCompiler:
    """ HttpRequestArgCompiler """

    @staticmethod
    def add_url_and_method(request_data: DotMap, request_arg: dict) -> None:
        """ add default request url and request method """
        if allowed_method(request_data.get(ConfElem.METHOD)):
            request_arg["method"] = request_data.get(ConfElem.METHOD)

        if allowed_url(request_data.get(ConfElem.URL)):
            request_arg["url"] = request_data.get(ConfElem.URL)

    @staticmethod
    def add_query_string(request_data: DotMap, request_arg: dict) -> None:
        """add query string"""
        if (params := request_data.get(ConfElem.PARAMS)) is not None:
            request_arg["params"] = params

    @staticmethod
    def add_headers(request_data: DotMap, request_arg: dict) -> None:
        """add custom header"""
        if (headers := request_data.get(ConfElem.HEADERS)) is not None:
            request_arg["headers"] = headers

    @staticmethod
    def add_authorization(request_data: DotMap, request_arg: dict) -> None:
        """handle authorization header"""
        # handle basic auth
        if (tag_ba := request_data.get(ConfElem.AUTH_BA)) is not None:
            request_arg["auth"] = HTTPBasicAuth(
                tag_ba.get(ConfElem.AUTH_BA_USR), tag_ba.get(ConfElem.AUTH_BA_PAS))

        # handle bearer auth
        if (tag_be := request_data.get(ConfElem.AUTH_BE)) is not None:
            request_arg["headers"]["authorization"] = "Bearer " + tag_be.get(ConfElem.AUTH_BE_TOK)

    @staticmethod
    def add_body(request_data: DotMap, request_arg: dict) -> None:
        """add body"""
        if (body := request_data.get(ConfElem.BODY_FRM)) is not None:
            request_arg["data"] = dict(body)
        elif (body := request_data.get(ConfElem.BODY_FRM_DAT)) is not None:
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

        elif (body := request_data.get(ConfElem.BODY_JSN)) is not None:
            request_arg["json"] = body.toDict()
        elif (body := request_data.get(ConfElem.BODY_XML)) is not None:
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
