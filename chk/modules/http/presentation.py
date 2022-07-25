"""
Presentation related logics
"""
from typing import Union

from chk.infrastructure.file_loader import FileContext


class Presentation:
    """Handle presentation of the outputs of chkware commands."""

    @classmethod
    def present_result(cls, file_ctx: FileContext, data: Union[dict, BaseException]):
        """Shows result of execution."""
        if isinstance(data, dict):
            print(cls.displayable_summary(file_ctx.filepath, 'Success'))
            print(cls.displayable_result(data))
        if isinstance(data, BaseException):
            print(cls.displayable_summary(file_ctx.filepath, 'Failed'))
            print(cls.displayable_error(data))

    @classmethod
    def displayable_result(cls, response: dict[str, object]) -> str:
        """Return result in presentable format."""
        prefix = '[RESULT]'

        def headers(res) -> str:
            """Headers"""
            return '{}'.format(
                '\r\n'.join('{}: {}'.format(k, v) for k, v in res.get('headers').items()),
            )

        if response.get('have_all'):
            summary = '{} {} {}'.format(
                response.get('version'),
                response.get('code'),
                response.get('reason'),
            )

            return '{}\r\n{}\r\n{}\r\n\r\n{}'.format(prefix, summary, headers(response), response.get('body'))
        else:
            response.pop('have_all')
            for _, val in response.items():
                if val:
                    return '{}\r\n{}'.format(prefix, str(val))

    @classmethod
    def displayable_error(cls, error: BaseException) -> str:
        """Returns error in presentable format."""
        return '[ERROR list / message]\r\n{}'.format(str(error))

    @classmethod
    def displayable_summary(cls, filepath: str, status: str) -> str:
        """Return execution summary in presentable format."""
        summary = 'File: {}\r\n\nExecuting request\r\n\n- Making request [{}]\r\n===='
        return summary.format(filepath, status)
