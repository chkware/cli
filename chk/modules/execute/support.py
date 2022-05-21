"""
execute module
"""


def _parse_args() -> list[str]:
    import sys
    if len(sys.argv) > 3: return sys.argv[3:]
    return []

