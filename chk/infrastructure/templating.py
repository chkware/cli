"""
Templating module
"""

import json
import typing

from jinja2 import TemplateError
from jinja2.environment import Template
from jinja2.nativetypes import NativeEnvironment

from chk.infrastructure.logging import error


class JinjaTemplate:
    """JinjaTemplate is wrapper class for JinjaNativeTemplate"""

    @staticmethod
    def build_env() -> NativeEnvironment:
        """Build a native env"""

        env = NativeEnvironment(
            variable_start_string="<%",
            variable_end_string="%>",
            block_start_string="<@",
            block_end_string="@>",
            comment_start_string="<#",
            comment_end_string="#>",
        )

        env.filters["fromjson"] = filter_fromjson
        return env

    @staticmethod
    def make(template: str) -> Template:
        """Create a NativeEnvironment with default settings"""

        if not template or not isinstance(template, str):
            e_msg = f"Template error: {type(template)} {template}"
            error(e_msg)
            raise ValueError(e_msg)

        env = NativeEnvironment(
            variable_start_string="<%",
            variable_end_string="%>",
            block_start_string="<@",
            block_end_string="@>",
            comment_start_string="<#",
            comment_end_string="#>",
        )

        env.filters["fromjson"] = filter_fromjson

        return env.from_string(template)


def is_template_str(tpl: str) -> bool:
    """Check given string is templated string or not"""

    _dm_sets = [("<%", "%>"), ("<@", "@>"), ("<#", "#>")]
    return any([_dm_set[0] in tpl and _dm_set[1] in tpl for _dm_set in _dm_sets])

######################################
# Jinja Filters
######################################

def filter_fromjson(value: typing.Any) -> str:
    """Convert a JSON string to a Python dictionary."""

    try:
        return json.loads(value)
    except json.JSONDecodeError as e:
        raise TemplateError(f"Invalid JSON string: {e}") from e
