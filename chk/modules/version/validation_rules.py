"""
Validation rules and supporting libs for version module
"""
from chk.modules.version.constants import VersionStrToSpecConfigMapping

version_schema = {
    'version': {
        'required': True,
        'type': 'string',
        'empty': False,
        'allowed': list(VersionStrToSpecConfigMapping.data.keys())
    }
}
