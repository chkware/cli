"""Commands"""

import click

import chk.modules.http.main as http_executor
import chk.modules.testcase.main as testcase_executor
import chk.modules.fetch as fetch_executor
import chk.modules.validate as validate_executor

from chk.infrastructure.file_loader import ExecuteContext, FileContext, FileLoader


def load_variables_as_dict(json_str: str, expect_msg: str) -> dict:
    """Reads a json string and converts to dict while doing validation

    Args:
        json_str: str
        expect_msg: str
    Returns:
        dict containing json_str
    """

    if json_str:
        try:
            return FileLoader.load_json_from_str(json_str)
        except Exception:
            raise click.UsageError(expect_msg)

    return {}


def after_hook(resp: object) -> None:
    """Saves custom data from commands to global context bus

    Args:
        resp: object
    """

    if curr_ctx := click.get_current_context():
        if curr_ctx.parent:
            if not curr_ctx.parent.obj:
                curr_ctx.parent.obj = {}

            curr_ctx.parent.obj |= resp
    else:
        raise RuntimeError("Default context not found")


# root command
@click.group
@click.pass_context
def chk(ctx: click.Context) -> None:
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
    ctx.ensure_object(dict)


# run fetch sub-command
@chk.command
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "-nf", "--no-format", is_flag=True, help="No formatting to show the output"
)
@click.option("-V", "--variables", type=str, help="Pass variable(s) as JSON object")
def fetch(file: str, no_format: bool, variables: str) -> None:
    """\b
    Command to run Http config files.
    FILE: Any .chk file, that has any of the following versions:

    \b
    - default.http.*"""

    ctx: FileContext = FileContext.from_file(file)

    execution_ctx = ExecuteContext(
        {
            "dump": True,
            "format": not no_format,
        },
        {
            "variables": load_variables_as_dict(
                variables,
                "-V, --variables accept values as JSON object",
            )
        },
    )

    fetch_executor.execute(ctx, execution_ctx, after_hook)


# run validate sub-command
@chk.command
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "-nf", "--no-format", is_flag=True, help="No formatting to show the output"
)
@click.option("-V", "--variables", type=str, help="Pass variable(s) as JSON object")
@click.option("-D", "--data", type=str, help="Pass data as JSON")
def validate(file: str, no_format: bool, variables: str, data: str) -> None:
    """\b
    Command to run Http config files.
    FILE: Any .chk file, that has any of the following versions:

    \b
    - default.http.*"""

    ctx: FileContext = FileContext.from_file(file)

    execution_ctx = ExecuteContext(
        {
            "dump": True,
            "format": not no_format,
        },
        {
            "variables": load_variables_as_dict(
                variables,
                "-V, --variables accept values as JSON object",
            ),
            "data": load_variables_as_dict(
                data,
                "-D, --data accept values as JSON object",
            ),
        },
    )

    validate_executor.execute(ctx, execution_ctx, after_hook)
