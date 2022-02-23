import pytest
import tests
from chk.archetypes.defaults.doc_config import DocV072
from chk.support.loader import ChkFileLoader


class TestDocV072:
    def test_validate_config_success(self):
        """when version string given"""
        config = {
            'version': 'default:http:0.7.2'
        }

        ver = DocV072()
        assert ver.validate_config(dict(config)) is True

    def test_validate_config_empty_version(self):
        """when version string not given"""
        config = {
            'version': ''
        }

        ver = DocV072()
        with pytest.raises(SystemExit):
            assert ver.validate_config(config) is True

    def test_validate_config_fail_non_exist_ver(self):
        """when version string not given"""
        config = {
            'version': 'default:http:0.7'
        }

        ver = DocV072()
        with pytest.raises(SystemExit):
            assert ver.validate_config(config) is True

    def test_validate_config_fail_no_doc(self):
        """when version string not given"""
        config = {}

        ver = DocV072()
        with pytest.raises(SystemExit):
            assert ver.validate_config(config) is True

    def test_validate_config_fail_on_none(self):
        """when version string not given"""
        config = None

        ver = DocV072()
        with pytest.raises(SystemExit):
            assert ver.validate_config(config) is True

    def test_validate_config_fail_no_version(self):
        """when version string not given"""
        config = {
            'request': {
                'url': 'some.url'
            }
        }

        ver = DocV072()
        with pytest.raises(SystemExit):
            assert ver.validate_config(config) is True
