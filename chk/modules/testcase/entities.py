from cerberus import Validator
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.work import (
    WorkerContract,
    RequestProcessorContract,
    handle_request,
)
from chk.infrastructure.exception import err_message

from chk.modules.http.request_helper import RequestProcessorMixin_PyRequests
from chk.modules.http.support import RequestMixin
from chk.modules.testcase.support import TestSpecMixin
from chk.modules.variables.support import VariableMixin
from chk.modules.variables.constants import LexicalAnalysisType
from chk.modules.version.support import VersionMixin
from chk.modules.testcase.presentation import Presentation, AssertResult

from types import MappingProxyType

from chk.modules.version.constants import DocumentType


class TestSpec(
    RequestProcessorMixin_PyRequests,
    VersionMixin,
    RequestMixin,
    VariableMixin,
    TestSpecMixin,
    WorkerContract,
    RequestProcessorContract,
):
    def __init__(self, file_ctx: FileContext):
        self.file_ctx, self.document, self.validator = (
            file_ctx,
            file_ctx.document,
            Validator(),
        )

    def __work__(self) -> None:
        self.version_validated(DocumentType.TESTCASE)
        self.testcase_validated()
        self.variable_validated()

        print(Presentation.displayable_file_info(self.file_ctx))
        print(Presentation.displayable_string(f"Executing spec"))
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
                out_response = handle_request(self, ctx_document)
                print(Presentation.displayable_string(f"- Making request [Success]"))
            except Exception as ex:
                print(Presentation.displayable_string(f"- Making request [Fail]"))
                raise ex

            try:
                request_mut = self.variable_assemble_values(ctx_document, out_response)

                self.document = self.variable_update_symbol_table(
                    ctx_document, MappingProxyType(request_mut)
                )
                self.document = self.variable_process(LexicalAnalysisType.TESTCASE)

                print(
                    Presentation.displayable_string(
                        f"- Process data for assertion [Success]"
                    )
                )
            except Exception as ex:
                print(
                    Presentation.displayable_string(
                        f"- Process data for assertion [Fail]"
                    )
                )
                raise ex

            assertion_results = self.assertion_process()
            for assertion_result in assertion_results:  # type: AssertResult
                print(
                    Presentation.displayable_assert_status(
                        assertion_result.name,
                        "Success" if assertion_result.is_success else "Fail",
                    )
                )

                if assertion_result.is_success is False:
                    print(Presentation.displayable_assert_message(assertion_result.message))
