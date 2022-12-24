"""
Main driver
"""
import sys
from traceback import print_exc
from typing import Any

from chk.infrastructure.contexts import app
from chk.infrastructure.work import handle_worker
from chk.infrastructure.file_loader import FileContext

from chk.modules.http.entities import HttpSpec


def present_result(exposable: Any) -> str:
    """Present result"""

    def pprint(sections: dict) -> str:
        resp = ""

        if "version" in sections and "code" in sections and "reason" in sections:
            resp += f'{sections["version"]} {sections["code"]} {sections["reason"]}'

            resp += "\r\n\r\n"

        if "headers" in sections:
            items = sections["headers"].items()
            resp += "\r\n".join(f"{k}: {v}" for k, v in items)

            resp += "\r\n\r\n"

        if "body" in sections:
            b = sections["body"]
            resp += str(b) if not isinstance(b, str) else b

        if not resp:
            resp = str(sections)

        return resp

    return "\r\n\r\n".join(
        [pprint(item) if isinstance(item, dict) else str(item) for item in exposable]
    )


def execute(file_ctx: FileContext) -> None:
    """Execute command functionality"""

    http_spec = HttpSpec(file_ctx)
    try:
        response = handle_worker(http_spec)
        app.print_fmt(response, present_result)
    except RuntimeError:
        print_exc(file=sys.stderr)
