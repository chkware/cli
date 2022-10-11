import pytest

from chk.modules.variables.validation_rules import allowed_variable_name


class TestAllowedVariableName:
    def test_leading_dunder_fail(self):
        with pytest.raises(ValueError):
            assert allowed_variable_name('__var') is True

    def test_trailing_dunder_fail(self):
        with pytest.raises(ValueError):
            assert allowed_variable_name('var__') is True

    def test_success(self):
        assert allowed_variable_name('POT') is True
