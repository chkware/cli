# type: ignore

import pytest
import tests

from chk.infrastructure.contexts import app
from chk.infrastructure.file_loader import FileContext
from chk.modules.version.constants import DocumentType
from chk.modules.version.support import (
    VersionMixin,
    RawFileVersionParser,
    DocumentMixin,
)
from chk.modules.version.validation_rules import version_schema_testcase


class HavingVersion(VersionMixin):
    def __init__(self, file_ctx: FileContext) -> None:
        self.file_ctx = file_ctx

    def get_file_context(self) -> FileContext:
        return self.file_ctx


class TestVersionMixin:
    def test_validate_config_success(self):
        file_ctx = FileContext(filepath_hash="a1b2")
        app.original_doc[file_ctx.filepath_hash] = {"version": "default:http:0.7.2"}

        ver = HavingVersion(file_ctx)
        assert isinstance(ver.version_validated(), dict)

        del app.original_doc[file_ctx.filepath_hash]

    def test_validate_config_empty_version(self):
        file_ctx = FileContext(filepath_hash="a1b2")
        app.original_doc[file_ctx.filepath_hash] = {"version": ""}

        ver = HavingVersion(file_ctx)
        with pytest.raises(RuntimeError):
            ver.version_validated()

        del app.original_doc[file_ctx.filepath_hash]

    def test_validate_config_fail_non_exist_ver(self):
        file_ctx = FileContext(filepath_hash="a1b2")
        app.original_doc[file_ctx.filepath_hash] = {"version": "default:http:0.7"}

        ver = HavingVersion(file_ctx)
        with pytest.raises(RuntimeError):
            ver.version_validated()

        del app.original_doc[file_ctx.filepath_hash]

    def test_validate_config_fail_no_doc(self):
        file_ctx = FileContext(filepath_hash="a1b2")
        app.original_doc[file_ctx.filepath_hash] = {}

        ver = HavingVersion(file_ctx)
        with pytest.raises(RuntimeError):
            ver.version_validated()

        del app.original_doc[file_ctx.filepath_hash]

    def test_validate_config_fail_on_none(self):
        file_ctx = FileContext(filepath_hash="a1b2")
        app.original_doc[file_ctx.filepath_hash] = None

        ver = HavingVersion(file_ctx)
        with pytest.raises(RuntimeError):
            ver.version_validated()

        del app.original_doc[file_ctx.filepath_hash]

    def test_validate_config_fail_no_version(self):
        config = {"request": {"url": "some.url"}}

        file_ctx = FileContext(filepath_hash="a1b2")
        app.original_doc[file_ctx.filepath_hash] = config

        ver = HavingVersion(file_ctx)
        with pytest.raises(RuntimeError):
            ver.version_validated()

        del app.original_doc[file_ctx.filepath_hash]

    def test_get_document_type_pass_with_http_doc(self):
        config = {"version": "default:http:0.7.2"}

        file_ctx = FileContext(filepath_hash="a1b2")
        app.original_doc[file_ctx.filepath_hash] = config

        ver = HavingVersion(file_ctx)
        assert ver.get_document_type() == DocumentType.HTTP

        del app.original_doc[file_ctx.filepath_hash]

    def test_get_document_type_pass_with_testcase_doc(self):
        config = {"version": "default:testcase:0.7.2"}

        file_ctx = FileContext(filepath_hash="a1b2")
        app.original_doc[file_ctx.filepath_hash] = config

        ver = HavingVersion(file_ctx)
        assert ver.get_document_type() == DocumentType.TESTCASE

        del app.original_doc[file_ctx.filepath_hash]

    def test_get_document_type_fail_with_unsupported_doc(self):
        config = {"version": "default:unsupported:0.8.0"}

        file_ctx = FileContext(filepath_hash="a1b2")
        app.original_doc[file_ctx.filepath_hash] = config

        ver = HavingVersion(file_ctx)

        with pytest.raises(ValueError):
            ver.get_document_type()

        del app.original_doc[file_ctx.filepath_hash]

    def test_get_validation_schema_pass(self):
        config = {"version": "default:testcase:0.8.0"}

        file_ctx = FileContext(filepath_hash="a1b2")
        app.original_doc[file_ctx.filepath_hash] = config

        ver = HavingVersion(file_ctx)
        assert ver.get_validation_schema() == version_schema_testcase

        del app.original_doc[file_ctx.filepath_hash]

    def test_get_validation_schema_fail(self):
        config = {"version": "default:unsupported:0.8.0"}

        file_ctx = FileContext(filepath_hash="a1b2")
        app.original_doc[file_ctx.filepath_hash] = config

        ver = HavingVersion(file_ctx)
        with pytest.raises(ValueError):
            ver.get_validation_schema()

        del app.original_doc[file_ctx.filepath_hash]


class TestRawFileVersionParser:
    def test_find_version_str_success(self):
        file = tests.RES_DIR + "UserOk.chk"
        assert RawFileVersionParser.find_version_str(file) == "default:http:0.7.2"

    def test_find_version_str_fails_when_no_version_found(self):
        file = tests.RES_DIR + "UserNoVersion.chk"
        assert not RawFileVersionParser.find_version_str(file)

    def test_find_version_str_fails_when_commented_version_found(self):
        file = tests.RES_DIR + "UserCommentedVersion.chk"
        assert not RawFileVersionParser.find_version_str(file)

    def test_find_version_str_fails_when_file_not_found(self):
        file = tests.RES_DIR + "UserCommentedVersions.chk"
        assert not RawFileVersionParser.find_version_str(file)

    def test_convert_version_str_to_num_success_with_full_version_doc(self):
        v1 = "version: 'default:http:0.7.2'"
        assert RawFileVersionParser.convert_version_str_to_num(v1) == "072"

    def test_convert_version_str_to_num_success_with_version_value(self):
        v1 = "default:http:0.7.2"
        assert RawFileVersionParser.convert_version_str_to_num(v1) == "072"

    def test_convert_version_str_to_num_success_with_version_value_underscore(self):
        v1 = "default:http:0.7_2"
        assert RawFileVersionParser.convert_version_str_to_num(v1) == "072"

    def test_convert_version_str_to_num_success_with_version_value_dash(self):
        v1 = "default:http:0.7-2"
        assert RawFileVersionParser.convert_version_str_to_num(v1) == "072"


class TestDocumentMixin:
    def test_as_dict_success(self):
        file_ctx = FileContext(filepath_hash="a1b2")
        app.original_doc[file_ctx.filepath_hash] = {"version": "default:http:0.7.2"}

        ver = HavingVersion(file_ctx)

        assert isinstance(ver.as_dict("version"), dict)
        assert ver.as_dict("version").get("version") == "default:http:0.7.2"
        assert isinstance(ver.as_dict("version", False), str)

        del app.original_doc[file_ctx.filepath_hash]

    def test_as_dict_pass_for_compiled_doc(self):
        file_ctx = FileContext(filepath_hash="a1b2")
        app.compiled_doc[file_ctx.filepath_hash] = {"version": "default:http:0.7.2"}

        ver = HavingVersion(file_ctx)

        assert ver.as_dict("version", False, True) == "default:http:0.7.2"
        del app.compiled_doc[file_ctx.filepath_hash]

    def test_as_dict_pass_no_ctx(self):
        ver = DocumentMixin()
        assert ver.as_dict("version", False, True) is None
