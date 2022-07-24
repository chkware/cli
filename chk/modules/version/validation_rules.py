"""
Validation rules and supporting libs for version module
"""
from chk.modules.version.constants import VersionStore

version_schema_http = {
    'version': {
        'required': True,
        'type': 'string',
        'empty': False,
        'allowed': VersionStore.request_versions
    }
}

version_schema_testcase = {
    'version': {
        'required': True,
        'type': 'string',
        'empty': False,
        'allowed': VersionStore.testcase_versions
    }
}
