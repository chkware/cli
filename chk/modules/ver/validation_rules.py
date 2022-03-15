"""
Validation rules and supporting libs for ver module
"""
from chk.modules.ver.constants import VersionStrToSpecConfigMapping

version_schema = {
    'version': {
        'required': True,
        'type': 'string',
        'empty': False,
        'allowed': list(VersionStrToSpecConfigMapping.data.keys())
    }
}
