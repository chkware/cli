"""
Module for variables management
"""
from cerberus.validator import DocumentError
from chk.infrastructure.exception import err_message
from chk.modules.http.constants import RequestConfigNode
from chk.modules.variables.constants import VariableConfigNode
from chk.modules.variables.lexicon import StringLexicalAnalyzer
from chk.modules.variables.validation_rules import variable_schema


class VariableMixin(object):
    """ Mixin for variable spec. for v0.7.2"""

    def variable_validated(self) -> dict[str, dict]:
        """Validate the schema against config"""
        try:
            request_doc = self.variable_as_dict()
            if not self.validator.validate(request_doc, variable_schema):  # type: ignore
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))  # type: ignore
        except DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err

        return request_doc  # or is a success

    def variable_as_dict(self) -> dict[str, dict]:
        """Get variable dict"""
        if not hasattr(self, 'validator') or not hasattr(self, 'document'):
            raise SystemExit(err_message('fatal.V0005'))

        try:
            return {key: self.document[key] for key in (VariableConfigNode.ROOT,) if key in self.document}  # type: ignore
        except Exception as ex:
            raise SystemExit(err_message('fatal.V0005', extra=ex))

    def variable_process(self) -> dict:
        symbol_tbl = self._build_symbol_table()
        request_doc = self.request_as_dict()  # type: ignore

        return self._lexical_analysis(request_doc, symbol_tbl)

    def _build_symbol_table(self) -> dict:
        """ Fill variable space"""
        doc = self.variable_as_dict().get(VariableConfigNode.ROOT, {})
        if doc: return {key: doc[key] for key in doc.keys() if key in doc.keys()}

        return doc

    def _lexical_analysis(self, document: dict, symbol_table: dict) -> dict:
        """lexical validation"""

        return {
            RequestConfigNode.ROOT: self._request_expression(document, symbol_table)
        }

    def _request_expression(self, document: dict, symbol_table: dict):
        """Convert request block variables"""
        def process_dict(doc: dict, var_s: dict):
            for key in doc.keys():
                if type(doc[key]) is str:
                    item = str(doc[key])
                    doc[key] = StringLexicalAnalyzer.replace_in_str(item, var_s)
                elif type(doc[key]) is dict:
                    doc[key] = process_dict(doc[key], var_s)
            return doc

        request_document = document.get(RequestConfigNode.ROOT, {})
        import copy; request_document = copy.deepcopy(request_document)

        return process_dict(request_document, symbol_table)
