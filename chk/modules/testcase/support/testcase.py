"""
Support functions and classes for testcase
"""

import abc
import copy
from collections.abc import Callable
from types import MappingProxyType

from cerberus import validator as cer_validator

from chk.infrastructure.contexts import validator, app
from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import dict_get
from chk.modules.http.constants import RequestConfigNode as RConf
from chk.modules.http.support import RequestMixin
from chk.modules.testcase.support.execute import ExecuteMixin

from chk.modules.testcase.support.assertion import AssertionMixin

from chk.modules.testcase.constants import (
    AssertConfigNode as AtConf,
    TestcaseConfigNode as TstConf,
    ExecuteConfigNode as ExConf,
)
from chk.modules.testcase.validation_rules import testcase_schema


class TestcaseMixin(RequestMixin, ExecuteMixin, AssertionMixin):
    """
    Mixin for Testcase spec
    """

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """Abstract method to get file context"""

    def __init_testcase_mixin(self) -> None:
        self.in_file = True

    def is_request_infile(self) -> bool:
        return isinstance(
            app.get_original_doc(self.get_file_context().filepath_hash).get(RConf.ROOT),
            dict,
        )

    def testcase_validated(self) -> dict:
        """Validate the schema against config"""

        try:
            testcase_doc = self.testcase_as_dict()
            if not validator.validate(testcase_doc, testcase_schema):
                raise RuntimeError(err_message("fatal.V0006", extra=validator.errors))

            # case: spec with no request
            if not self.is_request_infile() and not dict_get(
                testcase_doc, f"{TstConf.ROOT}.{TstConf.EXECUTE}.{ExConf.FILE}"
            ):
                raise RuntimeError(err_message("fatal.V0006", extra="No request found"))

            # case: spec.execute.with having request is not allowed
            if self.is_request_infile() and dict_get(
                testcase_doc, f"{TstConf.ROOT}.{TstConf.EXECUTE}.{ExConf.WITH}"
            ):
                raise RuntimeError(
                    err_message(
                        "fatal.V0021",
                        extra={"spec": {"execute": {"with": "Not allowed"}}},
                    )
                )

        except cer_validator.DocumentError as doc_err:
            raise RuntimeError(err_message("fatal.V0001", extra=doc_err)) from doc_err

        return testcase_doc if isinstance(testcase_doc, dict) else {}

    def testcase_as_dict(
        self, with_key: bool = True, compiled: bool = False
    ) -> dict | None:
        """Get testcase as a dictionary"""

        return self.as_dict(TstConf.ROOT, with_key, compiled)

    def validate_request_block(self) -> None:
        """
        If request in file validate it or set False to internal in_file
        :return: None
        """

        file_ctx = self.get_file_context()
        document = app.get_original_doc(file_ctx.filepath_hash)

        keys = [TstConf.ROOT, ExConf.ROOT, ExConf.FILE]
        out_file_request = dict_get(document, ".".join(keys)) is not None
        in_file_request = document.get(RConf.ROOT) is not None

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


class TestcaseValueHandler:
    """
    Handle variables and values regarding testcase
    """

    @staticmethod
    def assertions_fill_val(
        document: dict, symbol_table: dict, replace_method: Callable[[dict, dict], dict]
    ):
        """Convert request block variables"""

        assertion_document = document.get(AtConf.ROOT, {})
        assertion_document = copy.deepcopy(assertion_document)

        for each_assert in assertion_document:
            actual_original = each_assert[AtConf.ACTUAL]
            replace_method(each_assert, symbol_table)
            each_assert[f"{AtConf.ACTUAL}_original"] = actual_original

        return assertion_document

    @staticmethod
    def request_set_result(
        execute_doc: dict, symbol_table: MappingProxyType, request_ret: MappingProxyType
    ) -> dict:
        arg = [ExConf.ROOT, ExConf.RESULT]
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
