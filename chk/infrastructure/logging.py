"""
Logging Module
"""

import os
from pathlib import Path


class LoggingManager:
    """LoggingManager"""

    cache_dir = '.chkware_cache/'


    @classmethod
    def get_log_file(cls) -> str:
        """get_log_file"""

        # get cache dir name from env
        try:
            cache_dir = os.environ["CHK_CACHE_PATH"]
        except KeyError:
            cache_dir = ""

        # populate cache dir
        cache_path = os.getcwd() / Path(cache_dir)
        if not cache_path.exists():
            cache_path.mkdir()

        return ""