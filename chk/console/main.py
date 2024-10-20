"""Commands"""

import click

import chk.modules.fetch as fetch_executor
import chk.modules.validate as validate_executor
import chk.modules.workflow as workflow_executor
from chk.console.services import (
    after_hook,
    combine_initial_variables,
    load_variables_as_dict,
)
from chk.infrastructure.file_loader import ExecuteContext, FileContext

VAR_ERROR_MSG = "-V, --variables accept values as JSON object"


# root command
@click.group()
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
    Version 0.5.0, supported version strings: 0.7.2
    """
    ctx.ensure_object(dict)


# run fetch sub-command
@chk.command()
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
            "variables": combine_initial_variables(
                variables,
                except_msg=VAR_ERROR_MSG,
            )
        },
    )

    fetch_executor.execute(ctx, execution_ctx, after_hook)


# run validate sub-command
@chk.command()
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "-nf", "--no-format", is_flag=True, help="No formatting to show the output"
)
@click.option("-V", "--variables", type=str, help="Pass variable(s) as JSON object")
@click.option("-D", "--data", type=str, help="Pass data as JSON")
def validate(file: str, no_format: bool, variables: str, data: str) -> None:
    """\b
    Command to run Validation specification files.
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
            "variables": combine_initial_variables(
                variables,
                except_msg=VAR_ERROR_MSG,
            ),
            "data": load_variables_as_dict(
                data,
                except_msg="-D, --data accept values as JSON object",
            ),
        },
    )

    validate_executor.execute(ctx, execution_ctx, after_hook)


# run validate sub-command
@chk.command()
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "-nf", "--no-format", is_flag=True, help="No formatting to show the output"
)
@click.option("-V", "--variables", type=str, help="Pass variable(s) as JSON object")
def workflow(file: str, no_format: bool, variables: str) -> None:
    """\b
    Command to run Workflow specification files.
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
            "variables": combine_initial_variables(
                variables,
                except_msg=VAR_ERROR_MSG,
            ),
        },
    )

    workflow_executor.execute(ctx, execution_ctx, after_hook)
