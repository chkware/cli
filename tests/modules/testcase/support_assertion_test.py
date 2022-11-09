# type: ignore

from tests import RES_DIR

from chk.infrastructure.containers import App
from chk.infrastructure.file_loader import FileContext
from chk.modules.testcase.support.assertion import AssertionMixin

app = App()


class HavingAssertion(AssertionMixin):
    def __init__(self, file_ctx: FileContext) -> None:
        self.file_ctx = file_ctx

    def get_file_context(self) -> FileContext:
        return self.file_ctx


class TestAssertionMixin:
    def test_assertions_as_dict_pass(self):
        file = RES_DIR + "pass_cases/testcases/02_POST-SpecWithRequest.chk"
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingAssertion(ctx)
        assert isinstance(tc.assertions_as_dict(), dict)

        del app.original_doc[ctx.filepath_hash]

    def test_assertions_as_dict_pass_when_spec_not_found(self):
        file = RES_DIR + "fail_cases/testcases/GET-Plain.chk"
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingAssertion(ctx)

        assert isinstance(tc.assertions_as_dict(), dict)
        assert tc.assertions_as_dict() == {"spec": {"asserts": None}}

        del app.original_doc[ctx.filepath_hash]

    def test_execute_as_dict_pass_with_none(self):
        file = RES_DIR + "fail_cases/testcases/GET-Plain.chk"
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingAssertion(ctx)

        assert tc.assertions_as_dict(with_key=False) is None

        del app.original_doc[ctx.filepath_hash]

    def test_execute_as_dict_pass_with_full_execute(self):
        file = (
            RES_DIR + "pass_cases/testcases/02_POST-SpecWithRequestAndSpecFullVar.chk"
        )
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingAssertion(ctx)

        assert isinstance(tc.assertions_as_dict(), dict)
        assert isinstance(tc.assertions_as_dict(with_key=False), list)

        del app.original_doc[ctx.filepath_hash]
