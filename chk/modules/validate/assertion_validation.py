"""
Assertion validation module
"""
import copy
import enum

AssertionEntityProperty = ("type", "actual", "expected", "cast_actual_to")


class AssertionEntityType(enum.StrEnum):
    """Type value constants for assertion entities"""

    Accepted = "Accepted"
    Declined = "Declined"
    Equal = "Equal"
    NotEqual = "NotEqual"
    Empty = "Empty"
    NotEmpty = "NotEmpty"
    Boolean = "Boolean"
    Integer = "Integer"


_generic_schema = {
    "type": {
        "required": True,
        "empty": False,
        "nullable": False,
        "type": "string",
        "allowed": [],
    },
    "actual": {
        "required": True,
        "empty": True,
        "nullable": True,
    },
    "expected": {
        "required": False,
        "empty": True,
        "nullable": True,
    },
    "cast_actual_to": {
        "required": False,
        "empty": False,
        "nullable": False,
        "type": "string",
        "allowed": [
            "int_or_flot",
            "int",
            "float",
            "bool",
            "none",
            "dict",
            "list",
            "str",
            "auto",
        ],
    },
}


def _get_schema_for_equal(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.Equal)
    _t_gen_schema["expected"]["required"] = True
    return _t_gen_schema


def _get_schema_for_not_equal(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.NotEqual)
    _t_gen_schema["expected"]["required"] = True
    return _t_gen_schema


def _get_schema_for_accepted(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.Accepted)
    del _t_gen_schema["expected"]
    return _t_gen_schema


def _get_schema_for_declined(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.Declined)
    del _t_gen_schema["expected"]
    return _t_gen_schema


def get_schema_map(item: AssertionEntityType | None = None) -> dict:
    """get_schema_map

    Args:
        item: Assertion type
    """

    schema_map = {
        AssertionEntityType.Equal: _get_schema_for_equal(_generic_schema),
        AssertionEntityType.NotEqual: _get_schema_for_not_equal(_generic_schema),
        AssertionEntityType.Accepted: _get_schema_for_accepted(_generic_schema),
        AssertionEntityType.Declined: _get_schema_for_declined(_generic_schema),
    }

    if item:
        return schema_map[item]

    return schema_map
