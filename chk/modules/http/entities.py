"""
Entities for http document specification
"""
from chk.infrastructure.contexts import app
from chk.infrastructure.file_loader import ChkFileLoader, FileContext
from chk.infrastructure.work import (
    WorkerContract,
    RequestProcessorContract,
    handle_request,
)

from chk.modules.version.support import VersionMixin
from chk.modules.version.entities import get_version_doc_spec

from chk.modules.http.request_helper import RequestProcessorMixin_PyRequests
from chk.modules.http.support import RequestMixin
from chk.modules.http.constants import RequestConfigNode as RConst

from chk.modules.variables.support import VariableMixin
from chk.modules.variables.constants import LexicalAnalysisType
from chk.modules.variables.entities import get_returnable_variable_doc_spec

__request_document_specification = {
    RConst.ROOT: {
        RConst.URL: "",
        RConst.METHOD: "",
        RConst.PARAMS: {},
        RConst.HEADERS: {},
        RConst.AUTH_BA: {
            RConst.AUTH_BA_USR: "",
            RConst.AUTH_BA_PAS: "",
        },
        RConst.AUTH_BE: {
            RConst.AUTH_BE_TOK: "",
        },
        RConst.BODY_FRM: {},
        RConst.BODY_FRM_DAT: {},
        RConst.BODY_TXT: "",
        RConst.BODY_XML: "",
        RConst.BODY_JSN: {},
    }
}


def get_request_doc_spec() -> dict:
    """
    Get request document specification
    """
    return __request_document_specification


class HttpSpec(
    RequestProcessorMixin_PyRequests,
    VersionMixin,
    RequestMixin,
    VariableMixin,
    WorkerContract,
    RequestProcessorContract,
):
    """
    Holds http specification activity
    """

    def __init__(self, file_ctx: FileContext):
        self.file_ctx = file_ctx

    def get_file_context(self) -> FileContext:
        return self.file_ctx

    def __work__(self) -> dict:
        ctx_document = self.variable_process(LexicalAnalysisType.REQUEST)
        out_response = handle_request(self, ctx_document)
        return self.variable_assemble_values(ctx_document, out_response)

    @staticmethod
    def get_default_http_doc() -> dict:
        """
        Get a http document specification with default values set
        """
        request_dict = get_request_doc_spec()[RConst.ROOT] | get_returnable_variable_doc_spec()
        return get_version_doc_spec() | {RConst.ROOT: request_dict}

    def pre_process(self):
        document = ChkFileLoader.to_dict(self.file_ctx.filepath)
        app.original_doc[self.file_ctx.filepath_hash] = document

        version_doc = self.version_validated()
        request_doc = self.request_validated()
        variable_doc = self.variable_validated()

        app.compiled_doc[self.file_ctx.filepath_hash] = {
            "version": version_doc,
            "request": request_doc,
            "variable": variable_doc,
        }

    def process(self):
        pass

    def make_response(self):
        pass
