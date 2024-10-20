"""
Console service module
"""
from typing import Any

import click

from chk.infrastructure.file_loader import FileLoader
from chk.infrastructure.typing_extras import JsonDecodingError


def load_variables_as_dict(json_str: str, **kwargs: Any) -> dict:
    """Reads a json string and converts  and returns the dict while doing validation"""

    if json_str:
        try:
            return FileLoader.load_json_from_str(json_str)
        except JsonDecodingError as err:
            message = kwargs.get("except_msg") or "JSON loading error."
            raise click.UsageError(str(message)) from err

    return {}


def combine_initial_variables(external_vars: str, **kwargs: Any) -> dict:
    """Reads a json string and converts to dict, and combines with env and dotenv
    variables"""

    return load_variables_as_dict(external_vars, **kwargs)


def after_hook(resp: dict) -> None:
    """Saves custom data from commands to global context bus

    Args:
        resp: object
    """

    if curr_ctx := click.get_current_context():
        if curr_ctx.parent:
            if not curr_ctx.parent.obj:
                curr_ctx.parent.obj = {}

            curr_ctx.parent.obj |= resp
    else:
        raise RuntimeError("Default context not found")
