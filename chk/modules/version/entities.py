"""
Shared entities
"""
from abc import ABC, abstractmethod
from cerberus import Validator
from cerberus.validator import DocumentError
from chk.console.app_container import app
from chk.modules.version.validation_rules import version_schema
from typing import Dict


class AbstractSpecConfig(ABC):
    """Base class to all archetype"""

    def __init__(self):
        self.validator = Validator()

    @abstractmethod
    def get_schema(self) -> Dict:
        """abstract method to be implemented by child"""

    @abstractmethod
    def validate_config(self, config: Dict) -> bool:
        """Error handling at global level for schemas"""


class VersionConfigV072(AbstractSpecConfig):
    """
    Versioned schema repository for http specifications
    version: v0.7.2
    """

    def get_schema(self) -> Dict:
        """create and validate schema against the dict passed"""
        return version_schema

    def validate_config(self, config: Dict) -> bool:
        """Validate the schema against config"""
        self.validator.allow_unknown = True

        try:
            if self.validator.validate(config, self.get_schema()) is not True:
                raise SystemExit(str(self.validator.errors))
        except DocumentError as doc_err:
            raise SystemExit(f'{app.messages.exception.fatal.V0001}: {doc_err}') from doc_err
        else:
            return True  # or is a success
