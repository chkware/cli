"""
Module for variables management
"""
import abc
from copy import deepcopy
from types import MappingProxyType

from cerberus.validator import DocumentError

from chk.infrastructure.contexts import app, validator
from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import dict_set, data_get, dict_get

from chk.modules.version.constants import DocumentType

from chk.modules.http.constants import RequestConfigNode
from chk.modules.http.support import RequestValueHandler

from chk.modules.variables.constants import (
    VariableConfigNode as VarConf,
    LexicalAnalysisType,
)
from chk.modules.variables.validation_rules import (
    variable_schema,
    expose_schema,
    allowed_variable_name,
)
from chk.modules.variables.lexicon import StringLexicalAnalyzer

from chk.modules.testcase.support import TestcaseValueHandler
from chk.modules.testcase.constants import TestcaseConfigNode


def parse_args(argv_s: list[str], delimiter: str = "=") -> dict:
    """
    parse and return args to dict
    :return: dict
    """

    if argv_s:
        argv = [item for item in argv_s if delimiter in item]
        return {item[0]: item[1] for item in [item.split(delimiter) for item in argv]}

    return {}


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
            doc[key] = StringLexicalAnalyzer.replace_in_str(item, var_s)
        elif isinstance(doc[key], dict):
            doc[key] = replace_values(doc[key], var_s)
    return doc


class VariableMixin:
    """Mixin for variable spec. for v0.7.2"""

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """Abstract method to get file context"""

    @abc.abstractmethod
    def request_as_dict(self) -> dict:
        """Abstract method to get request"""

    def __init___(self, symbol_tbl=None):
        """Initialise mixing props"""

        self.file_ctx = self.get_file_context()

        if symbol_tbl is None:
            self.symbol_table = self.build_symbol_table()
        else:
            self.symbol_table = symbol_tbl

    def variable_validated(self) -> dict[str, dict]:
        """Validate the schema against config"""

        try:
            variables_doc = self.variable_as_dict()

            if not validator.validate(variables_doc, variable_schema):
                raise SystemExit(err_message("fatal.V0006", extra=validator.errors))

            if variables_doc:
                for key in variables_doc[VarConf.ROOT].keys():
                    allowed_variable_name(key)

        except DocumentError as doc_err:
            raise SystemExit(err_message("fatal.V0001", extra=doc_err)) from doc_err
        except ValueError as val_err:
            raise SystemExit(err_message("fatal.V0009", extra=val_err)) from val_err

        return variables_doc

    def variable_as_dict(self) -> dict[str, dict]:
        """Get variable dict"""

        document = app.get_original_doc(self.file_ctx.filepath_hash)

        try:
            return {key: document[key] for key in (VarConf.ROOT,) if key in document}
        except Exception as ex:
            raise SystemExit(err_message("fatal.V0005", extra=ex)) from ex

    def expose_validated(self) -> dict:
        """Validate the schema against config"""

        try:
            expose_doc = self.expose_as_dict()

            if not validator.validate(expose_doc, expose_schema):
                raise SystemExit(err_message("fatal.V0006", extra=validator.errors))

        except DocumentError as doc_err:
            raise SystemExit(err_message("fatal.V0001", extra=doc_err)) from doc_err

        return expose_doc

    def expose_as_dict(self) -> dict:
        """Get expose dict"""

        document = app.get_original_doc(self.file_ctx.filepath_hash)

        try:
            return {key: document[key] for key in (VarConf.EXPOSE,) if key in document}
        except Exception as ex:
            raise SystemExit(err_message("fatal.V0005", extra=ex)) from ex

    def variable_process(self, la_type: LexicalAnalysisType, symbol_table=None) -> dict:
        self.__init___(symbol_table)
        return self.lexical_analysis_for(la_type, self.symbol_table)

    def build_symbol_table(self) -> dict:
        """Fill variable space"""
        doc = self.variable_as_dict().get(VarConf.ROOT, {})
        if doc:
            return {key: doc[key] for key in doc.keys() if key in doc.keys()}

        return doc

    def lexical_analysis_for(
        self, la_type: LexicalAnalysisType, symbol_table: dict
    ) -> dict:
        """lexical validation"""
        document_replaced = app.get_original_doc(self.file_ctx.filepath_hash).copy()

        if la_type is LexicalAnalysisType.REQUEST:
            document_part = self.request_as_dict()

            document_replaced[
                RequestConfigNode.ROOT
            ] = RequestValueHandler.request_fill_val(
                document_part, symbol_table, replace_values
            )

        elif la_type is LexicalAnalysisType.TESTCASE:
            document_part = self.assertions_as_dict()

            keys = [TestcaseConfigNode.ROOT, TestcaseConfigNode.ASSERTS]
            dict_set(
                document_replaced,
                ".".join(keys),
                TestcaseValueHandler.assertions_fill_val(
                    document_part, symbol_table, replace_values
                ),
            )

        return document_replaced

    def lexical_analysis_for_request(self) -> None:
        """Lexical analysis for request block"""
        file_ctx = self.get_file_context()

        request_document = app.get_compiled_doc(
            file_ctx.filepath_hash, RequestConfigNode.ROOT
        )
        symbol_table = app.get_compiled_doc(file_ctx.filepath_hash, VarConf.ROOT)

        request_document_replaced = replace_values(request_document, symbol_table)

        app.set_compiled_doc(
            file_ctx.filepath_hash,
            part=RequestConfigNode.ROOT,
            value=request_document_replaced,
        )

    @staticmethod
    def variable_update_symbol_table(
        ctx_document: dict, updated: MappingProxyType
    ) -> dict:
        """
        Update symbol table and return updated document
        :param ctx_document:
        :param updated:
        :return:
        """
        document = deepcopy(ctx_document)

        document[VarConf.ROOT] = document.get(VarConf.ROOT, {}) | updated

        return document

    def variable_assemble_values(self, document: dict, response: dict) -> dict:
        """
        Assemble value based on return statement
        :param document:
        :param response:
        :return:
        """
        document_type = (
            DocumentType.HTTP
            if ":http:" in str(self.version_as_dict())
            else DocumentType.TESTCASE
        )

        if document_type is DocumentType.HTTP:
            return RequestValueHandler.request_get_return(document, response)

        elif document_type is DocumentType.TESTCASE:
            request_ret = RequestValueHandler.request_get_return(document, response)

            return TestcaseValueHandler.request_set_result(
                self.execute_as_dict(),
                MappingProxyType(self.symbol_table),
                MappingProxyType(request_ret),
            )

        raise ValueError(f"variable_assemble_values: `{document_type}` not allowed")

    def assemble_local_vars_for_request(self) -> dict:
        """Assemble value based on return statement"""
        document = self.request_as_dict()
        response = dict(app.get_compiled_doc(self.file_ctx.filepath_hash, "__local"))

        compiled_return: dict = RequestValueHandler.request_get_return(
            document, response.get(RequestConfigNode.LOCAL, {})
        )

        return compiled_return

    def make_exposable(self) -> None:
        """Prepare exposable data"""

        hf_name = self.get_file_context().filepath_hash

        symbol_table = app.get_compiled_doc(
            hf_name, VarConf.LOCAL
        ) | app.get_compiled_doc(hf_name, VarConf.ROOT)

        expose_items = app.get_compiled_doc(hf_name, VarConf.EXPOSE)

        if not isinstance(expose_items, list):
            raise ValueError

        exposables = [
            StringLexicalAnalyzer.replace(item, symbol_table)
            for item in expose_items
            if isinstance(item, str)
        ]

        app.set_compiled_doc(hf_name, part=VarConf.EXPOSE, value=exposables)

    def get_exposable(self) -> list:
        """Get exposable data"""

        hf_name = self.get_file_context().filepath_hash
        return app.get_compiled_doc(hf_name, VarConf.EXPOSE)

    def variable_prepare_value_table(self) -> None:
        updated_vars: dict = {}
        original_vars: dict = app.get_compiled_doc(
            self.file_ctx.filepath_hash, "variables"
        )

        # TODO: variable_handle_value_table_for_import()
        self.variable_handle_value_table_for_absolute(original_vars, updated_vars)
        self.variable_handle_value_table_for_composite(original_vars, updated_vars)

        app.set_compiled_doc(
            self.file_ctx.filepath_hash, part="variables", value=updated_vars
        )

    @staticmethod
    def variable_handle_value_table_for_absolute(actual: dict, updated: dict) -> None:
        """Detect only variable with absolute value"""

        for key, val in actual.items():
            if isinstance(val, str) and "{$" in val:
                continue

            updated[key] = val

    @staticmethod
    def variable_handle_value_table_for_composite(actual: dict, updated: dict) -> None:
        """Detect only variable with composite value"""

        temp = {key: val for key, val in actual.items() if key not in updated}

        replace_values(temp, updated)

        updated |= temp
