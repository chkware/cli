"""
Lexical analysis functionalities
"""
import re

from chk.infrastructure.helper import data_get


class StringLexicalAnalyzer:
    """Lexical analyzer for strings"""

    @staticmethod
    def replace_in_str(container: str, replace_with: dict) -> str:
        if not isinstance(container, str):
            raise TypeError

        if len(replace_with) == 0:
            return container

        line_split = re.split(r'({\s*\$\w+\s*})', container)
        line_strip = [''.join(item.split()) for item in line_split if item]

        for i, item in enumerate(line_strip):
            item = item.strip('{}')
            if item.startswith('$'):
                value = data_get(replace_with, item.lstrip('$'), None)
                line_strip[i] = str(value) if value else '{' + item + '}'

        return ''.join(line_strip)
