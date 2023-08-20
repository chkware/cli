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
}


def get_pass_assert_msg_for(function_name: str) -> str:
    try:
        return _AMessages[function_name].get("pass", "")
    except KeyError:
        return ""


def get_fail_assert_msg_for(function_name: str) -> str:
    try:
        return _AMessages[function_name].get("fail", "")
    except KeyError:
        return ""
