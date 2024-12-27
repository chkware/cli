# type: ignore

"""
Fetch module tests
"""

import requests

from chk.infrastructure.file_loader import ExecuteContext, FileContext
from chk.infrastructure.symbol_table import ExecResponse
from chk.modules.fetch import call


class TestFetchCall:
    @staticmethod
    def test_call_pass():
        file_ctx = FileContext(
            document={
                "version": "default:http:0.7.2",
                "request": {
                    "url": "https://jsonplaceholder.typicode.com/albums/1",
                    "method": "GET",
                },
            }
        )

        exec_ctx = ExecuteContext(
            options={
                "dump": True,
                "format": False,
            }
        )

        er = call(file_ctx, exec_ctx)
        assert "_response" in er.variables_exec

    @staticmethod
    def test_fails_for_doc_with_no_version():
        file_ctx = FileContext(
            document={
                # "version": "default:http:0.7.2",
                "request": {
                    "url": "https://jsonplaceholder.typicode.com/albums/1",
                    "method": "GET",
                },
            }
        )

        exec_ctx = ExecuteContext(
            options={
                "dump": True,
                "format": False,
            }
        )

        er = call(file_ctx, exec_ctx)

        assert isinstance(er, ExecResponse)
        assert isinstance(er.exception, RuntimeError)

    @staticmethod
    def test_fails_for_http_error():
        file_ctx = FileContext(
            document={
                "version": "default:http:0.7.2",
                "request": {
                    "url": "https://jsonplaceholdery.typicode.com/albums/1",
                    "method": "GET",
                },
            }
        )

        exec_ctx = ExecuteContext(
            options={
                "dump": True,
                "format": False,
            }
        )

        er = call(file_ctx, exec_ctx)

        assert isinstance(er, ExecResponse)
        assert isinstance(er.exception, requests.ConnectionError)

