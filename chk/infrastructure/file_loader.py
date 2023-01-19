"""
File loader utility
"""

from pathlib import Path
from types import MappingProxyType
from typing import NamedTuple, Self

from yaml import safe_load

from chk.infrastructure import exception, mangle


class ChkFileLoader:
    """Loader for CHK files"""

    @staticmethod
    def to_dict(file_name: str) -> dict:
        """read yml data"""
        with open(file_name, "r", encoding="UTF-8") as yaml_file:
            try:
                return safe_load(yaml_file)
            except Exception as ex:
                yaml_file.close()
                raise SystemExit(
                    exception.err_message("fatal.V0003", {"file_name": file_name})
                ) from ex

    @staticmethod
    def is_file_ok(file_name: str) -> bool:
        """Check if chk file exists, extension is okay"""

        if Path(file_name).is_file() and Path(file_name).suffix == ".chk":
            return True

        raise SystemExit(exception.err_message("fatal.V0002"))

    @staticmethod
    def get_mangled_name(file_name: str) -> tuple[str, str]:
        return mangle.filename(file_name), mangle.uniq_sha255(file_name)


class FileContext(NamedTuple):
    """File context that holds file information"""

    options: MappingProxyType = MappingProxyType({})
    arguments: MappingProxyType = MappingProxyType({})
    filepath: str = ""
    filepath_mangled: str = ""
    filepath_hash: str = ""

    @staticmethod
    def from_file(file: str, **kwarg: dict) -> Self:
        ChkFileLoader.is_file_ok(file)
        absolute_path = str(Path(file).absolute())
        fpath_mangled, fpath_hash = ChkFileLoader.get_mangled_name(absolute_path)

        return FileContext(
            filepath=absolute_path,
            filepath_mangled=fpath_mangled,
            filepath_hash=fpath_hash,
            options=MappingProxyType(kwarg["options"] if "options" in kwarg else {}),
            arguments=MappingProxyType(
                kwarg["arguments"] if "arguments" in kwarg else {}
            ),
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
