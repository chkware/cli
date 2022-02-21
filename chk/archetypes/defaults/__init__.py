"""
Default archetypes
"""
from abc import ABC, abstractmethod
from typing import Dict
from chk.constants.archetype import ArchetypeConfigModules, validation
from chk.globals import current_app


class ArchetypeConfig(ABC):
    """Base class to all archetype"""

    @classmethod
    def validate_version(cls, config: Dict) -> bool:
        """check if this version is supported"""
        app = current_app()

        ver = config.get('version')
        if ver is None: raise SystemExit(app.config.error.fatal.V0001)

        archetype_class = ArchetypeConfigModules.data.get(ver)
        if archetype_class is None: raise SystemExit(app.config.error.fatal.V0002)

        return True

    @classmethod
    @abstractmethod
    def validate_schema(cls, config: Dict):
        """abstract method to be implemented by child"""

    @classmethod
    def get_validation_schema(cls) -> Dict: return validation.version_schema
