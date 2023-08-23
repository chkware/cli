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
    IntegerBetween = "IntegerBetween"
    IntegerGreater = "IntegerGreater"
    IntegerGreaterOrEqual = "IntegerGreaterOrEqual"


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


def _get_schema_for_empty(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.Empty)
    del _t_gen_schema["expected"]
    return _t_gen_schema


def _get_schema_for_not_empty(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.NotEmpty)
    del _t_gen_schema["expected"]
    return _t_gen_schema


def _get_schema_for_boolean(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.Boolean)
    return _t_gen_schema


def _get_schema_for_integer(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.Integer)
    del _t_gen_schema["expected"]
    return _t_gen_schema


def _get_schema_for_integer_between(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.IntegerBetween)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "min": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "integer",
        },
        "max": {
            "required": False,
            "empty": False,
            "nullable": False,
            "type": "integer",
        },
    }


def _get_schema_for_integer_greater(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.IntegerGreater)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "other": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "integer",
        },
    }


def _get_schema_for_integer_greater_or_equal(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.IntegerGreaterOrEqual)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "other": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "integer",
        },
    }


# ------------------------------------------------
# Scheme selector
# ------------------------------------------------


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
        AssertionEntityType.Empty: _get_schema_for_empty(_generic_schema),
        AssertionEntityType.NotEmpty: _get_schema_for_not_empty(_generic_schema),
        AssertionEntityType.Boolean: _get_schema_for_boolean(_generic_schema),
        AssertionEntityType.Integer: _get_schema_for_integer(_generic_schema),
        AssertionEntityType.IntegerBetween: _get_schema_for_integer_between(
            _generic_schema
        ),
        AssertionEntityType.IntegerGreater: _get_schema_for_integer_greater(
            _generic_schema
        ),
        AssertionEntityType.IntegerGreaterOrEqual: _get_schema_for_integer_greater_or_equal(
            _generic_schema
        ),
    }

    if item:
        return schema_map[item]

    return schema_map
