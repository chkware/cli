# type: ignore

from chk.modules.testcase.support.execute import ExecuteMixin
from tests import RES_DIR

from chk.infrastructure.containers import App
from chk.infrastructure.file_loader import FileContext

app = App()


class HavingExecute(ExecuteMixin):
    def __init__(self, file_ctx: FileContext) -> None:
        self.file_ctx = file_ctx

    def get_file_context(self) -> FileContext:
        return self.file_ctx


class TestExecuteMixin:
    def test_execute_as_dict_pass(self):
        file = RES_DIR + "pass_cases/testcases/02_POST-SpecWithRequest.chk"
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingExecute(ctx)
        assert isinstance(tc.execute_as_dict(), dict)

        del app.original_doc[ctx.filepath_hash]

    def test_execute_as_dict_pass_when_spec_not_found(self):
        file = RES_DIR + "fail_cases/testcases/GET-Plain.chk"
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingExecute(ctx)

        assert isinstance(tc.execute_as_dict(), dict)
        assert tc.execute_as_dict() == {"spec": {"execute": None}}

        del app.original_doc[ctx.filepath_hash]

    def test_execute_as_dict_pass_with_full_execute(self):
        file = (
            RES_DIR + "pass_cases/testcases/02_POST-SpecWithRequestAndSpecFullVar.chk"
        )
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingExecute(ctx)

        assert isinstance(tc.execute_as_dict(), dict)
        assert tc.execute_as_dict() == {
            "spec": {"execute": {"file": None, "result": "$Response"}}
        }

        del app.original_doc[ctx.filepath_hash]
