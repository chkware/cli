"""
Default archetypes
"""
from abc import ABC, abstractmethod
from typing import Dict
from chk.constants.archetype import ArchetypeConfigModules


class ArchetypeConfig(ABC):
    """Base class to all archetype"""

    @classmethod
    def validate_version(cls, config: Dict) -> bool:
        """check if this version is supported"""
        if (v := config.get('version')) is not None:
            archetype_class = ArchetypeConfigModules.data.get(v)
            if archetype_class is None: raise SystemExit('Version not supported.')
            return True

    @classmethod
    @abstractmethod
    def validate_schema(cls, config: Dict):
        """abstract method to be implemented by child"""
        pass
