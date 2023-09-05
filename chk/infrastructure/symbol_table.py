"""
Symbol and variable management
"""
import enum
import os
import re
from collections import UserDict
from collections.abc import Callable

from chk.infrastructure.document import VersionedDocument
from chk.infrastructure.file_loader import FileContext, ExecuteContext
from chk.infrastructure.helper import data_get, StrTemplate


class VariableConfigNode(enum.StrEnum):
    """
    Represent variables config section
    """

    VARIABLES = enum.auto()
    EXPOSE = enum.auto()
    RETURN = enum.auto()
    RESULT = enum.auto()

    LOCAL = "__local"
    ENV = "_ENV"


VARIABLE_CONFIG_ALLOWED_LOCAL = [
    "_response",
    "_assertion_results",
]

# cerberus validation rules for variables
VARIABLE_SCHEMA = {
    VariableConfigNode.VARIABLES: {
        "required": False,
        "type": "dict",
        "empty": True,
        "nullable": True,
    }
}

# cerberus validation rules for variables
EXPOSE_SCHEMA = {
    VariableConfigNode.EXPOSE: {
        "required": False,
        "type": "list",
        "empty": True,
        "nullable": True,
    }
}


class Variables(UserDict):
    """Holds data for a variable"""


class ExposableVariables(UserDict):
    """Holds data for a expose data"""


def replace_value(doc: dict | list, var_s: dict) -> dict | list:
    """
    replace variables with values
    :param doc:
    :param var_s:
    :return:
    """

    for key, val in list(doc.items() if isinstance(doc, dict) else enumerate(doc)):
        if isinstance(val, str):
            str_tpl = StrTemplate(val)
            doc[key] = str_tpl.substitute(var_s)
        elif isinstance(val, (dict, list)):
            doc[key] = replace_value(doc[key], var_s)
    return doc


class VariableTableManager:
    """VariableTableManager"""

    @staticmethod
    def handle(
        variable_doc: Variables, document: VersionedDocument, exec_ctx: ExecuteContext
    ) -> None:
        """Handles variable handling

        Args:
            variable_doc: VariableDocument to add values to
            document: VersionedDocument of document data
            exec_ctx: ExecuteContext; passed ExecuteContext
        """

        # make file contexts out od tuple
        file_ctx = FileContext(*document.context)

        VariableTableManager.handle_environment(variable_doc)

        if variables := data_get(file_ctx.document, VariableConfigNode.VARIABLES):
            VariableTableManager.handle_absolute(variable_doc, variables)

        VariableTableManager.handle_execute_context(variable_doc, exec_ctx)

        if variables:
            VariableTableManager.handle_composite(variable_doc, variables)

    @staticmethod
    def handle_absolute(variable_doc: Variables, document: dict) -> None:
        """Handles absolute variables and values from document

        Args:
            variable_doc: VariableDocument to add values to
            document: dict of document data
        """

        for key, val in document.items():
            if isinstance(val, str) and StrTemplate.is_tpl(val):
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
            if isinstance(val, str) and StrTemplate.is_tpl(val):
                composite_values[key] = val

        if composite_values:
            replaced_values: dict = replace_callback(
                composite_values, variable_doc.data
            )
            for key, val in replaced_values.items():
                variable_doc[key] = val

    @staticmethod
    def handle_execute_context(
        variable_doc: Variables, exec_ctx: ExecuteContext
    ) -> None:
        """Handle variables passed from external context

        Args:
            variable_doc: Variables; Variable store
            exec_ctx: ExecuteContext; passed external context
        """

        ext_vars = data_get(exec_ctx.arguments, VariableConfigNode.VARIABLES, {})

        for key, val in ext_vars.items():
            variable_doc[key] = val


class ExposeManager:
    """ExposeManager handles all expose related functionality"""

    @staticmethod
    def get_expose_doc(document: dict) -> list:
        """Get `expose:` from a given document in dict

        Args:
            document: dict
        Returns:
            list: Contains expose as list or an empty list
        """

        return data_get(document, VariableConfigNode.EXPOSE, [])

    @staticmethod
    def replace_values(
        expose_doc: list,
        values: dict,
        replace_callback: Callable = replace_value,
    ) -> list:
        """Replace values on expose document

        Args:
            expose_doc: list containing the expose document
            values: dict containing data to replace values with
            replace_callback: Callable to use for value replace strategy.
                            default: replace_value
        """

        if not isinstance(expose_doc, list):
            raise RuntimeError("Unsupported expose structure")

        return replace_callback(expose_doc, values)

    @staticmethod
    def get_exposed_replaced_data(document: VersionedDocument, store: dict) -> list:
        """Get expose doc from a `VersionedDocument`, and prepare it from the
            value of `Variables`, and `store`, and return

        Args:
            document: VersionedDocument to get expose definition from it
            store: dict to use as value store

        Returns:
            dict: list of expose data
        """

        file_ctx = FileContext(*document.context)

        if expose_doc := ExposeManager.get_expose_doc(file_ctx.document):
            return ExposeManager.replace_values(expose_doc, store)

        return []
