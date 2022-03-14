from chk.console.app_container import app
from chk.infrastructure.translation import l10n
from pathlib import Path
from typing import Dict
from yaml import safe_load


class ChkFileLoader:
    """Loader for CHK files"""

    @staticmethod
    def to_dict(file_name: str) -> Dict:
        """read yml data"""
        with open(file_name, 'r') as yaml_file:
            try:
                return safe_load(yaml_file)
            except:
                raise SystemExit(l10n(app.messages.error.fatal.V0003, {'file_name': file_name}))

    @staticmethod
    def is_file_ok(file_name: str) -> bool:
        """Check if chk file exists, extension is okay"""
        return Path(file_name).is_file() and Path(file_name).suffix == '.chk'
