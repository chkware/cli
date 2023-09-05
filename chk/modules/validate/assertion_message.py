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
        "actual_not_allowed": "actual `{type_actual}({value_actual})` is not an accepted value",
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
        "pass": "actual `{type_actual}({value_actual})` is a boolean value.",
        "fail": "actual `{type_actual}({value_actual})` is not a boolean value",
        "actual_not_bool": "actual `{type_actual}({value_actual})` is not a boolean value",
        "expected_not_bool": "expected `{type_expected}({value_expected})` is not a boolean value",
        "expected_mismatch": "actual `{type_actual}({value_actual})` and expected `{type_expected}({value_expected})` mismatch",
    },
    "integer": {
        "pass": "actual `{type_actual}({value_actual})` is a integer value",
        "fail": "actual `{type_actual}({value_actual})` is not a integer value",
    },
    "integer_between": {
        "pass": "actual `{type_actual}({value_actual})` is between `{extra_fields[min]}` and `{extra_fields[max]}`",
        "fail": "actual `{type_actual}({value_actual})` is not between `{extra_fields[min]}` and `{extra_fields[max]}`",
        "actual_not_int": "actual `{type_actual}({value_actual})` is not an integer value",
    },
    "integer_greater": {
        "pass": "actual `{type_actual}({value_actual})` is greater than `{extra_fields[other]}`",
        "fail": "actual `{type_actual}({value_actual})` is not greater than `{extra_fields[other]}`",
        "actual_not_int": "actual `{type_actual}({value_actual})` is not an integer value",
    },
    "integer_greater_or_equal": {
        "pass": "actual `{type_actual}({value_actual})` is greater than or equal to `{extra_fields[other]}`",
        "fail": "actual `{type_actual}({value_actual})` is not greater than or equal to `{extra_fields[other]}`",
        "actual_not_int": "actual `{type_actual}({value_actual})` is not an integer value",
    },
    "integer_less": {
        "pass": "actual `{type_actual}({value_actual})` is less than `{extra_fields[other]}`",
        "fail": "actual `{type_actual}({value_actual})` is not less than `{extra_fields[other]}`",
        "actual_not_int": "actual `{type_actual}({value_actual})` is not an integer value",
    },
    "integer_less_or_equal": {
        "pass": "actual `{type_actual}({value_actual})` is less than or equal to `{extra_fields[other]}`",
        "fail": "actual `{type_actual}({value_actual})` is not less than or equal to `{extra_fields[other]}`",
        "actual_not_int": "actual `{type_actual}({value_actual})` is not an integer value",
    },
    "float_": {
        "pass": "actual `{type_actual}({value_actual})` is a float value",
        "fail": "actual `{type_actual}({value_actual})` is not a float value",
    },
    "float_between": {
        "pass": "actual `{type_actual}({value_actual})` is between `{extra_fields[min]}` and `{extra_fields[max]}`",
        "fail": "actual `{type_actual}({value_actual})` is not between `{extra_fields[min]}` and `{extra_fields[max]}`",
        "actual_not_float": "actual `{type_actual}({value_actual})` is not a float value",
    },
    "float_greater": {
        "pass": "actual `{type_actual}({value_actual})` is greater than `{extra_fields[other]}`",
        "fail": "actual `{type_actual}({value_actual})` is not greater than `{extra_fields[other]}`",
        "actual_not_float": "actual `{type_actual}({value_actual})` is not a float value",
    },
    "float_greater_or_equal": {
        "pass": "actual `{type_actual}({value_actual})` is greater than or equal to `{extra_fields[other]}`",
        "fail": "actual `{type_actual}({value_actual})` is not greater than or equal to `{extra_fields[other]}`",
        "actual_not_float": "actual `{type_actual}({value_actual})` is not a float value",
    },
    "float_less": {
        "pass": "actual `{type_actual}({value_actual})` is less than `{extra_fields[other]}`",
        "fail": "actual `{type_actual}({value_actual})` is not less than `{extra_fields[other]}`",
        "actual_not_float": "actual `{type_actual}({value_actual})` is not a float value",
    },
    "float_less_or_equal": {
        "pass": "actual `{type_actual}({value_actual})` is less than or equal to `{extra_fields[other]}`",
        "fail": "actual `{type_actual}({value_actual})` is not less than or equal to `{extra_fields[other]}`",
        "actual_not_float": "actual `{type_actual}({value_actual})` is not a float value",
    },
    "str_": {
        "pass": "actual `{type_actual}({value_actual})` is a string",
        "fail": "actual `{type_actual}({value_actual})` is not a string",
    },
    "str_have": {
        "pass": "actual `{type_actual}({value_actual})` have `{extra_fields[other]}` in it.",
        "fail": "actual `{type_actual}({value_actual})` do not have `{extra_fields[other]}` in it.",
        "actual_not_str": "actual `{type_actual}({value_actual})` is not a string.",
        "other_not_str": "other `{extra_fields[other]}` is not a string.",
    },
    "str_do_not_have": {
        "pass": "actual `{type_actual}({value_actual})` do not have `{extra_fields[other]}` in it.",
        "fail": "actual `{type_actual}({value_actual})` have `{extra_fields[other]}` in it.",
        "actual_not_str": "actual `{type_actual}({value_actual})` is not a string.",
        "other_not_str": "other `{extra_fields[other]}` is not a string.",
    },
    "str_starts_with": {
        "pass": "actual `{type_actual}({value_actual})` starts with `{extra_fields[other]}`.",
        "fail": "actual `{type_actual}({value_actual})` do not starts with `{extra_fields[other]}`.",
        "actual_not_str": "actual `{type_actual}({value_actual})` is not a string.",
        "other_not_str": "other `{extra_fields[other]}` is not a string.",
    },
    "str_do_not_starts_with": {
        "pass": "actual `{type_actual}({value_actual})` do not starts with `{extra_fields[other]}`.",
        "fail": "actual `{type_actual}({value_actual})` starts with `{extra_fields[other]}`.",
        "actual_not_str": "actual `{type_actual}({value_actual})` is not a string.",
        "other_not_str": "other `{extra_fields[other]}` is not a string.",
    },
    "str_ends_with": {
        "pass": "actual `{type_actual}({value_actual})` ends with `{extra_fields[other]}`.",
        "fail": "actual `{type_actual}({value_actual})` do not ends with `{extra_fields[other]}`.",
        "actual_not_str": "actual `{type_actual}({value_actual})` is not a string.",
        "other_not_str": "other `{extra_fields[other]}` is not a string.",
    },
    "str_do_not_ends_with": {
        "pass": "actual `{type_actual}({value_actual})` do not ends with `{extra_fields[other]}`.",
        "fail": "actual `{type_actual}({value_actual})` ends with `{extra_fields[other]}`.",
        "actual_not_str": "actual `{type_actual}({value_actual})` is not a string.",
        "other_not_str": "other `{extra_fields[other]}` is not a string.",
    },
    "date": {
        "pass": "actual `{type_actual}({value_actual})` match format `{extra_fields[format]}`.",
        "fail": "actual `{type_actual}({value_actual})` do not match format `{extra_fields[format]}`.",
        "actual_not_str": "actual `{type_actual}({value_actual})` is not a string formatted date.",
    },
    "date_after": {
        "pass": "actual `{type_actual}({value_actual})` is after `{type_expected}({value_expected})`",
        "fail": "actual `{type_actual}({value_actual})` is not after `{type_expected}({value_expected})`",
        "actual_not_str": "actual `{type_actual}({value_actual})` is not a string formatted date.",
        "expected_not_str": "expected `{type_expected}({value_expected})` is not a string formatted date.",
        "date_conversion_issue": "date conversion error. actual `{type_actual}({value_actual})`, expected `{type_expected}({value_expected})`, format `{extra_fields[format]}`.",
    },
    "date_after_or_equal": {
        "pass": "actual `{type_actual}({value_actual})` is after or equal `{type_expected}({value_expected})`",
        "fail": "actual `{type_actual}({value_actual})` is not after or equal `{type_expected}({value_expected})`",
        "actual_not_str": "actual `{type_actual}({value_actual})` is not a string formatted date.",
        "expected_not_str": "expected `{type_expected}({value_expected})` is not a string formatted date.",
        "date_conversion_issue": "date conversion error. actual `{type_actual}({value_actual})`, expected `{type_expected}({value_expected})`, format `{extra_fields[format]}`.",
    },
    "date_before": {
        "pass": "actual `{type_actual}({value_actual})` is before `{type_expected}({value_expected})`",
        "fail": "actual `{type_actual}({value_actual})` is not before `{type_expected}({value_expected})`",
        "actual_not_str": "actual `{type_actual}({value_actual})` is not a string formatted date.",
        "expected_not_str": "expected `{type_expected}({value_expected})` is not a string formatted date.",
        "date_conversion_issue": "date conversion error. actual `{type_actual}({value_actual})`, expected `{type_expected}({value_expected})`, format `{extra_fields[format]}`.",
    },
    "date_before_or_equal": {
        "pass": "actual `{type_actual}({value_actual})` is before or equal `{type_expected}({value_expected})`",
        "fail": "actual `{type_actual}({value_actual})` is not before or equal `{type_expected}({value_expected})`",
        "actual_not_str": "actual `{type_actual}({value_actual})` is not a string formatted date.",
        "expected_not_str": "expected `{type_expected}({value_expected})` is not a string formatted date.",
        "date_conversion_issue": "date conversion error. actual `{type_actual}({value_actual})`, expected `{type_expected}({value_expected})`, format `{extra_fields[format]}`.",
    },
    "list_": {
        "pass": "actual `{type_actual}({value_actual})` is a list",
        "fail": "actual `{type_actual}({value_actual})` is not a list",
    },
    "list_contains": {
        "pass": "expected `{type_expected}({value_expected})` found in actual `{type_actual}({value_actual})`",
        "fail": "expected `{type_expected}({value_expected})` not found in actual `{type_actual}({value_actual})`",
        "actual_not_list": "actual `{type_actual}({value_actual})` is not a list",
    },
    "list_do_not_contains": {
        "pass": "expected `{type_expected}({value_expected})` not found in actual `{type_actual}({value_actual})`",
        "fail": "expected `{type_expected}({value_expected})` found in actual `{type_actual}({value_actual})`",
        "actual_not_list": "actual `{type_actual}({value_actual})` is not a list",
    },
    "list_has_index": {
        "pass": "index `{extra_fields[index]}` found in actual `{type_actual}({value_actual})`",
        "fail": "index `{extra_fields[index]}` not found in actual `{type_actual}({value_actual})`",
        "actual_not_list": "actual `{type_actual}({value_actual})` is not a list",
        "index_not_int": "index `{extra_fields[index]}` is not a list",
    },
    "list_do_not_has_index": {
        "pass": "index `{extra_fields[index]}` not found in actual `{type_actual}({value_actual})`",
        "fail": "index `{extra_fields[index]}` found in actual `{type_actual}({value_actual})`",
        "actual_not_list": "actual `{type_actual}({value_actual})` is not a list",
        "index_not_int": "index `{extra_fields[index]}` is not a list",
    },
    "map_": {
        "pass": "actual `{type_actual}({value_actual})` is a map",
        "fail": "actual `{type_actual}({value_actual})` is not a map",
    },
    "map_key_count": {
        "pass": "actual `{type_actual}({value_actual})` key count is `{value_expected}`",
        "fail": "actual `{type_actual}({value_actual})` key count is not `{value_expected}`",
        "actual_not_dict": "actual `{type_actual}({value_actual})` is not a map",
        "expected_not_int": "expected `{type_expected}({value_expected})` is not integer",
    },
    "map_has_keys": {
        "pass": "actual `{type_actual}({value_actual})` has keys `{value_expected}`",
        "fail": "actual `{type_actual}({value_actual})` do not have keys `{value_expected}`",
        "actual_not_dict": "actual `{type_actual}({value_actual})` is not a map",
        "expected_not_list": "expected `{type_expected}({value_expected})` is not a list",
    },
    "map_do_not_has_keys": {
        "pass": "actual `{type_actual}({value_actual})` do not have keys `{value_expected}`",
        "fail": "actual `{type_actual}({value_actual})` have keys `{value_expected}`",
        "actual_not_dict": "actual `{type_actual}({value_actual})` is not a map",
        "expected_not_list": "expected `{type_expected}({value_expected})` is not a list",
    },
    "map_exact_keys": {
        "pass": "actual `{type_actual}({value_actual})` exactly have keys `{value_expected}`",
        "fail": "actual `{type_actual}({value_actual})` do not exactly have keys `{value_expected}`",
        "actual_not_dict": "actual `{type_actual}({value_actual})` is not a map",
        "expected_not_list": "expected `{type_expected}({value_expected})` is not a list",
    },
    "count": {
        "pass": "actual `{type_actual}({value_actual})` count is `{value_expected}`",
        "fail": "actual `{type_actual}({value_actual})` count is not `{value_expected}`",
        "actual_no_len": "actual `{type_actual}({value_actual})` is not countable",
        "expected_not_int": "expected `{type_expected}({value_expected})` is not integer",
    },
}


def get_assert_msg_for(fn_signature: str) -> str:
    [func, sign] = fn_signature.split(".")

    try:
        return _AMessages[func][sign]
    except KeyError:
        return ""
