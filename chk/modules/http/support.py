"""
Versioned schema repository for http specifications
"""
from cerberus.validator import DocumentError
from chk.infrastructure.exception import err_message
from chk.modules.http.constants import RequestConfigElements_V072
from chk.modules.http.validation_rules import request_schema


class RequestMixin_V072(object):
    """ Mixin for request spec. for v0.7.2"""

    def request_validated(self) -> dict[str, dict]:
        """Validate the schema against config"""
        try:
            request_doc = self.request_as_dict()
            if not self.validator.validate(request_doc, request_schema):  # type: ignore
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))  # type: ignore
        except DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err
        else:
            return request_doc  # or is a success

    def request_as_dict(self) -> dict[str, dict]:
        """Get version string"""
        if not hasattr(self, 'validator') or not hasattr(self, 'document'):
            raise SystemExit(err_message('fatal.V0005'))

        try:
            return {RequestConfigElements_V072.ROOT: dict(self.document[RequestConfigElements_V072.ROOT])}  # type: ignore
        except:
            raise SystemExit(err_message('fatal.V0005'))
