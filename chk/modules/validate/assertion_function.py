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
        return False

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
        return ValueError("actual_not_allowed")

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
    """Assert boolean"""

    if not isinstance(actual, bool):
        return ValueError("actual_not_bool")

    if not isinstance(expected, types.NotImplementedType) and not isinstance(
        expected, bool
    ):
        return ValueError("expected_not_bool")

    if isinstance(expected, bool):
        return True if actual == expected else ValueError("expected_mismatch")

    return True


def integer(actual: object, **_: object) -> _AResult:
    """Assert integer"""

    return isinstance(actual, int)


def integer_between(actual: object, extra_fields: dict, **_: object) -> _AResult:
    """Assert integer between"""

    if not isinstance(actual, int):
        return ValueError("actual_not_int")

    return int(extra_fields["min"]) < actual < int(extra_fields["max"])


def integer_greater(actual: object, extra_fields: dict, **_: object) -> _AResult:
    """Assert integer is greater than"""

    if not isinstance(actual, int):
        return ValueError("actual_not_int")

    return int(extra_fields["other"]) < actual


def integer_greater_or_equal(
    actual: object, extra_fields: dict, **_: object
) -> _AResult:
    """Assert integer is greater than or equal to other"""

    if not isinstance(actual, int):
        return ValueError("actual_not_int")

    return int(extra_fields["other"]) <= actual


def integer_less(actual: object, extra_fields: dict, **_: object) -> _AResult:
    """Assert integer is less than"""

    if not isinstance(actual, int):
        return ValueError("actual_not_int")

    return int(extra_fields["other"]) > actual


def integer_less_or_equal(actual: object, extra_fields: dict, **_: object) -> _AResult:
    """Assert integer is less than or equal to other"""

    if not isinstance(actual, int):
        return ValueError("actual_not_int")

    return int(extra_fields["other"]) >= actual


def float_(actual: object, **_: object) -> _AResult:
    """Assert float"""

    return isinstance(actual, float)


def float_between(actual: object, extra_fields: dict, **_: object) -> _AResult:
    """Assert float between"""

    if not isinstance(actual, float):
        return ValueError("actual_not_float")

    return extra_fields["min"] < actual < extra_fields["max"]


def float_greater(actual: object, extra_fields: dict, **_: object) -> _AResult:
    """Assert float is greater than"""

    if not isinstance(actual, float):
        return ValueError("actual_not_float")

    return extra_fields["other"] < actual


def float_greater_or_equal(actual: object, extra_fields: dict, **_: object) -> _AResult:
    """Assert float is greater than or equal to other"""

    if not isinstance(actual, float):
        return ValueError("actual_not_float")

    return extra_fields["other"] <= actual


def float_less(actual: object, extra_fields: dict, **_: object) -> _AResult:
    """Assert float is less than"""

    if not isinstance(actual, float):
        return ValueError("actual_not_float")

    return extra_fields["other"] > actual


def float_less_or_equal(actual: object, extra_fields: dict, **_: object) -> _AResult:
    """Assert float is greater than or equal to other"""

    if not isinstance(actual, float):
        return ValueError("actual_not_float")

    return extra_fields["other"] >= actual


def str_(actual: object, **_: object) -> _AResult:
    """Assert string"""

    return isinstance(actual, str)
