"""
Validation rules and supporting libs for variables module
"""


variable_schema = {  # cerberus validation rules
    'variables': {
        'required': False,
        'type': 'dict',
        'empty': True,
    }
}
