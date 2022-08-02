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
            if not file_ctx.options.get('result'):
                print(cls.displayable_summary(file_ctx.filepath, 'Success'))
            print(cls.displayable_result(data))
        else:
            if not file_ctx.options.get('result'):
                print(cls.displayable_summary(file_ctx.filepath, 'Failed'))
            print(str(data))

    @classmethod
    def displayable_result(cls, response: dict[str, object]) -> str:
        """Return result in presentable format."""

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
            return '{}\r\n{}\r\n\r\n{}'.format(summary, headers(response), response.get('body'))
        response.pop('have_all')
        for _, val in response.items():
            if val:
                return str(val)

    @classmethod
    def displayable_summary(cls, filepath: str, status: str) -> str:
        """Return execution summary in presentable format."""
        summary = 'File: {}\r\n\nExecuting request\r\n\n- Making request [{}]\r\n===='
        return summary.format(filepath, status)
