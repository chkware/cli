"""
Assertion Functions mod
"""
from typing import TypeAlias, Union

# assertion result type; internal use
_AResult: TypeAlias = Union[ValueError | bool]

_AMessages = {
    "equal": {
        "pass": "actual `{0}({1})` is equal to expected `{2}({3})`",
        "fail": "actual `{0}({1})` is not equal to expected `{2}({3})`",
    },
    "not_equal": {
        "pass": "actual `{0}({1})` is equal to expected `{2}({3})`",
        "fail": "actual `{0}({1})` is not equal to expected `{2}({3})`",
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


def equal(actual: object, expected: object, **_: object) -> _AResult:
    """Assert equals

    Args:
        actual: object
        expected: object
        **_: object ignores any other params
    Returns:
        _AResult result
    """

    return actual == expected


def not_equal(actual: object, expected: object, **_: object) -> _AResult:
    """Assert not equal

    Args:
        actual: object
        expected: object
        **_: object ignores any other params
    Returns:
        _AResult result
    """

    return actual != expected
