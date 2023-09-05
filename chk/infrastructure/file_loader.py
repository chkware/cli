"""
File loader utility
"""

from typing import NamedTuple
from pathlib import Path

import json
import yaml

from chk.infrastructure import exception, mangle


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
            allowed_list = [".chk"]

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
            raise RuntimeError("JSON loading error.") from ex


class FileContext(NamedTuple):
    """File context that holds file information"""

    options: dict = {}
    arguments: dict = {}
    document: dict = {}
    filepath: str = ""
    filepath_hash: str = ""

    @staticmethod
    def from_file(file: str, **kwarg: dict) -> "FileContext":
        FileLoader.is_file_ok(file)
        absolute_path = str(Path(file).absolute())
        fpath_hash = mangle.uniq_sha255(absolute_path)
        document = FileLoader.load_yaml(absolute_path)

        return FileContext(
            filepath=absolute_path,
            filepath_hash=fpath_hash,
            document=document,
            options=kwarg["options"] if "options" in kwarg else {},
            arguments=kwarg["arguments"] if "arguments" in kwarg else {},
        )


class PathFrom:
    """Utility to expand to full path"""

    def __init__(self, base: Path):
        self.base = base.absolute().parent

    def absolute(self, target: str) -> str:
        """Find absolute in comparison to base URL"""

        if target.startswith("./") or target.startswith("../"):
            if self.base.exists():
                to_path = self.base

                target_path_sp = target.split("/")
                for part in target_path_sp:
                    if part == "..":
                        to_path = to_path.parent
                    else:
                        to_path = Path(str(to_path) + "/" + part)

                return str(to_path)
            raise ValueError("Invalid base path.")
        raise ValueError("Invalid target path.")


class ExecuteContext(NamedTuple):
    """Information storage for execution context"""

    options: dict = {}
    arguments: dict = {}
