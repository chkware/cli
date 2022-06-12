from cerberus import Validator
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.work import WorkerContract, RequestProcessorContract, handle_request
from chk.modules.http.request_helper import RequestProcessorMixin_PyRequests
from chk.modules.http.support import RequestMixin
from chk.modules.variables.support import VariableMixin
from chk.modules.version.support import VersionMixin


class HttpSpec_V072(
    RequestProcessorMixin_PyRequests,
    VersionMixin,
    RequestMixin,
    VariableMixin,
    WorkerContract,
    RequestProcessorContract
):

    def __init__(self, file_ctx: FileContext):
        self.file_ctx, self.document, self.validator = file_ctx, file_ctx.document, Validator()

    def __work__(self) -> dict:
        VersionMixin.version_validated(self)
        RequestMixin.request_validated(self)
        VariableMixin.variable_validated(self)

        ctx_document = VariableMixin.variable_process(self)
        out_response = handle_request(self, ctx_document)
        return VariableMixin.assemble_values(self, ctx_document, out_response)
