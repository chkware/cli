"""
Support helper package
"""

import os
from typing import Any


def get_os_env_vars() -> dict[str, Any]:
    """Get a dic of environment variables set for current user

    Returns:
        dict[str, Any]: Dict containing environment variables
    """

    return dict(os.environ)
