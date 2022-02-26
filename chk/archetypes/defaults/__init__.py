"""
Default archetypes
"""
from abc import ABC, abstractmethod
from typing import Dict
from cerberus import Validator


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
