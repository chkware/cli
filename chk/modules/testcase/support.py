"""
testcase related support services
"""
from typing import Callable

from cerberus import validator
from chk.infrastructure.helper import dict_get
from chk.infrastructure.exception import err_message

from chk.modules.assertion.support import AssertionHandler
from chk.modules.http.constants import RequestConfigNode
from chk.modules.testcase.constants import (
    TestcaseConfigNode,
    ExecuteConfigNode,
    AssertConfigNode,
)
from chk.modules.testcase.validation_rules import testcase_schema

from types import MappingProxyType


class ExecuteMixin:
    """
    Mixin for Execute sub-spec
    """

    def execute_as_dict(self) -> dict[str, str]:
        """
        Get execute as dict
        """
        try:
            if spec := self.document.get(TestcaseConfigNode.ROOT):
                if execute := spec.get(ExecuteConfigNode.ROOT):
                    return {ExecuteConfigNode.ROOT: execute}
                else:
                    raise ValueError({"spec": [{"execute": ["required field"]}]})
        except Exception as ex:
            raise SystemExit(err_message("fatal.V0005", extra=ex))


class AssertionMixin:
    """
    Mixin for Execute sub-spec
    """

    def assertions_as_dict(self) -> dict[str, object]:
        """
        Get execute as dict
        """
        try:
            doc_key = [TestcaseConfigNode.ROOT, TestcaseConfigNode.ASSERTS]
            if asserts := dict_get(self.document, ".".join(doc_key)):
                if type(asserts) != list:
                    raise TypeError({"spec": [{"asserts": ["expected `list`"]}]})

                asrt_list = [f"{item.get('type')}.{item.get('actual')}" for item in asserts if type(item) == dict]
                if len(asrt_list) != len(set(asrt_list)):
                    raise TypeError({"spec": [{"asserts": ["duplicate assertion of same value"]}]})

                return {TestcaseConfigNode.ASSERTS: asserts}
            else:
                raise ValueError({"spec": [{"asserts": ["required field"]}]})
        except Exception as ex:
            raise SystemExit(err_message("fatal.V0005", extra=ex))

    def assertion_process(self) -> list:
        """
        Run assertion of testcase spec
        :return:
        """
        assertions = dict_get(self.assertions_as_dict(), TestcaseConfigNode.ASSERTS)
        return AssertionHandler.asserts_test_run(assertions)


class TestcaseMixin(ExecuteMixin, AssertionMixin):
    """
    Mixin for Testcase spec
    """

    def __init_testcase_mixin(self):
        self.in_file = True

    def is_request_infile(self) -> bool:
        return self.in_file

    def testcase_validated(self) -> dict[str, str]:
        """
        Validate the schema against config
        """
        try:
            testcase_doc = self.testcase_as_dict()
            if not self.validator.validate(testcase_doc, testcase_schema):
                raise SystemExit(
                    err_message("fatal.V0006", extra=self.validator.errors)
                )

            # validate request if it exists in-file
            self.validate_request_block()
            self.validate_with_block()
        except validator.DocumentError as doc_err:
            raise SystemExit(err_message("fatal.V0001", extra=doc_err)) from doc_err

        return testcase_doc  # or is a success

    def testcase_as_dict(self) -> dict[str, str]:
        """
        Get version string
        """
        if not hasattr(self, "validator") or not hasattr(self, "document"):
            raise SystemExit(err_message("fatal.V0005"))

        try:
            return {
                key: self.document[key]
                for key in (TestcaseConfigNode.ROOT,)
                if key in self.document
            }
        except Exception as ex:
            raise SystemExit(err_message("fatal.V0005", extra=ex))

    def validate_request_block(self) -> None:
        """
        If request in file validate it or set False to internal in_file
        :return: None
        """
        keys = [TestcaseConfigNode.ROOT, ExecuteConfigNode.ROOT, ExecuteConfigNode.FILE]
        out_file_request = dict_get(self.document, ".".join(keys)) is not None
        in_file_request = self.document.get(RequestConfigNode.ROOT) is not None

        if in_file_request is out_file_request:
            raise SystemExit(
                err_message("fatal.V0020", extra={"spec": {"execute": {"file": "..."}}})
            )

        self.__init_testcase_mixin()

        if in_file_request:
            self.request_validated()
            self.in_file = True
        else:
            self.in_file = False

    def validate_with_block(self) -> None:
        """
        Check is data passing to same context
        :return: None
        """
        in_file_request = self.document.get(RequestConfigNode.ROOT) is not None

        keys = [TestcaseConfigNode.ROOT, ExecuteConfigNode.ROOT, ExecuteConfigNode.WITH]
        out_file_with = dict_get(self.document, ".".join(keys)) is not None

        if in_file_request and out_file_with:
            raise SystemExit(
                err_message(
                    "fatal.V0021", extra={"spec": {"execute": {"with": "Not allowed"}}}
                )
            )


class TestcaseValueHandler:
    """
    Handle variables and values regarding testcase
    """

    @staticmethod
    def assertions_fill_val(
        document: dict, symbol_table: dict, replace_method: Callable[[dict, dict], dict]
    ):
        """Convert request block variables"""

        assertion_document = document.get(AssertConfigNode.ROOT, {})
        import copy

        assertion_document = copy.deepcopy(assertion_document)

        for each_assert in assertion_document:
            actual_original = each_assert[AssertConfigNode.ACTUAL]
            replace_method(each_assert, symbol_table)
            each_assert[f"{AssertConfigNode.ACTUAL}_original"] = actual_original

        return assertion_document

    @staticmethod
    def request_set_result(
        execute_doc: dict, symbol_table: MappingProxyType, request_ret: MappingProxyType
    ) -> dict:
        arg = [ExecuteConfigNode.ROOT, ExecuteConfigNode.RESULT]
        result_replaceable = str(dict_get(execute_doc, ".".join(arg))).strip()

        if result_replaceable.startswith("$"):  # if starts with $ remove it
            result_replaceable = result_replaceable[1:]

        if symbol_table.get(result_replaceable, "##") == "##":  # if key is non-existant
            raise SystemExit(f"Variable `${result_replaceable}` was not declared")

        if request_ret.get("have_all"):
            return {
                result_replaceable: {
                    key: val for key, val in request_ret.items() if key != "have_all"
                }
            }
        else:
            for _, val in request_ret.items():
                if val:
                    return {result_replaceable: val}

        return {}
