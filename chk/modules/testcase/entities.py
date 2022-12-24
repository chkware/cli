"""
Entities for testcase document specification
"""
from chk.infrastructure.contexts import app
from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.work import WorkerContract
from chk.modules.assertion.support import AssertionHandler
from chk.modules.testcase.presentation import Presentation
from chk.modules.variables.lexicon import StringLexicalAnalyzer

from chk.modules.version.support import VersionMixin

from chk.modules.variables.entities import (
    DefaultVariableDoc,
    DefaultExposableDoc,
    ApiResponse,
)
from chk.modules.variables.support import VariableMixin, replace_values

from chk.modules.http.constants import RequestConfigNode as RConst
from chk.modules.http.request_helper import RequestProcessorPyRequests
from chk.modules.http.support import RequestMixin

from chk.modules.testcase.support.testcase import TestcaseMixin


class Testcase(
    VersionMixin,
    RequestMixin,
    VariableMixin,
    TestcaseMixin,
    WorkerContract,
):
    def __init__(self, file_ctx: FileContext):
        app.config("buffer_access_off", bool(file_ctx.options["result"]))
        self.file_ctx = file_ctx
        app.print_fmt(
            f"File: {file_ctx.filepath}\r\n",
            ret_s=bool(app.config("buffer_access_off")),
        )

    def get_file_context(self) -> FileContext:
        return self.file_ctx

    def __before_main__(self) -> None:
        """Validate and prepare doc components"""

        # save original doc
        app.load_original_doc_from_file_context(self.file_ctx)

        # validation
        version_doc = self.version_validated()
        testcase_doc = self.testcase_validated()

        request_doc = {}
        if self.is_request_infile():
            request_doc = self.request_validated()  # case: validate in-file request

        variable_doc = self.variable_validated()
        expose_doc = self.expose_validated()

        app.set_compiled_doc(
            self.file_ctx.filepath_hash,
            (
                version_doc
                | DefaultVariableDoc().merged(variable_doc)
                | DefaultExposableDoc({"expose": ["_response"]}).merged(expose_doc)
                | request_doc
                | testcase_doc
            ),
        )

    def __main__(self) -> None:
        """Process document"""

        # execute process
        if self.is_request_infile():
            self.variable_prepare_value_table()
            self.lexical_analysis_for_request(self.get_symbol_table(), replace_values)

            try:
                request_doc = self.request_as_dict(with_key=False, compiled=True)
                if not isinstance(request_doc, dict):
                    raise RuntimeError("error: request doc malformed")

                response = RequestProcessorPyRequests.perform(request_doc)

                app.set_local(
                    self.file_ctx.filepath_hash,
                    ApiResponse.from_dict(response).dict(),  # type: ignore
                    RConst.LOCAL,
                )

                app.print_fmt(
                    "- Making request [Success]",
                    ret_s=bool(app.config("buffer_access_off")),
                )
            except RuntimeError as err:
                app.print_fmt(
                    "- Making request [Fail]",
                    ret_s=bool(app.config("buffer_access_off")),
                )
                raise err

        else:
            # this is a temporary situation
            # TODO: support file linking; remove this message
            raise RuntimeError(
                err_message(
                    "fatal.V0029",
                    extra={"spec": {"execute": {"file": "External file linked"}}},
                )
            )

        try:
            self.assertion_preserve_original()
            assertions = self.assertions_as_dict(with_key=False, compiled=True)

            if not isinstance(assertions, list):
                raise RuntimeError

            assertion_results = AssertionHandler.asserts_test_run(
                assertions, self.get_symbol_table(), StringLexicalAnalyzer.replace
            )

            app.print_fmt(
                "- Process data for assertion [Success]",
                ret_s=bool(app.config("buffer_access_off")),
            )

        except RuntimeError as err:
            app.print_fmt(
                "- Process data for assertion [Fail]",
                ret_s=bool(app.config("buffer_access_off")),
            )
            raise err

        for assertion_result in assertion_results:
            print(
                Presentation.displayable_assert_status(
                    assertion_result.name,
                    assertion_result.actual_original,
                    "Success" if assertion_result.is_success else "Fail",
                )
            )

            if assertion_result.is_success is False:
                print(Presentation.displayable_assert_message(assertion_result.message))

    def __after_main__(self) -> dict:
        return {}
