"""test loader"""
import pytest
import tests
from chk.support.loader import ChkFileLoader


class TestChkFileLoader:
    """test ChkFileLoader"""

    def test_to_dict_valid_file(self):
        """test to_dict with valid file"""
        filename = tests.RES_DIR + "UserOk.chk"
        assert type(ChkFileLoader.to_dict(filename)) == dict

    def test_to_dict_invalid_file(self):
        """test with invalid file"""
        filename = tests.RES_DIR + "UserNotOk.chk"
        with pytest.raises(SystemExit):
            assert type(ChkFileLoader.to_dict(filename)) == dict

    def test_is_file_ok_valid_file(self):
        """test is_file_ok with valid existing file"""
        filename = tests.RES_DIR + "UserOk.chk"
        assert ChkFileLoader.is_file_ok(filename) is True

    def test_is_file_ok_invalid_file(self):
        """test to_dict"""
        filename = tests.RES_DIR + "UserOk.yaml"
        assert ChkFileLoader.is_file_ok(filename) is False

    def test_is_file_ok_inexistent_file(self):
        """test to_dict"""
        filename = tests.RES_DIR + "UserOk.yml"
        assert ChkFileLoader.is_file_ok(filename) is False
