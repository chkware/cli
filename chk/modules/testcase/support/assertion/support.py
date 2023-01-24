""" Assertion related services """

import uuid
from collections.abc import Callable
from io import StringIO
from typing import Any
from unittest import TestCase, TestSuite, TextTestRunner

from chk.infrastructure.helper import Cast
from chk.modules.testcase.constants import AssertConfigNode
from chk.modules.testcase.presentation import AssertResult


class AssertionCase(TestCase):
    """
    each assertion case
    """

    def __init__(self, name: str, name_run: str, actual: Any, expect: Any):
        """Constructor for AssertionCase"""

        method_name = f"case_{name}"
        method_name_run = f"case_{name_run}"

        setattr(self, method_name_run, getattr(self, method_name))
        super().__init__(method_name_run)

        self.type = type
        self.actual = actual
        self.expect = expect

    def case_AssertEqual(self) -> None:
        """Asserts equality for actual value on expected value"""
        actual = Cast.to_auto(self.actual)

        self.assertEqual(actual, self.expect)

    def case_AssertNotEqual(self) -> None:
        """Asserts equality for actual value on expected value"""
        actual = Cast.to_auto(self.actual)

        self.assertNotEqual(actual, self.expect)

    def case_AssertEmpty(self) -> None:
        """Asserts emptiness for actual value"""
        assert not self.actual, f"`{self.actual}` is not empty"

    def case_AssertFalse(self) -> None:
        """Asserts Falsy for actual value"""
        actual = Cast.to_bool(self.actual)

        self.assertFalse(actual)

    def case_AssertTrue(self) -> None:
        """Asserts truthy for actual value"""
        actual = Cast.to_bool(self.actual)

        self.assertTrue(actual)

    def case_AssertIsInt(self) -> None:
        """Asserts integer for actual value"""
        actual = Cast.to_int(self.actual)

        assert isinstance(actual, int), f"`{self.actual}` is not int"

    def case_AssertIsString(self) -> None:
        """Asserts string for actual value"""

        assert isinstance(self.actual, str), f"`{self.actual}` is not string"

    def case_AssertIsFloat(self) -> None:
        """Asserts float for actual value"""
        actual = Cast.to_float(self.actual)

        assert isinstance(actual, float), f"`{self.actual}` is not floating point"

    def case_AssertIsBool(self) -> None:
        """Asserts boolean for any type"""
        actual = Cast.to_bool(self.actual)

        assert isinstance(actual, bool), f"`{self.actual}` is not boolean"

    def case_AssertIsMap(self) -> None:
        """Asserts map for any value on actual"""
        actual = Cast.to_hashable(self.actual)

        assert isinstance(actual, dict), f"`{self.actual}` is not map"

    def case_AssertIsList(self) -> None:
        """Asserts list for any value on actual"""
        actual = Cast.to_hashable(self.actual)

        assert isinstance(actual, list), f"`{self.actual}` is not list"

    def case_AssertCount(self) -> None:
        """Asserts count of sequence on actual"""
        assert isinstance(self.expect, int), f"`{self.expect}` is not int"

        actual = Cast.to_hashable(self.actual)
        assert hasattr(actual, "__len__"), f"`{self.actual}` is not countable"

        self.assertEqual(len(actual), self.expect)

    def case_AssertGreater(self) -> None:
        """Asserts count of sequence on actual"""
        actual = Cast.to_int_or_float(self.actual)

        assert not isinstance(actual, str), f"`{self.actual}` is not int or float"
        self.assertGreater(actual, self.expect)

    def case_AssertGreaterOrEqual(self) -> None:
        """Asserts count of sequence on actual"""
        actual = Cast.to_int_or_float(self.actual)

        assert not isinstance(actual, str), f"`{self.actual}` is not int or float"
        self.assertGreaterEqual(actual, self.expect)

    def case_AssertLess(self) -> None:
        """Asserts count of sequence on actual"""
        actual = Cast.to_int_or_float(self.actual)

        assert not isinstance(actual, str), f"`{self.actual}` is not int or float"
        self.assertLess(actual, self.expect)

    def case_AssertLessOrEqual(self) -> None:
        """Asserts count of sequence on actual"""
        actual = Cast.to_int_or_float(self.actual)

        assert not isinstance(actual, str), f"`{self.actual}` is not int or float"
        self.assertLessEqual(actual, self.expect)

    def case_AssertListContains(self) -> None:
        """Asserts expected exist in the actual."""
        actual = (
            Cast.to_hashable(self.actual)
            if isinstance(self.actual, str)
            else self.actual
        )

        assert isinstance(actual, list), f"`{self.actual}` is not a list"
        assert self.expect in actual, f"`{self.expect}` is not in the list"

    def case_AssertMapHasKey(self) -> None:
        """Asserts expected key exists in the map."""
        actual = (
            Cast.to_hashable(self.actual)
            if isinstance(self.actual, str)
            else self.actual
        )

        assert isinstance(actual, dict), f"`{self.actual}` is not a map"
        assert self.expect in actual, f"key `{self.expect}` is not in the map"

    def case_AssertMapDoNotHasKey(self) -> None:
        """Asserts expected key does not exist in the map."""
        actual = (
            Cast.to_hashable(self.actual)
            if isinstance(self.actual, str)
            else self.actual
        )

        assert isinstance(actual, dict), f"`{self.actual}` is not a map"
        assert self.expect not in actual, f"key `{self.expect}` is in the map"

    def case_AssertStrContains(self) -> None:
        """Asserts expected is in the actual string."""
        assert isinstance(self.actual, str), f"`{self.actual}` is not a string"
        assert self.expect in self.actual, f"key `{self.expect}` is not in the str"

    def case_AssertMapKeyCount(self) -> None:
        """Asserts expected is equal to the number of keys in the map."""
        actual = (
            Cast.to_hashable(self.actual)
            if isinstance(self.actual, str)
            else self.actual
        )

        assert isinstance(actual, dict), f"`{self.actual}` is not a map"
        assert self.expect == len(actual), f" the map has `{len(self.actual)}` keys"

    def case_AssertMapHasKeys(self) -> None:
        """Asserts expected is a subset of keys of the map."""
        actual = (
            Cast.to_hashable(self.actual)
            if isinstance(self.actual, str)
            else self.actual
        )

        assert isinstance(actual, dict), f"`{self.actual}` is not a map"
        intersection = set(actual.keys()) & set(self.expect)
        assert intersection == set(
            self.expect
        ), f"key(s) `{set(self.expect) - intersection}` not present in the map"

    def case_AssertMapDoNotHasKeys(self) -> None:
        """Asserts expected is not a subset of map keys."""
        actual = (
            Cast.to_hashable(self.actual)
            if isinstance(self.actual, str)
            else self.actual
        )

        assert isinstance(actual, dict), f"`{self.actual}` is not a map"
        intersection = set(actual.keys()) & set(self.expect)
        assert not intersection, f"key(s) `{intersection}` present in the map"

    def case_AssertMapExactKeys(self) -> None:
        """Asserts all keys of the map is present in expected."""
        actual = (
            Cast.to_hashable(self.actual)
            if isinstance(self.actual, str)
            else self.actual
        )

        assert isinstance(actual, dict), f"`{self.actual}` is not a map"
        assert (
            set(actual.keys()) & set(self.expect)
            == set(self.expect)
            == set(actual.keys())
        ), "`key(s) are not exactly matched"

    def case_AssertListHasIndex(self) -> None:
        """Asserts list has `expected` index."""
        actual = (
            Cast.to_hashable(self.actual)
            if isinstance(self.actual, str)
            else self.actual
        )

        assert isinstance(actual, list), f"`{self.actual}` is not a list"
        assert 0 <= self.expect < len(actual), f"`{self.expect}` is an invalid index"

    def case_AssertMapContains(self) -> None:
        """Asserts map contains expected as value"""
        actual = (
            Cast.to_hashable(self.actual)
            if isinstance(self.actual, str)
            else self.actual
        )

        assert isinstance(actual, dict), f"`{self.actual}` is not a map"
        assert self.expect in actual.values(), f"`{self.expect}` is not in the map"


class AssertionHandler:
    """
    AssertionHandler
    """

    @staticmethod
    def asserts_test_run(
        assertions: list, actual_values: dict, replace_values: Callable
    ) -> list[AssertResult]:
        """Process given assertions and run test based on those"""

        suite = TestSuite()
        results = []

        for each_assertion in assertions:
            name_run = f"{each_assertion[AssertConfigNode.TYPE]}_{uuid.uuid1().hex}"
            assert_actual_value = replace_values(
                each_assertion[AssertConfigNode.ACTUAL], actual_values
            )

            suite.addTest(
                AssertionCase(
                    each_assertion[AssertConfigNode.TYPE],
                    name_run,
                    assert_actual_value,
                    each_assertion.get(AssertConfigNode.EXPECTED),
                )
            )

            results.append(
                AssertResult(
                    each_assertion[AssertConfigNode.TYPE],
                    name_run,
                    each_assertion[AssertConfigNode.ACTUAL_ORIG],
                )
            )

        run_result = TextTestRunner(stream=StringIO(), verbosity=0).run(suite)

        if run_result.wasSuccessful() is False:
            for run_result_kind in ("failures", "errors"):
                for (tc, string) in getattr(run_result, run_result_kind):
                    for item in results:
                        if item.name_run in tc.id():
                            item.is_success = False
                            item.message = string
                            item.assert_fn = tc.id()

        return results
