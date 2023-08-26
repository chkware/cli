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
        assert isinstance(asrt.accepted("Nein"), bool)
        assert asrt.accepted("Nein") == False


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


class TestBoolean:
    @staticmethod
    def test_pass_with_actual():
        assert asrt.boolean(True, NotImplemented)
        assert asrt.boolean(False, NotImplemented)

        err = asrt.boolean(1, NotImplemented)
        assert isinstance(err, ValueError)
        assert str(err) == "actual_not_bool"

    @staticmethod
    def test_pass_with_expected():
        assert asrt.boolean(True, True)
        assert asrt.boolean(False, False)

        err = asrt.boolean(True, "NotImplemented")
        assert isinstance(err, ValueError)
        assert str(err) == "expected_not_bool"

        err = asrt.boolean(True, False)
        assert isinstance(err, ValueError)
        assert str(err) == "expected_mismatch"


class TestInteger:
    @staticmethod
    def test_pass_with_actual():
        assert asrt.integer(10)
        assert asrt.integer(-10)
        assert not asrt.integer("-10")


class TestIntegerBetween:
    @staticmethod
    def test_pass_with_actual():
        assert asrt.integer_between(
            10,
            {
                "min": 2,
                "max": 12,
            },
        )
        assert not asrt.integer_between(
            -10,
            {
                "min": 2,
                "max": 12,
            },
        )

        ret = asrt.integer_between("-10", {})
        assert isinstance(ret, ValueError)


class TestIntegerGreater:
    @staticmethod
    def test_pass():
        assert asrt.integer_greater(
            10,
            {
                "other": 2,
            },
        )
        assert not asrt.integer_greater(
            -10,
            {
                "other": 2,
            },
        )

        ret = asrt.integer_greater("-10", {})
        assert isinstance(ret, ValueError)


class TestIntegerGreaterOrEqual:
    @staticmethod
    def test_pass():
        assert asrt.integer_greater_or_equal(
            10,
            {
                "other": 2,
            },
        )
        assert not asrt.integer_greater_or_equal(
            -10,
            {
                "other": 2,
            },
        )

        assert asrt.integer_greater_or_equal(
            2,
            {
                "other": 2,
            },
        )

        ret = asrt.integer_greater_or_equal("-10", {})
        assert isinstance(ret, ValueError)


class TestIntegerLess:
    @staticmethod
    def test_pass():
        assert asrt.integer_less(
            10,
            {
                "other": 12,
            },
        )
        assert not asrt.integer_less(
            10,
            {
                "other": 2,
            },
        )

        ret = asrt.integer_less("-10", {})
        assert isinstance(ret, ValueError)


class TestIntegerLessOrEqual:
    @staticmethod
    def test_pass():
        assert asrt.integer_less_or_equal(
            10,
            {
                "other": 12,
            },
        )
        assert not asrt.integer_less_or_equal(
            10,
            {
                "other": 2,
            },
        )

        assert asrt.integer_less_or_equal(
            2,
            {
                "other": 2,
            },
        )

        ret = asrt.integer_less_or_equal("-10", {})
        assert isinstance(ret, ValueError)


class TestFloat:
    @staticmethod
    def test_pass():
        assert asrt.float_(10.0)
        assert asrt.float_(-10.9)
        assert not asrt.float_(9)
        assert not asrt.float_("-10.2")


class TestFloatBetween:
    @staticmethod
    def test_pass():
        assert asrt.float_between(
            10.9,
            {
                "min": 2,
                "max": 12,
            },
        )
        assert not asrt.float_between(
            -10.9,
            {
                "min": 2,
                "max": 12,
            },
        )
        ret = asrt.float_between(
            10,
            {
                "min": 2,
                "max": 12,
            },
        )

        assert isinstance(ret, ValueError)


class TestFloatGreater:
    @staticmethod
    def test_pass():
        assert asrt.float_greater(
            10.2,
            {
                "other": 2,
            },
        )
        assert not asrt.float_greater(
            -10.2,
            {
                "other": 2,
            },
        )

        ret = asrt.float_greater(10, {})
        assert isinstance(ret, ValueError)


class TestFloatGreaterOrEqual:
    @staticmethod
    def test_pass():
        assert asrt.float_greater_or_equal(
            10.2,
            {
                "other": 2,
            },
        )
        assert not asrt.float_greater_or_equal(
            -10.2,
            {
                "other": 2,
            },
        )

        assert asrt.float_greater_or_equal(
            2.9,
            {
                "other": 2.9,
            },
        )

        ret = asrt.float_greater_or_equal(-10, {})
        assert isinstance(ret, ValueError)


class TestFloatLess:
    @staticmethod
    def test_pass():
        assert asrt.float_less(
            10.0,
            {
                "other": 12,
            },
        )
        assert not asrt.float_less(
            10.0,
            {
                "other": 2,
            },
        )

        ret = asrt.float_less(-10, {})
        assert isinstance(ret, ValueError)


class TestFloatLessOrEqual:
    @staticmethod
    def test_pass():
        assert asrt.float_less_or_equal(
            10.0,
            {
                "other": 12,
            },
        )
        assert not asrt.float_less_or_equal(
            10.0,
            {
                "other": 2,
            },
        )

        assert asrt.float_less_or_equal(
            2.0,
            {
                "other": 2,
            },
        )

        ret = asrt.float_less_or_equal(-1, {})
        assert isinstance(ret, ValueError)


class TestStr:
    @staticmethod
    def test_pass():
        assert asrt.str_("10.0")
        assert asrt.str_("abcd")
        assert not asrt.str_(9)
        assert not asrt.str_(-10.2)


class TestStrHave:
    @staticmethod
    def test_pass():
        assert asrt.str_have("10.0", {"other": "0."})
        assert asrt.str_have("abcd", {"other": "bc"})
        assert isinstance(asrt.str_have(9, {"other": "bc"}), ValueError)
        assert isinstance(asrt.str_have("This", {"other": 2}), ValueError)


class TestStrDoNotHave:
    @staticmethod
    def test_pass():
        assert not asrt.str_do_not_have("10.0", {"other": "0."})
        assert asrt.str_do_not_have("abcd", {"other": "de"})
        assert isinstance(asrt.str_do_not_have(9, {"other": "bc"}), ValueError)
        assert isinstance(asrt.str_do_not_have("This", {"other": 2}), ValueError)


class TestStrStartsWith:
    @staticmethod
    def test_pass():
        assert asrt.str_starts_with("10.0", {"other": "10."})
        assert not asrt.str_starts_with("abcd", {"other": "bc"})
        assert isinstance(asrt.str_starts_with(9, {"other": "bc"}), ValueError)
        assert isinstance(asrt.str_starts_with("This", {"other": 2}), ValueError)


class TestStrDoNotStartsWith:
    @staticmethod
    def test_pass():
        assert asrt.str_do_not_starts_with("10.0", {"other": "0."})
        assert not asrt.str_do_not_starts_with("abcd", {"other": "ab"})
        assert isinstance(asrt.str_do_not_starts_with(9, {"other": "bc"}), ValueError)
        assert isinstance(asrt.str_do_not_starts_with("This", {"other": 2}), ValueError)


class TestStrEndsWith:
    @staticmethod
    def test_pass():
        assert asrt.str_ends_with("10.0", {"other": ".0"})
        assert asrt.str_ends_with("abcd", {"other": "d"})
        assert not asrt.str_ends_with("abcd", {"other": "c"})
        assert isinstance(asrt.str_ends_with(9, {"other": "bc"}), ValueError)
        assert isinstance(asrt.str_ends_with("This", {"other": 2}), ValueError)


class TestStrDoNotEndsWith:
    @staticmethod
    def test_pass():
        assert asrt.str_do_not_ends_with("10.0", {"other": "0."})
        assert asrt.str_do_not_ends_with("abcd", {"other": "ab"})
        assert not asrt.str_do_not_ends_with("abcd", {"other": "d"})
        assert isinstance(asrt.str_do_not_ends_with(9, {"other": "bc"}), ValueError)
        assert isinstance(asrt.str_do_not_ends_with("This", {"other": 2}), ValueError)


class TestDate:
    @staticmethod
    def test_pass():
        assert asrt.date("1972-07-30", {"format": "%Y-%m-%d"})
        assert not asrt.date("1972-30-07", {"format": "%Y-%m-%d"})
        assert not asrt.date("abcd", {"format": "%Y-%m-%d"})
        assert not asrt.date("1972-33-07", {"format": "%Y-%d-%m"})
        assert asrt.date("1972-07", {"format": "%Y-%m"})


class TestDateAfter:
    @staticmethod
    def test_pass():
        assert asrt.date_after("1972-07-30", "1972-07-29", {"format": "%Y-%m-%d"})
        assert not asrt.date_after("1972-07-20", "1972-07-29", {"format": "%Y-%m-%d"})

        ret = asrt.date_after("abcd", "1972-07-29", {"format": "%Y-%m-%d"})
        assert isinstance(ret, ValueError)
        assert str(ret) == "date_conversion_issue"

        ret = asrt.date_after("1972-33-07", "1972-07-29", {"format": "%Y-%d-%m"})
        assert isinstance(ret, ValueError)
        assert str(ret) == "date_conversion_issue"

        assert asrt.date_after("1972-07", "1972-06", {"format": "%Y-%m"})


class TestDateAfterOrEqual:
    @staticmethod
    def test_pass():
        assert asrt.date_after_or_equal(
            "1972-07-30", "1972-07-30", {"format": "%Y-%m-%d"}
        )
        assert asrt.date_after_or_equal(
            "1972-07-30", "1972-07-29", {"format": "%Y-%m-%d"}
        )
        assert not asrt.date_after_or_equal(
            "1972-07-20", "1972-07-29", {"format": "%Y-%m-%d"}
        )

        ret = asrt.date_after_or_equal("abcd", "1972-07-29", {"format": "%Y-%m-%d"})
        assert isinstance(ret, ValueError)
        assert str(ret) == "date_conversion_issue"

        ret = asrt.date_after_or_equal(
            "1972-33-07", "1972-07-29", {"format": "%Y-%d-%m"}
        )
        assert isinstance(ret, ValueError)
        assert str(ret) == "date_conversion_issue"

        assert asrt.date_after_or_equal("1972-07", "1972-06", {"format": "%Y-%m"})


class TestDateBefore:
    @staticmethod
    def test_pass():
        assert asrt.date_before("1972-07-30", "1972-07-31", {"format": "%Y-%m-%d"})
        assert not asrt.date_before("1972-07-30", "1972-07-29", {"format": "%Y-%m-%d"})

        ret = asrt.date_before("abcd", "1972-07-29", {"format": "%Y-%m-%d"})
        assert isinstance(ret, ValueError)
        assert str(ret) == "date_conversion_issue"

        ret = asrt.date_before("1972-33-07", "1972-07-29", {"format": "%Y-%d-%m"})
        assert isinstance(ret, ValueError)
        assert str(ret) == "date_conversion_issue"

        assert asrt.date_before("1972-05", "1972-06", {"format": "%Y-%m"})
