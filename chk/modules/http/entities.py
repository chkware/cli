from cerberus import Validator
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.work import WorkerContract, ProcessorContract, handle_processor
from chk.modules.http.request_helper import RequestProcessorMixin_PyRequests
from chk.modules.http.support import RequestMixin_V072
from chk.modules.variables.support import VariableMixin_V072
from chk.modules.version.support import VersionMixin_V072


class HttpSpec_V072(
    RequestProcessorMixin_PyRequests,
    VersionMixin_V072, RequestMixin_V072, VariableMixin_V072,
    WorkerContract, ProcessorContract):

    def __init__(self, file_ctx: FileContext):
        self.file_ctx, self.document, self.validator, self.response = file_ctx, file_ctx.document, Validator(), None
        self._variable_space: dict[str, object] = {}

    def __work__(self) -> None:
        VersionMixin_V072.version_validated(self)
        RequestMixin_V072.request_validated(self)
        VariableMixin_V072.variable_validated(self)

        ctx_document = VariableMixin_V072.variable_process(self)
        self.response = handle_processor(self, ctx_document)
