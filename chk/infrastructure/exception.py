"""
exception messages
"""
from typing import Any
from chk.infrastructure.translation import l10n

messages = dict(
    fatal=dict(
        # http errors
        V0001="Document exception: `version` string not found",
        V0002="Document exception: Invalid file format",
        V0003="Document exception: `{file_name}` is not a valid YAML",
        V0004="File exception: Unsupported document version",
        V0005="File exception: Unsupported document",
        V0006="File exception: Validation failed",
        V0007="System exception: Not a Callable",
        V0008="System exception: Wrong spec class",
        V0009="Document exception: ",
        # testcase errors
        V0020="None or many request found",
        V0021="Passing value on same context",
        V0029="File linking not supported",
    )
)


def err_message(key: str, repl: dict | None = None, extra: Any = None) -> str:
    """prepare error message"""
    if not isinstance(key, str):
        raise ValueError("Invalid `key`.")

    msg_sub, msg_pointer = key.split(".")

    if msg_pointer not in messages[msg_sub]:
        raise ValueError("Invalid `pointer`.")

    msg = messages[msg_sub][msg_pointer]
    msg = l10n(msg, repl)
    msg += " : " + str(extra) if extra else ""

    return "error: " + msg
