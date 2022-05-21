"""
execute module
"""
from collections import namedtuple


def _parse_args() -> list[str]:
    import sys
    if len(sys.argv) > 3: return sys.argv[3:]
    return []


# File context that holds file information
ExecutionContext = namedtuple('ExecutionContext', ['filepath', 'with_data', 'result'])

