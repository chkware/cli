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

        line_split = re.split(r"({\$[a-zA-Z0-9_.]+})", container)

        if len(line_split) == 1 and container in line_split:
            return container

        line_strip = [
            "".join(item.split() if "$" in item else item)
            for item in line_split
            if item
        ]

        for i, item in enumerate(line_strip):
            if "$" in item:
                value = data_get(replace_with, item.strip("{$}"), None)
                line_strip[i] = value or item

        return (
            "".join([str(li) for li in line_strip])
            if len(line_strip) > 1
            else line_strip.pop()
        )
