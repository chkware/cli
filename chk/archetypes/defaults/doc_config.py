"""
Versioned schema repository for http specifications
"""
from typing import Dict
from chk.archetypes.defaults import ArchetypeConfig
from chk.constants.archetype.validation import version_schema
import cerberus.errors
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
                return self.raise_exception()
        except DocumentError as de:
            raise SystemExit(f'{app.config.error.fatal.V0001}: {de}') from de

        # or is a success
        return True

    def raise_exception(self) -> bool:
        """Error handling at global level for schemas"""
        app = current_app()

        if cerberus.errors.EMPTY_NOT_ALLOWED in self.validator.document_error_tree['version']:
            raise SystemExit(app.config.error.fatal.V0004)

        return True
