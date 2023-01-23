"""
Entities for http document specification
"""
from typing import NamedTuple

from chk.infrastructure.contexts import app
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import dict_get
from chk.infrastructure.work import WorkerContract

from chk.modules.http.constants import RequestConfigNode as RConst
from chk.modules.http.request_helper import RequestProcessorPyRequests
from chk.modules.http.support import RequestMixin

from chk.modules.variables.entities import (
    DefaultVariableDoc,
    DefaultReturnableDoc,
    DefaultExposableDoc,
    ApiResponse,
)
from chk.modules.variables.support import VariableMixin, replace_values

from chk.modules.version.support import VersionMixin


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
        app.print_fmt(
            f"File: {self.file_ctx.filepath}\r\n",
            ret_s=bool(app.config(self.file_ctx.filepath_hash, "result")),
        )

        # validation
        version_doc = self.version_validated()
        request_doc = self.request_validated()
        variable_doc = self.variable_validated()
        expose_doc = self.expose_validated()

        # compile data with defaults
        app.set_compiled_doc(
            self.file_ctx.filepath_hash,
            (
                version_doc
                | DefaultVariableDoc().merged(variable_doc)
                | DefaultExposableDoc({"expose": ["$_response"]}).merged(expose_doc)
                | request_doc
            ),
        )

    def __main__(self) -> None:
        """Process http document"""
        self.variable_prepare_value_table()
        self.lexical_analysis_for_request(self.get_symbol_table(), replace_values)

        try:
            request_doc = self.request_as_dict(with_key=False, compiled=True)
            if not isinstance(request_doc, dict):
                raise RuntimeError("error: request doc malformed")

            response = RequestProcessorPyRequests.perform(request_doc)

            app.set_local(
                self.file_ctx.filepath_hash,
                ApiResponse.from_dict(response).dict(),  # type: ignore
                RConst.LOCAL,
            )

            app.print_fmt(
                "- Making request [Success]", ret_s=bool(app.config(self.file_ctx.filepath_hash, "result"))
            )
        except RuntimeError as err:
            app.print_fmt("- Making request [Fail]", ret_s=bool(app.config(self.file_ctx.filepath_hash, "result")))
            raise err

    def __after_main__(self) -> list:
        """Prepare response for http document"""

        try:
            self.make_exposable()
            app.print_fmt(
                "- Prepare exposable [Success]", ret_s=bool(app.config(self.file_ctx.filepath_hash, "result"))
            )
            app.print_fmt("\r\n---", ret_s=bool(app.config(self.file_ctx.filepath_hash, "result")))

            return self.get_exposable()
        except RuntimeError as err:
            app.print_fmt(
                "- Prepare exposable [Fail]", ret_s=bool(app.config(self.file_ctx.filepath_hash, "result"))
            )
            raise err
