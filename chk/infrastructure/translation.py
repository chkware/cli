"""Translation related package"""
from typing import Dict


def l10n(message: str, data: Dict | None = None) -> str:
    """get localized message from locale file"""

    if message is None: raise ValueError
    if not message: raise ValueError

    message = str(message)
    if data is None: data = {}

    return message.format(**data)