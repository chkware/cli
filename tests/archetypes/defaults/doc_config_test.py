import pytest
import tests
from chk.archetypes.defaults.doc_config import DocV072
from chk.support.loader import ChkFileLoader


class TestDocV072:

    def test_validate_config_success(self):
        """when version string given"""
        filename = tests.RES_DIR + "UserOk.chk"
        config = ChkFileLoader.to_dict(filename)

        ver = DocV072()
        # with pytest.raises(SystemExit):
        assert ver.validate_config(config) is True

    def test_validate_config_fail(self):
        """when version string not given"""
        filename = tests.RES_DIR + "User_EmptyVer.chk"
        config = ChkFileLoader.to_dict(filename)

        ver = DocV072()
        with pytest.raises(SystemExit):
            assert ver.validate_config(config) is True

