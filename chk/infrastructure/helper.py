"""
Helper functions module
"""
import ast
import re
from collections.abc import Callable
from typing import Any

import click


def dict_set(var: dict, keymap: str, value: Any) -> bool:
    """
    Set a value of a dictionary by dot notation key and given value
    If the key do not exist, this function returns False, True otherwise
    :param var: the dictionary we'll get value for
    :param keymap: dot separated keys
    :param value:
    :return:
    """

    if len(keymap) == 0 or not var:
        return False

    keymap_list = keymap.split(".")

    if (km := keymap_list.pop(0)) in var:
        if len(keymap_list) > 0:
            if not isinstance(var[km], dict):
                return False

            return dict_set(var[km], ".".join(keymap_list), value)

        var[km] = value
        return True

    return False


def data_set(data: dict | list, keymap: str, value: Any) -> Any:
    """
    Set a value of a dictionary by dot notation key and given value
    If the key do not exist, this function create the key by keymap
    Returns False if keymap is empty
    :param data: the dictionary we'll get value for
    :param keymap: dot separated keys
    :param value:
    :return:
    """

    keymap_list = keymap.split(".")
    current_item = keymap_list.pop(0)
    next_item = keymap_list[0] if len(keymap_list) > 0 else ""

    if isinstance(data, dict):
        if current_item.isnumeric():
            raise IndexError(
                f"Trying to set numeric key `{current_item}` on dict `{data}`"
            )

        if len(keymap_list) == 0:
            data[current_item] = value
            return True

        if current_item not in data:
            data[current_item] = [] if next_item.isnumeric() else {}

        return data_set(data[current_item], ".".join(keymap_list), value)

    if isinstance(data, list):
        if not current_item.isnumeric():
            raise IndexError(
                f"Trying to set non-numeric index `{current_item}` on list `{data}`"
            )
        current_item_i = int(current_item)

        if len(data) < current_item_i:
            raise IndexError(f"Out of bound index `{current_item}` on list `{data}`")

        if len(keymap_list) == 0:
            data[current_item_i] = value
            return True

        if len(data) == 0 and current_item_i == 0:
            data.append([] if next_item.isnumeric() else {})

        return data_set(data[current_item_i], ".".join(keymap_list), value)

    return False


def data_get(var: dict | list, keymap: str, default: object = None) -> Any:
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


def is_scalar(val: object) -> bool:
    """Check is a value is scalar"""
    return not (hasattr(val, "__len__") and (not isinstance(val, str)))


class Cast:
    """Cast to type"""

    @staticmethod
    def to_int(var: str) -> int | str:
        try:
            return int(var)
        except ValueError:
            return var

    @staticmethod
    def to_float(var: str) -> float | str:
        try:
            return float(var)
        except ValueError:
            return var

    @staticmethod
    def to_int_or_float(var: str) -> float | int | str:
        try:
            return int(var)
        except ValueError:
            try:
                return float(var)
            except ValueError:
                return var

    @staticmethod
    def to_bool(var: str) -> bool | str:
        if var in {"true", "True"}:
            return True

        if var in {"false", "False"}:
            return False

        return var

    @staticmethod
    def to_none(var: str) -> None | str:
        if var in {"null", "None"}:
            return None

        return var

    @staticmethod
    def to_hashable(var: str) -> dict | list | str:
        try:
            return ast.literal_eval(var)
        except Exception:
            return var

    @staticmethod
    def to_auto(var: str) -> Any:
        """Convert to appropriate type from string value"""

        if isinstance(var, str):
            var = Cast.to_int_or_float(var)  # type: ignore

        if isinstance(var, str):
            var = Cast.to_bool(var)  # type: ignore

        if isinstance(var, str):
            var = Cast.to_none(var)  # type: ignore

        if isinstance(var, str):
            var = Cast.to_hashable(var)  # type: ignore

        return var


def parse_args(argv_s: list[str], delimiter: str = "=") -> dict:
    """
    parse and return args to dict
    :return: dict
    """

    if argv_s:
        argv = [item for item in argv_s if delimiter in item]
        return {item[0]: item[1] for item in [item.split(delimiter) for item in argv]}

    return {}


def formatter(message: object, cb: Callable = str, dump: bool = True) -> str:
    """Format message with given callback

    Args:
        message: object
        cb: Callable
        dump: bool
    Returns:
        str
    """

    printable = str(cb(message))

    if dump:
        click.echo(printable)

    return printable


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

    def substitute(self, mapping: dict | None = None, /, **keywords: dict) -> Any:
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
    def _replace(container: str, replace_with: dict) -> Any:
        """replace values found in string with typed return

        Args:
            container: str
            replace_with: dict
        Returns:
            object: object found in replace_with
        """

        if not isinstance(container, str):
            return container

        if len(replace_with) == 0:
            return container

        line_split = re.split(
            r"("
            + StrTemplate.d_start
            + r"\s*[a-zA-Z0-9_.]+\s*"
            + StrTemplate.d_end
            + ")",
            container,
        )

        if len(line_split) == 1 and container in line_split:
            return container

        line_strip = [item for item in line_split if item]

        for i, item in enumerate(line_strip):
            if StrTemplate.d_start in item and StrTemplate.d_end in item:
                value = StrTemplate._get(replace_with, item.strip(" <>%"), None)

                line_strip[i] = value or item

        return (
            "".join([str(li) for li in line_strip])
            if len(line_strip) > 1
            else line_strip.pop()
        )

    @staticmethod
    def _get(var: dict | list, keymap: str, default: object = None) -> object:
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
