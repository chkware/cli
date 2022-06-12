import pytest

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
        
    def test_validate_config_empty_version(self):
        ver = HavingVersion()
        with pytest.raises(SystemExit):
            ver.document = {'version': ''}
            ver.version_validated()

    def test_validate_config_fail_non_exist_ver(self):
        ver = HavingVersion()
        with pytest.raises(SystemExit):
            ver.document = {'version': 'default:http:0.7'}
            ver.version_validated()
