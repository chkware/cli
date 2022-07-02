"""
Constants used in http modules
"""
from enum import Enum


class VariableConfigNode:
    """represent variable config section"""
    ROOT = 'variables'


class LexicalAnalysisType(Enum):
    REQUEST = 1
