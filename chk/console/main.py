"""Commands"""

import click

import chk.modules.fetch as fetch_executor
import chk.modules.validate as validate_executor
import chk.modules.workflow as workflow_executor
from chk.console.services import (
    after_hook,
    combine_initial_variables,
    get_stdin,
    load_variables_as_dict,
    setup_logger,
)
from chk.infrastructure.file_loader import ExecuteContext, FileContext
from chk.infrastructure.logging import with_catch_log

VAR_ERROR_MSG = "-V, --variables accept values as JSON object"


# root command
@click.group()
@click.option(
    "--debug/--no-debug", is_flag=True, default=True, help="Enable debug logging"
)
@click.pass_context
def chk(ctx: click.Context, debug: bool) -> None:
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
    Version 0.5.0
    """
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug

    setup_logger(debug)


# run fetch sub-command
@chk.command()
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "-nf", "--no-format", is_flag=True, help="No formatting to show the output"
)
@click.option("-V", "--variables", type=str, help="Pass variable(s) as JSON object")
@click.pass_context
def fetch(cctx: click.Context, file: str, no_format: bool, variables: str) -> None:
    """\b
    Command to run HTTP config files.
    FILE: Any .chk, .yaml and .yml file, that has any of the following versions:

    \b
    - default.http.*"""

    ctx: FileContext = FileContext.from_file(file)

    execution_ctx = ExecuteContext(
        {
            "dump": True,
            "format": not no_format,
            "debug": cctx.obj.get("debug", False),
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
@click.option("-Di", "--data-in", is_flag=True, help="Pass data as JSON [from pipe]")
@click.pass_context
def validate(
    cctx: click.Context,
    file: str,
    no_format: bool,
    variables: str,
    data: str,
    data_in: bool,
) -> None:
    """\b
    Command to run Validation specification files.
    FILE: Any .chk, .yaml and .yml file, that has any of the following versions:

    \b
    - default.validate.*"""

    ctx: FileContext = FileContext.from_file(file)

    with with_catch_log():
        _data = (
            load_variables_as_dict(
                get_stdin(), except_msg="-Di, --data-in: Pass data as JSON [from pipe]"
            )
            if data_in
            else load_variables_as_dict(
                data, except_msg="-D, --data: Pass data as JSON"
            )
        )

    execution_ctx = ExecuteContext(
        {
            "dump": True,
            "format": not no_format,
            "debug": cctx.obj.get("debug", False),
        },
        {
            "variables": combine_initial_variables(
                variables,
                except_msg=VAR_ERROR_MSG,
            ),
            "data": _data,
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
@click.pass_context
def workflow(cctx: click.Context, file: str, no_format: bool, variables: str) -> None:
    """\b
    Command to run Workflow specification files.
    FILE: Any .chk, .yaml and .yml file, that has any of the following versions:

    \b
    - default.workflow.*"""

    ctx: FileContext = FileContext.from_file(file)

    execution_ctx = ExecuteContext(
        {
            "dump": True,
            "format": not no_format,
            "debug": cctx.obj.get("debug", False),
        },
        {
            "variables": combine_initial_variables(
                variables,
                except_msg=VAR_ERROR_MSG,
            ),
        },
    )

    workflow_executor.execute(ctx, execution_ctx, after_hook)
