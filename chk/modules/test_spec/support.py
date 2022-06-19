"""
test_spec related support services
"""
from cerberus import validator
from chk.infrastructure.exception import err_message, messages
from chk.modules.test_spec.constants import TestSpecConfigNode, ExecuteConfigNode
from chk.modules.http.constants import RequestConfigNode
from chk.modules.test_spec.validation_rules import test_spec_schema


class TestSpecMixin:
    """
    Mixin for version spec. for v0.7.2
    """

    def __init_test_spec_mixin(self):
        self.in_file = None

    def test_spec_validated(self) -> dict[str, str]:
        """
        Validate the schema against config
        """
        try:
            test_spec_doc = self.test_spec_as_dict()
            if not self.validator.validate(test_spec_doc, test_spec_schema):
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))

            # validate request if it exists in-file
            self._validate_request()
        except validator.DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err

        return test_spec_doc  # or is a success

    def test_spec_as_dict(self) -> dict[str, str]:
        """
        Get version string
        """
        if not hasattr(self, 'validator') or not hasattr(self, 'document'):
            raise SystemExit(err_message('fatal.V0005'))

        try:
            return {key: self.document[key] for key in (TestSpecConfigNode.ROOT, ) if key in self.document}
        except Exception as ex:
            raise SystemExit(err_message('fatal.V0005', extra=ex))

    def _validate_request(self) -> None:
        """
        If request in file validate it or set False to internal in_file
        """
        out_file_request = self.document\
                               .get(TestSpecConfigNode.ROOT)\
                               .get(ExecuteConfigNode.ROOT)\
                               .get(ExecuteConfigNode.FILE) is not None
        in_file_request = self.document.get(RequestConfigNode.ROOT) is not None

        if in_file_request is out_file_request:
            raise SystemExit(err_message('fatal.V0020', extra={'spec': {'execute': {'file': '...'}}}))

        self.__init_test_spec_mixin()

        if in_file_request:
            self.request_validated()
            self.in_file = True
        else:
            self.in_file = False
