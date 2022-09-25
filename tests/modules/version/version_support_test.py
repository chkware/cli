import pytest

from chk.infrastructure.contexts import app
from chk.infrastructure.file_loader import FileContext
from chk.modules.version.support import VersionMixin
from chk.modules.version.constants import DocumentType


class HavingVersion(VersionMixin):
    def __init__(self, file_ctx: FileContext) -> None:
        self.file_ctx = file_ctx

    def get_file_context(self) -> FileContext:
        return self.file_ctx


class TestVersionMixin:
    def test_validate_config_success(self):
        file_ctx = FileContext(filepath_hash='a1b2')
        app.original_doc[file_ctx.filepath_hash] = \
            {'version': 'default:http:0.7.2'}

        ver = HavingVersion(file_ctx)
        assert isinstance(ver.version_validated(), dict)
        
    def test_validate_config_empty_version(self):
        file_ctx = FileContext(filepath_hash='a1b2')
        app.original_doc[file_ctx.filepath_hash] = \
            {'version': ''}

        ver = HavingVersion(file_ctx)
        with pytest.raises(SystemExit):
            ver.version_validated()

    def test_validate_config_fail_non_exist_ver(self):
        file_ctx = FileContext(filepath_hash='a1b2')
        app.original_doc[file_ctx.filepath_hash] = \
            {'version': 'default:http:0.7'}

        ver = HavingVersion(file_ctx)
        with pytest.raises(SystemExit):
            ver.version_validated()
            
    def test_validate_config_fail_no_doc(self):
        file_ctx = FileContext(filepath_hash='a1b2')
        app.original_doc[file_ctx.filepath_hash] = {}

        ver = HavingVersion(file_ctx)
        with pytest.raises(SystemExit):
            ver.version_validated()

    def test_validate_config_fail_on_none(self):
        file_ctx = FileContext(filepath_hash='a1b2')
        app.original_doc[file_ctx.filepath_hash] = None

        ver = HavingVersion(file_ctx)
        with pytest.raises(SystemExit):
            ver.version_validated()
            
    def test_validate_config_fail_no_version(self):
        config = {
            'request': {
                'url': 'some.url'
            }
        }

        file_ctx = FileContext(filepath_hash='a1b2')
        app.original_doc[file_ctx.filepath_hash] = config


        ver = HavingVersion(file_ctx)
        with pytest.raises(SystemExit):
            ver.version_validated()
