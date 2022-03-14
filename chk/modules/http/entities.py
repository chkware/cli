"""
Versioned schema repository for http specifications
"""
import cerberus.errors
from typing import Dict
from chk.modules.shared.entities import ArchetypeConfig, DocV072
from chk.constants.archetype.validation import request_schema
from cerberus.validator import DocumentError
from chk.console.app_container import app


class HttpV072(ArchetypeConfig):
    """http config v0.7.2"""
    def __init__(self):
        super().__init__()
        self.version_config = DocV072()

    def get_schema(self) -> Dict:
        """create and validate schema against the dict passed"""
        return self.version_config.get_schema() | request_schema

    def validate_config(self, config: Dict) -> bool:
        """Validate the schema against config"""
        self.version_config.validate_config(config)  # validate version

        try:
            if self.validator.validate(config, self.get_schema()) is not True:  # validate request
                raise SystemExit(str(self.validator.errors))
        except DocumentError as doc_err:
            raise SystemExit(f'{app.config.error.fatal.V0001}: {doc_err}') from doc_err
        else:
            return True  # or is a success
