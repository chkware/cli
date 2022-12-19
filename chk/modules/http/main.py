"""
Main driver
"""
from chk.infrastructure.contexts import app
from chk.infrastructure.work import handle_worker
from chk.infrastructure.file_loader import FileContext

from chk.modules.http.entities import HttpSpec


def present_result(exposable: list) -> str:
    return "\r\n\r\n".join([str(item) for item in exposable])


def execute(file_ctx: FileContext) -> None:
    """Execute command functionality"""

    http_spec = HttpSpec(file_ctx)
    try:
        response = handle_worker(http_spec)
        app.print_fmt(response, present_result)
    except BaseException as error:
        app.print_fmt("\r\n---", ret_s=bool(app.config("buffer_access_off")))
        app.print_fmt(error)
