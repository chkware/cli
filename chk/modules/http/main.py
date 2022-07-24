"""
main driver
"""
from chk.infrastructure.file_loader import ChkFileLoader, FileContext
from chk.infrastructure.work import handle_worker
from chk.modules.http.entities import HttpSpec
from chk.modules.http.presentation import make_displayable


def execute(file: str):
    """execute command"""
    ChkFileLoader.is_file_ok(file)
    document = ChkFileLoader.to_dict(file)
    fpath_mangled, fpath_hash = ChkFileLoader.get_mangled_name(file)

    file_ctx = FileContext(file, fpath_mangled, fpath_hash, document)
    http_spec = HttpSpec(file_ctx)

    response = handle_worker(http_spec)
    print(make_displayable(response))  # print data
