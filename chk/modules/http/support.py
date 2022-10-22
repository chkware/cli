"""
Versioned schema repository for http specifications
"""
import abc
from collections.abc import Callable
from copy import deepcopy

from cerberus.validator import DocumentError

from chk.infrastructure.contexts import validator, app
from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext

from chk.modules.http.constants import RequestConfigNode
from chk.modules.http.validation_rules import request_schema


class RequestValueHandler:
    """Handle variables and values regarding request"""

    @staticmethod
    def request_fill_val(
        document: dict, symbol_table: dict, replace_method: Callable[[dict, dict], dict]
    ):
        """Convert request block variables"""

        request_document = document.get(RequestConfigNode.ROOT, {})
        request_document = deepcopy(request_document)

        return replace_method(request_document, symbol_table)

    @staticmethod
    def request_get_return(document: dict, response: dict) -> dict:
        """Return request block variables"""
        returnable = response
        returnable["have_all"] = True

        if req := document.get(RequestConfigNode.ROOT, {}):
            if ret := req.get(RequestConfigNode.RETURN):
                ret = str(ret)
                if not ret.startswith("."):
                    raise ValueError("Unsupported key format in request.return")

                ret = ret.lstrip(".")
                if ret not in ("version", "code", "reason", "headers", "body"):
                    raise ValueError("Unsupported key in request.return")

                def fx(k: object, v: object) -> object:
                    return None if k != ret else v

                returnable = {key: fx(key, value) for key, value in response.items()}
                returnable["have_all"] = False

        return returnable


class RequestMixin:
    """Mixin for request spec. for v0.7.2"""

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """Abstract method to get file context"""

    def request_validated(self) -> dict[str, dict]:
        """Validate the schema against config"""

        try:
            request_doc = self.request_as_dict()
            if not validator.validate(request_doc, request_schema):
                raise SystemExit(err_message("fatal.V0006", extra=validator.errors))
        except DocumentError as doc_err:
            raise SystemExit(err_message("fatal.V0001", extra=doc_err)) from doc_err
        else:
            return request_doc  # or is a success

    def request_as_dict(self, compiled=False) -> dict:
        """Get request as a dictionary"""

        hf_name = self.get_file_context().filepath_hash
        document = (
            app.get_original_doc(hf_name).copy()
            if compiled is False
            else app.get_compiled_doc(hf_name).copy()
        )

        try:
            return {
                key: document[key]
                for key in (RequestConfigNode.ROOT,)
                if key in document
            }
        except Exception as ex:
            raise SystemExit(err_message("fatal.V0005", extra=ex)) from ex
