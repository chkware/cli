"""Commands"""
from types import MappingProxyType

import click

import chk.modules.http.main as http_executor
import chk.modules.test_spec.main as test_spec_executor


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
@click.command('test-spec')
@click.argument('file', nargs=-1)
def execute_test_spec(file):
    """Command to run HTTP request config file.\r\n
    FILE: Any .chk file, that has 'version: default.test-spec.*' string in it."""
    test_spec_executor.execute()


# root command
@click.group('chk')
def execute_root():
    """v0.3.4 | supported version strings: 0.7.2"""
    pass


execute_root.add_command(execute_http)  # add `http` as sub-command
# execute_root.add_command(execute_test_spec)  # add `http` as sub-command
