# type: ignore

"""
Test module for assertion Functions mod
"""
import pytest

import chk.modules.validate.assertion_function as asrt


class TestEqual:
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
        assert isinstance(response, bool)


class TestNotEqual:
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
        assert isinstance(response, bool)


class TestAccepted:
    @staticmethod
    def test_pass_with_allowed_values():
        assert asrt.accepted("YES")
        assert asrt.accepted("yes")
        assert asrt.accepted("Yes")
        assert asrt.accepted("ON")
        assert asrt.accepted("on")
        assert asrt.accepted("On")
        assert asrt.accepted(1)
        assert asrt.accepted(True)
        assert asrt.accepted("True")
        assert asrt.accepted("TRUE")
        assert asrt.accepted("true")

    @staticmethod
    def test_pass_with_not_allowed_values():
        assert not asrt.accepted("no")
        assert not asrt.accepted("NO")
        assert not asrt.accepted("No")
        assert not asrt.accepted("off")
        assert not asrt.accepted("OFF")
        assert not asrt.accepted("Off")
        assert not asrt.accepted(0)
        assert not asrt.accepted(False)
        assert not asrt.accepted("False")
        assert not asrt.accepted("FALSE")
        assert not asrt.accepted("false")

    @staticmethod
    def test_fail_with_exception_other_values():
        assert isinstance(asrt.accepted("Nein"), ValueError)


class TestDeclined:
    @staticmethod
    def test_pass_with_allowed_values():
        assert asrt.declined("no")
        assert asrt.declined("NO")
        assert asrt.declined("No")
        assert asrt.declined("off")
        assert asrt.declined("OFF")
        assert asrt.declined("Off")
        assert asrt.declined(0)
        assert asrt.declined(False)
        assert asrt.declined("False")
        assert asrt.declined("FALSE")
        assert asrt.declined("false")

    @staticmethod
    def test_pass_with_not_allowed_values():
        assert not asrt.declined("YES")
        assert not asrt.declined("yes")
        assert not asrt.declined("Yes")
        assert not asrt.declined("ON")
        assert not asrt.declined("on")
        assert not asrt.declined("On")
        assert not asrt.declined(1)
        assert not asrt.declined(True)
        assert not asrt.declined("True")
        assert not asrt.declined("TRUE")
        assert not asrt.declined("true")

    @staticmethod
    def test_fail_with_exception_other_values():
        assert isinstance(asrt.declined("Nein"), ValueError)


class TestEmpty:
    @staticmethod
    def test_pass_with_allowed_values():
        assert asrt.empty("")
        assert asrt.empty(None)
        assert asrt.empty(False)
        assert asrt.empty(0)
        assert asrt.empty([])
        assert asrt.empty({})
        assert asrt.empty(())

    @staticmethod
    def test_pass_with_not_allowed_values():
        assert not asrt.empty("YES")
        assert not asrt.empty(True)
        assert not asrt.empty(1)
        assert not asrt.empty([1])
        assert not asrt.empty({"a": 1})
        assert not asrt.empty((2, 3))


class TestNotEmpty:
    @staticmethod
    def test_pass_with_allowed_values():
        assert asrt.not_empty("YES")
        assert asrt.not_empty(True)
        assert asrt.not_empty(1)
        assert asrt.not_empty([1])
        assert asrt.not_empty({"a": 1})
        assert asrt.not_empty((2, 3))

    @staticmethod
    def test_pass_with_not_allowed_values():
        assert not asrt.not_empty("")
        assert not asrt.not_empty(None)
        assert not asrt.not_empty(False)
        assert not asrt.not_empty(0)
        assert not asrt.not_empty([])
        assert not asrt.not_empty({})
        assert not asrt.not_empty(())
