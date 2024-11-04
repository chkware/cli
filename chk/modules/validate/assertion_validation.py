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
    IntegerLess = "IntegerLess"
    IntegerLessOrEqual = "IntegerLessOrEqual"
    Float = "Float"
    FloatBetween = "FloatBetween"
    FloatGreater = "FloatGreater"
    FloatGreaterOrEqual = "FloatGreaterOrEqual"
    FloatLess = "FloatLess"
    FloatLessOrEqual = "FloatLessOrEqual"
    Str = "Str"
    StrHave = "StrHave"
    StrDoNotHave = "StrDoNotHave"
    StrStartsWith = "StrStartsWith"
    StrDoNotStartsWith = "StrDoNotStartsWith"
    StrEndsWith = "StrEndsWith"
    StrDoNotEndsWith = "StrDoNotEndsWith"
    Date = "Date"
    DateAfter = "DateAfter"
    DateAfterOrEqual = "DateAfterOrEqual"
    DateBefore = "DateBefore"
    DateBeforeOrEqual = "DateBeforeOrEqual"
    List = "List"
    ListContains = "ListContains"
    ListDoNotContains = "ListDoNotContains"
    ListHasIndex = "ListHasIndex"
    ListDoNotHasIndex = "ListDoNotHasIndex"
    Map = "Map"
    MapKeyCount = "MapKeyCount"
    MapHasKeys = "MapHasKeys"
    MapDoNotHasKeys = "MapDoNotHasKeys"
    MapExactKeys = "MapExactKeys"
    Count = "Count"


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
            "int_or_float",
            "int",
            "float",
            "bool",
            "none",
            "map",
            "list",
            "str",
            "auto",
        ],
    },
    "msg_pass": {
        "required": False,
        "empty": False,
        "nullable": False,
        "type": "string",
    },
    "msg_fail": {
        "required": False,
        "empty": False,
        "nullable": False,
        "type": "string",
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


def _get_schema_for_integer_less(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.IntegerLess)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "other": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "integer",
        },
    }


def _get_schema_for_integer_less_or_equal(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.IntegerLessOrEqual)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "other": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "integer",
        },
    }


def _get_schema_for_float(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.Float)
    del _t_gen_schema["expected"]
    return _t_gen_schema


def _get_schema_for_float_between(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.FloatBetween)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "min": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "number",
        },
        "max": {
            "required": False,
            "empty": False,
            "nullable": False,
            "type": "number",
        },
    }


def _get_schema_for_float_greater(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.FloatGreater)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "other": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "number",
        },
    }


def _get_schema_for_float_greater_or_equal(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.FloatGreaterOrEqual)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "other": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "number",
        },
    }


def _get_schema_for_float_less(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.FloatLess)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "other": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "number",
        },
    }


def _get_schema_for_float_less_or_equal(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.FloatLessOrEqual)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "other": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "number",
        },
    }


def _get_schema_for_str(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.Str)
    del _t_gen_schema["expected"]
    return _t_gen_schema


def _get_schema_for_str_have(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.StrHave)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "other": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "string",
        },
    }


def _get_schema_for_str_do_not_have(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.StrDoNotHave)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "other": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "string",
        },
    }


def _get_schema_for_str_starts_with(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.StrStartsWith)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "other": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "string",
        },
    }


def _get_schema_for_str_do_not_starts_with(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.StrDoNotStartsWith)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "other": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "string",
        },
    }


def _get_schema_for_str_ends_with(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.StrEndsWith)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "other": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "string",
        },
    }


def _get_schema_for_str_do_not_ends_with(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.StrDoNotEndsWith)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "other": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "string",
        },
    }


def _get_schema_for_date(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.Date)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "format": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "string",
        },
    }


def _get_schema_for_date_after(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.DateAfter)
    _t_gen_schema["expected"]["required"] = True
    _t_gen_schema["expected"]["type"] = "string"

    return _t_gen_schema | {
        "format": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "string",
        },
    }


def _get_schema_for_date_after_or_equal(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.DateAfterOrEqual)
    _t_gen_schema["expected"]["required"] = True
    _t_gen_schema["expected"]["type"] = "string"

    return _t_gen_schema | {
        "format": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "string",
        },
    }


def _get_schema_for_date_before(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.DateBefore)
    _t_gen_schema["expected"]["required"] = True
    _t_gen_schema["expected"]["type"] = "string"

    return _t_gen_schema | {
        "format": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "string",
        },
    }


def _get_schema_for_date_before_or_equal(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.DateBeforeOrEqual)
    _t_gen_schema["expected"]["required"] = True
    _t_gen_schema["expected"]["type"] = "string"

    return _t_gen_schema | {
        "format": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "string",
        },
    }


def _get_schema_for_list(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.List)
    del _t_gen_schema["expected"]

    return _t_gen_schema


def _get_schema_for_list_contains(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.ListContains)
    _t_gen_schema["expected"]["required"] = True

    return _t_gen_schema


def _get_schema_for_list_do_not_contains(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.ListDoNotContains)
    _t_gen_schema["expected"]["required"] = True

    return _t_gen_schema


def _get_schema_for_list_has_index(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.ListHasIndex)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "index": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "integer",
        },
    }


def _get_schema_for_list_do_not_has_index(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.ListDoNotHasIndex)
    del _t_gen_schema["expected"]

    return _t_gen_schema | {
        "index": {
            "required": True,
            "empty": False,
            "nullable": False,
            "type": "integer",
        },
    }


def _get_schema_for_map(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.Map)
    del _t_gen_schema["expected"]

    return _t_gen_schema


def _get_schema_for_map_key_count(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.MapKeyCount)
    _t_gen_schema["expected"]["required"] = True
    _t_gen_schema["expected"]["type"] = "integer"

    return _t_gen_schema


def _get_schema_for_map_has_keys(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.MapHasKeys)
    _t_gen_schema["expected"]["required"] = True

    return _t_gen_schema


def _get_schema_for_map_do_not_has_keys(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.MapDoNotHasKeys)
    _t_gen_schema["expected"]["required"] = True

    return _t_gen_schema


def _get_schema_for_map_exact_keys(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.MapExactKeys)
    _t_gen_schema["expected"]["required"] = True

    return _t_gen_schema


def _get_schema_for_count(_gen_schema: dict) -> dict:
    """Get schema for equal"""

    _t_gen_schema = copy.deepcopy(_gen_schema)
    _t_gen_schema["type"]["allowed"].append(AssertionEntityType.Count)
    _t_gen_schema["expected"]["required"] = True
    _t_gen_schema["expected"]["type"] = "integer"

    return _t_gen_schema


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
        AssertionEntityType.IntegerLess: _get_schema_for_integer_less(_generic_schema),
        AssertionEntityType.IntegerLessOrEqual: _get_schema_for_integer_less_or_equal(
            _generic_schema
        ),
        AssertionEntityType.Float: _get_schema_for_float(_generic_schema),
        AssertionEntityType.FloatBetween: _get_schema_for_float_between(
            _generic_schema
        ),
        AssertionEntityType.FloatGreater: _get_schema_for_float_greater(
            _generic_schema
        ),
        AssertionEntityType.FloatGreaterOrEqual: _get_schema_for_float_greater_or_equal(
            _generic_schema
        ),
        AssertionEntityType.FloatLess: _get_schema_for_float_less(_generic_schema),
        AssertionEntityType.FloatLessOrEqual: _get_schema_for_float_less_or_equal(
            _generic_schema
        ),
        AssertionEntityType.Str: _get_schema_for_str(_generic_schema),
        AssertionEntityType.StrHave: _get_schema_for_str_have(_generic_schema),
        AssertionEntityType.StrDoNotHave: _get_schema_for_str_do_not_have(
            _generic_schema
        ),
        AssertionEntityType.StrStartsWith: _get_schema_for_str_starts_with(
            _generic_schema
        ),
        AssertionEntityType.StrDoNotStartsWith: _get_schema_for_str_do_not_starts_with(
            _generic_schema
        ),
        AssertionEntityType.StrEndsWith: _get_schema_for_str_ends_with(_generic_schema),
        AssertionEntityType.StrDoNotEndsWith: _get_schema_for_str_do_not_ends_with(
            _generic_schema
        ),
        AssertionEntityType.Date: _get_schema_for_date(_generic_schema),
        AssertionEntityType.DateAfter: _get_schema_for_date_after(_generic_schema),
        AssertionEntityType.DateAfterOrEqual: _get_schema_for_date_after_or_equal(
            _generic_schema
        ),
        AssertionEntityType.DateBefore: _get_schema_for_date_before(_generic_schema),
        AssertionEntityType.DateBeforeOrEqual: _get_schema_for_date_before_or_equal(
            _generic_schema
        ),
        AssertionEntityType.List: _get_schema_for_list(_generic_schema),
        AssertionEntityType.ListContains: _get_schema_for_list_contains(
            _generic_schema
        ),
        AssertionEntityType.ListDoNotContains: _get_schema_for_list_do_not_contains(
            _generic_schema
        ),
        AssertionEntityType.ListHasIndex: _get_schema_for_list_has_index(
            _generic_schema
        ),
        AssertionEntityType.ListDoNotHasIndex: _get_schema_for_list_do_not_has_index(
            _generic_schema
        ),
        AssertionEntityType.Map: _get_schema_for_map(_generic_schema),
        AssertionEntityType.MapKeyCount: _get_schema_for_map_key_count(_generic_schema),
        AssertionEntityType.MapHasKeys: _get_schema_for_map_has_keys(_generic_schema),
        AssertionEntityType.MapDoNotHasKeys: _get_schema_for_map_do_not_has_keys(
            _generic_schema
        ),
        AssertionEntityType.MapExactKeys: _get_schema_for_map_exact_keys(
            _generic_schema
        ),
        AssertionEntityType.Count: _get_schema_for_count(_generic_schema),
    }

    if item:
        return schema_map[item]

    return schema_map
