"""
testcase module's driver
"""
from chk.infrastructure.file_loader import FileContext
from chk.modules.testcase.entities import Testcase
from chk.infrastructure.work import handle_worker


def execute(file_ctx: FileContext) -> None:
    """Execute command functionality"""
    testcase = Testcase(file_ctx)
    try:
        handle_worker(testcase)
    except RuntimeError as ex:
        raise SystemExit(ex) from ex
