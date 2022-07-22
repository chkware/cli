"""
version related support services
"""

from cerberus import validator

from chk.infrastructure.exception import err_message
from chk.modules.version.constants import VersionConfigNode
from chk.modules.version.validation_rules import version_schema


class VersionMixin(object):
    """ Mixin for version spec. for v0.7.2"""

    def version_validated(self) -> dict[str, str]:
        """Validate the schema against config"""
        try:
            version_doc = self.version_as_dict()
            if not self.validator.validate(version_doc, version_schema):
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))
        except validator.DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err

        return version_doc  # or is a success

    def version_as_dict(self) -> dict[str, str]:
        """Get version string"""
        if not hasattr(self, 'validator') or not hasattr(self, 'document'):
            raise SystemExit(err_message('fatal.V0005'))

        try:
            return {key: self.document[key] for key in (VersionConfigNode.VERSION,) if key in self.document}
        except Exception as ex:
            raise SystemExit(err_message('fatal.V0005', extra=ex))
