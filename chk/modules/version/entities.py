"""
Shared entities
"""
import pydoc

from cerberus import Validator
from cerberus.validator import DocumentError
from chk.infrastructure.exception import err_message
from chk.modules.version.constants import BaseConfigElements, VersionStrToSpecConfigMapping as Mapping
from chk.modules.version.validation_rules import version_schema


class BaseSpecConfig:
    """Base class to all archetype"""

    def __init__(self):
        self.document: dict = {}
        self.validator = Validator()

    @classmethod
    def to_spec_config(cls, version: str = ''):
        """Creates and returns AbstractSpecConfig from version stirng"""
        class_map = Mapping.find_by_version(version)
        http_config_class = pydoc.locate(class_map)

        if not callable(http_config_class):
            raise SystemExit(err_message('fatal.V0007'))

        return http_config_class()

    def version(self) -> str:
        """check and get version string"""
        return str(self.document.get(BaseConfigElements.VERSION))


class VersionMixin_V072:
    """ Mixin for version spec. for v0.7.2"""

    def rules(self) -> dict:
        """Get validation schema"""
        return version_schema

    def validated(self) -> dict[str, str]:
        """Validate the schema against config"""
        try:
            version_doc = self.as_dict()
            if not self.validator.validate(version_doc, self.rules()):
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))
        except DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err
        else:
            return version_doc  # or is a success

    def as_dict(self) -> dict[str, str]:
        """Get version string"""
        if not hasattr(self, 'validator') or not hasattr(self, 'document'):
            raise SystemExit(err_message('fatal.V0005'))

        try:
            return {BaseConfigElements.VERSION: str(self.document[BaseConfigElements.VERSION])}
        except:
            raise SystemExit(err_message('fatal.V0005'))
