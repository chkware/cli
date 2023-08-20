"""
Assertion validation module
"""
import enum


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
        "empty": False,
        "nullable": False,
    },
    "expected": {
        "required": False,
        "empty": False,
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

