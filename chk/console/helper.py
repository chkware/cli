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

    if len(keymap) == 0: return default
    elif not var: return default

    dot_loc = keymap.find('.')

    if dot_loc < 1: key = keymap
    else: key = keymap[:keymap.find('.')]

    if dot_loc < 1: key_last = None
    else: key_last = keymap[(keymap.find('.') + 1):]

    if key_last is None: return var.get(key, default)
    else: return dict_get(var.get(key), key_last, default)


def dict_set(var: dict, keymap: str, value: object) -> bool:
    """
    Set a value of a dictionary by dot notation key and given value
    :param var: the dictionary we'll get value for
    :param keymap: dot separated keys
    :param value:  
    :return:
    """

    if len(keymap) == 0: return False
    elif not var: return False

    keymap_list = keymap.split('.')
    km = keymap_list.pop(0)

    if km in var:
        if len(keymap_list) > 0:
            if type(var[km]) is dict:
                return dict_set(var[km], '.'.join(keymap_list), value)
            else:
                return False
        else:
            var[km] = value
            return True
    else:
        return False
