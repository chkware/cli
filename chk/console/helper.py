"""
Helper functions module
"""


def dict_get(var: dict, keymap: str, default=None):
    """
    Get a value of a dictionary by dot notation key
    :param var: the dictionary we'll get value for
    :param keymap: dot sperated keys
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
