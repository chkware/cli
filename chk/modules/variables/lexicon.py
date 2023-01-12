"""
Lexical analysis functionalities
"""
import re

from chk.infrastructure.helper import data_get


class StringLexicalAnalyzer:
    """Lexical analyzer for strings"""

    @staticmethod
    def replace(container: str, replace_with: dict) -> object:
        """replace values found in string with typed return"""

        if not isinstance(container, str):
            return container

        if len(replace_with) == 0:
            return container

        line_split = re.split(
            r"({\s*\$[a-zA-Z0-9_.]+\s*})|(\s*\$[a-zA-Z0-9_.]+)", container
        )
        line_strip = [
            "".join(item.split() if "$" in item else item)
            for item in line_split
            if item
        ]

        if len(line_strip) == 1:
            item = line_strip.pop()
            if "$" not in item:
                return container

            t_item = item.strip("{}").lstrip("$")
            value = data_get(replace_with, t_item)
            return value if value else "{ $" + t_item + " }"

        for i, item in enumerate(line_strip):
            item = item.strip("{}")
            if item.startswith("$"):
                value = data_get(replace_with, item.lstrip("$"), None)
                line_strip[i] = str(value) if value else "{" + item + "}"

        return "".join(line_strip)
