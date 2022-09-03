"""
Constants used in http modules
"""
from dataclasses import dataclass
from enum import Enum


@dataclass
class VariableConfigNode:
    """
    Represent variables config section
    """
    ROOT = 'variables'
    RETURN = 'return'
    RESULT = 'result'


class LexicalAnalysisType(Enum):
    REQUEST = 1
    TESTCASE = 2
