# type: ignore
"""
Test module for main
"""

import click
import pytest

from chk.console.main import combine_initial_variables


class TestLoadVariablesAsDict:
    @staticmethod
    def test_fail_with_default_except_message():
        external_vars = "a"

        with pytest.raises(click.UsageError, match="JSON loading error."):
            combine_initial_variables(external_vars)

    @staticmethod
    def test_fail_with_default_given_message():
        external_vars = "a"

        with pytest.raises(click.UsageError, match="except_msg"):
            combine_initial_variables(
                external_vars,
                except_msg="except_msg",
            )


class TestCombineInitialVariables:
    @staticmethod
    def test_pass():
        external_vars = '{"a": 1, "b": ["A", {"c": 3}]}'
        dct = combine_initial_variables(external_vars)

        assert isinstance(dct, dict)

    @staticmethod
    def test_fail_for_invalid_json():
        external_vars = "a"

        with pytest.raises(click.UsageError, match="JSON loading error."):
            combine_initial_variables(external_vars)
