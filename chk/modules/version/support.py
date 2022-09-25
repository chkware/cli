"""
version related support services
"""
import abc

from cerberus.validator import DocumentError

from chk.infrastructure.exception import err_message
from chk.infrastructure.contexts import validator, app
from chk.infrastructure.file_loader import FileContext

from chk.modules.version.constants import VersionConfigNode, DocumentType
from chk.modules.version.validation_rules import version_schema_http, version_schema_testcase


class VersionMixin:
    """ Mixin for version spec. for v0.7.2"""

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """ Abstract method to get file context """

    def version_validated(self) -> dict[str, str]:
        """ Validate the schema against config """

        try:
            version_doc = self.version_as_dict()
            version_schema = {}

            match self.get_document_type():
                case DocumentType.HTTP: version_schema = version_schema_http
                case DocumentType.TESTCASE: version_schema = version_schema_testcase

            if not validator.validate(version_doc, version_schema):
                raise SystemExit(err_message('fatal.V0006', extra=validator.errors))
        except DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err

        return version_doc  # or is a success

    def version_as_dict(self) -> dict[str, str]:
        """ Get version as dictionary """

        file_ctx = self.get_file_context()
        document = app.original_doc.get(file_ctx.filepath_hash)

        try:
            return {key: document[key] for key in (VersionConfigNode.VERSION,) if key in document}
        except Exception as ex:
            raise SystemExit(err_message('fatal.V0005', extra=ex)) from ex

    def get_document_type(self) -> DocumentType:
        """ Get document type """

        version_doc = self.version_as_dict().get(VersionConfigNode.VERSION)
        version_doc_l = str(version_doc).split(':')

        if len(version_doc_l) < 2:
            raise SystemExit('get_document_type: Invalid version type')

        return DocumentType.from_value(version_doc_l.pop(1))
