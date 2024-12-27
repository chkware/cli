"""
Helper functions module
"""

import ast
import re
from collections.abc import Callable
from typing import Any

import click


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

    @staticmethod
    def try_dict(to_dict: Any, say_exception: bool = False) -> dict | Any:
        try:
            return dict(to_dict)
        except ValueError as ex:
            if say_exception:
                raise ex
            else:
                return to_dict


def formatter(
    message: object, cb: Callable = str, dump: bool = True, is_err: bool = False
) -> str:
    """Format message with given callback

    Args:
        message: object
        cb: Callable
        dump: bool
        is_err: bool
    Returns:
        str
    """

    printable = str(cb(message))

    if dump:
        click.echo(printable, err=is_err)

    return printable


def slugify(string: str) -> str:
    """Make slug out of string"""

    if not isinstance(string, str):
        raise TypeError("slugify: only string value supported.")

    string = string.lower().strip()
    string = re.sub(r"[^\w\s-]", "", string)
    string = re.sub(r"[\s_-]+", "-", string)
    string = re.sub(r"-{2,}", "", string)
    return string
