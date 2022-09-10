"""
Global application functionality
"""
from dataclasses import dataclass, field


@dataclass
class App:
    """
    Global app container; used to bootstrap global level data structure
    """
    documents = {
        "original": field(default_factory=dict),
        "compiled": field(default_factory=dict),
    }

    variables: dict = field(default_factory=dict)
    display_buffer: dict = field(default_factory=dict)
