"""
Assertion related services
"""
from io import StringIO
from unittest import TestCase, TestSuite, TextTestRunner, TestResult

from chk.modules.testcase.presentation import AssertResult, AssertResultList
from chk.modules.testcase.constants import AssertConfigNode


class AssertionCase(TestCase):
    def __init__(self, name: str, actual, expect):
        super(AssertionCase, self).__init__(f"case_{name}")
        self.type = type
        self.actual = actual
        self.expect = expect

    def case_AssertEqual(self):
        self.assertEqual(self.actual, self.expect)


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
            suite.addTest(
                AssertionCase(
                    each_assertion[AssertConfigNode.TYPE],
                    each_assertion[AssertConfigNode.ACTUAL],
                    each_assertion[AssertConfigNode.EXPECTED],
                )
            )

            results.append(AssertResult(each_assertion["type"]))

        run_result = TextTestRunner(stream=StringIO(), verbosity=0).run(suite)

        if run_result.wasSuccessful():
            return results

        for (tc, string) in run_result.failures:
            for item in results:
                if item.name in tc.id():
                    item.is_success = False
                    item.message = string
                    item.assert_fn = tc.id()

        return results
