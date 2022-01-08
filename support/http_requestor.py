from requests import request, Response
from dotmap import DotMap
import enum


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
    def add_url_and_method(request_data: DotMap, request_arg: dict):
        request_arg["method"] = request_data.method
        request_arg["url"] = request_data.path

    @staticmethod
    def add_query_string(request_data: DotMap, request_arg: dict):
        if request_data.get('query') is not None:
            request_arg["params"] = request_data.query

    @staticmethod
    def add_compulsory_args(request_data: DotMap, request_arg: dict):
        HttpRequestArgCompiler.add_url_and_method(request_data, request_arg)
        HttpRequestArgCompiler.add_query_string(request_data, request_arg)


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
