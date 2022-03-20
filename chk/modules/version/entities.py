"""
Shared entities
"""
import pydoc
from abc import ABC, abstractmethod
from cerberus import Validator
from cerberus.validator import DocumentError
from chk.console.app_container import app
from chk.modules.version.validation_rules import version_schema
from chk.modules.version.constants import BaseDocElements, VersionStrToSpecConfigMapping as Mapping
from typing import Dict


class AbstractSpecConfig(ABC):
    """Base class to all archetype"""

    def __init__(self):
        self.document: Dict = {}
        self.validator = Validator()

    @abstractmethod
    def get_schema(self) -> Dict:
        """abstract method to be implemented by child"""

    @abstractmethod
    def validate_config(self) -> bool:
        """Error handling at global level for schemas"""

    @classmethod
    def from_version(cls, version: str = ''):
        """Creates and returns AbstractSpecConfig from version stirng"""
        class_map = Mapping.find_by_version(version)
        http_config_class = pydoc.locate(class_map)

        if not callable(http_config_class): raise SystemExit('Not callable.')

        return http_config_class()


class VersionConfigV072(AbstractSpecConfig):
    """
    Versioned schema repository for http specifications
    version: v0.7.2
    """

    def get_schema(self) -> Dict:
        """create and validate schema against the dict passed"""
        return version_schema

    def validate_config(self) -> bool:
        """Validate the schema against config"""
        self.validator.allow_unknown = True

        try:
            if not self.validator.validate(self.document, self.get_schema()):
                raise SystemExit(str(self.validator.errors))
        except DocumentError as doc_err:
            raise SystemExit(f'{app.messages.exception.fatal.V0001}: {doc_err}') from doc_err
        else:
            return True  # or is a success


def get_document_version(document: Dict) -> str:
    """check and get version string"""
    if not isinstance(document, dict): raise SystemExit(app.messages.exception.fatal.V0005)

    return str(document.get(BaseDocElements.VERSION))
