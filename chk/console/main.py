"""Commands"""

import click

import chk.modules.http.main as http_executor
import chk.modules.testcase.main as testcase_executor
import chk.modules.fetch as fetch_executor

from chk.infrastructure.file_loader import ExecuteContext, FileContext, FileLoader


def load_variables_as_dict(variables: str) -> dict:
    """Reads a json string and converts to dict while doing validation

    Args:
        variables: str
    Returns:
        dict containing variables
    """
    if variables:
        try:
            return FileLoader.load_json_from_str(variables)
        except Exception:
            raise click.UsageError("-V, --variables accept values as JSON object")

    return {}


# root command
@click.group()
def chk() -> None:
    """\b
       █████████  █████   █████ █████   ████
      ███░░░░░███░░███   ░░███ ░░███   ███░
     ███     ░░░  ░███    ░███  ░███  ███    █████ ███ █████  ██████   ████████   ██████
    ░███          ░███████████  ░███████    ░░███ ░███░░███  ░░░░░███ ░░███░░███ ███░░███
    ░███          ░███░░░░░███  ░███░░███    ░███ ░███ ░███   ███████  ░███ ░░░ ░███████
    ░░███     ███ ░███    ░███  ░███ ░░███   ░░███████████   ███░░███  ░███     ░███░░░
     ░░█████████  █████   █████ █████ ░░████  ░░████░████   ░░████████ █████    ░░██████
      ░░░░░░░░░  ░░░░░   ░░░░░ ░░░░░   ░░░░    ░░░░ ░░░░     ░░░░░░░░ ░░░░░      ░░░░░░

    \b
    Low-code API quality testing, and automation toolbox.
    Version 0.4.3, supported version strings: 0.7.2
    """


# run http sub-command
@chk.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("-r", "--result", is_flag=True, help="Only shows the returned output")
@click.option(
    "-nf", "--no-format", is_flag=True, help="No formatting to show the output"
)
@click.option("-V", "--variables", type=str, help="Pass variable(s) as JSON object")
def fetch(file: str, result: bool, no_format: bool, variables: str) -> None:
    """\b
    Command to run Http config files.
    FILE: Any .chk file, that has any of the following versions:

    \b
    - default.http.*"""

    ctx: FileContext = FileContext.from_file(file)

    execution_ctx = ExecuteContext(
        {
            "dump": True,
            "result": result,
            "format": not no_format,
        },
        {"variables": load_variables_as_dict(variables)},
    )

    fetch_executor.execute(ctx, execution_ctx)


# run http sub-command
@chk.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("-r", "--result", is_flag=True, help="Only shows the returned output")
@click.option(
    "-nf", "--no-format", is_flag=True, help="No formatting to show the output"
)
@click.option("-V", "--variables", type=str, help="Pass variable(s) as JSON object")
def http(file: str, result: bool, no_format: bool, variables: str) -> None:
    """\b
    Command to run Http config file.
    FILE: Any .chk file, that has 'version: default.http.*' string in it"""

    variables_j = load_variables_as_dict(variables)

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
@chk.command()
@click.argument("file")
@click.option("-r", "--result", is_flag=True, help="Only shows the returned output")
@click.option(
    "-nf", "--no-format", is_flag=True, help="No formatting to show the output"
)
@click.option("-V", "--variables", type=str, help="Pass variable(s) as JSON object")
def testcase(file: str, result: bool, no_format: bool, variables: str) -> None:
    """\b
    Command to run Testcase config file.
    FILE: Any .chk file, that has 'version: default.testcase.*' string in it."""

    variables_j = load_variables_as_dict(variables)

    ctx: FileContext = FileContext.from_file(
        file,
        options={
            "dump": True,
            "result": result,
            "format": not no_format,
        },
        arguments={"variables": variables_j},
    )

    testcase_executor.execute(ctx)
