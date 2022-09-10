"""
execute module
"""
from chk.modules.testcase.constants import ExecuteConfigNode
from collections import namedtuple


# File context that holds file information
ExecutionContext = namedtuple('ExecutionContext', ['file', 'variables', 'result'])


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
