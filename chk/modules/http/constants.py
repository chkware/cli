"""
Constants used in http modules
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


class RequestConfigNode:
    """represent request config section"""
    ROOT = 'request'

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

    # Body
    BODY_FRM = 'body[form]'
    BODY_FRM_DAT = 'body[form-data]'
    BODY_JSN = 'body[json]'
    BODY_XML = 'body[xml]'
