from requests import request, Response
from dotmap import DotMap
import enum
import pprint


# module functions
def make_request(request_data: DotMap) -> Response:
    """Make external api call"""
    request_args = get_request_args(request_data)
    return request(**request_args)


# class
class HttpMethod(enum.Enum):
    """Constants of wellknown http methods"""
    GET = 'GET'
    POST = 'POST'


class HttpRequestArgCompiler:
    @staticmethod
    def add_url_and_method(request_data: DotMap, request_arg: dict) -> None:
        request_arg["method"] = request_data.method
        request_arg["url"] = request_data.path

    @staticmethod
    def add_query_string(request_data: DotMap, request_arg: dict) -> None:
        if request_data.get('query') is not None:
            request_arg["params"] = request_data.query

    @staticmethod
    def add_headers(request_data: DotMap, request_arg: dict) -> None:
        if request_data.get('headers') is not None:
            request_arg["headers"] = request_data.headers

    @staticmethod
    def add_authorization(request_data: DotMap, request_arg: dict) -> None:
        if request_data.get(HttpDoc.AUTH_BA) is not None:
            from requests.auth import HTTPBasicAuth

            request_arg["auth"] = HTTPBasicAuth(
                request_data.get(HttpDoc.AUTH_BA).get(HttpDoc.AUTH_BA_USR),
                request_data.get(HttpDoc.AUTH_BA).get(HttpDoc.AUTH_BA_PAS),
            )

        if request_data.get(HttpDoc.AUTH_BE) is not None:
            request_arg["headers"]["Authorization"] = "Bearer " + request_data.get(HttpDoc.AUTH_BE).get(HttpDoc.AUTH_BE_TOK)

    @staticmethod
    def add_compulsory_args(request_data: DotMap, request_arg: dict) -> None:
        HttpRequestArgCompiler.add_url_and_method(request_data, request_arg)
        HttpRequestArgCompiler.add_query_string(request_data, request_arg)
        HttpRequestArgCompiler.add_headers(request_data, request_arg)
        HttpRequestArgCompiler.add_authorization(request_data, request_arg)


class BaseDoc:
    """represent the base of all kind of documents"""
    VERSION = 'version'


class HttpDoc(BaseDoc):
    """represent http documents"""
    # common request
    PATH = 'path'
    METHOD = 'method'

    # Basic
    AUTH_BA = 'auth[basic]'
    AUTH_BA_USR = 'username'
    AUTH_BA_PAS = 'password'

    # Bearer
    AUTH_BE = 'auth[bearer]'
    AUTH_BE_TOK = 'token'


# services
def get_request_args(request_data: DotMap) -> dict:
    """Prepare dotmap to dict before making request"""
    _args_http = {
        HttpMethod.GET.value: _args_http_get,
        HttpMethod.POST.value: _args_http_post,
    }.get(request_data.method)

    if _args_http is None:
        raise ValueError('The http method no allowed')

    return _args_http(request_data)


def _args_http_get(request_data: DotMap) -> dict:
    """Returns HTTP GET method compatible data from request_data"""
    request_args = {}

    HttpRequestArgCompiler.add_compulsory_args(request_data, request_args)

    return request_args


def _args_http_post(request_data: DotMap) -> dict:
    """Returns HTTP GET method compatible data from request_data"""
    request_args = {}

    HttpRequestArgCompiler.add_compulsory_args(request_data, request_args)

    return request_args
