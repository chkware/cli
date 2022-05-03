from chk.infrastructure.exception import err_message
from typing import Dict


class VersionConfigNode:
    """represent the base of all kind of documents"""
    VERSION = 'version'


class VersionStrToSpecConfigMapping:
    """VersionStrToSpecConfigMapping lists all archetypes by version string"""

    data: Dict = {
        "default:http:0.7.2": "chk.modules.http.entities.HttpSpec_V072",
    }

    @classmethod
    def find_by_version(cls, key: str) -> str:
        """find config by version str"""
        if not isinstance(key, str): raise SystemExit(err_message('fatal.V0004'))

        class_map = cls.data.get(key)
        if not isinstance(class_map, str): raise SystemExit(err_message('fatal.V0004'))
        elif len(class_map) == 0: raise SystemExit(err_message('fatal.V0004'))

        return class_map
