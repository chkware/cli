"""
Request specification validation schema
@deprecate
"""

from chk.constants.archetype import rules, ArchetypeConfigModules

version_schema = {
    'version': {
        'required': True,
        'type': 'string',
        'empty': False,
        'allowed': list(ArchetypeConfigModules.data.keys())
    }
}

request_schema = {
    'request': {
        'required': True,
        'type': 'dict',
        'schema': {
            'url': {
                'required': True,
                'empty': False,
                'type': 'string',
                'check_with': rules.allowed_url,
            },
            'method': {
                'required': True,
                'type': 'string',
                'check_with': rules.allowed_method,
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
            },
            'auth[bearer]': {
                'required': False,
                'empty': False,
                'type': 'dict',
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
