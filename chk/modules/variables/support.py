"""
Module for variables management
"""
from cerberus.validator import DocumentError
from chk.infrastructure.exception import err_message
from chk.modules.http.constants import RequestConfigNode
from chk.modules.http.support import RequestValueHandler
from chk.modules.variables.constants import VariableConfigNode as VarConf, LexicalAnalysisType
from chk.modules.variables.validation_rules import variable_schema
from copy import deepcopy


class VariableMixin(object):
    """ Mixin for variable spec. for v0.7.2"""

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
        symbol_tbl = self.build_symbol_table()

        return self.lexical_analysis_for(la_type, symbol_tbl)

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

    @staticmethod
    def assemble_values(document: dict, response: dict) -> dict:
        return RequestValueHandler.request_get_return(document, response)
