"""
testcase module's driver
"""
import sys
from traceback import print_exc

from chk.infrastructure.contexts import app
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.work import handle_worker

from chk.modules.testcase.entities import Testcase
from chk.modules.testcase.presentation import present_result


def execute(file_ctx: FileContext) -> None:
    """Execute command functionality"""

    testcase = Testcase(file_ctx)
    try:
        response = handle_worker(testcase)
        app.print_fmt(response, present_result)
    except RuntimeError:
        print_exc(file=sys.stderr)
