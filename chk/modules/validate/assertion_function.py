"""
Assertion Functions mod
"""
from typing import TypeAlias

import var_dump

from chk.infrastructure.symbol_table import linear_replace

# assertion result type; internal use
_AResult: TypeAlias = tuple[bool, Exception | str]


def assert_equals(actual: object, expected: object, **_: object) -> _AResult:
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
