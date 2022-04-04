"""
main driver
"""
from chk.infrastructure.file_loader import ChkFileLoader
from chk.modules.http.presentation import ResponseToStringFormatter
from chk.modules.version.support import SpecificationLoader
from chk.infrastructure.work import handle_worker


def execute(file: str):
    """execute command"""
    # ChkFileLoader.is_file_ok(file)
    #
    # document = ChkFileLoader.to_dict(file)
    # document_ver = get_document_version(document)
    #
    # http_config = AbstractSpecConfig.from_version(document_ver)
    # http_config.document = document
    # http_config.validate_config()
    #
    # doc = dotmap.DotMap(http_config.document)  # type: ignore
    #
    # request_args = prepare_request_args(doc.request)
    # response = do_http_request(request_args)
    # fmt_str = ResponseToStringFormatter(response).get()
    #
    # print(fmt_str)  # print data

    ChkFileLoader.is_file_ok(file)
    document = ChkFileLoader.to_dict(file)

    http_spec = SpecificationLoader.to_spec_config(document)

    handle_worker(http_spec)
    fmt_str = ResponseToStringFormatter(http_spec.response)

    print(fmt_str.get())  # print data
