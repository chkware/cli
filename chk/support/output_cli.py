"""
output_cli
"""
import sys

from urllib3.response import HTTPResponse
from requests import Response, PreparedRequest


class ResponseToStringFormatter:
    """out put formatter for http response"""
    def __init__(self, resp: Response) -> None:
        self.response: Response = resp
        self.response_raw: HTTPResponse = resp.raw
        self.request: PreparedRequest = resp.request

    def body(self) -> str:
        """Body"""
        try:
            return self.response.json()
        except Exception as ex:
            print(ex)
            return self.response.text

    def headers(self) -> str:
        """Headers"""
        return '{}'.format(
            '\r\n'.join('{}: {}'.format(k, v) for k, v in self.response.headers.items()),
        )

    def summary(self) -> str:
        """Summary"""
        def convert_version_to_string(proto_ver: int) -> str:
            if proto_ver == 10:
                return 'HTTP/1.0'
            elif proto_ver == 11:
                return 'HTTP/1.1'

        return '{} {} {}'.format(
            convert_version_to_string(self.response_raw.version),
            self.response.status_code,
            self.response.reason,
        )

    def get(self):
        """Get summary, headers, and body"""
        return '{}\r\n{}\r\n\r\n{}'.format(self.summary(), self.headers(), self.body())

    def dd(self):
        """Dump and die with raw response"""
        from requests_toolbelt.utils.dump import dump_all

        print(dump_all(self.response).decode('utf-8'))
        sys.exit(0)
