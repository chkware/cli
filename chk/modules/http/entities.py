from cerberus import Validator
from chk.infrastructure.work import WorkerContract, ProcessorContract, handle_processor
from chk.modules.http.support import RequestMixin_V072
from chk.modules.version.support import VersionMixin_V072
from chk.modules.http.request_helper import RequestProcessorMixin_PyRequests


class HttpSpec_V072(
    RequestProcessorMixin_PyRequests,
    VersionMixin_V072, RequestMixin_V072,
    WorkerContract, ProcessorContract):

    def __init__(self, doc: dict):
        self.document = doc
        self.validator = Validator()
        self.response = None

    def __before_work__(self) -> None:
        VersionMixin_V072.version_validated(self)
        RequestMixin_V072.request_validated(self)

    def __work__(self) -> None:
        self.response = handle_processor(self, self.document)

    def __after_work__(self):
        pass
