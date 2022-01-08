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
    GET = 'GET',
    POST = 'POST',


# services
def get_request_args(request_data: DotMap) -> dict:
    """Prepare dotmap to dict before making request"""
    _args_http = {
        HttpMethod.GET: _args_http_get,
    }.get(request_data.method)

    if _args_http is None:
        raise

    return _args_http(request_data)


def _args_http_get(request_data: DotMap) -> dict:
    """Returns HTTP GET method compatible data from request_data"""
    return {
        "method": request_data.method,
        "url": request_data.path,
    }
