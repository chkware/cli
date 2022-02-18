"""test loader"""
import pytest

from chk.support.loader import ChkFileLoader


class TestChkFileLoader:
    """test ChkFileLoader"""

    def test_to_dict_valid_file(self):
        """test to_dict"""
        filename = "./tests/resources/storage/sample_config/UserOk.chk"
        assert type(ChkFileLoader.to_dict(filename)) == dict

    def test_to_dict_invalid_file(self):
        """test to_dict"""
        filename = "./tests/resources/storage/sample_config/UserNotOk.chk"
        with pytest.raises(SystemExit):
            assert type(ChkFileLoader.to_dict(filename)) == dict
