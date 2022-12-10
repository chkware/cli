import abc

from chk.infrastructure.contexts import app
from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import dict_get

from chk.modules.testcase.constants import (
    AssertConfigNode as AtConf,
    TestcaseConfigNode as TstConf,
)

from chk.modules.version.support import DocumentMixin


class AssertionMixin(DocumentMixin):
    """Mixin for Execute sub-spec"""

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """Abstract method to get file context"""

    def assertions_validated(self) -> dict:
        """Validate the schema against config"""

        try:
            if not (assertions := self.assertions_as_dict()):
                raise RuntimeError(
                    f"assertions_validated: assertions[{str(assertions)}]"
                )

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
                raise TypeError(
                    {TstConf.ROOT: [{TstConf.ASSERTS: ["duplicate assertion"]}]}
                )
        except Exception as err:
            raise RuntimeError(err_message("fatal.V0001", extra=err)) from err

        return assertions if isinstance(assertions, dict) else {}

    def assertions_as_dict(
            self, with_key: bool = True, compiled: bool = False
    ) -> dict | None:
        """Get assertion as dict"""

        assert_doc = self.as_dict(f"{TstConf.ROOT}.{TstConf.ASSERTS}", False, compiled)
        return {TstConf.ROOT: {TstConf.ASSERTS: assert_doc}} if with_key else assert_doc

    def assertion_preserve_original(self) -> None:
        """Preserve original value of asserts.*.actual"""

        fh = self.get_file_context().filepath_hash
        assertions = app.get_compiled_doc(fh, f"{TstConf.ROOT}.{TstConf.ASSERTS}")

        if not isinstance(assertions, list):
            raise RuntimeError(f"assertion_process: assertions[{str(assertions)}]")

        for assertion in assertions:
            assertion[f"{AtConf.ACTUAL}_original"] = assertion[AtConf.ACTUAL]

        app.set_compiled_doc(fh, assertions, f"{TstConf.ROOT}.{TstConf.ASSERTS}")
