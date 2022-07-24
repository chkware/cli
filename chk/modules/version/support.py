"""
version related support services
"""

from cerberus import validator

from chk.infrastructure.exception import err_message
from chk.modules.version.constants import VersionConfigNode, DocumentType
from chk.modules.version.validation_rules import version_schema_http, version_schema_testcase


class VersionMixin(object):
    """ Mixin for version spec. for v0.7.2"""

    def version_validated(self, doc_type: DocumentType) -> dict[str, str]:
        """Validate the schema against config"""
        try:
            version_doc = self.version_as_dict()
            version_schema = {}

            match doc_type:
                case DocumentType.HTTP: version_schema = version_schema_http
                case DocumentType.TESTCASE: version_schema = version_schema_testcase

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

    def get_document_type(self) -> DocumentType:
        """
        Get document type
        :return: DocumentType
        """
        version_doc = self.version_as_dict().get(VersionConfigNode.VERSION)

        version_doc_l = str(version_doc).split(':')
        if len(version_doc_l) < 2:
            raise SystemExit('get_document_type: Invalid version type')

        return DocumentType.from_value(version_doc_l.pop(1))
