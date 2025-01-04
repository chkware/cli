"""
Logging Module
"""

import os
import time
from pathlib import Path
from uuid import uuid4

from loguru import logger

debug = logger.debug
error = logger.error
critical = logger.critical
success = logger.success
error_trace = logger.opt

with_catch_log = logger.catch


class LoggingManager:
    """LoggingManager"""

    cache_dir = ".chkware_cache/"
    loggin_dir = "logs/"
    loggin_ext = ".log"

    @classmethod
    def create_cache_dir(cls) -> Path:
        """create_cache_dir"""

        # get cache dir name from env
        try:
            cache_dir = os.environ["CHK_CACHE_PATH"]
        except KeyError:
            cache_dir = cls.cache_dir

        # populate cache dir
        cache_path = Path.cwd() / cache_dir
        if not cache_path.exists():
            cache_path.mkdir()

        return cache_path

    @classmethod
    def create_log_dir(cls, parent: Path) -> Path:
        """create_cache_dir"""

        if not parent.exists():
            raise NotADirectoryError("Parent directory do not exists.")
        log_dir = parent / cls.loggin_dir

        if not log_dir.exists():
            log_dir.mkdir()

        return log_dir

    @classmethod
    def create_new_log_file(cls) -> Path:
        """create new log file"""

        cache_dir = cls.create_cache_dir()
        log_dir = cls.create_log_dir(cache_dir)

        log_file = log_dir / create_session_id()
        log_file = log_file.with_suffix(cls.loggin_ext)

        log_file.touch()
        return log_file

    @classmethod
    def setup_loguru(cls, log_path: Path | None) -> None:
        """setup_loguru"""

        logger.add(str(log_path), backtrace=True, enqueue=True, catch=True)

    @classmethod
    def remove_loguru(cls) -> None:
        """setup_loguru"""

        logger.remove()


def create_session_id() -> str:
    """create_session_id"""

    return f"{int(time.time())}-{uuid4().hex}"
