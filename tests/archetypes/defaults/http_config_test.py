import pytest
import tests
from chk.archetypes.defaults.http_config import HttpV072
from chk.support.loader import ChkFileLoader


class TestHttpV072:
    """Test chk.archetypes.defaults.http_config.HttpV072"""

    def test_validate_schema(self):
        """when version string not given"""
        config = {
            'version': 'default:http:0.7.2',
            'request': {
                'url': 'https://example.com',
                'method': 'GET'
            }
        }

        ver = HttpV072()
        assert ver.validate_config(config) is True

    def test_validate_fail_if_url_empty(self):
        """when version string not given"""
        config = {
            'version': 'default:http:0.7.2',
            'request': {
                'url': None,
                'method': 'GET'
            }
        }

        ver = HttpV072()

        with pytest.raises(SystemExit) as ex:
            assert ver.validate_config(config) is True

    def test_validate_get_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-Plain.chk')
        ver = HttpV072()
        assert ver.validate_config(doc) is True

    def test_validate_get_with_query_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-WithQuery.chk')
        ver = HttpV072()
        assert ver.validate_config(doc) is True

    def test_validate_get_with_query_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithQuery-Empty.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

    def test_validate_get_with_query_as_list_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithQuery-AsList.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

    def test_validate_get_with_headers_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-WithHeaders.chk')
        ver = HttpV072()
        assert ver.validate_config(doc) is True

    def test_validate_get_with_headers_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithHeaders-Empty.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

    def test_validate_get_with_headers_as_list_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithHeaders-AsList.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

    def test_validate_get_with_ba_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-WithBasicAuth.chk')
        ver = HttpV072()
        assert ver.validate_config(doc) is True

    def test_validate_get_with_ba_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithBasicAuth-Empty.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

    def test_validate_get_with_ba_as_list_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithBasicAuth-AsList.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

    def test_validate_get_with_be_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-WithBearerAuth.chk')
        ver = HttpV072()
        assert ver.validate_config(doc) is True

    def test_validate_get_with_be_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithBearerAuth-Empty.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

    def test_validate_get_with_be_as_list_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithBearerAuth-AsList.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

    def test_validate_post_plain_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/POST-Plain.chk')
        ver = HttpV072()

        assert ver.validate_config(doc) is True

    def test_validate_post_with_form_body_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/POST-WithBodyForm.chk')
        ver = HttpV072()

        assert ver.validate_config(doc) is True

    def test_validate_post_with_form_body_as_list_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyForm-AsList.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

    def test_validate_post_with_form_body_as_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyForm-Empty.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

    def test_validate_post_with_form_data_body_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/POST-WithBodyFormData.chk')
        ver = HttpV072()

        assert ver.validate_config(doc) is True

    def test_validate_post_with_form_data_body_as_list_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyFormData-AsList.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

    def test_validate_post_with_form_data_body_as_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyFormData-Empty.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

    def test_validate_post_with_json_body_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/POST-WithBodyJson.chk')
        ver = HttpV072()

        assert ver.validate_config(doc) is True

    def test_validate_post_with_json_body_as_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyJson-Empty.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

    def test_validate_post_with_xml_body_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/POST-WithBodyXML.chk')
        ver = HttpV072()

        assert ver.validate_config(doc) is True

    def test_validate_post_with_xml_body_as_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/POST-WithBodyXML-Empty.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

