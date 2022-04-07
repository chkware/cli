"""
Module for variables management
"""
from cerberus.validator import DocumentError
from chk.infrastructure.exception import err_message
from chk.modules.variables.constants import VariableConfigElements_V072
from chk.modules.variables.validation_rules import variable_schema


class VariableMixin_V072(object):
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
            return {key:self.document[key] for key in (VariableConfigElements_V072.ROOT, ) if key in self.document}  # type: ignore
        except Exception as ex:
            raise SystemExit(err_message('fatal.V0005', extra=ex))