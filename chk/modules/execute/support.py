"""
Execute module
"""
from typing import NamedTuple

from chk.modules.testcase.constants import ExecuteConfigNode


class ExecutionContext(NamedTuple):
    """
    File context that holds file information
    """

    file: str
    arguments: list = []
    options: list = []


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
