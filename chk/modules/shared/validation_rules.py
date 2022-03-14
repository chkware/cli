"""
Validation rules and supporting libs for shared module
"""
from chk.modules.shared.constants import VersionStrToSpecConfigMapping

version_schema = {
    'version': {
        'required': True,
        'type': 'string',
        'empty': False,
        'allowed': list(VersionStrToSpecConfigMapping.data.keys())
    }
}
