"""
Entities for testcase document specification
"""
from chk.infrastructure.contexts import app
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.work import WorkerContract

from chk.modules.testcase.support.assertion.support import AssertionHandler

from chk.modules.http.constants import RequestConfigNode as RConst
from chk.modules.http.main import execute
from chk.modules.http.request_helper import RequestProcessorPyRequests
from chk.modules.http.support import RequestMixin

from chk.modules.testcase.constants import (
    AssertConfigNode as AConst,
    ExecuteConfigNode as ExConst,
)
from chk.modules.testcase.support.testcase import TestcaseMixin

from chk.modules.variables.lexicon import StringLexicalAnalyzer
from chk.modules.variables.entities import (
    DefaultVariableDoc,
    DefaultExposableDoc,
    ApiResponse,
)
from chk.modules.variables.support import VariableMixin, replace_values

from chk.modules.version.support import VersionMixin


class Testcase(
    VersionMixin,
    RequestMixin,
    VariableMixin,
    TestcaseMixin,
    WorkerContract,
):
    def __init__(self, file_ctx: FileContext):
        self.file_ctx = file_ctx

    def get_file_context(self) -> FileContext:
        return self.file_ctx

    def __before_main__(self) -> None:
        """Validate and prepare doc components"""

        # save original doc
        app.load_original_doc_from_file_context(self.file_ctx)
        app.print_fmt(
            f"File: {self.file_ctx.filepath}\r\n",
            ret_s=bool(app.config(self.file_ctx.filepath_hash, "result")),
        )

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
                | DefaultExposableDoc({"expose": ["$_assertion_results"]}).merged(
                    expose_doc
                )
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
                    ret_s=bool(app.config(self.file_ctx.filepath_hash, "result")),
                )
            except RuntimeError as err:
                app.print_fmt(
                    "- Making request [Fail]",
                    ret_s=bool(app.config(self.file_ctx.filepath_hash, "result")),
                )
                raise err

        else:
            response = self.execute_out_file(execute)
            if isinstance(response, RuntimeError):
                raise response

            if not isinstance(response, list):
                raise RuntimeError("Malformed response")

            self.execute_prepare_results(response)
            result_val = app.get_local(self.file_ctx.filepath_hash, ExConst.LOCAL)

            execute_doc = self.execute_as_dict(with_key=False, compiled=True)

            if not isinstance(execute_doc, dict):
                raise TypeError("execute_validated: invalid execute spec")

            if ExConst.RESULT not in execute_doc:
                app.set_local(self.file_ctx.filepath_hash, None, RConst.LOCAL)

                self.variable_replace_value_table(
                    app.compiled_doc[self.file_ctx.filepath_hash]["__local"],
                    result_val,
                )
            else:
                self.variable_replace_value_table(
                    app.compiled_doc[self.file_ctx.filepath_hash]["variables"],
                    result_val,
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
                ret_s=bool(app.config(self.file_ctx.filepath_hash, "result")),
            )

        except RuntimeError as err:
            app.print_fmt(
                "- Process data for assertion [Fail]",
                ret_s=bool(app.config(self.file_ctx.filepath_hash, "result")),
            )
            raise err

        app.set_local(self.file_ctx.filepath_hash, assertion_results, AConst.LOCAL)

    def __after_main__(self) -> list:
        try:
            self.make_exposable()
            app.print_fmt(
                "- Prepare exposable [Success]",
                ret_s=bool(app.config(self.file_ctx.filepath_hash, "result")),
            )
            app.print_fmt(
                "\r\n---", ret_s=bool(app.config(self.file_ctx.filepath_hash, "result"))
            )

            return self.get_exposable()
        except RuntimeError as err:
            app.print_fmt(
                "- Prepare exposable [Fail]",
                ret_s=bool(app.config(self.file_ctx.filepath_hash, "result")),
            )
            raise err
