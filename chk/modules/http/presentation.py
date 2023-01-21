"""
Http presentation logic
"""
from json import dumps as js_dump
from xml.dom.minidom import parseString


def present_dict(sections: dict) -> str:
    resp = ""

    if "version" in sections and "code" in sections and "reason" in sections:
        resp += f'{sections["version"]} {sections["code"]} {sections["reason"]}'

        resp += "\r\n\r\n"

    if "headers" in sections:
        items = sections["headers"].items()
        resp += "\r\n".join(f"{k}: {v}" for k, v in items)

        resp += "\r\n\r\n"

    if "body" in sections:
        try:
            parseString(sections["body"])
            resp += sections["body"]
        except TypeError:
            resp += js_dump(sections["body"])
        except Exception:  # just dump to console for now
            resp += sections["body"]

    if not resp:
        resp = js_dump(sections)

    return resp


def present_result(exposable: list) -> str:
    """Present result"""

    return "\r\n\r\n".join(
        [
            present_dict(item) if isinstance(item, dict) else str(item)
            for item in exposable
        ]
    )
