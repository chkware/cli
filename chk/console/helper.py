"""
Helper functions module
"""


def dict_get(var: dict, keymap: str, default=None) -> object:
    """
    Get a value of a dictionary by dot notation key
    :param var: the dictionary we'll get value for
    :param keymap: dot separated keys
    :param default: None
    :return:
    """

    if len(keymap) == 0:
        return default
    elif not var:
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
    else:
        return dict_get(var.get(key), key_last, default)


def dict_set(var: dict, keymap: str, value: object) -> bool:
    """
    Set a value of a dictionary by dot notation key and given value
    :param var: the dictionary we'll get value for
    :param keymap: dot separated keys
    :param value:
    :return:
    """

    if len(keymap) == 0:
        return False
    elif not var:
        return False

    keymap_list = keymap.split(".")
    km = keymap_list.pop(0)

    if km in var:
        if len(keymap_list) > 0:
            if type(var[km]) is dict:
                return dict_set(var[km], ".".join(keymap_list), value)
            else:
                return False
        else:
            var[km] = value
            return True
    else:
        return False


def data_get(var: dict | list, keymap: str, default=None) -> object:
    """
    Get a value of a dictionary|list by dot notation key
    :param var: the dictionary|list we'll get value for
    :param keymap: dot separated keys
    :param default: None
    :return:
    """
    if len(keymap) == 0:
        return default
    elif not var:
        return default

    dot_loc = keymap.find(".")

    if dot_loc < 1:
        key = keymap
    else:
        key = keymap[: keymap.find(".")]

    if key.isnumeric():
        key = int(key)

    if dot_loc < 1:
        key_last = None
    else:
        key_last = keymap[(keymap.find(".") + 1) :]

    try:
        if key_last is None:
            return var[key]
        else:
            return data_get(var[key], key_last, default)
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

    if var == "true":
        return True
    elif var == "false":
        return False
    elif var == "null":
        return None
    else:
        return var
