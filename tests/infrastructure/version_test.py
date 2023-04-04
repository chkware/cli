# type: ignore
"""
Test module for infrastructure.version module
"""
import pytest

from chk.infrastructure.version import DocumentVersion


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

    def test_create_pass(self):
        a = DocumentVersion("aa:bb:cc")
        assert a.version == "aa:bb:cc"
