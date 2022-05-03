"""
version related support services
"""
import pydoc

from cerberus import validator
from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext
from chk.modules.version.constants import VersionConfigNode, VersionStrToSpecConfigMapping as Mapping
from chk.modules.version.validation_rules import version_schema


class SpecificationLoader:
    """Specification file loading service"""

    @classmethod
    def to_spec_config(cls, file_ctx: FileContext):
        """Creates and returns AbstractSpecConfig from version string"""
        class_map = Mapping.find_by_version(cls.version(file_ctx.document))
        http_config_class = pydoc.locate(class_map)

        if not callable(http_config_class):
            raise SystemExit(err_message('fatal.V0007'))

        return http_config_class(file_ctx)

    @classmethod
    def version(cls, document) -> str:
        """check and get version string"""
        return str(document.get(VersionConfigNode.VERSION))


class VersionMixin(object):
    """ Mixin for version spec. for v0.7.2"""

    def version_validated(self) -> dict[str, str]:
        """Validate the schema against config"""
        try:
            version_doc = self.version_as_dict()
            if not self.validator.validate(version_doc, version_schema):  # type: ignore
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))  # type: ignore
        except validator.DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err

        return version_doc  # or is a success

    def version_as_dict(self) -> dict[str, str]:
        """Get version string"""
        if not hasattr(self, 'validator') or not hasattr(self, 'document'):
            raise SystemExit(err_message('fatal.V0005'))

        try:
            return {key:self.document[key] for key in (VersionConfigNode.VERSION, ) if key in self.document}  # type: ignore
        except Exception as ex:
            raise SystemExit(err_message('fatal.V0005', extra=ex))
