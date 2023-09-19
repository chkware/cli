# type: ignore

"""test loader"""
import sys
from pathlib import Path

import pytest
import tests

from chk.infrastructure.file_loader import (
    FileContext,
    PathFrom,
    FileLoader,
)
from chk.infrastructure.typing_extras import JsonDecodingError


class TestFileContext:
    def test_from_file_pass(self):
        file_path = tests.RES_DIR + "bitcoin-usd.chk"
        ctx = FileContext.from_file(file_path)

        if sys.platform.startswith("win"):
            file_path = file_path.replace("/", "\\")

        assert isinstance(ctx, FileContext)
        assert file_path.lstrip(".") in ctx.filepath

        assert len(ctx.options) == 0
        assert isinstance(ctx.options, dict)

        assert len(ctx.arguments) == 0
        assert isinstance(ctx.arguments, dict)

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
        assert isinstance(ctx.arguments, dict)

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

    def test_from_file_pass_with_doc(self):
        file_path = tests.RES_DIR + "bitcoin-usd.chk"
        ctx = FileContext.from_file(
            file_path, options={"result": False}, arguments={"variables": {"var": 1}}
        )

        if sys.platform.startswith("win"):
            file_path = file_path.replace("/", "\\")

        assert isinstance(ctx, FileContext)

        assert ctx.document == FileLoader.load_yaml(file_path)


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


FILE_PATH = "tests/resources/storage/sample_config/"


class TestFileLoaderIsFileOk:
    """Create tests"""

    def test_pass_with_default_allowed_list(self):
        file_name = FILE_PATH + "bitcoin-usd.chk"
        assert FileLoader.is_file_ok(file_name) is True

    def test_fail_with_default_allowed_list_file_not_found(self):
        file_name = FILE_PATH + "UserOk.yml"

        with pytest.raises(FileNotFoundError):
            FileLoader.is_file_ok(file_name)

    def test_fail_with_default_allowed_list_not_allowed_file(self):
        file_name = FILE_PATH + "UserOk.yaml"

        with pytest.raises(LookupError):
            FileLoader.is_file_ok(file_name)

    def test_pass_with_given_allowed_list(self):
        file_name = FILE_PATH + "UserOk.yaml"
        assert FileLoader.is_file_ok(file_name, [".chk", ".yaml", ".yml"]) is True


class TestFileLoaderLoadYaml:
    """Create tests"""

    def test_pass_valid_file(self):
        file_name = FILE_PATH + "bitcoin-usd.chk"
        loaded_content = FileLoader.load_yaml(file_name)

        assert isinstance(loaded_content, dict)
        assert isinstance(loaded_content.get("version"), str)

    def test_fail_invalid_file(self):
        file_name = FILE_PATH + "UserNotOk.chk"

        with pytest.raises(RuntimeError):
            FileLoader.load_yaml(file_name)


class TestFileLoaderLoadJson:
    """Create tests"""

    def test_pass_valid_file(self):
        file_name = FILE_PATH + "UserOk.json"
        loaded_content = FileLoader.load_json(file_name)

        assert isinstance(loaded_content, dict)
        assert isinstance(loaded_content.get("version"), str)

    def test_fail_invalid_file(self):
        file_name = FILE_PATH + "UserNotOk.json"

        with pytest.raises(JsonDecodingError, match="JSON loading error."):
            FileLoader.load_json(file_name)


class TestFileLoaderLoadJsonFromStr:
    """Create tests"""

    def test_pass_valid_file(self):
        file_name = FILE_PATH + "UserOk.json"
        with open(file_name, "r", encoding="UTF-8") as json_file_content:
            loaded_content = FileLoader.load_json_from_str(json_file_content.read())

            assert isinstance(loaded_content, dict)
            assert isinstance(loaded_content.get("version"), str)

    def test_fail_invalid_file(self):
        file_name = FILE_PATH + "UserNotOk.json"

        with open(file_name, "r", encoding="UTF-8") as json_file_content:
            with pytest.raises(JsonDecodingError, match="JSON loading error."):
                FileLoader.load_json_from_str(json_file_content.read())
