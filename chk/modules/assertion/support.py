"""
Assertion related services
"""
from io import StringIO
from unittest import TestCase, TestSuite, TextTestRunner

from chk.console.helper import type_converter
from chk.modules.testcase.presentation import AssertResult, AssertResultList
from chk.modules.testcase.constants import AssertConfigNode

import uuid


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

    def case_AssertEmpty(self):
        """Asserts emptiness for actual value"""
        if self.actual:
            raise AssertionError(f"`{self.actual}` is not empty")

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
        actual = type_converter(self.actual)
        if type(actual) != int:
            raise AssertionError(f"`{self.actual}` is not int")

    def case_AssertIsString(self):
        """Asserts string for actual value"""
        actual = type_converter(self.actual)
        if type(actual) != str:
            raise AssertionError(f"`{self.actual}` is not string")

    def case_AssertIsFloat(self):
        """Asserts float for actual value"""
        actual = type_converter(self.actual)
        if type(actual) != float:
            raise AssertionError(f"`{self.actual}` is not floating point")

    def case_AssertIsBool(self):
        """Asserts boolean for any type"""
        actual = type_converter(self.actual)
        if type(actual) != bool:
            raise AssertionError(f"`{self.actual}` is not boolean")

    def case_AssertIsMap(self):
        """Asserts map for any value on actual"""
        actual = type_converter(self.actual)
        if type(actual) != dict:
            raise AssertionError(f"`{self.actual}` is not map")

    def case_AssertIsList(self):
        """Asserts list for any value on actual"""
        actual = type_converter(self.actual)
        if type(actual) != list:
            raise AssertionError(f"`{self.actual}` is not list")

    def case_AssertCount(self):
        """Asserts count of sequence on actual"""
        if type(self.expect) != int:
            raise AssertionError(f"`{self.expect}` is not int")

        actual = type_converter(self.actual)
        if not hasattr(actual, '__len__'):
            raise AssertionError(f"`{self.actual}` is not countable")

        self.assertEqual(len(actual), self.expect)

    def case_AssertGreater(self):
        """Asserts count of sequence on actual"""
        actual = type_converter(self.actual)
        self.assertGreater(actual, self.expect)


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

        if run_result.wasSuccessful() is False:
            for run_result_kind in ["failures", "errors"]:
                for (tc, string) in getattr(run_result, run_result_kind):
                    for item in results:
                        if item.name_run in tc.id():
                            item.is_success = False
                            item.message = string
                            item.assert_fn = tc.id()


        return results
