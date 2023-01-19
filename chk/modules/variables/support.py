"""
Module for variables management
"""
import abc
import re

from cerberus.validator import DocumentError

from chk.infrastructure.contexts import app, validator
from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext
from chk.modules.variables.constants import VariableConfigNode as VarConf
from chk.modules.variables.validation_rules import variable_schema, expose_schema
from chk.modules.variables.lexicon import StringLexicalAnalyzer

from chk.modules.version.support import DocumentMixin


def replace_values(doc: dict, var_s: dict) -> dict[str, object]:
    """
    replace variables with values
    :param doc:
    :param var_s:
    :return:
    """

    for key in doc.keys():
        if isinstance(doc[key], str):
            item = str(doc[key])
            doc[key] = StringLexicalAnalyzer.replace(item, var_s)
        elif isinstance(doc[key], dict):
            doc[key] = replace_values(doc[key], var_s)
    return doc


class VariableMixin(DocumentMixin):
    """Mixin for variable spec. for v0.7.2"""

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """Abstract method to get file context"""

    def variable_validated(self) -> dict:
        """Validate the schema against config"""

        try:
            variables_doc = self.variable_as_dict()

            if not validator.validate(variables_doc, variable_schema):
                raise RuntimeError(err_message("fatal.V0006", extra=validator.errors))

        except DocumentError as doc_err:
            raise RuntimeError(err_message("fatal.V0001", extra=doc_err)) from doc_err

        return variables_doc if isinstance(variables_doc, dict) else {}

    def variable_as_dict(
        self, with_key: bool = True, compiled: bool = False
    ) -> dict | None:
        """Get variable dict"""

        try:
            if not (variable_data := self.as_dict(VarConf.ROOT, False, compiled)):
                return {VarConf.ROOT: {}} if with_key else {}

            return {VarConf.ROOT: variable_data} if with_key else variable_data
        except RuntimeError:
            return {VarConf.ROOT: {}} if with_key else {}

    def expose_validated(self) -> dict:
        """Validate the schema against config"""

        try:
            expose_doc = self.expose_as_dict()

            if not validator.validate(expose_doc, expose_schema):
                raise RuntimeError(err_message("fatal.V0006", extra=validator.errors))

        except DocumentError as doc_err:
            raise RuntimeError(err_message("fatal.V0001", extra=doc_err)) from doc_err

        return expose_doc if isinstance(expose_doc, dict) else {}

    def expose_as_dict(
        self, with_key: bool = True, compiled: bool = False
    ) -> dict | None:
        """Get expose dict"""

        try:
            return self.as_dict(VarConf.EXPOSE, with_key, compiled)
        except RuntimeError:
            return {VarConf.EXPOSE: None} if with_key else None

    def get_symbol_table(self) -> dict:
        """Get current symbol table"""

        hf_name = self.get_file_context().filepath_hash

        symbol_table_l = app.get_compiled_doc(hf_name, VarConf.LOCAL) or {}
        if not isinstance(symbol_table_l, dict):
            raise RuntimeError

        _t_symbol_tbl: dict[str, object] = {}

        _t_symbol_tbl |= {
            symbol: symbol_table_l[symbol]
            for symbol in symbol_table_l
            if symbol in VarConf.ALLOWED_LOCAL
        }

        del symbol_table_l
        symbol_table = app.get_compiled_doc(hf_name, VarConf.ROOT) or {}

        if not isinstance(symbol_table, dict):
            raise RuntimeError

        symbol_table |= _t_symbol_tbl

        return symbol_table

    def make_exposable(self) -> None:
        """Prepare exposable data"""

        expose_items = self.get_exposable()

        exposables = [
            StringLexicalAnalyzer.replace(item, self.get_symbol_table())
            for item in expose_items
            if isinstance(item, str)
        ]

        app.set_compiled_doc(
            self.get_file_context().filepath_hash,
            part=VarConf.EXPOSE,
            value=exposables,
        )

    def get_exposable(self) -> list:
        """Get exposable data"""

        expose_doc = app.get_compiled_doc(
            self.get_file_context().filepath_hash, VarConf.EXPOSE
        )

        if not isinstance(expose_doc, list):
            raise RuntimeError

        return expose_doc

    def variable_prepare_value_table(self) -> None:
        hf = self.get_file_context().filepath_hash
        updated_vars: dict = {}

        original_vars = app.get_compiled_doc(hf, VarConf.ROOT)
        if not isinstance(original_vars, dict):
            raise RuntimeError

        outer_vars = app.get_outer(hf, VarConf.ROOT)
        if isinstance(outer_vars, dict):
            if not all(k in original_vars for k in outer_vars):
                raise RuntimeError("One or more outer variable is undeclared")

            original_vars |= outer_vars

        # TODO: variable_handle_value_table_for_import()
        self.variable_handle_value_table_for_absolute(original_vars, updated_vars)
        self.variable_handle_value_table_for_composite(original_vars, updated_vars)

        app.set_compiled_doc(hf, part=VarConf.ROOT, value=updated_vars)

    @staticmethod
    def variable_handle_value_table_for_absolute(actual: dict, updated: dict) -> None:
        """Detect only variable with absolute value"""

        for key, val in actual.items():
            if isinstance(val, str) and re.search(r"{\s*(\$[a-zA-Z0-9_]+)\s*}", val):
                continue

            updated[key] = val

    @staticmethod
    def variable_handle_value_table_for_composite(actual: dict, updated: dict) -> None:
        """Detect only variable with composite value"""

        temp = {key: val for key, val in actual.items() if key not in updated}

        replace_values(temp, updated)

        updated |= temp

    @staticmethod
    def variable_replace_value_table(symbol_tbl: dict, value_tbl: dict) -> None:
        """Replace symbol table based on the value passed"""

        for key, val in value_tbl.items():
            if (key := key.lstrip("$")) not in symbol_tbl:
                raise ValueError(f"variable is not defined in `{VarConf.ROOT}:` block")

            symbol_tbl[key] = val
