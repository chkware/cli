"""
Assertion Functions mod
"""


def assert_equals(actual: object, expected: object, **_: object) -> bool:
    """Assert equals

    Args:
        actual: object
        expected: object
        **_: object ignores any other params
    Returns:
        True if equals
    Raises:
        AssertionError unless equal
    """

    if actual != expected:
        raise AssertionError(
            f"actual `{actual.__class__.__name__}({actual})`"
            + " is not equal to "
            + f"expected `{expected.__class__.__name__}({expected})`"
        )

    return True
