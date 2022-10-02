"""
File loader utility
"""

from pathlib import Path
from types import MappingProxyType
from typing import NamedTuple

from yaml import safe_load

from chk.infrastructure import exception, mangle


class ChkFileLoader:
    """Loader for CHK files"""

    @staticmethod
    def to_dict(file_name: str) -> dict:
        """read yml data"""
        with open(file_name, 'r', encoding='UTF-8') as yaml_file:
            try:
                return safe_load(yaml_file)
            except Exception as ex:
                yaml_file.close()
                raise SystemExit(exception.err_message('fatal.V0003', {'file_name': file_name})) from ex

    @staticmethod
    def is_file_ok(file_name: str) -> bool:
        """Check if chk file exists, extension is okay"""
        if (Path(file_name).is_file()
                and Path(file_name).suffix in {'.chk', '.yaml.chk', }):
            return True

        raise SystemExit(exception.err_message('fatal.V0002'))

    @staticmethod
    def get_mangled_name(file_name: str) -> tuple[str, str]:
        return mangle.filename(file_name), mangle.uniq_sha255(file_name)


class FileContext(NamedTuple):
    """ File context that holds file information """

    options: MappingProxyType[str, object] = {}
    arguments: MappingProxyType[str, object] = {}
    filepath: str = ""
    filepath_mangled: str = ""
    filepath_hash: str = ""
