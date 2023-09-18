# type: ignore
"""
Test module for main
"""
import click
import pytest

from chk.console.main import combine_initial_variables


class TestCombineInitialVariables:
    @staticmethod
    def test_pass():
        external_vars = '{"a": 1, "b": ["A", {"c": 3}]}'
        dct = combine_initial_variables(external_vars)

        assert isinstance(dct, dict)
        assert "_ENV" in dct

    @staticmethod
    def test_fail_for_invalid_json():
        external_vars = "a"

        with pytest.raises(click.UsageError, match="JSON loading error."):
            combine_initial_variables(external_vars)
