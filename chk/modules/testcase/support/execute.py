import abc

from chk.infrastructure.file_loader import FileContext
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

        execute_doc = self.as_dict(f"{TstConf.ROOT}.{ExConf.ROOT}", False, compiled)
        return {ExConf.ROOT: execute_doc} if with_key else execute_doc
