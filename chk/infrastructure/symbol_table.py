"""
Symbol and variable management
"""
import enum
import os
import re
from collections import UserDict

from chk.infrastructure.document import VersionedDocument
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import data_get


class VariableConfigNode(enum.StrEnum):
    """
    Represent variables config section
    """

    VARIABLES = enum.auto()
    EXPOSE = enum.auto()
    ENV = "_ENV"


class Variables(UserDict):
    """Holds data for a variable"""


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
