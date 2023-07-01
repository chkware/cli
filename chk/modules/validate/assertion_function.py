"""
Assertion Functions mod
"""

from typing import TypeAlias, Union

from chk.infrastructure.exception import ValidationError

# assertion result type; internal use
_AResult: TypeAlias = Union[ValidationError | bool]

_ExMsg = {
    "equal": {
        "pass": "actual `{0}({1})` is equal to expected `{2}({3})`",
        "fail": "actual `{0}({1})` is not equal to expected `{2}({3})`",
    },
    "not_equal": {
        "pass": "actual `{0}({1})` is equal to expected `{2}({3})`",
        "fail": "actual `{0}({1})` is not equal to expected `{2}({3})`",
    },
}


def equal(actual: object, expected: object, **_: object) -> _AResult:
    """Assert equals

    Args:
        actual: object
        expected: object
        **_: object ignores any other params
    Returns:
        _AResult result
    """

    if actual != expected:
        return ValidationError("equal")

    return True


def not_equal(actual: object, expected: object, **_: object) -> _AResult:
    """Assert not equal

    Args:
        actual: object
        expected: object
        **_: object ignores any other params
    Returns:
        _AResult result
    """

    resp = equal(actual, expected)

    if isinstance(resp, bool):
        return ValidationError("not_equal")

    return True
