# type: ignore

"""
Fetch module tests
"""
from chk.infrastructure.file_loader import ExecuteContext, FileContext
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
