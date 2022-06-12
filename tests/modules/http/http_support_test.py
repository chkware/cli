import pytest
import tests

from cerberus import Validator
from chk.infrastructure.file_loader import ChkFileLoader
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

    def test_validate_fail_if_url_empty(self):
        config = {
            'request': {
                'url': None,
                'method': 'GET'
            }
        }

        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = config
            ver.request_validated()

    def test_validate_get_expect_pass(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-Plain.chk')
        ver = HavingRequest()
        ver.document = doc
        assert type(ver.request_validated()) is dict
