"""
Templating module
"""

import re
import typing

from jinja2.environment import Template
from jinja2.nativetypes import NativeEnvironment

from chk.infrastructure.logging import error


class StrTemplate:
    """
    class to replace variables given in between <%, and %>.
    Supports value from dictionary and list.
    """

    d_start = "<%"
    d_end = "%>"

    def __init__(self, templated_string: str = "") -> None:
        """StrTemplate Constructor

        Args:
            templated_string: string to set, "" is default
        """
        if not isinstance(templated_string, str):
            raise ValueError("Only string allowed in template.")

        self.template = templated_string
        # (<%\s*[\'\"\(\)|a-zA-Z0-9_.]+\s*%>)

    def substitute(
        self, mapping: dict | None = None, /, **keywords: dict
    ) -> typing.Any:
        """Substitute values from mapping and keywords"""

        if not mapping:
            mapping = {}

        if not isinstance(mapping, dict):
            raise ValueError("Only mapping allowed in mapping.")

        if not (
            StrTemplate.d_start in self.template and StrTemplate.d_end in self.template
        ):
            return self.template

        return self._replace(self.template, {**mapping, **keywords})

    @staticmethod
    def _parse(container: str) -> list[str]:
        """replace values found in string with typed return

        Args:
            container: str
        Returns:
            list: list of parsed object
        """

        if not isinstance(container, str):
            return []

        line_split = re.split(
            "("
            + StrTemplate.d_start
            + r"\s*[a-zA-Z0-9_.]+\s*"
            + StrTemplate.d_end
            + ")",
            container,
        )

        return [item for item in line_split if item]

    @staticmethod
    def _replace(container: str, replace_with: dict) -> typing.Any:
        """replace values found in string with typed return

        Args:
            container: str
            replace_with: dict
        Returns:
            object: object found in replace_with
        """

        if len(replace_with) == 0:
            return container

        if not (line_strip := StrTemplate._parse(container)):
            return container

        if (
            len(line_strip) == 1
            and container in line_strip
            and StrTemplate.d_start not in container
            and StrTemplate.d_end not in container
        ):
            return container

        final_list_strip: list[object] = []

        for item in line_strip:
            if StrTemplate.d_start in item and StrTemplate.d_end in item:
                value = StrTemplate._get(replace_with, item.strip(" <>%"), None)

                final_list_strip.append(value or item)
            else:
                final_list_strip.append(item)

        return (
            "".join([str(li) for li in final_list_strip])
            if len(final_list_strip) > 1
            else final_list_strip.pop()
        )

    @staticmethod
    def _get(var: dict | list, keymap: str, default: object = None) -> typing.Any:
        """
        Get a value of a dict|list by dot notation key
        :param var: the dict|list we'll get value for
        :param keymap: dot separated keys
        :param default: None
        :return:
        """

        data = var.copy()
        indexes = keymap.split(".")

        for index in indexes:
            if isinstance(data, dict) and index in data:
                data = data[index]
            elif isinstance(data, list) and index.isnumeric():
                data = data[int(index)]
            else:
                return default

        return data

    @staticmethod
    def is_tpl(tpl_str: str) -> bool:
        """Check given string is templated string or not"""

        return StrTemplate.d_start in tpl_str and StrTemplate.d_end in tpl_str


class JinjaTemplate:
    """JinjaTemplate is wrapper class for JinjaNativeTemplate"""

    @staticmethod
    def make(template: str) -> Template:
        """Create a NativeEnvironment with default settings"""

        if not template or not isinstance(template, str):
            e_msg = f"Malformed template: {template}"
            error(e_msg)
            raise ValueError(e_msg)

        n_env = NativeEnvironment(
            variable_start_string="<%",
            variable_end_string="%>",
            block_start_string="<@",
            block_end_string="@>",
            comment_start_string="<#",
            comment_end_string="#>",
        )

        return n_env.from_string(template)
