import abc
import copy
from collections.abc import Callable
from types import MappingProxyType

from cerberus import validator as cer_validator

from chk.infrastructure.contexts import validator
from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import dict_get
from chk.modules.http.constants import RequestConfigNode as RConf
from chk.modules.testcase.support.execute import ExecuteMixin

from chk.modules.testcase.support.assertion import AssertionMixin

from chk.modules.testcase.constants import (
    AssertConfigNode as AtConf,
    TestcaseConfigNode as TstConf, ExecuteConfigNode as ExConf,
)
from chk.modules.testcase.validation_rules import testcase_schema


class TestcaseMixin(ExecuteMixin, AssertionMixin):
    """
    Mixin for Testcase spec
    """

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """Abstract method to get file context"""

    def __init_testcase_mixin(self) -> None:
        self.in_file = True

    def is_request_infile(self) -> bool:
        return self.in_file

    def testcase_validated(self) -> dict[str, str]:
        """
        Validate the schema against config
        """

        try:
            testcase_doc = self.testcase_as_dict()
            if not validator.validate(testcase_doc, testcase_schema):
                raise SystemExit(err_message("fatal.V0006", extra=validator.errors))

            # validate request if it exists in-file
            self.validate_request_block()
            self.validate_with_block()
        except cer_validator.DocumentError as doc_err:
            raise SystemExit(err_message("fatal.V0001", extra=doc_err)) from doc_err

        return testcase_doc  # or is a success

    def testcase_as_dict(self) -> dict[str, str]:
        """Get version string"""

        file_ctx = self.get_file_context()
        document = app.get_original_doc(file_ctx.filepath_hash)

        try:
            return {key: document[key] for key in (TstConf.ROOT,) if key in document}
        except Exception as ex:
            raise SystemExit(err_message("fatal.V0005", extra=ex))

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

    def validate_with_block(self) -> None:
        """
        Check is data passing to same context
        :return: None
        """

        file_ctx = self.get_file_context()
        document = app.get_original_doc(file_ctx.filepath_hash)

        in_file_request = document.get(RConf.ROOT) is not None

        keys = [TstConf.ROOT, ExConf.ROOT, ExConf.WITH]
        out_file_with = dict_get(document, ".".join(keys)) is not None

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
