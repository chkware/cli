"""
Entities for http document specification
"""
from typing import NamedTuple

from chk.infrastructure.containers import EventLog
from chk.infrastructure.contexts import app
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import dict_get
from chk.infrastructure.work import WorkerContract

from chk.modules.version.support import VersionMixin

from chk.modules.http.request_helper import RequestProcessorPyRequests
from chk.modules.http.support import RequestMixin
from chk.modules.http.constants import RequestConfigNode as RConst

from chk.modules.variables.entities import DefaultVariableDoc, DefaultReturnableDoc
from chk.modules.variables.support import VariableMixin


class DefaultRequestDoc(NamedTuple):
    """Default request doc"""

    returnable: dict = DefaultReturnableDoc().doc

    def merged(self, doc: dict) -> dict:
        """Merge given doc with default one"""
        if not doc:
            doc = {}

        return {RConst.ROOT: {**self.returnable, **dict_get(doc, RConst.ROOT, {})}}


class HttpSpec(
    VersionMixin,
    RequestMixin,
    VariableMixin,
    WorkerContract,
):
    """
    Holds http specification activity
    """

    def __init__(self, file_ctx: FileContext):
        self.file_ctx = file_ctx

    def get_file_context(self) -> FileContext:
        return self.file_ctx

    def __before_main__(self) -> None:
        """Validate and prepare doc components"""

        # save original doc
        app.load_original_doc_from_file_context(self.file_ctx)

        # validation
        version_doc = self.version_validated()
        request_doc = self.request_validated()
        variable_doc = self.variable_validated()

        # compile data with defaults
        app.set_compiled_doc(
            self.file_ctx.filepath_hash,
            (
                version_doc
                | DefaultRequestDoc().merged(request_doc)
                | DefaultVariableDoc().merged(variable_doc)
            ),
        )

    def __main__(self) -> None:
        """Process http document"""
        self.variable_prepare_value_table()
        self.lexical_analysis_for_request()

        request_doc = app.get_compiled_doc(self.file_ctx.filepath_hash, RConst.ROOT)
        response = RequestProcessorPyRequests.perform(request_doc)
        app.set_compiled_doc(
            self.file_ctx.filepath_hash, part="__local", value={RConst.ROOT: response}
        )

    def __after_main__(self) -> dict:
        """Prepare response for http document"""
        # return self.variable_assemble_values(self.ctx_document, self.out_response)
