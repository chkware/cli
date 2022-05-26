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
        self.file_ctx, self.document, self.validator, self.response = file_ctx, file_ctx.document, Validator(), None

    def __work__(self) -> None:
        VersionMixin.version_validated(self)
        RequestMixin.request_validated(self)
        VariableMixin.variable_validated(self)

        ctx_document = VariableMixin.variable_process(self)
        self.response = handle_request(self, ctx_document)
