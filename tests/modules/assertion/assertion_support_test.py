import pytest

from chk.modules.assertion.support import AssertionCase


class TestAssertionCase:
    """Tests assertion cases"""

    def test_assert_list_contains_expect_not_exist(self):
        """Tests AssertListContains when expect is not in actual."""
        name = 'AssertListContains'
        name_run = 'AssertListContains_72a688341d4611edb365ebb9b969d060'
        actual = [1, 2, 3]
        expect = 5
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertListContains()

    def test_assert_list_contains_actual_not_list(self):
        """Tests AssertListContains when actual is not a list."""
        name = 'AssertListContains'
        name_run = 'AssertListContains_72a688341d4611edb365ebb9b969d060'
        actual = 'some random int'
        expect = 5
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertListContains()

    def test_assert_map_has_key_expect_not_exist(self):
        """Tests AssertMapHasKey when expect is not in actual."""
        name = 'AssertMapHasKey'
        name_run = 'AssertMapHasKey_72a688341d4611edb365ebb9b969d060'
        actual = {'a': 1, 'b': 2}
        expect = 'd'
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertMapHasKey()

    def test_assert_map_has_key_actual_not_map(self):
        """Tests AsserMapContains when actual is not a map."""
        name = 'AssertMapHasKey'
        name_run = 'AssertMapHasKey_72a688341d4611edb365ebb9b969d060'
        actual = [1, 2, 3]
        expect = 3
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertMapHasKey()


