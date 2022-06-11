"""
Presentation related logics
"""


def make_displayable(response: dict[str, object]) -> str:
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
    else:
        response.pop('have_all')
        for _, val in response.items():
            if val:
                return str(val)
