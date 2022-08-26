"""
Assertion related services
"""
import uuid
from io import StringIO
from unittest import TestCase, TestSuite, TextTestRunner

from chk.console.helper import type_converter
from chk.modules.testcase.constants import AssertConfigNode
from chk.modules.testcase.presentation import AssertResult, AssertResultList


class AssertionCase(TestCase):
    """
    each assertion case
    """

    def __init__(self, name: str, name_run: str, actual, expect):
        """
        constructor for AssertionCase
        """
        method_name = f"case_{name}"
        method_name_run = f"case_{name_run}"

        setattr(self, method_name_run, getattr(self, method_name))
        super(AssertionCase, self).__init__(method_name_run)

        self.type = type
        self.actual = actual
        self.expect = expect

    def case_AssertEqual(self):
        """Asserts equality for actual value on expected value"""
        actual = type_converter(self.actual)

        self.assertEqual(actual, self.expect)

    def case_AssertNotEqual(self):
        """Asserts equality for actual value on expected value"""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        self.assertNotEqual(actual, self.expect)

    def case_AssertEmpty(self):
        """Asserts emptiness for actual value"""
        assert not self.actual, f"`{self.actual}` is not empty"

    def case_AssertFalse(self):
        """Asserts Falsy for actual value"""
        actual = type_converter(self.actual)

        self.assertFalse(actual)

    def case_AssertTrue(self):
        """Asserts truthy for actual value"""
        actual = type_converter(self.actual)

        self.assertTrue(actual)

    def case_AssertIsInt(self):
        """Asserts integer for actual value"""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        assert type(actual) == int, f"`{self.actual}` is not int"

    def case_AssertIsString(self):
        """Asserts string for actual value"""
        # actual = type_converter(self.actual)
        assert type(self.actual) == str, f"`{self.actual}` is not string"

    def case_AssertIsFloat(self):
        """Asserts float for actual value"""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        assert type(actual) == float, f"`{self.actual}` is not floating point"

    def case_AssertIsBool(self):
        """Asserts boolean for any type"""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        assert type(actual) == bool, f"`{self.actual}` is not boolean"

    def case_AssertIsMap(self):
        """Asserts map for any value on actual"""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        assert type(actual) == dict, f"`{self.actual}` is not map"

    def case_AssertIsList(self):
        """Asserts list for any value on actual"""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        assert type(actual) == list, f"`{self.actual}` is not list"

    def case_AssertCount(self):
        """Asserts count of sequence on actual"""
        assert type(self.expect) == int, f"`{self.expect}` is not int"

        actual = type_converter(self.actual)
        assert hasattr(actual, '__len__'), f"`{self.actual}` is not countable"

        self.assertEqual(len(actual), self.expect)

    def case_AssertGreater(self):
        """Asserts count of sequence on actual"""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        self.assertGreater(actual, self.expect)

    def case_AssertGreaterOrEqual(self):
        """Asserts count of sequence on actual"""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        self.assertGreaterEqual(actual, self.expect)

    def case_AssertLess(self):
        """Asserts count of sequence on actual"""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        self.assertLess(actual, self.expect)

    def case_AssertLessOrEqual(self):
        """Asserts count of sequence on actual"""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        self.assertLessEqual(actual, self.expect)

    def case_AssertListContains(self):
        """Asserts expected exist in the actual."""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        assert type(actual) == list, f"`{self.actual}` is not a list"
        assert self.expect in actual, f"`{self.expect}` is not in the list"

    def case_AssertMapHasKey(self):
        """Asserts expected key exists in the map."""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        assert type(actual) == dict, f"`{self.actual}` is not a map"
        assert self.expect in actual, f"key `{self.expect}` is not in the map"

    def case_AssertMapDoNotHasKey(self):
        """Asserts expected key does not exist in the map."""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        assert type(actual) == dict, f"`{self.actual}` is not a map"
        assert self.expect not in actual, f"key `{self.expect}` is in the map"

    def case_AssertStrContains(self):
        """Asserts expected is in the actual string."""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        assert type(actual) == str, f"`{self.actual}` is not a string"
        assert self.expect in actual, f"key `{self.expect}` is not in the str"

    def case_AssertMapKeyCount(self):
        """Asserts expected is equal to the number of keys in the map."""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        assert type(actual) == dict, f"`{self.actual}` is not a map"
        assert self.expect == len(actual), f" the map has `{len(self.actual)}` keys"

    def case_AssertMapHasKeys(self):
        """Asserts expected is a subset of keys of the map."""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        assert type(actual) == dict, f"`{self.actual}` is not a map"
        intersection = set(actual.keys()) & set(self.expect)
        assert intersection == set(self.expect), f"key(s) `{set(self.expect) - intersection}` not present in the map"

    def case_AssertMapDoNotHasKeys(self):
        """Asserts expected is not a subset of map keys."""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        assert type(actual) == dict, f"`{self.actual}` is not a map"
        intersection = set(actual.keys()) & set(self.expect)
        assert not intersection, f"key(s) `{intersection}` present in the map"

    def case_AssertMapExactKeys(self):
        """Asserts all keys of the map is present in expected."""
        actual = type_converter(self.actual) if type(self.actual) == str else self.actual

        assert type(actual) == dict, f"`{self.actual}` is not a map"
        assert set(actual.keys()) & set(self.expect) == set(self.expect) == set(actual.keys()), f"`key(s) are not exactly matched"


class AssertionHandler:
    """
    AssertionHandler
    """

    @staticmethod
    def asserts_test_run(assertions: list) -> AssertResultList:
        """
        Process given assertions and run test based on those
        :param assertions: list of passed assertions
        :return:
        """

        suite = TestSuite()
        results = []

        for each_assertion in assertions:
            name_run = f"{each_assertion[AssertConfigNode.TYPE]}_{uuid.uuid1().hex}"

            suite.addTest(
                AssertionCase(
                    each_assertion[AssertConfigNode.TYPE],
                    name_run,
                    each_assertion[AssertConfigNode.ACTUAL],
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

        # print('---')
        # print('run_result.wasSuccessful(): ', run_result.wasSuccessful())
        # print('run_result.failures: ', run_result.failures)
        # print('run_result.errors: ', run_result.errors)
        # print('---')

        if run_result.wasSuccessful() is False:
            for run_result_kind in ["failures", "errors"]:
                for (tc, string) in getattr(run_result, run_result_kind):
                    for item in results:
                        if item.name_run in tc.id():
                            item.is_success = False
                            item.message = string
                            item.assert_fn = tc.id()

        return results
