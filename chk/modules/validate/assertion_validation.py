"""
Assertion validation module
"""
import enum


class AssertionEntityType(enum.StrEnum):
    """Type value constants for assertion entities"""

    ACCEPTED = "Accepted"
    DECLINED = "Declined"
    EQUAL = "Equal"
    NOT_EQUAL = "NotEqual"
    EMPTY = "Empty"
    NOT_EMPTY = "NotEmpty"
    BOOLEAN = "Boolean"
    INTEGER = "Integer"


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

