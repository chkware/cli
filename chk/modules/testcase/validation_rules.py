"""
Validation rules and supporting libs for http module
"""
from chk.modules.testcase.constants import TestcaseConfigNode, ExecuteConfigNode

execute_schema = {
    ExecuteConfigNode.ROOT: {
        "required": False,
        "empty": True,
        "nullable": True,
        "type": "dict",
        "schema": {
            ExecuteConfigNode.FILE: {
                "required": False,
                "empty": True,
                "nullable": True,
                "type": "string",
            },
            ExecuteConfigNode.WITH: {
                "required": False,
                "empty": False,
                "nullable": True,
                "type": "dict",
            },
            ExecuteConfigNode.RESULT: {
                "required": False,
                "empty": True,
                "nullable": True,
                "type": "list",
                "valuesrules": {"type": "string"},
            },
        },
    }
}

testcase_schema = {
    TestcaseConfigNode.ROOT: {
        "required": True,
        "type": "dict",
        "schema": execute_schema
        | {
            TestcaseConfigNode.ASSERTS: {
                "required": True,
                "empty": False,
                "type": "list",
                "valuesrules": {"type": "dict"},
            }
        },
    }
}
