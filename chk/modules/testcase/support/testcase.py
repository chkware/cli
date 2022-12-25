"""
Support functions and classes for testcase
"""

import abc

from cerberus import validator as cer_validator

from chk.infrastructure.contexts import validator, app
from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import dict_get
from chk.modules.http.constants import RequestConfigNode as RConf
from chk.modules.testcase.support.execute import ExecuteMixin

from chk.modules.testcase.support.assertion import AssertionMixin

from chk.modules.testcase.constants import (
    TestcaseConfigNode as TstConf,
    ExecuteConfigNode as ExConf,
)
from chk.modules.testcase.validation_rules import testcase_schema


class TestcaseMixin(ExecuteMixin, AssertionMixin):
    """
    Mixin for Testcase spec
    """

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """Abstract method to get file context"""

    def is_request_infile(self) -> bool:
        return isinstance(
            app.get_original_doc(self.get_file_context().filepath_hash).get(RConf.ROOT),
            dict,
        )

    def testcase_validated(self) -> dict:
        """Validate the schema against config"""

        try:
            if not (testcase_doc := self.testcase_as_dict()):
                raise RuntimeError(
                    f"testcase_validated: testcase_doc[{str(testcase_doc)}]"
                )

            if not validator.validate(testcase_doc, testcase_schema):
                raise RuntimeError(err_message("fatal.V0006", extra=validator.errors))

            self.execute_validated()

            # case: spec with no or multiple request
            out_file_request = (
                dict_get(
                    testcase_doc, f"{TstConf.ROOT}.{TstConf.EXECUTE}.{ExConf.FILE}"
                )
                is not None
            )

            if self.is_request_infile() is out_file_request:
                raise RuntimeError(
                    err_message(
                        "fatal.V0020", extra={"spec": {"execute": {"file": "..."}}}
                    )
                )

            # case: spec.execute.with having request is not allowed
            if self.is_request_infile() and dict_get(
                testcase_doc, f"{TstConf.ROOT}.{TstConf.EXECUTE}.{ExConf.WITH}"
            ):
                raise RuntimeError(
                    err_message(
                        "fatal.V0021",
                        extra={
                            TstConf.ROOT: {
                                TstConf.EXECUTE: {ExConf.WITH: "Not allowed"}
                            }
                        },
                    )
                )

            # case: spec.execute.result having request is not allowed
            # TODO: at least for now: may be in future

            if self.is_request_infile() and dict_get(
                testcase_doc, f"{TstConf.ROOT}.{TstConf.EXECUTE}.{ExConf.RESULT}"
            ):
                raise RuntimeError(
                    err_message(
                        "fatal.V0021",
                        extra={
                            TstConf.ROOT: {
                                TstConf.EXECUTE: {ExConf.RESULT: "Not allowed"}
                            }
                        },
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
