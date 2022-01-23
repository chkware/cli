"""
http_requestor mod
"""
import enum
from urllib.parse import unquote, urlparse
from requests import request, Response
from dotmap import DotMap


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
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'


class HttpRequestArgCompiler:
    """
    HttpRequestArgCompiler
    """
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
            request_arg["headers"]["authorization"] = "Bearer " + tag_be.get(HttpDocElements.AUTH_BE_TOK)

    @staticmethod
    def add_body(request_data: DotMap, request_arg: dict) -> None:
        """add body"""
        if request_data.get(HttpDocElements.BODY_NO):
            pass
        elif (body := request_data.get(HttpDocElements.BODY_FRM)) is not None:
            request_arg["data"] = dict(body)
        elif (body := request_data.get(HttpDocElements.BODY_FRM_DAT)) is not None:
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

        elif (body := request_data.get(HttpDocElements.BODY_JSN)) is not None:
            request_arg["json"] = dict(body)
        elif (body := request_data.get(HttpDocElements.BODY_XML)) is not None:
            request_arg["headers"]["content-type"] = 'application/xml'
            request_arg["data"] = body

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

    # Body
    BODY_NO = 'body[none]'
    BODY_FRM = 'body[form]'
    BODY_FRM_DAT = 'body[form-data]'
    BODY_JSN = 'body[json]'
    BODY_XML = 'body[xml]'


# services
def get_request_args(request_data: DotMap) -> dict:
    """Prepare dotmap to dict before making request"""
    if request_data.method in \
        (HttpMethod.GET.value,
         HttpMethod.POST.value,
         HttpMethod.PUT.value,
         HttpMethod.PATCH.value,
         HttpMethod.DELETE.value):
        return _args_http_generic(request_data)

    elif request_data.method in \
        (HttpMethod.OPTIONS.value,
         HttpMethod.HEAD.value):
        return _args_http_generic(request_data)

    else:
        raise SystemExit(f'The http method no implemented yet. method: {request_data.method}')


def _args_http_generic(request_data: DotMap) -> dict:
    """Returns HTTP GET method compatible data from request_data"""
    request_args = {}

    HttpRequestArgCompiler.add_generic_args(request_data, request_args)
    HttpRequestArgCompiler.add_body(request_data, request_args)

    return request_args


def _args_http_status(request_data: DotMap) -> dict:
    """Returns HTTP GET method compatible data from request_data"""
    request_args = {}

    HttpRequestArgCompiler.add_generic_args(request_data, request_args)

    return request_args
