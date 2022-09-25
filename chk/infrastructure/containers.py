"""
Global application functionality
"""
from typing import NamedTuple


class App(NamedTuple):
    """
    Global app container; used to bootstrap global level data structure
    """

    original_doc: dict = {}
    compiled_doc: dict = {}
    display_buffer: dict = {}

    def __str__(self):
        return format(self)