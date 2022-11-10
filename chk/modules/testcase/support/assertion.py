import abc

from chk.infrastructure.exception import err_message
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

    def assertions_validated(self) -> dict:
        """Validate the schema against config"""

        try:
            assertions = self.assertions_as_dict()
            assertions_doc = dict_get(assertions, f"{TstConf.ROOT}.{TstConf.ASSERTS}")

            # case: if not list
            if not isinstance(assertions_doc, list):
                raise TypeError({TstConf.ROOT: [{TstConf.ASSERTS: ["expected list"]}]})

            # case: if list contains duplicate items
            asrt_list = [
                f"{item.get('type')}.{item.get('actual')}"
                for item in assertions_doc
                if isinstance(item, dict)
            ]

            if len(asrt_list) != len(set(asrt_list)):
                raise TypeError({TstConf.ROOT: [{TstConf.ASSERTS: ["duplicate assertion"]}]})
        except Exception as err:
            raise RuntimeError(err_message("fatal.V0001", extra=err)) from err

        return assertions if isinstance(assertions, dict) else {}

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
