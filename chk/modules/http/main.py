"""
main driver
"""
from chk.infrastructure.file_loader import ChkFileLoader, FileContext
from chk.infrastructure.work import handle_worker
from chk.modules.http.entities import HttpSpec_V072
from chk.modules.http.presentation import Presentation


def execute(file: str):
    """execute command"""
    ChkFileLoader.is_file_ok(file)
    document = ChkFileLoader.to_dict(file)
    fpath_mangled, fpath_hash = ChkFileLoader.get_mangled_name(file)

    file_ctx = FileContext(file, fpath_mangled, fpath_hash, document)
    http_spec = HttpSpec_V072(file_ctx)

    response = handle_worker(http_spec)
    print(Presentation.displayable_execution_summary(file_ctx.filepath))  # print execution summary
    print(Presentation.displayable_result(response))  # print data
