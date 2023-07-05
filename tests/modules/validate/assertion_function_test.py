# type: ignore

"""
Test module for assertion Functions mod
"""
import chk.modules.validate.assertion_function as asrt


class TestAssertEqual:
    @staticmethod
    def test_equal_pass_with_scaler():
        assert asrt.equal(1, 1)
        assert asrt.equal("abc", "abc")
        assert asrt.equal(3.02, 3.02)
        assert asrt.equal(True, True)
        assert asrt.equal(False, False)

    @staticmethod
    def test_equal_pass_with_collect():
        assert asrt.equal([1], [1])
        assert asrt.equal(["abc"], ["abc"])
        assert asrt.equal({"a": 3.02}, {"a": 3.02})
        assert asrt.equal({"a": 3.02, "b": "c"}, {"a": 3.02, "b": "c"})

    @staticmethod
    def test_equal_fails_with_non_equals():
        response = asrt.equal([1], [2])
        assert isinstance(response, AssertionError)


class TestAssertNotEqual:
    @staticmethod
    def test_equal_pass_with_scaler():
        assert asrt.not_equal(1, 2)
        assert asrt.not_equal("abc", "bac")
        assert asrt.not_equal(3.02, 3.0)
        assert asrt.not_equal(True, "True")
        assert asrt.not_equal(False, "False")

    @staticmethod
    def test_not_equal_pass_with_collect():
        assert asrt.not_equal([1], [2])
        assert asrt.not_equal(["abc"], ["bac"])
        assert asrt.not_equal({"a": 3.02}, {"a": 3.0})
        assert asrt.not_equal({"a": 3.02, "b": "c"}, {"a": 3.02, "b": "d"})

    @staticmethod
    def test_not_equal_fails_with_non_equals():
        response = asrt.not_equal([1], [1])
        assert isinstance(response, AssertionError)
