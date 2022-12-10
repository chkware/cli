"""
Helper functions module
"""
import ast
from typing import Any


def dict_get(var: dict, keymap: str, default: Any = None) -> Any:
    """
    Get a value of a dictionary by dot notation key
    :param var: the dictionary we'll get value for
    :param keymap: dot separated keys
    :param default: None
    :return:
    """

    if len(keymap) == 0 or not var:
        return default

    dot_loc = keymap.find(".")

    if dot_loc < 1:
        key = keymap
    else:
        key = keymap[: keymap.find(".")]

    if dot_loc < 1:
        key_last = None
    else:
        key_last = keymap[(keymap.find(".") + 1) :]

    if key_last is None:
        return var.get(key, default)

    return dict_get(var[key], key_last, default)


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


def data_set(var: dict | list, keymap: str, value: Any) -> bool:
    """
    Set a value of a dictionary by dot notation key and given value
    If the key do not exist, this function create the key by keymap
    Returns False if keymap is empty
    :param var: the dictionary we'll get value for
    :param keymap: dot separated keys
    :param value:
    :return:
    """

    km_l = keymap.split(".")

    while km_i := km_l.pop(0) if km_l else False:
        if isinstance(km_i, str) and km_i.isnumeric():
            km_i = int(km_i)

        if km_i in var:
            if km_l:
                return data_set(var[km_i], ".".join(km_l), value)

            var[km_i] = value
            return True

        else:
            if km_l:
                _tmp: list | dict = [] if km_l[0].isnumeric() else {}

                if isinstance(var, list):
                    var.append(_tmp)
                elif isinstance(var, dict):
                    var[km_i] = _tmp

                return data_set(var[km_i], ".".join(km_l), value)
            else:
                var[km_i] = value
                return True


def data_get(var: dict | list, keymap: str, default: object = None) -> Any:
    """
    Get a value of a dictionary|list by dot notation key
    :param var: the dictionary|list we'll get value for
    :param keymap: dot separated keys
    :param default: None
    :return:
    """
    if len(keymap) == 0 or not var:
        return default

    dot_loc = keymap.find(".")

    key = keymap if dot_loc < 1 else keymap[: keymap.find(".")]

    if isinstance(key, str) and key.isnumeric():
        key = int(key)

    key_last = None if dot_loc < 1 else keymap[(keymap.find(".") + 1) :]

    try:
        return var[key] if key_last is None else data_get(var[key], key_last, default)
    except (LookupError, TypeError):
        return default


def type_converter(var: str) -> object:
    """Convert to appropriate type from string value"""
    try:
        return int(var)
    except ValueError:
        pass  # not int

    try:
        return float(var)
    except ValueError:
        pass  # not float

    if var in {"true", "True"}:
        return True
    if var in {"false", "False"}:
        return False
    if var in {"null", "None"}:
        return None
    if isinstance(var, str):
        try:
            return ast.literal_eval(var)
        except (ValueError, TypeError, SyntaxError):
            pass

    return var


def is_scalar(val: object) -> bool:
    """Check is a value is scalar"""
    return not (hasattr(val, "__len__") and (not isinstance(val, str)))
