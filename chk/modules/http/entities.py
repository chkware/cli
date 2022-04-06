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
        self.file_ctx = file_ctx
        self.document = file_ctx.document
        self.validator = Validator()
        self.response = None

    def __work__(self) -> None:
        VersionMixin_V072.version_validated(self)
        RequestMixin_V072.request_validated(self)
        VariableMixin_V072.variable_validated(self)

        self.response = handle_processor(self, self.document)
