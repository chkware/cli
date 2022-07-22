"""
Validation rules and supporting libs for version module
"""
from chk.modules.version.constants import VersionStore

version_schema = {
    'version': {
        'required': True,
        'type': 'string',
        'empty': False,
        'allowed': VersionStore.request_versions
    }
}
