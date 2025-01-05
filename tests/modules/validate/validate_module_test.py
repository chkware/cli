"""
Validate module test
"""

from chk.infrastructure.file_loader import ExecuteContext, FileContext
from chk.infrastructure.symbol_table import ExecResponse
from chk.modules.validate import call


class TestValidateCall:
    """TestValidateCall"""

    @staticmethod
    def test_fail() -> None:
        file_ctx = FileContext(
            document={
                # "version": "default:validate:0.7.2",
                "asserts": [
                    {
                        "type": "Equal",
                        "actual": "<% _data.roll %>",
                        "expected": 39,
                    }
                ],
                "expose": ["<% _asserts_response %>"],
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
    def test_fail_for_wrong_key() -> None:
        file_ctx = FileContext(
            document={
                "version": "default:validate:0.7.2",
                "asserts": [
                    {
                        "type": "Equals",
                        "actual": "<% _data.roll %>",
                        "expected": 39,
                    }
                ],
                "data": {
                    "roll": 39
                },
                "expose": ["<% _asserts_response %>"],
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
        assert isinstance(er.exception, KeyError)
