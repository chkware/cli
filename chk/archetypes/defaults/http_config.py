"""
Versioned schema repository for http specifications
"""
from typing import Dict
from chk.archetypes.defaults import ArchetypeConfig
from chk.constants.archetype.validation import request_schema
from cerberus import Validator


class V072(ArchetypeConfig):
    """http config v0.7.2"""

    @classmethod
    def validate_schema(cls, config: Dict) -> bool:
        """create and validate schema against the dict passed"""
        schema = super().get_version_schema() | cls.get_validation_schema()
        validator = Validator()
        return validator.validate(config, schema)

    @classmethod
    def get_validation_schema(cls) -> Dict:
        return request_schema
