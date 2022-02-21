"""
Request specification validation schema
"""

version_schema = {
    'version': {
        'required': True,
        'type': 'string'
    }
}

request_schema = {
    'request': {
        'required': True,
        'type': 'dict',
        'schema': {
            'url': {
                'required': True,
                'type': 'string',
            },
            'method': {
                'required': True,
                'type': 'string',
            }
        }
    }
}
