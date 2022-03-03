"""
Cerberus validation rules
"""
from chk.constants.http import HttpMethod


def allowed_method(field, value, error):
    """Validate if given method is allowed"""
    if value not in set(method.value for method in HttpMethod):
        error(field, 'Invalid `method`.')
