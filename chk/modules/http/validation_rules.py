"""
Validation rules and supporting libs for http module
"""
from chk.modules.http.constants import HttpMethod
from urllib.parse import urlparse


def allowed_method(value):
    """Validate if given method is allowed"""
    if value not in set(method.value for method in HttpMethod):
        raise ValueError('Unsupported method')
    else:
        return True


def allowed_url(value):
    """Validate if given method is allowed"""

    parsed_url = urlparse(value)
    ret = all([parsed_url.scheme, parsed_url.netloc])

    if ret is False:
        raise ValueError('Invalid `url`')

    if parsed_url.scheme not in ['http', 'https']:
        raise ValueError('Invalid `url` scheme. http and https allowed')

    return True


request_schema = {  # cerberus validation rules
    'request': {
        'required': True,
        'type': 'dict',
        'schema': {
            'url': {
                'required': True,
                'empty': False,
                'type': 'string',
            },
            'method': {
                'required': True,
                'type': 'string',
            },
            'url_params': {
                'required': False,
                'empty': False,
                'type': 'dict',
            },
            'headers': {
                'required': False,
                'empty': False,
                'type': 'dict',
            },
            'auth[basic]': {
                'required': False,
                'empty': False,
                'type': 'dict',
                'excludes': 'auth[bearer]',
            },
            'auth[bearer]': {
                'required': False,
                'empty': False,
                'type': 'dict',
                'excludes': 'auth[basic]',
            },
            'body[form]': {
                'required': False,
                'empty': False,
                'type': 'dict',
                'excludes': ['body[form-data]', 'body[json]', 'body[xml]'],
            },
            'body[form-data]': {
                'required': False,
                'empty': False,
                'type': 'dict',
                'excludes': ['body[form]', 'body[json]', 'body[xml]'],
            },
            'body[json]': {
                'required': False,
                'empty': False,
                'type': 'dict',
                'excludes': ['body[form]', 'body[form-data]', 'body[xml]'],
            },
            'body[xml]': {
                'required': False,
                'empty': False,
                'type': 'string',
                'excludes': ['body[form]', 'body[form-data]', 'body[json]'],
            }
        }
    }
}
