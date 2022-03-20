"""
main driver
"""
import dotmap
from chk.console.app_container import app
from chk.infrastructure.file_loader import ChkFileLoader
from chk.modules.http.entities import HttpConfigV072
from chk.modules.http.presentation import ResponseToStringFormatter
from chk.modules.http.request_helper import prepare_request_args, do_http_request


def execute(file: str):
    """execute command"""
    if ChkFileLoader.is_file_ok(file):
        # load as dict
        doc = ChkFileLoader.to_dict(file)

        doc_ver = HttpConfigV072()
        doc_ver.validate_config(doc)
        del doc_ver

        doc = dotmap.DotMap(doc)

        request_args = prepare_request_args(doc.request)
        response = do_http_request(request_args)
        fmt_str = ResponseToStringFormatter(response).get()

        print(fmt_str)  # print data
    else:
        raise SystemExit(app.messages.exception.fatal.V0002)
