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
            }
        }
    }
}
