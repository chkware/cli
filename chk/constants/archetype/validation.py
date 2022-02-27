"""
Request specification validation schema
"""

import chk.constants.archetype

version_schema = {
    'version': {
        'required': True,
        'type': 'string',
        'empty': False,
        'allowed': list(chk.constants.archetype.ArchetypeConfigModules.data.keys())
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
