"""
Constants used throughout the software
"""
from enum import Enum


class HttpMethod(Enum):
    """Constants of wellknown http methods"""
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
