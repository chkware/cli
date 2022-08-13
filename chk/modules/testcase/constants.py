"""
Constants used in testcase modules
"""


class TestSpecConfigNode:
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


class AssertConfigNode:
    """represent asserts config section"""

    ROOT = "asserts"
    TYPE = "type"
    ACTUAL = "actual"
    ACTUAL_ORIG = "actual_original"
    EXPECTED = "expected"
