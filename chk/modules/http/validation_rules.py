"""
Validation rules and supporting libs for http module
"""
from urllib.parse import urlparse

from chk.modules.http.constants import HttpMethod, RequestConfigNode


def allowed_method(value: str) -> bool:
    """Validate if given method is allowed"""
    if value not in set(method.value for method in HttpMethod):
        raise ValueError('Unsupported method')

    return True


def allowed_url(value: str) -> bool:
    """Validate if given URL is allowed"""

    parsed_url = urlparse(value)
    ret = all([parsed_url.scheme, parsed_url.netloc])

    if ret is False:
        raise ValueError('Invalid `url`')

    if parsed_url.scheme not in ['http', 'https']:
        raise ValueError('Invalid `url` scheme. http and https allowed')

    return True


request_schema = {  # cerberus validation rules
    RequestConfigNode.ROOT: {
        'required': True,
        'type': 'dict',
        'schema': {
            RequestConfigNode.URL: {
                'required': True,
                'empty': False,
                'type': 'string',
            },
            RequestConfigNode.METHOD: {
                'required': True,
                'type': 'string',
            },
            RequestConfigNode.PARAMS: {
                'required': False,
                'empty': False,
                'type': 'dict',
            },
            RequestConfigNode.HEADERS: {
                'required': False,
                'empty': False,
                'type': 'dict',
            },
            RequestConfigNode.AUTH_BA: {
                'required': False,
                'empty': False,
                'type': 'dict',
                'excludes': RequestConfigNode.AUTH_BE,
            },
            RequestConfigNode.AUTH_BE: {
                'required': False,
                'empty': False,
                'type': 'dict',
                'excludes': RequestConfigNode.AUTH_BA,
            },
            RequestConfigNode.BODY_FRM: {
                'required': False,
                'empty': False,
                'type': 'dict',
                'excludes': [RequestConfigNode.BODY_FRM_DAT, RequestConfigNode.BODY_JSN, RequestConfigNode.BODY_XML,
                             RequestConfigNode.BODY_TXT],
            },
            RequestConfigNode.BODY_FRM_DAT: {
                'required': False,
                'empty': False,
                'type': 'dict',
                'excludes': [RequestConfigNode.BODY_FRM, RequestConfigNode.BODY_JSN, RequestConfigNode.BODY_XML,
                             RequestConfigNode.BODY_TXT],
            },
            RequestConfigNode.BODY_JSN: {
                'required': False,
                'empty': False,
                'type': 'dict',
                'excludes': [RequestConfigNode.BODY_FRM, RequestConfigNode.BODY_FRM_DAT, RequestConfigNode.BODY_XML,
                             RequestConfigNode.BODY_TXT],
            },
            RequestConfigNode.BODY_XML: {
                'required': False,
                'empty': False,
                'type': 'string',
                'excludes': [RequestConfigNode.BODY_FRM, RequestConfigNode.BODY_FRM_DAT, RequestConfigNode.BODY_JSN,
                             RequestConfigNode.BODY_TXT],
            },
            RequestConfigNode.BODY_TXT: {
                'required': False,
                'empty': False,
                'type': 'string',
                'excludes': [RequestConfigNode.BODY_FRM, RequestConfigNode.BODY_FRM_DAT, RequestConfigNode.BODY_JSN,
                             RequestConfigNode.BODY_XML],
            },
        }
    }
}
