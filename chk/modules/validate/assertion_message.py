"""
Assertion Functions return messages
"""

_AMessages = {
    "equal": {
        "pass": "actual `{type_actual}({value_actual})` is equal to expected `{type_expected}({value_expected})`",
        "fail": "actual `{type_actual}({value_actual})` is not equal to expected `{type_expected}({value_expected})`",
    },
    "not_equal": {
        "pass": "actual `{type_actual}({value_actual})` is equal to expected `{type_expected}({value_expected})`",
        "fail": "actual `{type_actual}({value_actual})` is not equal to expected `{type_expected}({value_expected})`",
    },
    "accepted": {
        "pass": "actual `{type_actual}({value_actual})` is an accepted value",
        "fail": "actual `{type_actual}({value_actual})` is not an accepted value",
    },
    "declined": {
        "pass": "actual `{type_actual}({value_actual})` is a declined value",
        "fail": "actual `{type_actual}({value_actual})` is not a declined value",
    },
    "empty": {
        "pass": "actual `{type_actual}({value_actual})` is an empty value",
        "fail": "actual `{type_actual}({value_actual})` is not an empty value",
    },
    "not_empty": {
        "pass": "actual `{type_actual}({value_actual})` is a non-empty value",
        "fail": "actual `{type_actual}({value_actual})` is not a non-empty value",
    },
    "boolean": {
        "pass": "actual `{type_actual}({value_actual})` is a boolean value, expected `{type_expected}({value_expected})`",
        "fail": "actual `{type_actual}({value_actual})` is not a boolean value, expected `{type_expected}({value_expected})`",
    },
    "integer": {
        "pass": "actual `{type_actual}({value_actual})` is a integer value",
        "fail": "actual `{type_actual}({value_actual})` is not a integer value",
    },
    "integer_between": {
        "pass": "actual `{type_actual}({value_actual})` is a integer value, between `{extra_fields[min]}` and `{extra_fields[max]}`",
        "fail": "actual `{type_actual}({value_actual})` is not a integer value, or not between `{extra_fields[min]}` and `{extra_fields[max]}`",
    },
    "integer_greater": {
        "pass": "actual `{type_actual}({value_actual})` is a integer value, greater than `{extra_fields[other]}`",
        "fail": "actual `{type_actual}({value_actual})` is not a integer value, or not greater than `{extra_fields[other]}`",
    },
    "integer_greater_or_equal": {
        "pass": "actual `{type_actual}({value_actual})` is a integer value, greater than or equal to `{extra_fields[other]}`",
        "fail": "actual `{type_actual}({value_actual})` is not a integer value, or not greater than or equal to `{extra_fields[other]}`",
    },
    "integer_less": {
        "pass": "actual `{type_actual}({value_actual})` is a integer value, less than `{extra_fields[other]}`",
        "fail": "actual `{type_actual}({value_actual})` is not a integer value, or not less than `{extra_fields[other]}`",
    },
    "integer_less_or_equal": {
        "pass": "actual `{type_actual}({value_actual})` is a integer value, less than or equal to `{extra_fields[other]}`",
        "fail": "actual `{type_actual}({value_actual})` is not a integer value, or not less than or equal to `{extra_fields[other]}`",
    },
    "float_": {
        "pass": "actual `{type_actual}({value_actual})` is a floating point value",
        "fail": "actual `{type_actual}({value_actual})` is not a floating point value",
    },
    "float_between": {
        "pass": "actual `{type_actual}({value_actual})` is a floating point value, between `{extra_fields[min]}` and `{extra_fields[max]}`",
        "fail": "actual `{type_actual}({value_actual})` is not a floating point value, or not between `{extra_fields[min]}` and `{extra_fields[max]}`",
    },
    "float_greater": {
        "pass": "actual `{type_actual}({value_actual})` is a floating point value, greater than `{extra_fields[other]}`",
        "fail": "actual `{type_actual}({value_actual})` is not a floating point value, or not greater than `{extra_fields[other]}`",
    },
    "float_greater_or_equal": {
        "pass": "actual `{type_actual}({value_actual})` is a floating point value, greater than or equal to `{extra_fields[other]}`",
        "fail": "actual `{type_actual}({value_actual})` is not a floating point value, or not greater than or equal to `{extra_fields[other]}`",
    },
}


def get_assert_msg_for(fn_signature: str) -> str:
    [func, sign] = fn_signature.split(".")

    try:
        return _AMessages[func][sign]
    except KeyError:
        return ""
