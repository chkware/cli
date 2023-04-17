"""
Loader module
"""
import json
from pathlib import Path

import yaml


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
            try:
                return json.loads(json_file_content.read())
            except ValueError as ex:
                raise RuntimeError("JSON loading error.") from ex

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
