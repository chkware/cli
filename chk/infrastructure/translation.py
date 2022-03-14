"""Translation related package"""
from typing import Dict


def l10n(message: str, data: Dict | None = None) -> str:
    """get localized message from locale file"""
    message = str(message)
    if data is None: data = {}

    return message.format(**data)