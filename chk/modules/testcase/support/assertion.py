import abc

from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import dict_get, data_set

from chk.modules.assertion.support import AssertionHandler
from chk.modules.testcase.constants import TestcaseConfigNode as TstConf
from chk.modules.version.support import DocumentMixin


class AssertionMixin(DocumentMixin):
    """Mixin for Execute sub-spec"""

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """Abstract method to get file context"""

    def assertions_as_dict(
            self, with_key: bool = True, compiled: bool = False
    ) -> dict | None:
        """Get assertion as dict"""

        _data: dict[object, object] = {}
        execute_doc = self.as_dict(f"{TstConf.ROOT}.{TstConf.ASSERTS}", False, compiled)

        if not with_key:
            return execute_doc

        data_set(_data, f"{TstConf.ROOT}.{TstConf.ASSERTS}", execute_doc)
        return _data

    def assertion_process(self) -> list:
        """
        Run assertion of testcase spec
        :return:
        """
        assertions = dict_get(self.assertions_as_dict(), TstConf.ASSERTS)
        return AssertionHandler.asserts_test_run(assertions)
