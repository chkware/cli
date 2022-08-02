"""
main driver
"""
from types import MappingProxyType

from chk.infrastructure.file_loader import ChkFileLoader, FileContext
from chk.infrastructure.work import handle_worker
from chk.modules.http.entities import HttpSpec
from chk.modules.http.presentation import Presentation


def execute(file: str, options: MappingProxyType[str, bool]):
    """execute command"""
    ChkFileLoader.is_file_ok(file)
    document = ChkFileLoader.to_dict(file)
    fpath_mangled, fpath_hash = ChkFileLoader.get_mangled_name(file)

    file_ctx = FileContext(file, fpath_mangled, fpath_hash, document, options)
    http_spec = HttpSpec(file_ctx)
    try:
        response = handle_worker(http_spec)
    except BaseException as error:
        response = error
    Presentation.present_result(file_ctx, response)
