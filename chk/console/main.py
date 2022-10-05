"""Commands"""
from types import MappingProxyType

import click

import chk.modules.http.main as http_executor
import chk.modules.testcase.main as testcase_executor

from chk.infrastructure.file_loader import ChkFileLoader, FileContext


# run command
@click.command('http')
@click.argument('file')
@click.option('--result', is_flag=True, help="Only shows the returned output")
def execute_http(file, result) -> None:
    """Command to run Http config file.\r\n
    FILE: Any .chk file, that has 'version: default.http.*' string in it."""

    options = MappingProxyType(
        dict(
            result=result,
        ),
    )

    ChkFileLoader.is_file_ok(file)
    fpath_mangled, fpath_hash = ChkFileLoader.get_mangled_name(file)

    ctx = FileContext(
        filepath=file,
        filepath_mangled=fpath_mangled,
        filepath_hash=fpath_hash,
        options=options,
    )

    http_executor.execute(ctx)


# run command
@click.command('testcase')
@click.argument('file')
def execute_testcase(file) -> None:
    """Command to run Testcase config file.\r\n
    FILE: Any .chk file, that has 'version: default.testcase.*' string in it."""

    ChkFileLoader.is_file_ok(file)
    fpath_mangled, fpath_hash = ChkFileLoader.get_mangled_name(file)

    ctx = FileContext(
        filepath=file,
        filepath_mangled=fpath_mangled,
        filepath_hash=fpath_hash,
    )

    testcase_executor.execute(ctx)


# root command
@click.group('chk')
def execute_root():
    """v0.4.0 | supported version strings: 0.7.2"""


execute_root.add_command(execute_http)  # add `http` as sub-command
execute_root.add_command(execute_testcase)  # add `testcase` as sub-command
