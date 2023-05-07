# type: ignore
"""
Test module for infrastructure.version module
"""

import pytest

from chk.infrastructure.version import DocumentVersion, DocumentVersionMaker


class TestDocumentVersionCreation:
    """Create tests"""

    def test_create_with_blank_str_fails(self):
        with pytest.raises(ValueError):
            DocumentVersion("")

    def test_create_with_malformed_str_1_fails(self):
        with pytest.raises(ValueError):
            DocumentVersion("aa:bb")

    def test_create_with_malformed_str_2_fails(self):
        with pytest.raises(ValueError):
            DocumentVersion(":bb:cc")

    def test_one_doc_type_pass(self):
        a = DocumentVersion("default:http:0.7.2")
        assert a.provider == "default"
        assert a.doc_type == "http"
        assert a.doc_type_ver == "0.7.2"


class TestFromDictOfDocumentVersionMaker:
    def test_one_doc_type_pass(self):
        dd = {"version": "default:http:0.7.2"}
        a = DocumentVersionMaker.from_dict(dd)

        assert a.provider == "default"
        assert a.doc_type == "http"
        assert a.doc_type_ver == "0.7.2"
