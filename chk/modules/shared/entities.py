"""
Shared entities
"""
from abc import ABC, abstractmethod
from typing import Dict
from cerberus import Validator
from chk.constants.archetype.validation import version_schema
from cerberus.validator import DocumentError
from chk.console.app_container import app


class ArchetypeConfig(ABC):
    """Base class to all archetype"""

    def __init__(self):
        self.validator = Validator()

    @abstractmethod
    def get_schema(self) -> Dict:
        """abstract method to be implemented by child"""

    @abstractmethod
    def validate_config(self, config: Dict) -> bool:
        """Error handling at global level for schemas"""


class DocV072(ArchetypeConfig):
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
            raise SystemExit(f'{app.config.error.fatal.V0001}: {doc_err}') from doc_err
        else:
            return True  # or is a success
