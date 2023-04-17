# type: ignore
"""
Test module for infrastructure.version module
"""
import pytest

from chk.infrastructure.loader import FileLoader

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

        with pytest.raises(RuntimeError):
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
            with pytest.raises(RuntimeError):
                FileLoader.load_json_from_str(json_file_content.read())
