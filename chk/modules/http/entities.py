"""
Versioned schema repository for http specifications
"""
from typing import Dict
from chk.modules.http.validation_rules import request_schema
from cerberus.validator import DocumentError
from chk.infrastructure.exception import err_message
from chk.modules.http.constants import RequestConfigElements_V072


class RequestMixin_V072:
    """ Mixin for request spec. for v0.7.2"""
    def rules(self) -> Dict:
        """ get schema"""
        return request_schema

    def validated(self) -> dict[str, dict]:
        """Validate the schema against config"""
        try:
            request_doc = self.as_dict()
            if not self.validator.validate(request_doc, self.rules()):  # validate request
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))
        except DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err
        else:
            return request_doc  # or is a success

    def as_dict(self) -> dict[str, dict]:
        """Get version string"""
        if not hasattr(self, 'validator') or not hasattr(self, 'document'):
            raise SystemExit(err_message('fatal.V0005'))

        try:
            return {RequestConfigElements_V072.ROOT: dict(self.document[RequestConfigElements_V072.ROOT])}
        except:
            raise SystemExit(err_message('fatal.V0005'))
