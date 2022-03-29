"""
Versioned schema repository for http specifications
"""
from typing import Dict
from chk.modules.version.entities import AbstractSpecConfig, VersionConfigV072
from chk.modules.http.validation_rules import request_schema
from cerberus.validator import DocumentError
from chk.infrastructure.exception import err_message


class HttpConfigV072(AbstractSpecConfig):
    """http config v0.7.2"""
    def __init__(self):
        super().__init__()
        self.version_config = VersionConfigV072()

    def get_schema(self) -> Dict:
        """create and validate schema against the dict passed"""
        return self.version_config.get_schema() | request_schema

    def validate_config(self) -> bool:
        """Validate the schema against config"""
        self.version_config.document = self.document
        self.version_config.validate_config()  # validate version

        try:
            if not self.validator.validate(self.document, self.get_schema()):  # validate request
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))
        except DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err
        else:
            return True  # or is a success

# --------------

class RequestMixin_V072:
    
    def rules(self) -> Dict:
        """ get schema"""
        return request_schema
    
    def validate(self) -> Dict:
        """Validate the schema against config"""
        if not hasattr(self, 'validator') or not hasattr(self, 'document'):
            raise SystemExit(err_message('fatal.V0005'))
        
        try:
            if not self.validator.validate(self.document, self.rules()):  # validate request
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))
        except DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err
        else:
            return True  # or is a success