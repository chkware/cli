"""
File loader utility
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import NamedTuple

import yaml

from chk.infrastructure.typing_extras import JsonDecodingError


class FileLoader:
    """File loader utility"""

    @staticmethod
    def is_file_ok(file_name: str, allowed_list: list | None = None) -> bool:
        """Check if chk file exists, when extension is allowed
        :param file_name: File name to check
        :param allowed_list: List of allowed file extension, default is [".chk"]
        :return: bool
        :raises FileNotFoundError When file not found
        :raises LookupError When file extension do not match
        """

        if not allowed_list:
            allowed_list = [".chk", ".yaml", ".yml"]

        if not Path(file_name).is_file():
            raise FileNotFoundError("File not found")

        if Path(file_name).suffix not in allowed_list:
            raise LookupError("File not allowed")

        return True

    @staticmethod
    def load_yaml(file_name: str) -> dict:
        """Try to load yaml file and return content as dictionary
        :param file_name: str File name to be loaded
        :return: File content as dictionary
        """

        with open(file_name, "r", encoding="UTF-8") as yaml_file:
            try:
                return yaml.safe_load(yaml_file)
            except Exception as ex:
                raise RuntimeError("YAML loading error.") from ex

    @staticmethod
    def load_json(file_name: str) -> dict:
        """Try to load json file and return content as dictionary
        :param file_name: str File name to be loaded
        :return: File content as dictionary
        """

        with open(file_name, "r", encoding="UTF-8") as json_file_content:
            return FileLoader.load_json_from_str(json_file_content.read())

    @staticmethod
    def load_json_from_str(expected_json: str) -> dict:
        """Try to load json file and return content as dictionary
        :param expected_json: str JSON document to be loaded
        :return: JSON document as dictionary
        """

        try:
            return json.loads(expected_json)
        except ValueError as ex:
            raise JsonDecodingError("JSON loading error.") from ex


class FileContext(NamedTuple):
    """File context that holds file information"""

    options: dict = {}
    arguments: dict = {}
    document: dict = {}
    filepath: str = ""
    filepath_hash: str = ""

    @staticmethod
    def from_file(file: str, **kwarg: dict) -> FileContext:
        FileLoader.is_file_ok(file)
        absolute_path = str(Path(file).absolute())
        fpath_hash = hashlib.sha256(absolute_path.encode("utf-8")).hexdigest()
        document = FileLoader.load_yaml(absolute_path)

        return FileContext(
            filepath=absolute_path,
            filepath_hash=fpath_hash,
            document=document,
            options=kwarg["options"] if "options" in kwarg else {},
            arguments=kwarg["arguments"] if "arguments" in kwarg else {},
        )

    @property
    def filepath_as_path(self) -> Path:
        """Get filepath as Path"""

        return Path(self.filepath)

    @property
    def filepath_base_as_path(self) -> Path:
        """Get filepath parent or base as Path"""

        return Path(self.filepath).absolute().parent


def generate_abs_path(base_: str, target_: str) -> str:
    """Generate absolute path in comparison to base path
    Args:
        base_: str, base path to calculate from
        target_: str, file path that need absolute path

    Returns:
        Absolute path for given filepath
    """

    base = Path(base_)
    base_abs = base.absolute().parent if base.is_file() else base.absolute()

    if not base_abs.exists():
        raise ValueError("Invalid base path.")
    if not (target_.startswith("./") or target_.startswith("../")):
        raise ValueError("Invalid target path.")

    to_path = base_abs
    target_path_sp = target_.split("/")

    for part in target_path_sp:
        if part == "..":
            to_path = to_path.parent
        else:
            to_path = to_path / part

    return str(to_path)


class ExecuteContext(NamedTuple):
    """Information storage for execution context"""

    options: dict = {}
    arguments: dict = {}
