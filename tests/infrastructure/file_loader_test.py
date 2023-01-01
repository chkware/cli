# type: ignore

"""test loader"""

import pytest
import tests

from pathlib import Path
from chk.infrastructure.file_loader import ChkFileLoader, FileContext, PathFrom


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
        with pytest.raises(SystemExit):
            assert ChkFileLoader.is_file_ok(filename) is False

    def test_is_file_ok_inexistent_file(self):
        """test to_dict"""
        filename = tests.RES_DIR + "UserOk.yml"
        with pytest.raises(SystemExit):
            assert ChkFileLoader.is_file_ok(filename) is False


class TestFileContext:
    def test_from_file_pass(self):
        file = tests.RES_DIR + "bitcoin-usd.chk"
        ctx = FileContext.from_file(file, {})

        assert isinstance(ctx, FileContext)


class TestPathFrom:
    """Test PathResolver"""

    @staticmethod
    def test_absolute_pass():
        file = tests.RES_DIR + "bitcoin-usd.chk"
        ctx = FileContext.from_file(file, {})

        p = PathFrom(Path(ctx.filepath))
        assert (
            p.absolute("./bitcoin-usd-testcase-data.chk")
            == "/Users/mlbdmba21/Works/chkware/cli/tests/resources/storage/sample_config/bitcoin-usd-testcase-data.chk"
        )

        assert (
            p.absolute("./some-folder/bitcoin-usd-testcase-data.chk")
            == "/Users/mlbdmba21/Works/chkware/cli/tests/resources/storage/sample_config/some-folder/bitcoin-usd-testcase-data.chk"
        )

        assert (
            p.absolute("./../bitcoin-usd-testcase-data.chk")
            == "/Users/mlbdmba21/Works/chkware/cli/tests/resources/storage/bitcoin-usd-testcase-data.chk"
        )

        assert (
            p.absolute("./some-folder/../bitcoin-usd-testcase-data.chk")
            == "/Users/mlbdmba21/Works/chkware/cli/tests/resources/storage/sample_config/bitcoin-usd-testcase-data.chk"
        )

        assert (
            p.absolute("../some-folder/../bitcoin-usd-testcase-data.chk")
            == "/Users/mlbdmba21/Works/chkware/cli/tests/resources/storage/bitcoin-usd-testcase-data.chk"
        )

        assert (
            p.absolute("../some-folder/./bitcoin-usd-testcase-data.chk")
            == "/Users/mlbdmba21/Works/chkware/cli/tests/resources/storage/some-folder/bitcoin-usd-testcase-data.chk"
        )

        assert (
            p.absolute("./some-folder////bitcoin-usd-testcase-data.chk")
            == "/Users/mlbdmba21/Works/chkware/cli/tests/resources/storage/sample_config/some-folder/bitcoin-usd-testcase-data.chk"
        )
