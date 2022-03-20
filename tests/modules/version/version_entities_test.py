import pytest
from chk.modules.version.entities import VersionConfigV072


class TestVersionConfigV072:
    def test_validate_config_success(self):
        """when version string given"""
        config = {
            'version': 'default:http:0.7.2'
        }

        ver = VersionConfigV072()
        ver.document = config
        assert ver.validate_config() is True

    def test_validate_config_empty_version(self):
        """when version string not given"""
        config = {
            'version': ''
        }

        ver = VersionConfigV072()
        with pytest.raises(SystemExit):
            ver.document = config
            assert ver.validate_config() is True

    def test_validate_config_fail_non_exist_ver(self):
        """when version string not given"""
        config = {
            'version': 'default:http:0.7'
        }

        ver = VersionConfigV072()
        with pytest.raises(SystemExit):
            ver.document = config
            assert ver.validate_config() is True

    def test_validate_config_fail_no_doc(self):
        """when version string not given"""
        config = {}

        ver = VersionConfigV072()
        with pytest.raises(SystemExit):
            ver.document = config
            assert ver.validate_config() is True

    def test_validate_config_fail_on_none(self):
        """when version string not given"""
        config = None

        ver = VersionConfigV072()
        with pytest.raises(SystemExit):
            ver.document = config
            assert ver.validate_config() is True

    def test_validate_config_fail_no_version(self):
        """when version string not given"""
        config = {
            'request': {
                'url': 'some.url'
            }
        }

        ver = VersionConfigV072()
        with pytest.raises(SystemExit):
            ver.document = config
            assert ver.validate_config() is True
