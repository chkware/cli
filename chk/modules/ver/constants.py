from typing import Dict


class VersionStrToSpecConfigMapping:
    """VersionStrToSpecConfigMapping lists all archetypes by version string"""

    data: Dict = {
        "default:http:0.7.2": "chk.archetypes.defaults.http_config.HttpV072",
    }
