# type: ignore
"""
common config
"""

import pytest

from chk.infrastructure.file_loader import ExecuteContext, FileContext, FileLoader

RES_DIR = "./tests/resources/storage/sample_config/"
SPEC_DIR = "./tests/resources/storage/spec_docs/"


@pytest.fixture
def load_chk_file():
    def wrapper(file_path):
        if FileLoader.is_file_ok(file_path):
            return FileLoader.load_yaml(file_path)

        raise RuntimeError("Issue with file loading.")

    return wrapper


@pytest.fixture
def load_file_ctx_for_file(load_chk_file):
    def wrapper(filepath):
        return FileContext(document=load_chk_file(filepath), filepath=filepath)

    return wrapper


@pytest.fixture
def get_exec_ctx():
    def wrapper(format=True):
        return ExecuteContext(
            options={
                "dump": True,
                "format": format,
            }
        )

    return wrapper
