"""
Commands
"""
from types import MappingProxyType
from typing import Any

import click

import chk.modules.http.main as http_executor
import chk.modules.testcase.main as testcase_executor

from chk.infrastructure.file_loader import ChkFileLoader, FileContext


# run command
@click.command('http')
@click.argument('file')
@click.option('--result', is_flag=True, help="Only shows the returned output")
def execute_http(file: str, result: bool) -> None:
    """Command to run Http config file.\r\n
    FILE: Any .chk file, that has 'version: default.http.*' string in it."""

    ctx = FileContext.from_file(file, options={"result": result})

    http_executor.execute(ctx)


# run command
@click.command('testcase')
@click.argument('file')
@click.option('--result', is_flag=True, help="Only shows the returned output")
def execute_testcase(file: str, result: bool) -> None:
    """Command to run Testcase config file.\r\n
    FILE: Any .chk file, that has 'version: default.testcase.*' string in it."""

    ctx = FileContext.from_file(file, options={"result": result})

    testcase_executor.execute(ctx)


# root command
@click.group('chk')
def execute_root() -> None:
    """v0.4.0 | supported version strings: 0.7.2"""


execute_root.add_command(execute_http)  # add `http` as sub-command
execute_root.add_command(execute_testcase)  # add `testcase` as sub-command
