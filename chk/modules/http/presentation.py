"""
Presentation related logics
"""


class Presentation:
    """Handle presentation of the outputs of chkware commands."""

    @staticmethod
    def displayable_result(response: dict[str, object]) -> str:
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

    @staticmethod
    def displayable_execution_summary(filepath: str) -> str:
        """Return execution summary in presentable format."""
        summary = 'File: {}\r\n\nExecuting request\r\n\n- Making request [Success]\r\n===='
        return summary.format(filepath)
