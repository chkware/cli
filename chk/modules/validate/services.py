"""
General validation services
"""

import json

from chk.infrastructure.view import PresentationBuilder
from chk.modules.validate.entities import RunReport


class ValidatePresenter(PresentationBuilder):
    """ValidatePresenter"""

    def dump_error_json(self, err: object = None) -> str:
        """dump_error_json"""

        if not err:
            err = self.data.exception

        return json.dumps({"error": (repr(err) if err else "Unspecified error")})

    def dump_error_fmt(self, err: object = None) -> str:
        """dump fmt error str"""

        if not err:
            err = self.data.exception

        return (
            f"Validate error\n------\n{repr(err)}"
            if err
            else "Validate error\n------\nUnspecified error"
        )

    def dump_fmt(self) -> str:
        """dump formatted string"""

        display_items: list[str] = []

        for key, item in self.data.exposed.items():
            if key == "_asserts_response" and isinstance(item, RunReport):
                display_items.append(item.as_fmt_str())
            else:
                display_items.append(json.dumps(item))

        return "\n======\n".join(display_items)

    def dump_json(self) -> str:
        """dump json"""

        display_items: list[dict] = []

        for key, item in self.data.exposed.items():
            display_items.append(dict(item))

        return json.dumps(display_items)
