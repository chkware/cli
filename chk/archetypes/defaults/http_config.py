"""
Versioned schema repository for http specifications
"""
from typing import Dict
from chk.archetypes.defaults import ArchetypeConfig


class V072(ArchetypeConfig):
    """http config v0.7.2"""

    @classmethod
    def validate_schema(cls, config: Dict):
        """create and validate schema against the dict passed"""
        pass
