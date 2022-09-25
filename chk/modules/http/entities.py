"""
Entities for http document specification
"""
from typing import NamedTuple

from chk.infrastructure.contexts import app
from chk.infrastructure.file_loader import ChkFileLoader, FileContext
from chk.infrastructure.work import (
    WorkerContract,
    RequestProcessorContract,
    handle_request,
)

from chk.modules.version.support import VersionMixin

from chk.modules.http.request_helper import RequestProcessorMixin_PyRequests
from chk.modules.http.support import RequestMixin
from chk.modules.http.constants import RequestConfigNode as RConst

from chk.modules.variables.support import VariableMixin
from chk.modules.variables.constants import LexicalAnalysisType


class DefaultRequestDoc(NamedTuple):
    """ Default request doc """

    doc: dict[str, object] = {
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

    def merged(self, doc: dict) -> dict:
        """ Merge given doc with default one """
        if not doc:
            doc = {}

        return doc | self.doc


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

    def pre_process(self) -> None:
        document = ChkFileLoader.to_dict(self.file_ctx.filepath)
        app.original_doc[self.file_ctx.filepath_hash] = document

        version_doc = self.version_validated()
        request_doc = self.request_validated()
        variable_doc = self.variable_validated()

        app.compiled_doc[self.file_ctx.filepath_hash] = {
            "version": version_doc,
            "request": DefaultRequestDoc().merged(request_doc),
            "variable": variable_doc,
        }

    def process(self):
        pass

    def make_response(self):
        pass
