"""
Assertion Functions mod
"""
from typing import TypeAlias, Union

# assertion result type; internal use
_AResult: TypeAlias = Union[ValueError | bool]


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


def accepted(actual: object, **_: object) -> _AResult:
    """Assert has accepted values:
    1. yes, YES, Yes
    2. 1
    3. on, ON, On
    3. True, "True", "TRUE", "true"

    Args:
        actual: object
        **_: object ignores any other params
    Returns:
        _AResult result
    """

    accepted_values = [
        "yes",
        "YES",
        "Yes",
        "on",
        "ON",
        "On",
        1,
        True,
        "True",
        "TRUE",
        "true",
    ]
    declined_values = [
        "no",
        "NO",
        "No",
        "off",
        "OFF",
        "Off",
        0,
        False,
        "False",
        "FALSE",
        "false",
    ]

    if actual not in accepted_values + declined_values:
        return ValueError("accepted_not_allowed")

    return actual in accepted_values

