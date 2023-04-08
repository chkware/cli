"""Commands"""

import click
from click import Context

import chk.modules.http.main as http_executor
import chk.modules.testcase.main as testcase_executor

from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import parse_args


# root command
@click.group()
@click.pass_context
def chk(ctx: Context) -> None:
    """\b
       █████████  █████   █████ █████   ████
      ███░░░░░███░░███   ░░███ ░░███   ███░
     ███     ░░░  ░███    ░███  ░███  ███    █████ ███ █████  ██████   ████████   ██████
    ░███          ░███████████  ░███████    ░░███ ░███░░███  ░░░░░███ ░░███░░███ ███░░███
    ░███          ░███░░░░░███  ░███░░███    ░███ ░███ ░███   ███████  ░███ ░░░ ░███████
    ░░███     ███ ░███    ░███  ░███ ░░███   ░░███████████   ███░░███  ░███     ░███░░░
     ░░█████████  █████   █████ █████ ░░████  ░░████░████   ░░████████ █████    ░░██████
      ░░░░░░░░░  ░░░░░   ░░░░░ ░░░░░   ░░░░    ░░░░ ░░░░     ░░░░░░░░ ░░░░░      ░░░░░░

    v0.4.3 | supported version strings: 0.7.2"""
    ctx.ensure_object(dict)


# run http sub-command
@chk.command()
@click.argument("file", type=click.Path(exists=True))
@click.argument("variables", nargs=-1)
@click.option(
    "-r",
    "--result",
    is_flag=True,
    help="Only shows the returned output",
)
@click.option(
    "-nf",
    "--no-format",
    is_flag=True,
    help="No formatting to show the output",
)
def http(file: str, variables: tuple, result: bool, no_format: bool) -> None:
    """
    \b
    Command to run Http config file.

    FILE: Any .chk file, that has 'version: default.http.*' string in it.
    VARIABLES: Space separated Name=Value. eg: Name='User Name' Age=17"""

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

    http_executor.execute(ctx)


# run testcase sub-command
@chk.command()
@click.argument("file")
@click.argument("variables", nargs=-1)
@click.option(
    "-r",
    "--result",
    is_flag=True,
    help="Only shows the returned output",
)
@click.option(
    "-nf",
    "--no-format",
    is_flag=True,
    help="No formatting to show the output",
)
def testcase(file: str, variables: tuple, result: bool, no_format: bool) -> None:
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
