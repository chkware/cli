"""
Main driver
"""
import sys
from traceback import print_exc

from chk.infrastructure.contexts import app
from chk.infrastructure.work import handle_worker
from chk.infrastructure.file_loader import FileContext

from chk.modules.http.entities import HttpSpec
from chk.modules.http.presentation import present_result


def execute(file_ctx: FileContext) -> None:
    """Execute command functionality"""

    http_spec = HttpSpec(file_ctx)
    try:
        response = handle_worker(http_spec)
        app.print_fmt(response, present_result)
    except RuntimeError:
        print_exc(file=sys.stderr)
