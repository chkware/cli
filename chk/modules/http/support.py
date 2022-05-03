"""
Versioned schema repository for http specifications
"""
from cerberus.validator import DocumentError
from chk.infrastructure.exception import err_message
from chk.modules.http.constants import RequestConfigNode
from chk.modules.http.validation_rules import request_schema


class RequestMixin(object):
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
            return {key:self.document[key] for key in (RequestConfigNode.ROOT, ) if key in self.document}  # type: ignore
        except Exception as ex:
            raise SystemExit(err_message('fatal.V0005', extra=ex))
