# type: ignore
"""
Document test
"""
import pytest

from chk.infrastructure.document import VersionedDocument, VersionedDocumentSupport
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.version import SCHEMA as VER_SCHEMA
from chk.infrastructure.symbol_table import VARIABLE_SCHEMA as VAR_SCHEMA


class TestVersionedDocumentSupport:

    @staticmethod
    def test_validate_with_schema_pass():
        document = {
            "version": "default:http:0.7.2",
            "variables": {
                "var_1": "bar",
                "var_2": 2,
                "var_3": "ajax<%var_1%>",
                "var_4": "ajax <% Var_1 %>",
                "var_5": "  <% var_2 %>",
            },
        }

        schema = {**VER_SCHEMA, **VAR_SCHEMA}
        file_ctx = FileContext(filepath_hash="ab12", document=document)
        doc = VersionedDocument(tuple(file_ctx), "default:http:0.7.2")

        assert VersionedDocumentSupport.validate_with_schema(schema, doc)

    @staticmethod
    def test_validate_with_schema_fail():
        document = {
            "variables": {
                "var_1": "bar",
                "var_2": 2,
                "var_3": "ajax<%var_1%>",
                "var_4": "ajax <% Var_1 %>",
                "var_5": "  <% var_2 %>",
            },
        }

        schema = {**VER_SCHEMA, **VAR_SCHEMA}
        file_ctx = FileContext(filepath_hash="ab12", document=document)
        doc = VersionedDocument(tuple(file_ctx), "default:http:0.7.2")

        with pytest.raises(Exception):
            VersionedDocumentSupport.validate_with_schema(schema, doc)
