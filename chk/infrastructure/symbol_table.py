"""
Symbol and variable management
"""
import enum
import json
import os
import re
from collections import UserDict
from typing import Callable

from chk.infrastructure.document import VersionedDocument
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import data_get
from chk.infrastructure.third_party.symbol_template import get_template_from_str


class VariableConfigNode(enum.StrEnum):
    """
    Represent variables config section
    """

    VARIABLES = enum.auto()
    EXPOSE = enum.auto()
    ENV = "_ENV"


class Variables(UserDict):
    """Holds data for a variable"""


def replace_value(obj: dict, vals: dict) -> dict:
    """Replaces all values on a given dict

    Args:
        obj: dict, target dict
        vals: dict, value dict
    Returns:
        dict: replaced dict
    """

    obj_s = json.dumps(obj)

    tpl = get_template_from_str(obj_s)
    repl = tpl.render(**vals)

    return json.loads(repl)


class VariableTableManager:
    """VariableTableManager"""

    @staticmethod
    def handle(variable_doc: Variables, document: VersionedDocument) -> None:
        """Handles variable handling

        Args:
            variable_doc: VariableDocument to add values to
            document: VersionedDocument of document data
        """

        # make file contexts out od tuple
        file_ctx = FileContext(*document.context)

        VariableTableManager.handle_environment(variable_doc)

        if variables := data_get(file_ctx.document, VariableConfigNode.VARIABLES):
            VariableTableManager.handle_absolute(variable_doc, variables)
            VariableTableManager.handle_composite(variable_doc, variables)

    @staticmethod
    def handle_absolute(variable_doc: Variables, document: dict) -> None:
        """Handles absolute variables and values from document

        Args:
            variable_doc: VariableDocument to add values to
            document: dict of document data
        """

        for key, val in document.items():
            if isinstance(val, str) and re.search(r"{{.*}}|{%.*%}", val):
                continue

            variable_doc[key] = val

    @staticmethod
    def handle_environment(variable_doc: Variables) -> None:
        """Handles environment variables and values

        Args:
            variable_doc: VariableDocument to add values to
        """

        variable_doc[VariableConfigNode.ENV] = dict(os.environ)

    @staticmethod
    def handle_composite(
        variable_doc: Variables,
        document: dict,
        replace_callback: Callable = replace_value,
    ) -> None:
        """Handles absolute variables and values from document

        Args:
            variable_doc: VariableDocument to add values to
            document: dict of document data
            replace_callback: Callback for replace strategy, default is replace_value
        """

        composite_values = {}
        for key, val in document.items():
            if isinstance(val, str) and re.search(r"{{.*}}|{%.*%}", val):
                composite_values[key] = val

        if composite_values:
            replaced_values: dict = replace_callback(
                composite_values, variable_doc.data
            )
            for key, val in replaced_values.items():
                variable_doc[key] = val
