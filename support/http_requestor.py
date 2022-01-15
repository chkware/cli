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
            from requests.auth import HTTPBasicAuth

            request_arg["auth"] = HTTPBasicAuth(
                tag_ba.get(HttpDocElements.AUTH_BA_USR), tag_ba.get(HttpDocElements.AUTH_BA_PAS))

        # handle bearer auth
        if (tag_be := request_data.get(HttpDocElements.AUTH_BE)) is not None:
            request_arg["headers"]["Authorization"] = "Bearer " + tag_be.get(HttpDocElements.AUTH_BE_TOK)

    @staticmethod
    def add_generic_args(request_data: DotMap, request_arg: dict) -> None:
        """add default request parameters regardless of method"""
        HttpRequestArgCompiler.add_url_and_method(request_data, request_arg)
        HttpRequestArgCompiler.add_query_string(request_data, request_arg)
        HttpRequestArgCompiler.add_headers(request_data, request_arg)
        HttpRequestArgCompiler.add_authorization(request_data, request_arg)


class BaseDocElements:
    """represent the base of all kind of documents"""
    VERSION = 'version'


class HttpDocElements(BaseDocElements):
    """represent http documents"""
    # common request
    URL = 'url'
    METHOD = 'method'
    HEADERS = 'headers'
    PARAMS = 'url_params'

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

    HttpRequestArgCompiler.add_generic_args(request_data, request_args)

    return request_args


def _args_http_post(request_data: DotMap) -> dict:
    """Returns HTTP GET method compatible data from request_data"""
    request_args = {}

    HttpRequestArgCompiler.add_generic_args(request_data, request_args)

    return request_args
