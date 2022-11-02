# type: ignore

from chk.infrastructure.containers import App
from chk.infrastructure.file_loader import FileContext
from chk.modules.testcase.support.testcase import TestcaseMixin
from tests import RES_DIR

app = App()


class HavingTestcase(TestcaseMixin):
    def __init__(self, file_ctx: FileContext) -> None:
        self.file_ctx = file_ctx

    def get_file_context(self) -> FileContext:
        return self.file_ctx


class TestTestcaseMixin:
    def test_testcase_as_dict_pass(self):
        file = RES_DIR + "pass_cases/testcases/02_POST-SpecWithRequest.chk"
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)
        assert isinstance(tc.testcase_as_dict(), dict)

        del app.original_doc[ctx.filepath_hash]

    def test_testcase_as_dict_pass_when_spec_not_found(self):
        file = RES_DIR + "fail_cases/testcases/GET-Plain.chk"
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)
        print(tc.testcase_as_dict())

        assert isinstance(tc.testcase_as_dict(), dict)
        assert tc.testcase_as_dict() == {"spec": None}

        del app.original_doc[ctx.filepath_hash]
