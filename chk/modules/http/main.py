"""
main driver
"""
import dotmap

from chk.console.app_container import app
from chk.infrastructure.file_loader import ChkFileLoader
from chk.modules.http.presentation import ResponseToStringFormatter
from chk.modules.http.request_helper import prepare_request_args, do_http_request
from chk.modules.version.entities import get_document_version, AbstractSpecConfig


def execute(file: str):
    """execute command"""
    if ChkFileLoader.is_file_ok(file):
        # load as dict
        document = ChkFileLoader.to_dict(file)
        document_ver = get_document_version(document)

        http_config = AbstractSpecConfig.from_version(document_ver)
        http_config.document = document
        http_config.validate_config()

        doc = dotmap.DotMap(http_config.document)  # type: ignore

        request_args = prepare_request_args(doc.request)
        response = do_http_request(request_args)
        fmt_str = ResponseToStringFormatter(response).get()

        print(fmt_str)  # print data
    else:
        raise SystemExit(app.messages.exception.fatal.V0002)
