"""
Logging Module
"""

import os
import time
from pathlib import Path
from uuid import uuid4


class LoggingManager:
    """LoggingManager"""

    cache_dir = '.chkware_cache/'
    loggin_dir = 'logs/'


    @classmethod
    def create_cache_dir(cls) -> Path:
        """create_cache_dir"""

        # get cache dir name from env
        try:
            cache_dir = os.environ["CHK_CACHE_PATH"]
        except KeyError:
            cache_dir = ""

        # populate cache dir
        cache_path = os.getcwd() / Path(cache_dir)
        if not cache_path.exists():
            cache_path.mkdir()

        return cache_path


    @classmethod
    def create_log_dir(cls, parent: Path) -> Path:
        """create_cache_dir"""

        if not parent.exists():
            raise NotADirectoryError("Parent directory do not exists.")
        log_dir = parent / cls.loggin_dir
        log_dir.mkdir()

        return log_dir


def create_session_id() -> str:
    """create_session_id"""

    return "%s-%s" % (int(time.time()), uuid4().hex)