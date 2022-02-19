from chk.archetypes.defaults.http_config import V072


class TestV072:
    """Test chk.archetypes.defaults.http_config.V072"""
    def test_validate_version_valid(self):
        config = {
            "version": "default:http:0.7.2"
        }
        ver = V072()
        assert ver.validate_version(config) is True
