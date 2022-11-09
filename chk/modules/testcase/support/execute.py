import abc

from chk.infrastructure.file_loader import FileContext
from chk.infrastructure.helper import data_set
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

    def execute_as_dict(
        self, with_key: bool = True, compiled: bool = False
    ) -> dict | None:
        """Get execute as dictionary"""

        _data: dict[object, object] = {}
        execute_doc = self.as_dict(f"{TstConf.ROOT}.{ExConf.ROOT}", False, compiled)

        if not with_key:
            return execute_doc

        data_set(_data, f"{TstConf.ROOT}.{ExConf.ROOT}", execute_doc)
        return _data
