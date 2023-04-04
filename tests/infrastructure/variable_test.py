# type: ignore
"""
Test module for infrastructure.variable module
"""
import types
import pytest

from chk.infrastructure.variable import Variable, LocalVariable


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

    def test_create_with_malformed_str_1_fails(self):
        with pytest.raises(ValueError):
            LocalVariable("__Abc", None)

    def test_create_with_malformed_str_2_fails(self):
        with pytest.raises(ValueError):
            LocalVariable("1Abc", None)

    def test_create_pass(self):
        a = LocalVariable("A_", 1)
        assert a.value == 1
        assert a.value_type == int

    def test_create_is_variable_pass(self):
        a = LocalVariable("A_", 1)
        assert isinstance(a, Variable)
