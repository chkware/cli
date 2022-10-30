"""
version related support services
"""
import abc

from cerberus.validator import DocumentError

from chk.infrastructure.exception import err_message
from chk.infrastructure.contexts import validator, app
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import dict_get

from chk.modules.version.constants import VersionConfigNode, DocumentType
from chk.modules.version.validation_rules import (
    version_schema_http,
    version_schema_testcase,
)


class DocumentMixin:
    """Document mixin"""

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """Abstract method to get file context"""

    def as_dict(self, key: str, include_key: bool = True) -> dict:
        """Get a spec part of doc by its key"""

        document = app.get_original_doc(self.get_file_context().filepath_hash)

        if not document:
            raise RuntimeError(
                err_message("fatal.V0009", extra="Original document missing")
            )

        value = dict_get(document, key)
        if not value:
            raise RuntimeError(
                err_message("fatal.V0009", extra="Document missing")
            )

        return value if include_key is False else {key: value}


class VersionMixin(DocumentMixin):
    """Mixin for version spec. for v0.7.2"""

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """Abstract method to get file context"""

    def version_validated(self) -> dict[str, str]:
        """Validate the schema against config"""

        try:
            version_doc = self.version_as_dict()
            version_schema = self.get_validation_schema()

            if not validator.validate(version_doc, version_schema):
                raise SystemExit(err_message("fatal.V0006", extra=validator.errors))
        except DocumentError as doc_err:
            raise SystemExit(err_message("fatal.V0001", extra=doc_err)) from doc_err

        return version_doc  # or is a success

    def version_as_dict(self) -> dict[str, str]:
        """Get version as dictionary"""

        file_ctx = self.get_file_context()
        document = app.get_original_doc(file_ctx.filepath_hash)

        try:
            return {
                key: document[key]
                for key in (VersionConfigNode.VERSION,)
                if key in document
            }
        except Exception as ex:
            raise SystemExit(err_message("fatal.V0005", extra=ex)) from ex

    def get_document_type(self) -> DocumentType:
        """Get document type"""

        version_doc = self.version_as_dict().get(VersionConfigNode.VERSION)
        version_doc_l = str(version_doc).split(":")

        if len(version_doc_l) < 2:
            raise SystemExit("get_document_type: Invalid version type")

        return DocumentType.from_value(version_doc_l.pop(1))

    def get_validation_schema(self) -> dict[str, dict]:
        """Get validation schema based on document version"""

        match self.get_document_type():
            case DocumentType.HTTP:
                return version_schema_http
            case DocumentType.TESTCASE:
                return version_schema_testcase
            case _:
                raise RuntimeError(err_message('fatal.V0004'))


class RawFileVersionParser:
    """Utility to parse version string from raw file"""

    @staticmethod
    def find_version_str(file: str) -> str:
        """Read a document in raw format, and find version string"""

        try:
            with open(file, encoding="UTF-8") as file_handle:
                file_content = file_handle.readlines()
                version_doc = next(
                    each_line
                    for each_line in file_content
                    if each_line.startswith("version:")
                )

                version_doc = version_doc.strip(" \r\n")
                version_parts = [item.strip(" '") for item in version_doc.split(":", 1)]

                if len(version_parts) < 2:
                    return ""

                return version_parts[1]

        except (FileNotFoundError, StopIteration):
            return ""

    @staticmethod
    def convert_version_str_to_num(version_str: str) -> str:
        """Convert a chkware supported version string to numeric"""

        if len(version_str) == 0:
            return ""

        version_part_list = version_str.split(":")
        version_number = version_part_list[-1].strip("'")

        return version_number.replace(".", "").replace("_", "").replace("-", "")
