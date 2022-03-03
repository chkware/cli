"""
Cerberus validation rules
"""
from chk.constants.http import HttpMethod
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

