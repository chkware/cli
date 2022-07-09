from cerberus import Validator
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.work import WorkerContract, RequestProcessorContract, handle_request
from chk.infrastructure.exception import err_message

from chk.modules.http.request_helper import RequestProcessorMixin_PyRequests
from chk.modules.http.support import RequestMixin
from chk.modules.testcase.support import TestSpecMixin
from chk.modules.variables.support import VariableMixin
from chk.modules.variables.constants import LexicalAnalysisType
from chk.modules.version.support import VersionMixin

from types import MappingProxyType


class TestSpec(
    RequestProcessorMixin_PyRequests,
    VersionMixin,
    RequestMixin,
    VariableMixin,
    TestSpecMixin,
    WorkerContract,
    RequestProcessorContract
):

    def __init__(self, file_ctx: FileContext):
        self.file_ctx, self.document, self.validator = file_ctx, file_ctx.document, Validator()

    def __work__(self) -> None:
        self.version_validated()
        self.testcase_validated()
        self.variable_validated()

        ctx_document = {}

        if self.is_request_infile():
            ctx_document = self.variable_process(LexicalAnalysisType.REQUEST)
        else:
            # this is a temporary situation
            # TODO: support file linking; remove this message
            raise SystemExit(err_message('fatal.V0029', extra={'spec': {'execute': {'file': 'External file linked'}}}))

        if ctx_document:
            out_response = handle_request(self, ctx_document)
            request_mut = self.variable_assemble_values(ctx_document, out_response)

            self.document = self.variable_update_symbol_table(ctx_document, MappingProxyType(request_mut))
            self.assertion_process()

        exit(0)


# validation
# spec execution
# spec assertion
# spec return_preparation
