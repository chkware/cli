"""
Validation rules and supporting libs for http module
"""
from chk.modules.http.constants import HttpMethod
from urllib.parse import urlparse


def allowed_method(field, value, error):
    """Validate if given method is allowed"""
    if value not in set(method.value for method in HttpMethod):
        error(field, 'Invalid `method`.')


def allowed_url(field, value, error):
    """Validate if given method is allowed"""

    parsed_url = urlparse(value)
    ret = all([parsed_url.scheme, parsed_url.netloc])

    if ret is False:
        error(field, 'Invalid `url`.')

    if parsed_url.scheme not in ['http', 'https']:
        error(field, 'Invalid `url` scheme. http and https allowed')


request_schema = {  # cerberus validation rules
    'request': {
        'required': True,
        'type': 'dict',
        'schema': {
            'url': {
                'required': True,
                'empty': False,
                'type': 'string',
                'check_with': allowed_url,
            },
            'method': {
                'required': True,
                'type': 'string',
                'check_with': allowed_method,
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
            'body[none]': {
                'required': False,
                'nullable': True,
                'type': 'string',
            },
            'body[form]': {
                'required': False,
                'empty': False,
                'type': 'dict',
            },
            'body[form-data]': {
                'required': False,
                'empty': False,
                'type': 'dict',
            },
            'body[json]': {
                'required': False,
                'empty': False,
                'type': 'dict',
            },
            'body[xml]': {
                'required': False,
                'empty': False,
                'type': 'string',
            }
        }
    }
}
