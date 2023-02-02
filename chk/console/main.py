"""
Commands
"""
import click

import chk.modules.http.main as http_executor
import chk.modules.testcase.main as testcase_executor

from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import parse_args


# run command
@click.command("http")
@click.argument("file", type=click.Path(exists=True))
@click.argument("variables", nargs=-1)
@click.option("-r", "--result", is_flag=True, help="Only shows the returned output")
@click.option(
    "-nf", "--no-format", is_flag=True, help="No formatting to show the output"
)
def execute_http(file: str, variables: tuple, result: bool, no_format: bool) -> None:
    """Command to run Http config file.\r\n
    FILE: Any .chk file, that has 'version: default.http.*' string in it.
    VARIABLES: Space separated Name=Value. eg: Name='User Name' Age=17"""

    if not all("=" in k for k in variables):
        raise click.UsageError("One or more variable/s is not `=` separated")

    ctx = FileContext.from_file(
        file,
        options={
            "dump": True,
            "result": result,
            "format": not no_format,
        },
        arguments={"variables": parse_args(list(variables))},
    )

    http_executor.execute(ctx)


# run command
@click.command("testcase")
@click.argument("file")
@click.option("-r", "--result", is_flag=True, help="Only shows the returned output")
@click.option(
    "-nf", "--no-format", is_flag=True, help="No formatting to show the output"
)
def execute_testcase(file: str, result: bool, no_format: bool) -> None:
    """Command to run Testcase config file.\r\n
    FILE: Any .chk file, that has 'version: default.testcase.*' string in it."""

    ctx = FileContext.from_file(
        file,
        options={
            "dump": True,
            "result": result,
            "format": not no_format,
        },
    )

    testcase_executor.execute(ctx)


# root command
@click.group("chk")
def execute_root() -> None:
    """v0.4.2 | supported version strings: 0.7.2"""


execute_root.add_command(execute_http)  # add `http` as sub-command
execute_root.add_command(execute_testcase)  # add `testcase` as sub-command
