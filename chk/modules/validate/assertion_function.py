"""
Assertion Functions mod
"""
from typing import TypeAlias

# assertion result type; internal use
_AResult: TypeAlias = tuple[bool, Exception | str]


def assert_equal(actual: object, expected: object, **_: object) -> _AResult:
    """Assert equals

    Args:
        actual: object
        expected: object
        **_: object ignores any other params
    Returns:
        _AResult result
    """

    if actual != expected:
        return (
            False,
            AssertionError(
                f"actual `{actual.__class__.__name__}({actual})`"
                + " is not equal to "
                + f"expected `{expected.__class__.__name__}({expected})`"
            ),
        )

    return (
        True,
        (
            f"actual `{actual.__class__.__name__}({actual})`"
            + " is equal to "
            + f"expected `{expected.__class__.__name__}({expected})`"
        ),
    )


# case_AssertNotEqual
def assert_not_equal(actual: object, expected: object, **_: object) -> _AResult:
    """Assert not equal

    Args:
        actual: object
        expected: object
        **_: object ignores any other params
    Returns:
        _AResult result
    """

    is_success, _ = assert_equal(actual, expected)

    if is_success:
        return (
            False,
            AssertionError(
                f"actual `{actual.__class__.__name__}({actual})`"
                + " is equal to "
                + f"expected `{expected.__class__.__name__}({expected})`"
            ),
        )

    return (
        True,
        (
            f"actual `{actual.__class__.__name__}({actual})`"
            + " is not equal to "
            + f"expected `{expected.__class__.__name__}({expected})`"
        ),
    )
