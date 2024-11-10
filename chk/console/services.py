"""
Console service module
"""

import os
import sys
from typing import Any

import click

from chk.infrastructure.file_loader import FileLoader
from chk.infrastructure.logging import LoggingManager
from chk.infrastructure.typing_extras import JsonDecodingError


def load_variables_as_dict(json_str: str, **kwargs: Any) -> dict:
    """Reads a json string and converts  and returns the dict while doing validation"""

    if json_str:
        try:
            return FileLoader.load_json_from_str(json_str)
        except JsonDecodingError as err:
            message = kwargs.get("except_msg", "JSON loading error.")
            raise click.UsageError(str(message)) from err

    return {}


def combine_initial_variables(external_vars: str, **kwargs: Any) -> dict:
    """Reads a json string and converts to dict, and combines with env and dotenv
    variables"""

    return load_variables_as_dict(external_vars, **kwargs)


def after_hook(*args: list, **kwargs: dict) -> Any:
    """Run any function after implementation. Default pass"""


def setup_logger(should_log: bool) -> None:
    """setup_logger"""

    LoggingManager.remove_loguru()

    if should_log:
        log_file = LoggingManager.create_new_log_file()
        LoggingManager.setup_loguru(log_file)


def get_stdin() -> str:
    """This will get stdin piped input *if exists*"""

    raw_str = ""
    with os.fdopen(sys.stdin.fileno(), "rb", buffering=0) as stdin:
        if not stdin.seekable():
            raw_str = "".join([_.decode("utf-8") for _ in stdin.readlines()])

    return raw_str
