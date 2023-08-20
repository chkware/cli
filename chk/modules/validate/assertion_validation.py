"""
Assertion validation module
"""
import enum


class AssertionEntityType(enum.StrEnum):
    """Type value constants for assertion entities"""

    ACCEPTED = "Accepted"
    DECLINED = "Declined"
    EQUAL = "Equal"
    NOT_EQUAL = "NotEqual"
    EMPTY = "Empty"
    NOT_EMPTY = "NotEmpty"
    BOOLEAN = "Boolean"
    INTEGER = "Integer"

