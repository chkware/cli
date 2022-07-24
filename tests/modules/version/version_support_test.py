import pytest

from cerberus import Validator
from chk.modules.version.support import VersionMixin
from chk.modules.version.constants import DocumentType


class HavingVersion(VersionMixin):
    def __init__(self) -> None:
        self.document, self.validator = None, Validator()        


class TestVersionMixin:
    def test_validate_config_success(self):
        ver = HavingVersion()
        ver.document = {'version': 'default:http:0.7.2'}
        assert type(ver.version_validated(DocumentType.HTTP)) is dict
        
    def test_validate_config_empty_version(self):
        ver = HavingVersion()
        with pytest.raises(SystemExit):
            ver.document = {'version': ''}
            ver.version_validated(DocumentType.HTTP)

    def test_validate_config_fail_non_exist_ver(self):
        ver = HavingVersion()
        with pytest.raises(SystemExit):
            ver.document = {'version': 'default:http:0.7'}
            ver.version_validated(DocumentType.HTTP)
            
    def test_validate_config_fail_no_doc(self):
        ver = HavingVersion()
        with pytest.raises(SystemExit):
            ver.document = {}
            ver.version_validated(DocumentType.HTTP)

    def test_validate_config_fail_on_none(self):
        ver = HavingVersion()
        with pytest.raises(SystemExit):
            ver.document = None
            ver.version_validated(DocumentType.HTTP)
            
    def test_validate_config_fail_no_version(self):
        config = {
            'request': {
                'url': 'some.url'
            }
        }

        ver = HavingVersion()
        with pytest.raises(SystemExit):
            ver.document = config
            ver.version_validated(DocumentType.HTTP)

