from cerberus import Validator
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.work import WorkerContract, ProcessorContract, handle_processor
from chk.modules.http.request_helper import RequestProcessorMixin_PyRequests
from chk.modules.http.support import RequestMixin
from chk.modules.variables.support import VariableMixin_V072
from chk.modules.version.support import VersionMixin


class HttpSpec_V072(
    RequestProcessorMixin_PyRequests,
    VersionMixin,
    RequestMixin,
    VariableMixin_V072,
    WorkerContract,
    ProcessorContract,
):

    def __init__(self, file_ctx: FileContext):
        self.file_ctx, self.document, self.validator, self.response = file_ctx, file_ctx.document, Validator(), None

    def __work__(self) -> None:
        VersionMixin.version_validated(self)
        RequestMixin.request_validated(self)
        VariableMixin_V072.variable_validated(self)

        ctx_document = VariableMixin_V072.variable_process(self)
        self.response = handle_processor(self, ctx_document)
