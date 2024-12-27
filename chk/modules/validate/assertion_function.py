"""
Assertion Functions mod
"""

import datetime
import types
from typing import TypeAlias, Union
from collections.abc import Sized

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


def str_have(actual: str, extra_fields: dict, **_: object) -> _AResult:
    """Assert string have a sub-string"""

    if not isinstance(actual, str):
        return ValueError("actual_not_str")

    if not isinstance(extra_fields["other"], str):
        return ValueError("other_not_str")

    return extra_fields["other"] in actual


def str_do_not_have(actual: str, extra_fields: dict, **_: object) -> _AResult:
    """Assert string do not have a sub-string"""

    if not isinstance(actual, str):
        return ValueError("actual_not_str")

    if not isinstance(extra_fields["other"], str):
        return ValueError("other_not_str")

    return extra_fields["other"] not in actual


def str_starts_with(actual: str, extra_fields: dict, **_: object) -> _AResult:
    """Assert string starts with sub-string"""

    if not isinstance(actual, str):
        return ValueError("actual_not_str")

    if not isinstance(extra_fields["other"], str):
        return ValueError("other_not_str")

    return actual.startswith(extra_fields["other"])


def str_do_not_starts_with(actual: str, extra_fields: dict, **_: object) -> _AResult:
    """Assert string do not starts with sub-string"""

    if not isinstance(actual, str):
        return ValueError("actual_not_str")

    if not isinstance(extra_fields["other"], str):
        return ValueError("other_not_str")

    return not actual.startswith(extra_fields["other"])


def str_ends_with(actual: str, extra_fields: dict, **_: object) -> _AResult:
    """Assert string ends with sub-string"""

    if not isinstance(actual, str):
        return ValueError("actual_not_str")

    if not isinstance(extra_fields["other"], str):
        return ValueError("other_not_str")

    return actual.endswith(extra_fields["other"])


def str_do_not_ends_with(actual: str, extra_fields: dict, **_: object) -> _AResult:
    """Assert string do not ends with sub-string"""

    if not isinstance(actual, str):
        return ValueError("actual_not_str")

    if not isinstance(extra_fields["other"], str):
        return ValueError("other_not_str")

    return not actual.endswith(extra_fields["other"])


def date(actual: str, extra_fields: dict, **_: object) -> _AResult:
    """Assert actual date"""

    if not isinstance(actual, str):
        return ValueError("actual_not_str")

    try:
        datetime.datetime.strptime(actual, extra_fields["format"]).date()
        return True
    except ValueError:
        return False


def date_after(actual: str, expected: str, extra_fields: dict, **_: object) -> _AResult:
    """Assert actual date is after expected date"""

    if not isinstance(actual, str):
        return ValueError("actual_not_str")

    if not isinstance(expected, str):
        return ValueError("expected_not_str")

    try:
        d_actual = datetime.datetime.strptime(actual, extra_fields["format"]).date()
        d_expected = datetime.datetime.strptime(expected, extra_fields["format"]).date()

        return d_actual > d_expected
    except ValueError:
        return ValueError("date_conversion_issue")


def date_after_or_equal(
    actual: str, expected: str, extra_fields: dict, **_: object
) -> _AResult:
    """Assert actual date is after or equal to expected date"""

    if not isinstance(actual, str):
        return ValueError("actual_not_str")

    if not isinstance(expected, str):
        return ValueError("expected_not_str")

    try:
        d_actual = datetime.datetime.strptime(actual, extra_fields["format"]).date()
        d_expected = datetime.datetime.strptime(expected, extra_fields["format"]).date()

        return d_actual >= d_expected
    except ValueError:
        return ValueError("date_conversion_issue")


def date_before(
    actual: str, expected: str, extra_fields: dict, **_: object
) -> _AResult:
    """Assert actual date is after expected date"""

    if not isinstance(actual, str):
        return ValueError("actual_not_str")

    if not isinstance(expected, str):
        return ValueError("expected_not_str")

    try:
        d_actual = datetime.datetime.strptime(actual, extra_fields["format"]).date()
        d_expected = datetime.datetime.strptime(expected, extra_fields["format"]).date()

        return d_actual < d_expected
    except ValueError:
        return ValueError("date_conversion_issue")


def date_before_or_equal(
    actual: str, expected: str, extra_fields: dict, **_: object
) -> _AResult:
    """Assert actual date is after expected date"""

    if not isinstance(actual, str):
        return ValueError("actual_not_str")

    if not isinstance(expected, str):
        return ValueError("expected_not_str")

    try:
        d_actual = datetime.datetime.strptime(actual, extra_fields["format"]).date()
        d_expected = datetime.datetime.strptime(expected, extra_fields["format"]).date()

        return d_actual <= d_expected
    except ValueError:
        return ValueError("date_conversion_issue")


def list_(actual: list, **_: object) -> _AResult:
    """Assert actual value is a list"""

    return isinstance(actual, list)


def list_contains(actual: list, expected: object, **_: object) -> _AResult:
    """Assert actual list contains given value"""

    if not isinstance(actual, list):
        return ValueError("actual_not_list")

    return expected in actual


def list_do_not_contains(actual: list, expected: object, **_: object) -> _AResult:
    """Assert actual list do no contains given value"""

    if not isinstance(actual, list):
        return ValueError("actual_not_list")

    return expected not in actual


def list_has_index(actual: list, extra_fields: dict, **_: object) -> _AResult:
    """Assert actual list has given index"""

    if not isinstance(actual, list):
        return ValueError("actual_not_list")

    if not isinstance(extra_fields["index"], int):
        return ValueError("index_not_int")

    return len(actual) > extra_fields["index"]


def list_do_not_has_index(actual: list, extra_fields: dict, **_: object) -> _AResult:
    """Assert actual list do no has given index"""

    if not isinstance(actual, list):
        return ValueError("actual_not_list")

    if not isinstance(extra_fields["index"], int):
        return ValueError("index_not_int")

    return len(actual) <= extra_fields["index"]


def map_(actual: list, **_: object) -> _AResult:
    """Actual is a map"""

    return isinstance(actual, dict)


def map_key_count(actual: dict, expected: int, **_: object) -> _AResult:
    """Actual is a map key count as expected"""

    if not isinstance(actual, dict):
        return ValueError("actual_not_dict")

    if not isinstance(expected, int):
        return ValueError("expected_not_int")

    return len(actual.keys()) == expected


def map_has_keys(actual: dict, expected: list, **_: object) -> _AResult:
    """Actual is a map has same keys as expected"""

    if not isinstance(actual, dict):
        return ValueError("actual_not_dict")

    if not isinstance(expected, list):
        return ValueError("expected_not_list")

    intersection = set(actual.keys()) & set(expected)
    return intersection == set(expected)


def map_do_not_has_keys(actual: dict, expected: list, **_: object) -> _AResult:
    """Actual is a map do no have keys as expected"""

    if not isinstance(actual, dict):
        return ValueError("actual_not_dict")

    if not isinstance(expected, list):
        return ValueError("expected_not_list")

    intersection = set(actual.keys()) & set(expected)
    return intersection != set(expected)


def map_exact_keys(actual: dict, expected: list, **_: object) -> _AResult:
    """Actual is a map keys are as expected"""

    if not isinstance(actual, dict):
        return ValueError("actual_not_dict")

    if not isinstance(expected, list):
        return ValueError("expected_not_list")

    return set(actual.keys()) & set(expected) == set(expected) == set(actual.keys())


def count(actual: Sized, expected: object, **_: object) -> _AResult:
    """If actual is countable validate count"""

    if not hasattr(actual, "__len__"):
        return ValueError("actual_no_len")

    if not isinstance(expected, int):
        return ValueError("expected_not_int")

    return len(actual) == expected
