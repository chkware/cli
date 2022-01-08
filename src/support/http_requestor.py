from requests import request, Response
from dotmap import DotMap


def make_request(request_data: DotMap) -> Response:
    """Make external api call"""
    request_args = get_request_args(request_data)
    return request(**request_args)


def get_request_args(request_data: DotMap) -> dict:
    """Prepare dotmap to dict before making request"""
    _args_http = {
        'GET': _args_http_get,
    }.get(request_data.method)

    if _args_http is None:
        raise

    return _args_http(request_data)


def _args_http_get(request_data: DotMap) -> dict:
    return {
        "method": request_data.method,
        "url": request_data.path,
    }
