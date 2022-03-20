import pytest
import tests
from chk.modules.http.entities import HttpConfigV072
from chk.infrastructure.file_loader import ChkFileLoader


class TestHttpConfigV072:
    """Test chk.archetypes.defaults.http_config.HttpConfigV072"""

    def test_validate_schema(self):
        """when version string not given"""
        config = {
            'version': 'default:http:0.7.2',
            'request': {
                'url': 'https://example.com',
                'method': 'GET'
            }
        }

        ver = HttpConfigV072()
        ver.document = config
        assert ver.validate_config() is True

    def test_validate_fail_if_url_empty(self):
        """when version string not given"""
        config = {
            'version': 'default:http:0.7.2',
            'request': {
                'url': None,
                'method': 'GET'
            }
        }

        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = config
            assert ver.validate_config() is True

    def test_validate_fail_if_url_wrong(self):
        """when version string not given"""
        config = {
            'version': 'default:http:0.7.2',
            'request': {
                'url': 'ftp://example.com/wrong/url.html',
                'method': 'GET'
            }
        }

        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = config
            assert ver.validate_config() is True

    def test_validate_success_with_method(self):
        """when version string not given"""
        config = {
            'version': 'default:http:0.7.2',
            'request': {
                'url': 'https://example.com',
                'method': 'GET'
            }
        }

        ver = HttpConfigV072()
        ver.document = config
        assert ver.validate_config() is True

    def test_validate_fail_if_method_wrong(self):
        """when version string not given"""
        config = {
            'version': 'default:http:0.7.2',
            'request': {
                'url': 'https://example.com',
                'method': 'WRONG'
            }
        }

        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = config
            assert ver.validate_config() is True

    def test_validate_get_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-Plain.chk')
        ver = HttpConfigV072()
        ver.document = doc
        assert ver.validate_config() is True

    def test_validate_get_with_query_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-WithQuery.chk')
        ver = HttpConfigV072()
        ver.document = doc
        assert ver.validate_config() is True

    def test_validate_get_with_query_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithQuery-Empty.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_get_with_query_as_list_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithQuery-AsList.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_get_with_headers_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-WithHeaders.chk')
        ver = HttpConfigV072()
        ver.document = doc
        assert ver.validate_config() is True

    def test_validate_get_with_headers_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithHeaders-Empty.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_get_with_headers_as_list_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithHeaders-AsList.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_get_with_ba_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-WithBasicAuth.chk')
        ver = HttpConfigV072()
        ver.document = doc
        assert ver.validate_config() is True

    def test_validate_get_with_ba_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithBasicAuth-Empty.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_get_with_ba_as_list_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithBasicAuth-AsList.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_get_with_ba_and_be_sametime_expect_fail(self):
        """when basic and bearer auth given same time"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithBasicAuth-AndBearer.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_get_with_be_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-WithBearerAuth.chk')
        ver = HttpConfigV072()
        ver.document = doc
        assert ver.validate_config() is True

    def test_validate_get_with_be_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithBearerAuth-Empty.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_get_with_be_as_list_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithBearerAuth-AsList.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_post_plain_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/POST-Plain.chk')
        ver = HttpConfigV072()

        ver.document = doc
        assert ver.validate_config() is True

    def test_validate_post_with_form_body_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/POST-WithBodyForm.chk')
        ver = HttpConfigV072()

        ver.document = doc
        assert ver.validate_config() is True

    def test_validate_post_with_form_body_as_list_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyForm-AsList.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_post_with_form_body_as_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyForm-Empty.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_post_with_form_data_body_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/POST-WithBodyFormData.chk')
        ver = HttpConfigV072()

        ver.document = doc
        assert ver.validate_config() is True

    def test_validate_post_with_form_data_body_as_list_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyFormData-AsList.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_post_with_form_data_body_as_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyFormData-Empty.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_post_with_json_body_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/POST-WithBodyJson.chk')
        ver = HttpConfigV072()

        ver.document = doc
        assert ver.validate_config() is True

    def test_validate_post_with_json_body_as_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyJson-Empty.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_post_with_xml_body_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/POST-WithBodyXML.chk')
        ver = HttpConfigV072()

        ver.document = doc
        assert ver.validate_config() is True

    def test_validate_post_with_xml_body_as_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyXML-Empty.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True

    def test_validate_post_with_many_body_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithManyBody.chk')
        ver = HttpConfigV072()

        with pytest.raises(SystemExit):
            ver.document = doc
            assert ver.validate_config() is True
