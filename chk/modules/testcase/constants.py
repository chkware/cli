"""
Constants used in testcase modules
"""


class TestcaseConfigNode:
    """represent request config section"""

    ROOT = "spec"

    # common request
    EXECUTE = "execute"
    ASSERTS = "asserts"


class ExecuteConfigNode:
    """represent execute config section"""

    ROOT = "execute"
    FILE = "file"
    WITH = "with"
    RESULT = "result"
    LOCAL = "_execution_results"


class AssertConfigNode:
    """represent asserts config section"""

    ROOT = "asserts"
    LOCAL = "_assertion_results"

    TYPE = "type"
    ACTUAL = "actual"
    ACTUAL_ORIG = "actual_original"
    EXPECTED = "expected"
