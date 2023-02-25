# type: ignore
import pytest

from tests import RES_DIR

from chk.infrastructure.containers import App
from chk.infrastructure.file_loader import FileContext

# avoid ns collision
from chk.modules.testcase.support.testcase import TestcaseMixin as TCMixin
from chk.modules.http.support import RequestMixin

app = App()


class HavingTestcase(RequestMixin, TCMixin):
    def __init__(self, file_ctx: FileContext) -> None:
        self.file_ctx = file_ctx

    def get_file_context(self) -> FileContext:
        return self.file_ctx


class TestTestcaseMixin:
    def test_testcase_as_dict_pass(self):
        file_path = RES_DIR + "pass_cases/testcases/02_POST-SpecWithRequest.chk"
        ctx = FileContext.from_file(file_path)
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)
        assert isinstance(tc.testcase_as_dict(), dict)

        del app.original_doc[ctx.filepath_hash]

    def test_testcase_as_dict_pass_when_spec_not_found(self):
        file_path = RES_DIR + "fail_cases/testcases/GET-Plain.chk"
        ctx = FileContext.from_file(file_path)
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)

        assert isinstance(tc.testcase_as_dict(), dict)
        assert tc.testcase_as_dict() == {"spec": None}

        del app.original_doc[ctx.filepath_hash]

    def test_testcase_validated_pass_when_spec_found(self):
        file_path = RES_DIR + "pass_cases/testcases/02_POST-SpecWithRequest.chk"
        ctx = FileContext.from_file(file_path)
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)
        assert isinstance(tc.testcase_validated(), dict)

        del app.original_doc[ctx.filepath_hash]

    def test_testcase_validated_fails_when_no_spec(self):
        file_path = RES_DIR + "fail_cases/testcases/GET-Plain.chk"
        ctx = FileContext.from_file(file_path)
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)
        with pytest.raises(RuntimeError):
            tc.testcase_validated()

        del app.original_doc[ctx.filepath_hash]

    def test_testcase_validated_fails_when_no_in_file_request_spec(self):
        file_path = RES_DIR + "fail_cases/testcases/GET-NoRequest.chk"
        ctx = FileContext.from_file(file_path)
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)
        with pytest.raises(RuntimeError):
            tc.testcase_validated()

        del app.original_doc[ctx.filepath_hash]

    def test_testcase_validated_pass_with_out_file_req(self):
        file_path = RES_DIR + "pass_cases/testcases/01_UserCreateSpecPassVars.chk"
        ctx = FileContext.from_file(file_path)
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)
        tc.testcase_validated()

        del app.original_doc[ctx.filepath_hash]

    def test_testcase_validated_fail_with_in_file_req(self):
        file_path = RES_DIR + "fail_cases/testcases/01_UserCreateSpecPassVars.chk"
        ctx = FileContext.from_file(file_path)
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)
        with pytest.raises(RuntimeError):
            tc.testcase_validated()

        del app.original_doc[ctx.filepath_hash]

    def test_testcase_validated_pass_with_declarative_execute(self):
        file_path = RES_DIR + "pass_cases/testcases/02_POST-SpecWithRequestAndSpecFull.chk"
        ctx = FileContext.from_file(file_path)
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)
        tc.testcase_validated()

        del app.original_doc[ctx.filepath_hash]

    def test_testcase_validated_pass_with_declarative_execute_and_var(self):
        file_path = (
            RES_DIR + "pass_cases/testcases/02_POST-SpecWithRequestAndSpecFullVar.chk"
        )
        ctx = FileContext.from_file(file_path)
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)
        tc.testcase_validated()

        del app.original_doc[ctx.filepath_hash]

    def test_testcase_validated_fail_for_multiple_request(self):
        file_path = RES_DIR + "fail_cases/testcases/GET-MultipleRequest.chk"
        ctx = FileContext.from_file(file_path)
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)
        with pytest.raises(RuntimeError):
            tc.testcase_validated()

        del app.original_doc[ctx.filepath_hash]

    def test_testcase_validated_fail_for_result_when_request_in_file(self):
        file_path = RES_DIR + "fail_cases/testcases/01_UserCreateSpecUseResult.chk"
        ctx = FileContext.from_file(file_path)
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)
        with pytest.raises(RuntimeError):
            tc.testcase_validated()

        del app.original_doc[ctx.filepath_hash]

    def test_is_request_infile_pass(self):
        file_path = RES_DIR + "pass_cases/testcases/02_POST-SpecWithRequest.chk"
        ctx = FileContext.from_file(file_path)
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)
        assert tc.is_request_infile()

        del app.original_doc[ctx.filepath_hash]

    def test_is_request_infile_fails(self):
        file_path = RES_DIR + "pass_cases/testcases/01_UserCreateSpec.chk"
        ctx = FileContext.from_file(file_path)
        app.load_original_doc_from_file_context(ctx)

        tc = HavingTestcase(ctx)
        assert not tc.is_request_infile()

        del app.original_doc[ctx.filepath_hash]
