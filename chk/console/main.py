"""Commands"""
from types import MappingProxyType

import click

import chk.modules.http.main as http_executor
import chk.modules.testcase.main as testcase_executor


# run command
@click.command('http')
@click.argument('file')
@click.option('--result', is_flag=True, help="Only shows the returned output")
def execute_http(file, result):
    """Command to run HTTP request config file.\r\n
    FILE: Any .chk file, that has 'version: default.http.*' string in it."""

    options = MappingProxyType(
        dict(
            result=result,
        ),
    )
    http_executor.execute(file, options)


# run command
@click.command('testcase')
@click.argument('file', nargs=-1)
def execute_testcase(file):
    """Command to run HTTP request config file.\r\n
    FILE: Any .chk file, that has 'version: default.testcase.*' string in it."""

    file = list(file).pop(0)
    testcase_executor.execute(file)


# root command
@click.group('chk')
def execute_root():
    """v0.4.0 | supported version strings: 0.7.2"""
    pass


execute_root.add_command(execute_http)  # add `http` as sub-command
execute_root.add_command(execute_testcase)  # add `testcase` as sub-command
