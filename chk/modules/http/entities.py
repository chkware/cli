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
        print(HttpSpec_V072.__mro__)
        print('HttpSpec_V072::__before_work__')

        # super(VersionMixin_V072, self).validated()
        # print('after: VersionMixin_V072.validated')
        # super(RequestMixin_V072, self).validated()
        # print('after: RequestMixin_V072.validated')

        # VersionMixin_V072.validated(self)
        # print('after: VersionMixin_V072.validated')
        # RequestMixin_V072.validated(self)
        # print('after: RequestMixin_V072.validated')

        super().validated()

    def __work__(self) -> None:
        print('HttpSpec_V072::__work__')
        self.response = handle_processor(self, self.document)

    def __after_work__(self):
        pass
