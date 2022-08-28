"""
Global application functionality
"""
from dataclasses import dataclass


@dataclass
class App:
    """
    Global app container; used to bootstrap global level data structure
    """

    documents = {
        "original": {},
        "compiled": {},
    }

    variables = {}
    display_buffer = {}
