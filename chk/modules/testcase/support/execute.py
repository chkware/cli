import abc
from collections.abc import Callable
from pathlib import Path
from typing import Any

from chk.infrastructure.contexts import app
from chk.infrastructure.exception import err_message
from chk.infrastructure.file_loader import FileContext, PathFrom
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
                raise TypeError("execute_validated: invalid execute spec")

            if (
                result_val := dict_get(execute_doc, f"{ExConf.ROOT}.{ExConf.RESULT}")
            ) is None:
                return {}

            if isinstance(result_val, list):
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
                raise TypeError("{'execute': {'result': 'must be list type'}}")

        except Exception as ex:
            raise RuntimeError(err_message("fatal.V0009", extra=ex)) from ex

        return execute_doc if isinstance(execute_doc, dict) else {}

    def execute_as_dict(
        self, with_key: bool = True, compiled: bool = False
    ) -> dict | None:
        """Get execute as dictionary"""

        execute_doc = self.as_dict(f"{TstConf.ROOT}.{ExConf.ROOT}", False, compiled)
        return {ExConf.ROOT: execute_doc} if with_key else execute_doc

    def execute_out_file(self, cb: Callable) -> Any:
        """Handle out file execution"""

        base_file = self.get_file_context().filepath

        execute_doc = self.execute_as_dict(with_key=False, compiled=True)
        if not isinstance(execute_doc, dict):
            raise TypeError("execute_out_file: invalid execute spec")

        file_name = dict_get(execute_doc, f"{ExConf.FILE}")
        file_name = PathFrom(Path(base_file)).absolute(file_name)

        execute_with_doc = (
            execute_doc[ExConf.WITH] if ExConf.WITH in execute_doc else {}
        )

        file_ctx = FileContext.from_file(
            file_name,
            options=dict(self.get_file_context().options) | {"dump": False},
            arguments=dict(variables=execute_with_doc),
        )

        return cb(file_ctx)

    def execute_prepare_results(self, value_l: list[object]) -> None:
        """Make results out of values"""

        execute_doc = self.execute_as_dict(with_key=False, compiled=True)

        if not isinstance(execute_doc, dict):
            raise TypeError("execute_prepare_results: invalid execute spec")

        result_l = dict_get(execute_doc, f"{ExConf.RESULT}")

        if result_l is not None:
            if len(result_l) != len(value_l):
                raise ValueError("{'execute': {'result': 'value length do not match'}}")

            result_dict = {
                variable_name: value_l[index]
                for index, variable_name in enumerate(result_l)
                if variable_name != "_"
            }

        else:
            result_dict = {
                "$_response": value_l,
            }

        app.set_local(self.get_file_context().filepath_hash, result_dict, ExConf.LOCAL)
