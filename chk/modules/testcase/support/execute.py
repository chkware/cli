import abc

from chk.infrastructure.contexts import app
from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext
from chk.modules.testcase.constants import (
    TestcaseConfigNode as TstConf,
    ExecuteConfigNode as ExConf,
)


class ExecuteMixin:
    """
    Mixin for Execute sub-spec
    """

    @abc.abstractmethod
    def get_file_context(self) -> FileContext:
        """Abstract method to get file context"""

    def execute_as_dict(self) -> dict[str, str]:
        """
        Get execute as dict
        """
        file_ctx = self.get_file_context()
        document = app.get_original_doc(file_ctx.filepath_hash)

        try:
            if spec := document.get(TstConf.ROOT):
                if execute := spec.get(ExConf.ROOT):
                    return {ExConf.ROOT: execute}
                else:
                    raise ValueError({"spec": [{"execute": ["required field"]}]})
        except Exception as ex:
            raise SystemExit(err_message("fatal.V0005", extra=ex))
