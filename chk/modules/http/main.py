"""
main driver
"""
from chk.infrastructure.work import handle_worker
from chk.modules.http.entities import HttpSpec
from chk.modules.http.presentation import Presentation

from chk.infrastructure.file_loader import FileContext


def execute(file_ctx: FileContext):
    """ Execute command functionality """
    http_spec = HttpSpec(file_ctx)
    try:
        response = handle_worker(http_spec)
    except BaseException as error:
        response = error
    Presentation.present_result(file_ctx, response)
