"""
test_spec related support services
"""
from cerberus import validator
from chk.infrastructure.exception import err_message
from chk.modules.test_spec.constants import TestSpecConfigNode
from chk.modules.test_spec.validation_rules import test_spec_schema


class TestSpecMixin:
    """ Mixin for version spec. for v0.7.2"""

    def test_spec_validated(self) -> dict[str, str]:
        """Validate the schema against config"""
        try:
            test_spec_doc = self.test_spec_as_dict()
            if not self.validator.validate(test_spec_doc, test_spec_schema):  # type: ignore
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))  # type: ignore
        except validator.DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err

        return test_spec_doc  # or is a success

    def test_spec_as_dict(self) -> dict[str, str]:
        """Get version string"""
        if not hasattr(self, 'validator') or not hasattr(self, 'document'):
            raise SystemExit(err_message('fatal.V0005'))

        try:
            return {key: self.document[key] for key in (TestSpecConfigNode.ROOT, ) if key in self.document}  # type: ignore
        except Exception as ex:
            raise SystemExit(err_message('fatal.V0005', extra=ex))
