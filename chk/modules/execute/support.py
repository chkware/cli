"""
execute module
"""
from chk.modules.execute.constants import ExecuteConfigNode
from collections import namedtuple


# File context that holds file information
ExecutionContext = namedtuple('ExecutionContext', ['file', 'variables', 'result'])


def _parse_args() -> dict[str, str]:
    """
    parse and return args to dict
    :return: dict
    """
    import sys
    if len(sys.argv) > 3:
        c_args = sys.argv[3:]
        c_args = list(filter(lambda x: True if '=' in x else False, c_args))
        return {arg_i[0]:arg_i[1] for arg_i in list(map(lambda x: x.split('='), c_args))}

    return {}


class ExecutionContextBuilder:
    """
    Build `ExecutionContext` from different execution context
    """
    @staticmethod
    def from_dict(document: dict[str, object]) -> ExecutionContext:
        file = document.get(ExecuteConfigNode.FILE)
        if not file: raise SystemExit(f'`{ExecuteConfigNode.FILE}` is required')

        return ExecutionContext(
            file,
            document.get(ExecuteConfigNode.WITH),
            document.get(ExecuteConfigNode.RESULT)
        )
