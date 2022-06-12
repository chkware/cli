from cerberus import Validator
from chk.modules.http.support import RequestMixin


class HavingRequest(RequestMixin):
    def __init__(self) -> None:
        self.document, self.validator = None, Validator()        


class TestRequestMixin:
    def test_request_validated_passes(self):
        config = {
            'request': {
                'url': 'https://example.com',
                'method': 'GET'
            }
        }

        ver = HavingRequest()
        ver.document = config
        assert type(ver.request_validated()) is dict
