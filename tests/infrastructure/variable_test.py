# type: ignore
"""
Test module for infrastructure.variable module
"""
import types

from chk.infrastructure.variable import LocalVariable


class TestLocalVariableCreation:
    """Create tests"""

    def test_create_with_none_passes(self):
        a = LocalVariable("A", None)
        assert not a.value
        assert a.value_type is types.NoneType

    def test_create_with_blank_str_passes(self):
        a = LocalVariable("A", "")
        assert a.value == ""
        assert a.value_type == str
