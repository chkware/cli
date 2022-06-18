"""
Validation rules and supporting libs for http module
"""
from chk.modules.test_spec.constants import TestSpecConfigNode, ExecuteConfigNode

execute_schema = {
    ExecuteConfigNode.ROOT: {
        'required': True,
        'empty': False,
        'nullable': False,
        'type': 'dict',
        'schema': {
            ExecuteConfigNode.FILE: {
                'required': False,
                'empty': False,
                'nullable': True,
                'type': 'string',
            },
            ExecuteConfigNode.WITH: {
                'required': False,
                'empty': False,
                'nullable': True,
                'type': 'dict',
            },
            ExecuteConfigNode.RESULT: {
                'required': True,
                'empty': False,
                'nullable': False,
                'type': 'string',
            }
        }
    }
}

test_spec_schema = {
    TestSpecConfigNode.ROOT: {
        'required': True,
        'type': 'dict',
        'schema': {
            TestSpecConfigNode.EXECUTE: {
                'required': False,
                'empty': False,
                'type': 'dict',
                'schema': execute_schema,
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
