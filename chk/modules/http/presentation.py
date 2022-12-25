"""
Http presentation logic
"""


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
        b = sections["body"]
        resp += str(b) if not isinstance(b, str) else b

    if not resp:
        resp = str(sections)

    return resp


def present_result(exposable: list) -> str:
    """Present result"""

    return "\r\n\r\n".join(
        [
            present_dict(item) if isinstance(item, dict) else str(item)
            for item in exposable
        ]
    )
