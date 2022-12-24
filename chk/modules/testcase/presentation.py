"""
Presenting assert data
"""
from typing import TypeAlias
from dataclasses import dataclass

from chk.infrastructure.file_loader import FileContext


@dataclass
class AssertResult:
    """
    Holds assertion result after test run complete
    """

    name: str
    name_run: str
    actual_original: str
    is_success: bool = True
    message: str = ""
    assert_fn: str = ""


AssertResultList: TypeAlias = list[AssertResult]


class Presentation:
    @staticmethod
    def displayable_file_info(file_ctx: FileContext) -> str:
        return f"File: {file_ctx.filepath}\n"

    @staticmethod
    def displayable_string(string: str) -> str:
        if type(string) != str:
            return str(string)

        return string

    @staticmethod
    def displayable_assert_status(assert_name: str, actual: str, status: str) -> str:
        return f"- Running `{assert_name}` on `{actual}` [{status}]"

    @staticmethod
    def displayable_assert_message(message: str) -> str:
        return f"---\n{message}"
