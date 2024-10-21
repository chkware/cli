"""
General validation services
"""

from json import dumps

from chk.infrastructure.view import PresentationBuilder
from chk.modules.validate.entities import RunReport


class ValidatePresenter(PresentationBuilder):
    """ValidatePresenter"""

    def dump_error_json(self) -> str:
        return dumps(
            {
                "error": (
                    repr(self.data.exception)
                    if self.data.exception
                    else "Unspecified error"
                )
            }
        )

    def dump_error_fmt(self) -> str:
        """dump fmt error str"""

        # TODO also add tests those failed.
        return (
            f"Validate error\n------\n{repr(self.data.exception)}"
            if self.data.exception
            else "Validate error\n------\nUnspecified error"
        )

    def dump_fmt(self) -> str:
        """dump formatted string"""

        display_items: list[str] = []

        for key, item in self.data.exposed.items():
            if key == "_asserts_response" and isinstance(item, RunReport):
                display_items.append(item.as_fmt_str())
            else:
                display_items.append(dumps(item))

        return "\n======\n".join(display_items)

    def dump_json(self) -> str:
        """dump json"""

        display_items: list[dict] = []

        for key, item in self.data.exposed.items():
            display_items.append(dict(item))

        return dumps(display_items)
