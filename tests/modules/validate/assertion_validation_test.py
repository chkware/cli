# type: ignore
"""
Test mod for assertion_validation
"""

from chk.modules.validate.assertion_validation import (
    get_schema_map,
    AssertionEntityType,
)


class TestGetSchemaMap:
    @staticmethod
    def test_get_all():
        schema_map = get_schema_map()

        assert AssertionEntityType.Equal in schema_map

    @staticmethod
    def test_get_single():
        equal_schema = get_schema_map(AssertionEntityType.Equal)

        assert "type" in equal_schema
        assert "actual" in equal_schema
        assert AssertionEntityType.Equal in equal_schema["type"]["allowed"]
        assert len(equal_schema["type"]["allowed"]) == 1
