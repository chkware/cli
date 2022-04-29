"""
Lexical analysis functionalities
"""
import re


class StringLexicalAnalyzer:
    """Lexical analyzer for strings"""

    @staticmethod
    def replace_in_str(container: str, replace_with: dict) -> str:
        if type(container) is not str: raise TypeError
        if len(replace_with) == 0: return container

        line_split = re.split("{|}", container)
        line_strip = [item.strip() for item in line_split if item]

        for i, item in enumerate(line_strip):
            if item.startswith('$'):
                value = replace_with.get(item.lstrip('$'), None)
                line_strip[i] = str(value) if value else '{' + item + '}'

        return ''.join(line_strip)

    @staticmethod
    def replace(container: str, replace_with: dict) -> str:
        if type(container) is not str: raise TypeError
        if len(replace_with) == 0: return container

        if container.startswith('$'):
            value = replace_with.get(container.lstrip('$'), None)
            return value if value else container

        return container
