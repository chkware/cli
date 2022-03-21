"""
exception messages
"""
from typing import Any, Dict
from chk.infrastructure.translation import l10n

messages = dict(
    fatal=dict(
        V0001='`version` string not found.',
        V0002='Invalid file format.',
        V0003='`{file_name}` is not a valid YAML.',
        V0004='Unsupported document version',
        V0005='Unsupported document',
        V0006='Validation error.',
    )
)


def err_message(key: str, repl: Dict | None = None, extra: Any = None) -> str:
    """prepare error message"""
    if not isinstance(key, str): raise ValueError('Invalid `key`.')

    msg_sub, msg_pointer = key.split('.')
    if msg_pointer not in messages[msg_sub]: raise ValueError('Invalid `pointer`.')

    msg = messages[msg_sub][msg_pointer]
    msg = l10n(msg, repl)
    msg += (' : ' + str(extra) if extra else '')

    return 'error: ' + msg
