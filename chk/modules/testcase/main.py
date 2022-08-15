"""
testcase module's driver
"""
from chk.infrastructure.file_loader import ChkFileLoader, FileContext
from chk.modules.testcase.entities import Testcase
from chk.infrastructure.work import handle_worker


def execute(file: str):
    """ execute command """
    ChkFileLoader.is_file_ok(file)
    document = ChkFileLoader.to_dict(file)
    fpath_mangled, fpath_hash = ChkFileLoader.get_mangled_name(file)

    file_ctx = FileContext(file, fpath_mangled, fpath_hash, document, None)
    testcase = Testcase(file_ctx)

    response = handle_worker(testcase)
