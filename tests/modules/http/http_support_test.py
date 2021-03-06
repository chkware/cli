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

    def test_validate_get_with_query_expect_pass(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-WithQuery.chk')
        ver = HavingRequest()
        ver.document = doc
        assert type(ver.request_validated()) is dict

    def test_validate_get_with_query_empty_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithQuery-Empty.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_get_with_query_as_list_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithQuery-AsList.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_get_with_headers_expect_pass(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-WithHeaders.chk')
        ver = HavingRequest()
        ver.document = doc
        assert type(ver.request_validated()) is dict

    def test_validate_get_with_headers_empty_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithHeaders-Empty.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_get_with_headers_as_list_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithHeaders-AsList.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_get_with_ba_expect_pass(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-WithBasicAuth.chk')
        ver = HavingRequest()
        ver.document = doc
        assert type(ver.request_validated()) is dict

    def test_validate_get_with_ba_empty_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithBasicAuth-Empty.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_get_with_ba_as_list_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithBasicAuth-AsList.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_get_with_ba_and_be_sametime_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithBasicAuth-AndBearer.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_get_with_be_expect_pass(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-WithBearerAuth.chk')
        ver = HavingRequest()
        ver.document = doc
        assert type(ver.request_validated()) is dict

    def test_validate_get_with_be_empty_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithBearerAuth-Empty.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_get_with_be_as_list_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithBearerAuth-AsList.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_post_plain_expect_pass(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/POST-Plain.chk')
        ver = HavingRequest()

        ver.document = doc
        assert type(ver.request_validated()) is dict

    def test_validate_post_with_form_body_expect_pass(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/POST-WithBodyForm.chk')
        ver = HavingRequest()

        ver.document = doc
        assert type(ver.request_validated()) is dict

    def test_validate_post_with_form_body_as_list_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyForm-AsList.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_post_with_form_body_as_empty_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyForm-Empty.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_post_with_form_data_body_expect_pass(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/POST-WithBodyFormData.chk')
        ver = HavingRequest()

        ver.document = doc
        assert type(ver.request_validated()) is dict

    def test_validate_post_with_form_data_body_as_list_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyFormData-AsList.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_post_with_form_data_body_as_empty_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyFormData-Empty.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_post_with_json_body_expect_pass(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/POST-WithBodyJson.chk')
        ver = HavingRequest()

        ver.document = doc
        assert type(ver.request_validated()) is dict

    def test_validate_post_with_json_body_as_empty_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyJson-Empty.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_post_with_xml_body_expect_pass(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-WithBodyXML.chk')
        ver = HavingRequest()

        ver.document = doc
        assert type(ver.request_validated()) is dict

    def test_validate_post_with_xml_body_as_empty_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyXML-Empty.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()

    def test_validate_post_with_many_body_expect_fail(self):
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithManyBody.chk')
        ver = HavingRequest()

        with pytest.raises(SystemExit):
            ver.document = doc
            ver.request_validated()
