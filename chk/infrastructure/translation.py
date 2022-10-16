"""Translation related package"""


def l10n(message: str, data: dict | None = None) -> str:
    """get localized message from locale file"""

    if not message or message is None:
        raise ValueError

    if data is None:
        data = {}

    return message.format(**data)
