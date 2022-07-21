"""
Presenting assert data
"""
from typing import List, TypeAlias
from dataclasses import dataclass


@dataclass
class AssertResult:
    """
    Holds assertion result after test run complete
    """

    name: str
    is_success: bool = True
    message: str = ''
    assert_fn: str = ''


AssertResultList: TypeAlias = List[AssertResult]
