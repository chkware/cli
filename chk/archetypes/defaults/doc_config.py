"""
Versioned schema repository for http specifications
"""
from typing import Dict
from chk.archetypes.defaults import ArchetypeConfig
from chk.constants.archetype.validation import version_schema
from cerberus.validator import DocumentError
from chk.globals import current_app


class DocV072(ArchetypeConfig):
    """http config v0.7.2"""

    def get_schema(self) -> Dict:
        """create and validate schema against the dict passed"""
        return version_schema

    def validate_config(self, config: Dict) -> bool:
        """Validate the schema against config"""
        app = current_app()
        self.validator.allow_unknown = True

        try:
            if self.validator.validate(config, self.get_schema()) is not True:
                raise SystemExit(str(self.validator.errors))
        except DocumentError as doc_err:
            raise SystemExit(f'{app.config.error.fatal.V0001}: {doc_err}') from doc_err
        else:
            return True # or is a success
