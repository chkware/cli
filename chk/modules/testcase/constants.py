"""
Constants used in testcase modules
"""


class TestSpecConfigNode:
    """represent request config section"""
    ROOT = 'spec'

    # common request
    EXECUTE = 'execute'
    ASSERTS = 'asserts'


class ExecuteConfigNode:
    """represent request config section"""
    ROOT = 'execute'
    FILE = 'file'
    WITH = 'with'
    RESULT = 'result'
