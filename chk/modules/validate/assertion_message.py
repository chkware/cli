"""
Assertion Functions return messages
"""

_AMessages = {
    "equal": {
        "pass": "actual `{0}({1})` is equal to expected `{2}({3})`",
        "fail": "actual `{0}({1})` is not equal to expected `{2}({3})`",
    },
    "not_equal": {
        "pass": "actual `{0}({1})` is equal to expected `{2}({3})`",
        "fail": "actual `{0}({1})` is not equal to expected `{2}({3})`",
    },
    "accepted": {
        "pass": "actual `{0}({1})` is an accepted value",
        "fail": "actual `{0}({1})` is not an accepted value",
    },
    "declined": {
        "pass": "actual `{0}({1})` is a declined value",
        "fail": "actual `{0}({1})` is not a declined value",
    },
    "empty": {
        "pass": "actual `{0}({1})` is an empty value",
        "fail": "actual `{0}({1})` is not an empty value",
    },
    "not_empty": {
        "pass": "actual `{0}({1})` is a non-empty value",
        "fail": "actual `{0}({1})` is not a non-empty value",
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
