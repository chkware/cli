import abc

from chk.infrastructure.contexts import app
from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import dict_get

from chk.modules.assertion.support import AssertionHandler
from chk.modules.testcase.constants import TestcaseConfigNode as TstConf
from chk.modules.version.support import DocumentMixin


class AssertionMixin(DocumentMixin):
    """Mixin for Execute sub-spec"""

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """Abstract method to get file context"""

    def assertions_as_dict(self) -> dict[str, object]:
        """Get execute as dict"""

        try:
            file_ctx = self.get_file_context()
            document = app.get_original_doc(file_ctx.filepath_hash)

            doc_key = [TstConf.ROOT, TstConf.ASSERTS]
            if asserts := dict_get(document, ".".join(doc_key)):
                if type(asserts) != list:
                    raise TypeError({"spec": [{"asserts": ["expected `list`"]}]})

                asrt_list = [
                    f"{item.get('type')}.{item.get('actual')}"
                    for item in asserts
                    if type(item) == dict
                ]
                if len(asrt_list) != len(set(asrt_list)):
                    raise TypeError(
                        {"spec": [{"asserts": ["duplicate assertion of same value"]}]}
                    )

                return {TstConf.ASSERTS: asserts}
            else:
                raise ValueError({"spec": [{"asserts": ["required field"]}]})
        except Exception as ex:
            raise SystemExit(err_message("fatal.V0005", extra=ex))

    def assertion_process(self) -> list:
        """
        Run assertion of testcase spec
        :return:
        """
        assertions = dict_get(self.assertions_as_dict(), TstConf.ASSERTS)
        return AssertionHandler.asserts_test_run(assertions)
