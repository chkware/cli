from cerberus import Validator
from chk.modules.version.support import VersionMixin


class HavingVersion(VersionMixin):
    def __init__(self) -> None:
        self.document, self.validator = None, Validator()        


class TestVersionMixin:
    def test_validate_config_success(self):
        ver = HavingVersion()
        ver.document = {'version': 'default:http:0.7.2'}
        print(ver.version_validated())
        assert type(ver.version_validated()) is dict
