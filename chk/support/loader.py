from pathlib import Path
from yaml import safe_load
from typing import Dict


class ChkFileLoader:
    """Loader for CHK files"""

    @staticmethod
    def to_dict(file_name: str) -> Dict:
        """read yml data"""
        with open(file_name, 'r') as yaml_file:
            try:
                chk_yaml = safe_load(yaml_file)
            except:
                raise SystemExit(f'`{file_name}` is not a valid YAML.')

            return chk_yaml

    @staticmethod
    def is_file_ok(file_name: str) -> bool:
        """Check if chk file exists, extension is okay"""
        return Path(file_name).is_file() and \
               Path(file_name).suffix == '.chk'

