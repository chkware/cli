"""
Validation rules and supporting libs for http module
"""
from chk.modules.test_spec.constants import TestSpecConfigNode

test_spec_schema = {  # cerberus validation rules
    TestSpecConfigNode.ROOT: {
        'required': True,
        'type': 'dict',
        'schema': {
            TestSpecConfigNode.EXECUTE: {
                'required': False,
                'empty': False,
                'type': 'dict',
            },
            TestSpecConfigNode.ASSERTS: {
                'required': True,
                'empty': False,
                'type': 'list',
                'valuesrules': {'type': 'dict'},
            }
        }
    }
}
