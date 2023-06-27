# type: ignore

"""
Test module for assertion Functions mod
"""
import chk.modules.validate.assertion_function as asrt


class TestAssertEquals:
    @staticmethod
    def test_assert_equals_pass_with_scaler():
        assert asrt.assert_equals(1, 1)
        assert asrt.assert_equals("abc", "abc")
        assert asrt.assert_equals(3.02, 3.02)
        assert asrt.assert_equals(True, True)
        assert asrt.assert_equals(False, False)

    @staticmethod
    def test_assert_equals_pass_with_collect():
        assert asrt.assert_equals([1], [1])
        assert asrt.assert_equals(["abc"], ["abc"])
        assert asrt.assert_equals({"a": 3.02}, {"a": 3.02})
        assert asrt.assert_equals({"a": 3.02, "b": "c"}, {"a": 3.02, "b": "c"})
