"""
Assertion related services
"""
from io import StringIO
from unittest import TestCase, TestSuite, TextTestRunner, TestResult

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
        """
        asserts equals for any type
        """
        self.assertEqual(self.actual, self.expect)

    def case_AssertEmpty(self):
        """
        asserts emptiness for any type
        """
        if self.actual:
            raise AssertionError(f"`{self.actual}` is not empty")

    def case_AssertFalse(self):
        """
        asserts emptiness for any type
        """
        self.assertFalse(self.actual)

    def case_AssertTrue(self):
        """
        asserts emptiness for any type
        """
        self.assertTrue(self.actual)

    def case_AssertIsInt(self):
        """
        asserts emptiness for any type
        """
        if type(self.actual) != int:
            raise AssertionError(f"`{self.actual}` is not int")

    def case_AssertIsString(self):
        """
        asserts emptiness for any type
        """
        if type(self.actual) != str:
            raise AssertionError(f"`{self.actual}` is not string")


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

        if run_result.wasSuccessful():
            return results

        for (tc, string) in run_result.failures:
            for item in results:
                if item.name_run in tc.id():
                    item.is_success = False
                    item.message = string
                    item.assert_fn = tc.id()

        return results
