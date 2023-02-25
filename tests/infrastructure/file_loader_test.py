# type: ignore

"""test loader"""
import sys
from types import MappingProxyType
from pathlib import Path

import pytest
import tests

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
        file_path = tests.RES_DIR + "bitcoin-usd.chk"
        ctx = FileContext.from_file(file_path)

        if sys.platform.startswith("win"):
            file_path = file_path.replace("/", "\\")

        assert isinstance(ctx, FileContext)
        assert file_path.lstrip(".") in ctx.filepath

        assert len(ctx.options) == 0
        assert isinstance(ctx.options, MappingProxyType)

        assert len(ctx.arguments) == 0
        assert isinstance(ctx.arguments, MappingProxyType)

    def test_from_file_pass_with_opt_set(self):
        file_path = tests.RES_DIR + "bitcoin-usd.chk"
        ctx = FileContext.from_file(file_path, options={"result": False})

        if sys.platform.startswith("win"):
            file_path = file_path.replace("/", "\\")

        assert isinstance(ctx, FileContext)
        assert file_path.lstrip(".") in ctx.filepath

        assert len(ctx.options) == 1
        assert not ctx.options["result"]

        assert len(ctx.arguments) == 0
        assert isinstance(ctx.arguments, MappingProxyType)

    def test_from_file_pass_with_opt_arg_set(self):
        file_path = tests.RES_DIR + "bitcoin-usd.chk"
        ctx = FileContext.from_file(
            file_path, options={"result": False}, arguments={"variables": {"var": 1}}
        )

        if sys.platform.startswith("win"):
            file_path = file_path.replace("/", "\\")

        assert isinstance(ctx, FileContext)
        assert file_path.lstrip(".") in ctx.filepath

        assert len(ctx.options) == 1
        assert not ctx.options["result"]

        assert len(ctx.arguments) == 1
        assert isinstance(ctx.arguments["variables"], dict)
        assert ctx.arguments["variables"]["var"] == 1


class TestPathFrom:
    """Test PathResolver"""

    @staticmethod
    def test_absolute_pass():
        ctx = FileContext.from_file(tests.RES_DIR + "bitcoin-usd.chk")
        p = PathFrom(Path(ctx.filepath))

        path_1 = "tests/resources/storage/sample_config/bitcoin-usd-testcase-data.chk"
        path_2 = "tests/resources/storage/sample_config/some-folder/bitcoin-usd-testcase-data.chk"
        path_3 = "tests/resources/storage/bitcoin-usd-testcase-data.chk"
        path_4 = "tests/resources/storage/some-folder/bitcoin-usd-testcase-data.chk"

        if sys.platform.startswith("win"):
            path_1 = path_1.replace("/", "\\")
            path_2 = path_2.replace("/", "\\")
            path_3 = path_3.replace("/", "\\")
            path_4 = path_4.replace("/", "\\")

        assert path_1 in p.absolute("./bitcoin-usd-testcase-data.chk")
        assert path_2 in p.absolute("./some-folder/bitcoin-usd-testcase-data.chk")
        assert path_3 in p.absolute("./../bitcoin-usd-testcase-data.chk")
        assert path_1 in p.absolute("./some-folder/../bitcoin-usd-testcase-data.chk")
        assert path_3 in p.absolute("../some-folder/../bitcoin-usd-testcase-data.chk")
        assert path_4 in p.absolute("../some-folder/./bitcoin-usd-testcase-data.chk")
        assert path_2 in p.absolute("./some-folder////bitcoin-usd-testcase-data.chk")
