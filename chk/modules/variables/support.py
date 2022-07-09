"""
Module for variables management
"""
from types import MappingProxyType

from cerberus.validator import DocumentError
from chk.infrastructure.exception import err_message
from chk.modules.http.constants import RequestConfigNode
from chk.modules.http.support import RequestValueHandler
from chk.modules.testcase.support import TestcaseValueHandler
from chk.modules.variables.constants import VariableConfigNode as VarConf, LexicalAnalysisType
from chk.modules.variables.validation_rules import variable_schema
from chk.modules.version.constants import DocumentType
from copy import deepcopy


class VariableMixin(object):
    """ Mixin for variable spec. for v0.7.2"""

    def __init__mixin__(self, symbol_tbl=None):
        """
        Initialise mixing props
        :param symbol_tbl: dict
        """
        if symbol_tbl is None:
            self.symbol_table = self.build_symbol_table()
        else:
            self.symbol_table = symbol_tbl

    def variable_validated(self) -> dict[str, dict]:
        """Validate the schema against config"""
        try:
            request_doc = self.variable_as_dict()
            if not self.validator.validate(request_doc, variable_schema):
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))
        except DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err

        return request_doc  # or is a success

    def variable_as_dict(self) -> dict[str, dict]:
        """Get variable dict"""
        if not hasattr(self, 'validator') or not hasattr(self, 'document'):
            raise SystemExit(err_message('fatal.V0005'))

        try:
            return {key: self.document[key] for key in (VarConf.ROOT,) if
                    key in self.document}
        except Exception as ex:
            raise SystemExit(err_message('fatal.V0005', extra=ex))

    def variable_process(self, la_type: LexicalAnalysisType) -> dict:
        self.__init__mixin__()
        return self.lexical_analysis_for(la_type, self.symbol_table)

    def build_symbol_table(self) -> dict:
        """ Fill variable space"""
        doc = self.variable_as_dict().get(VarConf.ROOT, {})
        if doc: return {key: doc[key] for key in doc.keys() if key in doc.keys()}

        return doc

    def lexical_analysis_for(self, la_type: LexicalAnalysisType, symbol_table: dict) -> dict:
        """lexical validation"""
        document_part = {}

        if la_type is LexicalAnalysisType.REQUEST:
            document_part = self.request_as_dict()

        document_replaced = deepcopy(self.document)
        document_replaced[RequestConfigNode.ROOT] = RequestValueHandler.request_fill_val(document_part, symbol_table)

        return document_replaced

    def variable_assemble_values(self, document: dict, response: dict) -> dict:
        """
        Assemble value based on return statement
        :param document:
        :param response:
        :return:
        """
        document_type = self.get_document_type()

        if document_type is DocumentType.HTTP:
            return RequestValueHandler.request_get_return(document, response)

        elif document_type is DocumentType.TESTCASE:
            request_ret = RequestValueHandler.request_get_return(document, response)

            return TestcaseValueHandler.request_set_result(
                self.execute_as_dict(),
                MappingProxyType(self.symbol_table),
                MappingProxyType(request_ret)
            )

        raise ValueError(f'variable_assemble_values: `{document_type}` not allowed')

    @staticmethod
    def variable_update_symbol_table(ctx_document: dict, updated: MappingProxyType) -> dict:
        """
        Update symbol table and return updated document
        :param ctx_document:
        :param updated:
        :return:
        """
        document = deepcopy(ctx_document)

        document[VarConf.ROOT] = document.get(VarConf.ROOT, {}) | updated

        return document
