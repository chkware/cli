from pathlib import Path
from yaml import safe_load
from typing import Dict
from chk.globals import current_app, l10n


class ChkFileLoader:
    """Loader for CHK files"""

    @staticmethod
    def to_dict(file_name: str) -> Dict:
        """read yml data"""
        with open(file_name, 'r') as yaml_file:
            try:
                chk_yaml = safe_load(yaml_file)
            except:
                raise SystemExit(l10n(current_app().config.error.fatal.V0003, {'file_name': file_name}))

            return chk_yaml

    @staticmethod
    def is_file_ok(file_name: str) -> bool:
        """Check if chk file exists, extension is okay"""
        return Path(file_name).is_file() and Path(file_name).suffix == '.chk'
