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

    def test_assert_map_has_key_passed(self):
        """Tests AssertMapHasKey when expect in actual."""
        name = 'AssertMapHasKey'
        name_run = 'AssertMapHasKey_72a688341d4611edb365ebb9b969d060'
        actual = {'a': 1, 'b': 2}
        expect = 'b'
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        assert assertion_case.case_AssertMapHasKey() is None

    def test_assert_map_has_key_failed(self):
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

    def test_assert_map_do_not_has_key_expect_exist(self):
        """Tests AssertMapDoNotHasKey when expect is in the actual."""
        name = 'AssertMapDoNotHasKey'
        name_run = 'AssertMapDoNotHasKey_72a688341d4611edb365ebb9b969d060'
        actual = {'a': 1, 'b': 2}
        expect = 'a'
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertMapDoNotHasKey()

    def test_assert_map_do_not_has_key_not_map(self):
        """Tests AssertMapDoNotHasKey when actual is not a map."""
        name = 'AssertMapDoNotHasKey'
        name_run = 'AssertMapDoNotHasKey_72a688341d4611edb365ebb9b969d060'
        actual = [1, 2, 3]
        expect = 3
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertMapDoNotHasKey()

    def test_assert_str_contains_expect_not_exist(self):
        """Tests AssertStrContains when expect is not in the actual."""
        name = 'AssertStrContains'
        name_run = 'AssertStrContains_72a688341d4611edb365ebb9b969d060'
        actual = 'https://someurl.com'
        expect = 'not_exists'
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertStrContains()

    def test_assert_str_contains_actual_not_str(self):
        """Tests AssertStrContains when actual is not a string."""
        name = 'AssertStrContains'
        name_run = 'AssertStrContains_72a688341d4611edb365ebb9b969d060'
        actual = 123456
        expect = '3'
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertStrContains()

    def test_assert_map_key_count_valid(self):
        """Tests AssertMapKeyCount with valid params."""
        name = 'AssertMapKeyCount'
        name_run = 'AssertMapKeyCount_72a688341d4611edb365ebb9b969d060'
        actual = {'a': 1, 'b': 2}
        expect = 2
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        assert assertion_case.case_AssertMapKeyCount() is None

    def test_assert_map_key_count_invalid(self):
        """Tests AssertMapKeyCount with invalid params."""
        name = 'AssertMapKeyCount'
        name_run = 'AssertMapKeyCount_72a688341d4611edb365ebb9b969d060'
        actual = {'a': 1, 'b': 2}
        expect = 4
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertMapKeyCount()

    def test_assert_map_has_keys_passed(self):
        """Tests AssertMapHasKeys when actual keys contain expect."""
        name = 'AssertMapHasKeys'
        name_run = 'AssertMapHasKeys_72a688341d4611edb365ebb9b969d060'
        actual = {'a': 1, 'b': 2}
        expect = ['a', 'b']
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        assert assertion_case.case_AssertMapHasKeys() is None

    def test_assert_map_has_keys_failed(self):
        """Tests AssertMapHasKeys when actual keys do not contain expect."""
        name = 'AssertMapHasKeys'
        name_run = 'AssertMapHasKeys_72a688341d4611edb365ebb9b969d060'
        actual = {'a': 1, 'b': 2}
        expect = ['a', 'c']
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertMapHasKeys()

    def test_assert_map_do_not_has_keys_passed(self):
        """Tests AssertMapDoNotHasKeys when expect does not contain a key of actual."""
        name = 'AssertMapDoNotHasKeys'
        name_run = 'AssertMapDoNotHasKeys_72a688341d4611edb365ebb9b969d060'
        actual = {'a': 1, 'b': 2}
        expect = ['d', 'c']
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        assert assertion_case.case_AssertMapDoNotHasKeys() is None

    def test_assert_map_do_not_has_keys_failed(self):
        """Tests AssertMapDoNotHasKeys when expect contains a key of actual."""
        name = 'AssertMapDoNotHasKeys'
        name_run = 'AssertMapDoNotHasKeys_72a688341d4611edb365ebb9b969d060'
        actual = {'a': 1, 'b': 2}
        expect = ['a', 'c']
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertMapDoNotHasKeys()

    def test_assert_map_exact_keys_passed(self):
        """Tests AssertMapExactKeys when map has exactly same keys as expect."""
        name = 'AssertMapExactKeys'
        name_run = 'AssertMapExactKeys_72a688341d4611edb365ebb9b969d060'
        actual = {'a': 1, 'b': 2}
        expect = ['a', 'b']
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        assert assertion_case.case_AssertMapExactKeys() is None

    def test_assert_map_exact_keys_failed(self):
        """Tests AssertMapExactKeys when map has exactly same keys as expect."""
        name = 'AssertMapExactKeys'
        name_run = 'AssertMapExactKeys_72a688341d4611edb365ebb9b969d060'
        actual = {'a': 1, 'b': 2}
        expect = ['a']
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertMapExactKeys()

    def test_assert_list_has_index_passed(self):
        """Tests AssertListHasIndex expected index is present."""
        name = 'AssertListHasIndex'
        name_run = 'AssertListHasIndex_72a688341d4611edb365ebb9b969d060'
        actual = [1, 2, 3, 4, 5]
        expect = 4
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        assert assertion_case.case_AssertListHasIndex() is None

    def test_assert_list_has_index_overflow(self):
        """Tests AssertListHasIndex expected index greater than the len of the list."""
        name = 'AssertListHasIndex'
        name_run = 'AssertListHasIndex_72a688341d4611edb365ebb9b969d060'
        actual = [1, 2, 3, 4, 5]
        expect = 5
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertListHasIndex()

    def test_assert_list_has_index_underflow(self):
        """Tests AssertListHasIndex expected index is negative."""
        name = 'AssertListHasIndex'
        name_run = 'AssertListHasIndex_72a688341d4611edb365ebb9b969d060'
        actual = [1, 2, 3, 4, 5]
        expect = -1
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertListHasIndex()

    def test_assert_map_contains_int(self):
        """Tests AssertMapContains when expect is an integer"""
        name = 'AssertMapContains'
        name_run = 'AssertMapContains_72a688341d4611edb365ebb9b969d060'
        actual = {'a': 1, 'b': 2}
        expect = 1
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        assert assertion_case.case_AssertMapContains() is None

    def test_assert_map_contains_list(self):
        """Tests AssertMapContains when expect is a list"""
        name = 'AssertMapContains'
        name_run = 'AssertMapContains_72a688341d4611edb365ebb9b969d060'
        actual = {'a': [1, 2], 'b': 2}
        expect = [1, 2]
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        assert assertion_case.case_AssertMapContains() is None

    def test_assert_map_contains_map(self):
        """Tests AssertMapContains when expect is a map"""
        name = 'AssertMapContains'
        name_run = 'AssertMapContains_72a688341d4611edb365ebb9b969d060'
        actual = {"a": {"foo": "bar"}, "b": 2}
        expect = {"foo": "bar"}
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        assert assertion_case.case_AssertMapContains() is None

    def test_assert_map_contains_failed(self):
        """Tests AssertMapContains when expect not in the map"""
        name = 'AssertMapContains'
        name_run = 'AssertMapContains_72a688341d4611edb365ebb9b969d060'
        actual = {"a": {"foo": "bar"}, "b": 2}
        expect = [1, 3]
        assertion_case = AssertionCase(
            name=name,
            name_run=name_run,
            actual=actual,
            expect=expect
        )
        with pytest.raises(AssertionError):
            assertion_case.case_AssertMapContains()
