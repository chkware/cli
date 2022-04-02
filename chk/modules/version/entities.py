"""
Version entities
"""
import pydoc

from cerberus import Validator
from chk.infrastructure.exception import err_message
from chk.modules.version.constants import BaseConfigElements, VersionStrToSpecConfigMapping as Mapping


class BaseSpecConfig:
    """Base class to all archetype"""

    def __init__(self):
        self.document: dict = {}
        self.validator = Validator()

    @classmethod
    def to_spec_config(cls, version: str = ''):
        """Creates and returns AbstractSpecConfig from version string"""
        class_map = Mapping.find_by_version(version)
        http_config_class = pydoc.locate(class_map)

        if not callable(http_config_class):
            raise SystemExit(err_message('fatal.V0007'))

        return http_config_class()

    def version(self) -> str:
        """check and get version string"""
        return str(self.document.get(BaseConfigElements.VERSION))
