"""
version related support services
"""
import pydoc

from cerberus import validator, Validator
from chk.infrastructure.exception import err_message
from chk.modules.version.constants import BaseConfigElements, VersionStrToSpecConfigMapping as Mapping
from chk.modules.version.validation_rules import version_schema


class SpecificationLoader:
    """Specification file loading service"""

    @classmethod
    def to_spec_config(cls, document: dict):
        """Creates and returns AbstractSpecConfig from version string"""
        class_map = Mapping.find_by_version(cls.version(document))
        http_config_class = pydoc.locate(class_map)

        if not callable(http_config_class):
            raise SystemExit(err_message('fatal.V0007'))

        return http_config_class(document)

    @classmethod
    def version(cls, document) -> str:
        """check and get version string"""
        return str(document.get(BaseConfigElements.VERSION))


class VersionMixin_V072(object):
    """ Mixin for version spec. for v0.7.2"""

    def rules(self) -> dict:
        """Get validation schema"""
        return version_schema

    def validated(self) -> dict[str, str]:
        """Validate the schema against config"""
        try:
            version_doc = self.as_dict()
            print(version_doc, self.rules())
            if not self.validator.validate(version_doc, self.rules()):  # type: ignore
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))  # type: ignore
        except validator.DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err
        return version_doc  # or is a success

    def as_dict(self) -> dict[str, str]:
        """Get version string"""
        if not hasattr(self, 'validator') or not hasattr(self, 'document'):
            raise SystemExit(err_message('fatal.V0005'))

        try:
            return {BaseConfigElements.VERSION: str(self.document[BaseConfigElements.VERSION])}  # type: ignore
        except:
            raise SystemExit(err_message('fatal.V0005'))
