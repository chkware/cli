"""
Loader module
"""
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
