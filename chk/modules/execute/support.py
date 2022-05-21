"""
execute module
"""
from collections import namedtuple


def _parse_args() -> dict[str, str]:
    """
    parse and return args to dict
    :return: dict
    """
    import sys
    if len(sys.argv) > 3:
        c_args = sys.argv[3:]
        c_args = list(filter(lambda x: True if '=' in x else False, c_args))
        return {arg_i[0]:arg_i[1] for arg_i in list(map(lambda x: x.split('='), c_args)) }

    return {}


# File context that holds file information
ExecutionContext = namedtuple('ExecutionContext', ['filepath', 'with_data', 'result'])

