import abc

from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import dict_get
from chk.modules.testcase.constants import (
    TestcaseConfigNode as TstConf,
    ExecuteConfigNode as ExConf,
)
from chk.modules.version.support import DocumentMixin


class ExecuteMixin(DocumentMixin):
    """
    Mixin for Execute sub-spec
    """

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """Abstract method to get file context"""

    def execute_validated(self) -> dict:
        """Validate the schema against config"""

        try:
            execute_doc = self.execute_as_dict()
            if not isinstance(execute_doc, dict):
                raise TypeError("Invalid execute spec")

            if (
                result_val := dict_get(execute_doc, f"{ExConf.ROOT}.{ExConf.RESULT}")
            ) is None:
                return {}

            if isinstance(result_val, str):
                if not result_val.startswith("$"):
                    raise TypeError(
                        "{'execute': {'result': 'use variable name with $'}}"
                    )
            elif isinstance(result_val, list):
                for each_var in result_val:
                    if not isinstance(each_var, str):
                        raise TypeError(
                            "{'execute': {'result': 'list variable must be string'}}"
                        )
                    if not each_var.startswith("$") and each_var != "_":
                        raise TypeError(
                            "{'execute': {'result': 'list variable name start with $'}}"
                        )
            else:
                raise TypeError(
                    "{'execute': {'result': 'must be string or list type'}}"
                )

        except Exception as ex:
            raise RuntimeError(err_message("fatal.V0009", extra=ex)) from ex

        return execute_doc if isinstance(execute_doc, dict) else {}

    def execute_as_dict(
        self, with_key: bool = True, compiled: bool = False
    ) -> dict | None:
        """Get execute as dictionary"""

        execute_doc = self.as_dict(f"{TstConf.ROOT}.{ExConf.ROOT}", False, compiled)
        return {ExConf.ROOT: execute_doc} if with_key else execute_doc
