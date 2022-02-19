from chk.archetypes.defaults.http_config import V072
import pytest


class TestV072:
    """Test chk.archetypes.defaults.http_config.V072"""
    def test_validate_version_valid(self):
        config = {
            "version": "default:http:0.7.2"
        }
        ver = V072()
        assert ver.validate_version(config) is True

    def test_validate_version_invalid(self):
        config = {
            "version": "default:http:0.7"
        }
        ver = V072()
        with pytest.raises(SystemExit):
            assert ver.validate_version(config) is True

    def test_validate_version_fail_when_empty_version(self):
        config = {
            "version": ""
        }
        ver = V072()
        with pytest.raises(SystemExit):
            assert ver.validate_version(config) is True

    def test_validate_version_fail_when_no_version(self):
        config = {
        }
        ver = V072()
        with pytest.raises(SystemExit):
            assert ver.validate_version(config) is True
