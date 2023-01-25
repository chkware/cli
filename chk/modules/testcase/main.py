"""
testcase module's driver
"""
import functools
from typing import Any

import click

from chk.infrastructure.contexts import app
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.work import handle_worker

from chk.modules.testcase.entities import Testcase
from chk.modules.testcase.presentation import present_result


def execute(file_ctx: FileContext) -> Any:
    """Execute command functionality"""

    testcase = Testcase(file_ctx)
    try:
        response = handle_worker(testcase)

        if app.config(file_ctx.filepath_hash, "dump"):
            present_result_t = (
                present_result
                if app.config(file_ctx.filepath_hash, "format")
                else functools.partial(present_result, as_json=True)
            )

            app.print_fmt(response, present_result_t)  # type: ignore

        return response
    except RuntimeError as err:
        return (
            click.echo(f"\r\n---\r\n{str(err)}")
            if app.config(file_ctx.filepath_hash, "dump")
            else err
        )
