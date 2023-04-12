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
