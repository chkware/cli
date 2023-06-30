# type: ignore

"""
Test module for assertion Functions mod
"""
import chk.modules.validate.assertion_function as asrt


class TestAssertEqual:
    @staticmethod
    def test_assert_equal_pass_with_scaler():
        assert asrt.assert_equal(1, 1)[0]
        assert asrt.assert_equal("abc", "abc")[0]
        assert asrt.assert_equal(3.02, 3.02)[0]
        assert asrt.assert_equal(True, True)[0]
        assert asrt.assert_equal(False, False)[0]

    @staticmethod
    def test_assert_equal_pass_with_collect():
        assert asrt.assert_equal([1], [1])[0]
        assert asrt.assert_equal(["abc"], ["abc"])[0]
        assert asrt.assert_equal({"a": 3.02}, {"a": 3.02})[0]
        assert asrt.assert_equal({"a": 3.02, "b": "c"}, {"a": 3.02, "b": "c"})[0]

    @staticmethod
    def test_assert_equal_fails_with_non_equals():
        is_success, response = asrt.assert_equal([1], [2])

        assert not is_success
        assert isinstance(response, AssertionError)

        assert not is_success
        assert isinstance(response, AssertionError)
