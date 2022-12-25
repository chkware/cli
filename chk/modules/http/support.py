"""
Versioned schema repository for http specifications
"""
import abc
from collections.abc import Callable
from cerberus.validator import DocumentError

from chk.infrastructure.contexts import validator, app
from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext

from chk.modules.http.constants import RequestConfigNode as RConf
from chk.modules.http.validation_rules import request_schema

from chk.modules.version.support import DocumentMixin


class RequestMixin(DocumentMixin):
    """Mixin for request spec. for v0.7.2"""

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """Abstract method to get file context"""

    def request_validated(self) -> dict:
        """Validate the schema against config"""

        try:
            request_doc = self.request_as_dict()
            if not validator.validate(request_doc, request_schema):
                raise RuntimeError(err_message("fatal.V0006", extra=validator.errors))
        except DocumentError as doc_err:
            raise RuntimeError(err_message("fatal.V0001", extra=doc_err)) from doc_err

        return request_doc if isinstance(request_doc, dict) else {}

    def request_as_dict(
        self, with_key: bool = True, compiled: bool = False
    ) -> dict | None:
        """Get request as a dictionary"""

        return self.as_dict(RConf.ROOT, with_key, compiled)

    def lexical_analysis_for_request(
        self, symbol_table: dict, replace_fn: Callable
    ) -> None:
        """Lexical analysis for request block"""

        f_hash = self.get_file_context().filepath_hash

        request_document = app.get_compiled_doc(f_hash, RConf.ROOT)
        request_document_replaced = replace_fn(request_document, symbol_table)

        app.set_compiled_doc(
            f_hash,
            part=RConf.ROOT,
            value=request_document_replaced,
        )
