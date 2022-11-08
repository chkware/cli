from types import MappingProxyType

from chk.infrastructure.contexts import app
from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import dict_get
from chk.infrastructure.work import WorkerContract

from chk.modules.version.support import VersionMixin

from chk.modules.variables.entities import ApiResponse
from chk.modules.variables.support import VariableMixin
from chk.modules.variables.constants import LexicalAnalysisType

from chk.modules.http.request_helper import RequestProcessorPyRequests
from chk.modules.http.support import RequestMixin

from chk.modules.testcase.support.testcase import TestcaseMixin
from chk.modules.testcase.presentation import Presentation, AssertResult


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
        # print(app)

        # validation
        self.version_validated()
        self.testcase_validated()
        self.variable_validated()
        self.expose_validated()

    def __main__(self) -> None:
        """Process document"""

        ctx_document = {}

        if self.is_request_infile():
            ctx_document = self.variable_process(LexicalAnalysisType.REQUEST)
        else:
            # this is a temporary situation
            # TODO: support file linking; remove this message
            raise SystemExit(
                err_message(
                    "fatal.V0029",
                    extra={"spec": {"execute": {"file": "External file linked"}}},
                )
            )

        if ctx_document:
            try:
                out_response = RequestProcessorPyRequests.perform(
                    dict_get(ctx_document, "request")
                )
                out_response = ApiResponse.from_dict(out_response).dict()

                print(Presentation.displayable_string("- Making request [Success]"))
            except Exception as ex:
                print(Presentation.displayable_string("- Making request [Fail]"))
                raise ex

            try:
                request_mut = self.variable_assemble_values(ctx_document, out_response)
                document = self.variable_update_symbol_table(
                    ctx_document, MappingProxyType(request_mut)
                )
                self.document = self.variable_process(
                    LexicalAnalysisType.TESTCASE, dict_get(document, "variables")
                )

                print(
                    Presentation.displayable_string(
                        "- Process data for assertion [Success]"
                    )
                )
            except Exception as ex:
                print(
                    Presentation.displayable_string(
                        "- Process data for assertion [Fail]"
                    )
                )
                raise ex

            assertion_results = self.assertion_process()
            for assertion_result in assertion_results:  # type: AssertResult
                print(
                    Presentation.displayable_assert_status(
                        assertion_result.name,
                        assertion_result.actual_original,
                        "Success" if assertion_result.is_success else "Fail",
                    )
                )

                if assertion_result.is_success is False:
                    print(
                        Presentation.displayable_assert_message(
                            assertion_result.message
                        )
                    )

    def __after_main__(self) -> dict:
        return {}
