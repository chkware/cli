"""
version related support services
"""
from cerberus.validator import DocumentError
from chk.infrastructure.exception import err_message
from chk.modules.version.constants import BaseConfigElements
from chk.modules.version.validation_rules import version_schema


class VersionMixin_V072:
    """ Mixin for version spec. for v0.7.2"""

    def rules(self) -> dict:
        """Get validation schema"""
        return version_schema

    def validated(self) -> dict[str, str]:
        """Validate the schema against config"""
        try:
            version_doc = self.as_dict()
            if not self.validator.validate(version_doc, self.rules()):  # type: ignore
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))  # type: ignore
        except DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err
        else:
            return version_doc  # or is a success

    def as_dict(self) -> dict[str, str]:
        """Get version string"""
        if not hasattr(self, 'validator') or not hasattr(self, 'document'):
            raise SystemExit(err_message('fatal.V0005'))

        try:
            return {BaseConfigElements.VERSION: str(self.document[BaseConfigElements.VERSION])}  # type: ignore
        except:
            raise SystemExit(err_message('fatal.V0005'))
