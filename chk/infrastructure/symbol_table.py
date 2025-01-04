"""
Symbol and variable management
"""

from __future__ import annotations

import copy
import enum
import os
import typing
from collections import UserDict
from collections.abc import Callable

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field

from chk.infrastructure.document import VersionedDocument, VersionedDocumentV2
from chk.infrastructure.file_loader import ExecuteContext, FileContext
from chk.infrastructure.helper import data_get
from chk.infrastructure.templating import JinjaTemplate, is_template_str


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


class ExecResponse(BaseModel):
    """ExecResponse"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    file_ctx: FileContext
    exec_ctx: ExecuteContext
    variables: Variables = Field(default_factory=Variables)
    variables_exec: Variables = Field(default_factory=Variables)
    extra: object = Field(default=None)
    exception: Exception | None = Field(default=None)
    exposed: dict = Field(default_factory=dict)
    report: dict = Field(default_factory=dict)


@typing.overload
def replace_value(doc: dict, var_s: dict) -> dict: ...


@typing.overload
def replace_value(doc: list, var_s: dict) -> list: ...


def replace_value(doc: dict | list, var_s: dict) -> dict | list:
    """
    replace variables with values
    :param doc:
    :param var_s:
    :return:
    """

    for key, val in list(doc.items() if isinstance(doc, dict) else enumerate(doc)):
        if isinstance(val, str):
            str_tpl = JinjaTemplate.make(val)
            doc[key] = str_tpl.render(var_s)
        elif isinstance(val, (dict, list)):
            doc[key] = replace_value(doc[key], var_s)
    return doc


class VariableTableManager:
    """VariableTableManager"""

    @classmethod
    def handle(
        cls,
        variable_doc: Variables,
        document: VersionedDocument | VersionedDocumentV2,
        exec_ctx: ExecuteContext,
    ) -> None:
        """Handles variable handling

        Args:
            variable_doc: VariableDocument to add values to
            document: VersionedDocument of document data
            exec_ctx: ExecuteContext; passed ExecuteContext
        """
        # load environment variables
        cls.handle_environment(variable_doc)

        # make file contexts out of tuple
        file_ctx = FileContext(*document.context)

        if variables := data_get(file_ctx.document, VariableConfigNode.VARIABLES):
            cls.handle_absolute(variable_doc, variables)

        cls.handle_execute_context(variable_doc, exec_ctx)

        if variables:
            cls.handle_composite(variable_doc, variables)

    @classmethod
    def handle_absolute(cls, variable_doc: Variables, document: dict) -> None:
        """Handles absolute variables and values from document

        Args:
            variable_doc: VariableDocument to add values to
            document: dict of document data
        """

        for key, val in document.items():
            if isinstance(val, str) and is_template_str(val):
                continue

            variable_doc[key] = val

    @classmethod
    def handle_composite(
        cls,
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
            if isinstance(val, str) and is_template_str(val):
                composite_values[key] = val

        if composite_values:
            replaced_values: dict = replace_callback(
                composite_values, variable_doc.data
            )
            for key, val in replaced_values.items():
                variable_doc[key] = val

    @classmethod
    def handle_execute_context(
        cls, variable_doc: Variables, exec_ctx: ExecuteContext
    ) -> None:
        """Handle variables passed from external context

        Args:
            variable_doc: Variables; Variable store
            exec_ctx: ExecuteContext; passed external context
        """

        ext_vars = data_get(exec_ctx.arguments, VariableConfigNode.VARIABLES, {})

        for key, val in ext_vars.items():
            variable_doc[key] = val

    @classmethod
    def handle_environment(cls, variable_doc: Variables) -> None:
        """Handle variables passed from external context

        Args:
            variable_doc: Variables; Variable store
        """
        load_dotenv()
        variable_doc["_ENV"] = dict(os.environ)


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
    def get_exposed_replaced_data(document: VersionedDocumentV2, store: dict) -> dict:
        """
        Get expose doc from a `VersionedDocument`, and prepare it from the
            value of `Variables`, and `store`, and return

        Args:
            document: VersionedDocument to get expose definition from it
            store: dict to use as value store

        Returns:
            dict: list of expose data
        """

        file_ctx = FileContext(*document.context)

        if expose_doc := ExposeManager.get_expose_doc(file_ctx.document):
            exposed_doc_t = copy.copy(expose_doc)
            exposed_doc_t = [
                str(key).replace("%>", "").replace("<%", "").strip()
                for key in exposed_doc_t
            ]

            expose_val = ExposeManager.replace_values(expose_doc, store)
            return dict(zip(exposed_doc_t, expose_val))

        return {}
