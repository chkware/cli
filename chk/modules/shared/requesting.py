"""Executor service"""
from typing import Dict
from requests import request, Response


def do_http_request(request_args: Dict[str, str]) -> Response:
    """Make external api call"""
    return request(**request_args)
