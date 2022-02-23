"""
Versioned schema repository for http specifications
"""
from typing import Dict
from chk.archetypes.defaults import ArchetypeConfig, doc_config
from chk.constants.archetype.validation import request_schema


class HttpV072(ArchetypeConfig):
    """http config v0.7.2"""
    def __init__(self):
        super().__init__()
        self.version_config = doc_config.DocV072()

    def get_schema(self) -> Dict:
        """create and validate schema against the dict passed"""
        return self.version_config.get_schema() | request_schema

    def validate_config(self, config: Dict) -> bool:
        """Validate the schema against config"""
        try:
            if self.validator.validate(config, self.get_schema()) is not True:
                print(1)
        except BaseException as base_ex:
            print(base_ex)
        else:
            return True # or is a success
