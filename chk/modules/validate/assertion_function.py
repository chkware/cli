"""
Assertion Functions mod
"""
import types
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

    # fmt: off
    accepted_values = [
        "yes", "YES", "Yes",
        "on", "ON", "On",
        1, True,
        "True", "TRUE", "true",
    ]
    declined_values = [
        "no", "NO", "No",
        "off", "OFF", "Off",
        0, False,
        "False", "FALSE", "false",
    ]
    # fmt: on

    if actual not in accepted_values + declined_values:
        return ValueError("accepted_actual_not_allowed")

    return actual in accepted_values


def declined(actual: object, **_: object) -> _AResult:
    """Assert has declined values:
    1. no, NO, No
    2. 0, False,
    3. off, OFF, Off
    3. "False", "FALSE", "false"

    Args:
        actual: object
        **_: object ignores any other params
    Returns:
        _AResult result
    """

    # fmt: off
    accepted_values = [
        "yes", "YES", "Yes",
        "on", "ON", "On",
        1, True,
        "True", "TRUE", "true",
    ]
    declined_values = [
        "no", "NO", "No",
        "off", "OFF", "Off",
        0, False,
        "False", "FALSE", "false",
    ]
    # fmt: on

    if actual not in accepted_values + declined_values:
        return ValueError("declined_actual_not_allowed")

    return actual in declined_values


def empty(actual: object, **_: object) -> _AResult:
    """Assert empty

    Args:
        actual: object
        **_: object ignores any other params
    Returns:
        _AResult result
    """

    return not bool(actual)


def not_empty(actual: object, **_: object) -> _AResult:
    """Assert not empty

    Args:
        actual: object
        **_: object ignores any other params
    Returns:
        _AResult result
    """

    return bool(actual)


def boolean(actual: object, expected: object, **_: object) -> _AResult:
    """Assert boolean

    Args:
        actual: object
        expected: object
        **_: object ignores any other params
    Returns:
        _AResult result
    """

    eq_response: _AResult = True

    if not isinstance(expected, types.NotImplementedType):
        if not isinstance(expected, bool):
            return ValueError("expected_not_bool")

        eq_response = equal(actual, expected)

        if isinstance(eq_response, ValueError):
            return eq_response

    return eq_response and isinstance(actual, bool)


def integer(actual: object, **_: object) -> _AResult:
    """Assert integer

    Args:
        actual: object
        **_: object ignores any other params
    Returns:
        _AResult result
    """

    return isinstance(actual, int)


def integer_between(actual: object, extra_fields: dict, **_: object) -> _AResult:
    """Assert integer"""

    return isinstance(actual, int) and (
        int(extra_fields["min"]) < actual < int(extra_fields["max"])
    )
