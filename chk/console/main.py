"""Commands"""

import click

import chk.modules.http.main as http_executor
import chk.modules.testcase.main as testcase_executor

from chk.infrastructure.file_loader import FileContext, FileLoader
from chk.infrastructure.helper import parse_args


# run http sub-command
@click.command("http")
@click.argument("file", type=click.Path(exists=True))
@click.option("-r", "--result", is_flag=True, help="Only shows the returned output")
@click.option("-V", "--variables", type=str, help="Pass variable(s) as JSON object")
@click.option(
    "-nf", "--no-format", is_flag=True, help="No formatting to show the output"
)
def execute_http(file: str, result: bool, no_format: bool, variables: str) -> None:
    """Command to run Http config file.\r\n
    FILE: Any .chk file, that has 'version: default.http.*' string in it"""

    variables_j = {}

    if variables:
        try:
            variables_j = FileLoader.load_json_from_str(variables)
        except Exception as ex:
            raise click.UsageError(
                "-V, --variables accept values as JSON object"
            ) from ex

    ctx: FileContext = FileContext.from_file(
        file,
        options={
            "dump": True,
            "result": result,
            "format": not no_format,
        },
        arguments={"variables": variables_j},
    )

    http_executor.execute(ctx)


# run testcase sub-command
@click.command("testcase")
@click.argument("file")
@click.argument("variables", nargs=-1)
@click.option("-r", "--result", is_flag=True, help="Only shows the returned output")
@click.option(
    "-nf", "--no-format", is_flag=True, help="No formatting to show the output"
)
def execute_testcase(
    file: str, variables: tuple, result: bool, no_format: bool
) -> None:
    """Command to run Testcase config file.\r\n
    FILE: Any .chk file, that has 'version: default.testcase.*' string in it."""

    if not all("=" in k for k in variables):
        raise click.UsageError("One or more variable/s is not `=` separated")

    ctx: FileContext = FileContext.from_file(
        file,
        options={
            "dump": True,
            "result": result,
            "format": not no_format,
        },
        arguments={"variables": parse_args(list(variables))},
    )

    testcase_executor.execute(ctx)


# root command
@click.group("chk")
def execute_root() -> None:
    """v0.4.3 | supported version strings: 0.7.2"""


execute_root.add_command(execute_http)  # add `http` as sub-command
execute_root.add_command(execute_testcase)  # add `testcase` as sub-command
