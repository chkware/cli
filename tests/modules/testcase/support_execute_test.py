# type: ignore
import pytest
import functools

from chk.infrastructure.helper import dict_get
from chk.modules.http.main import execute as execute_fn
from chk.modules.testcase.constants import ExecuteConfigNode
from tests import RES_DIR

from chk.infrastructure.containers import App
from chk.infrastructure.file_loader import FileContext, ChkFileLoader
from chk.modules.testcase.support.execute import ExecuteMixin

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
        assert tc.execute_as_dict() == {"execute": None}

        del app.original_doc[ctx.filepath_hash]

    def test_execute_as_dict_pass_with_none(self):
        file = RES_DIR + "fail_cases/testcases/GET-Plain.chk"
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingExecute(ctx)

        assert tc.execute_as_dict(with_key=False) is None

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
            "execute": {"file": "./01_UserCreateRequest.chk", "result": ["$Response"]}
        }

        del app.original_doc[ctx.filepath_hash]

    def test_execute_validated_pass_when_result_is_list(self):
        file = RES_DIR + "pass_cases/testcases/03_UserCreateSpec_ResultList.chk"
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingExecute(ctx)

        assert isinstance(tc.execute_validated(), dict)
        assert tc.execute_as_dict() == {
            "execute": {
                "file": "./03_UserCreateRequest_ResList.chk",
                "result": ["$Code", "$Headers"],
            }
        }

        del app.original_doc[ctx.filepath_hash]

    def test_execute_validated_fails_with_num(self):
        file = RES_DIR + "fail_cases/testcases/03_UserCreateSpec_ResultNum.chk"
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingExecute(ctx)

        with pytest.raises(RuntimeError):
            tc.execute_validated()

        del app.original_doc[ctx.filepath_hash]

    def test_execute_validated_fails_with_variable_name(self):
        file = RES_DIR + "fail_cases/testcases/03_UserCreateSpec_ResultVar.chk"
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingExecute(ctx)

        with pytest.raises(RuntimeError):
            tc.execute_validated()

        del app.original_doc[ctx.filepath_hash]

    def test_execute_validated_fails_with_list_num(self):
        file = RES_DIR + "fail_cases/testcases/03_UserCreateSpec_ResultListHaveNum.chk"
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingExecute(ctx)

        with pytest.raises(RuntimeError):
            tc.execute_validated()

        del app.original_doc[ctx.filepath_hash]

    def test_execute_validated_fails_with_list_sp_chars(self):
        file = RES_DIR + "fail_cases/testcases/03_UserCreateSpec_ResultListHaveSp.chk"
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingExecute(ctx)

        with pytest.raises(RuntimeError):
            tc.execute_validated()

        del app.original_doc[ctx.filepath_hash]

    def test_execute_validated_pass_with_underscore(self):
        file = RES_DIR + "pass_cases/testcases/03_UserCreateSpec_ResultListIgnore.chk"
        ctx = FileContext.from_file(file, {})
        app.load_original_doc_from_file_context(ctx)

        tc = HavingExecute(ctx)
        assert tc.execute_validated() == {
            "execute": {
                "file": "./03_UserCreateRequest_ResList.chk",
                "result": ["$Code", "_"],
            }
        }

        del app.original_doc[ctx.filepath_hash]

    def test_execute_out_file_pass(self):
        file = (
            RES_DIR + "pass_cases/testcases/02_POST-SpecWithRequestAndSpecFullVar.chk"
        )
        ctx = FileContext.from_file(file, {"result": True})

        document = ChkFileLoader.to_dict(ctx.filepath)
        app.set_compiled_doc(ctx.filepath_hash, document)

        tc = HavingExecute(ctx)
        execute = functools.partial(execute_fn, display=False)

        response = tc.execute_out_file(execute)

        assert isinstance(response, list)

        del app.compiled_doc[ctx.filepath_hash]

    def test_execute_prepare_results_pass(self):
        file = RES_DIR + "pass_cases/testcases/03_UserCreateSpec_ResultList.chk"
        ctx = FileContext.from_file(file, {"result": True})

        document = ChkFileLoader.to_dict(ctx.filepath)
        app.set_compiled_doc(ctx.filepath_hash, document)

        tc = HavingExecute(ctx)
        execute = functools.partial(execute_fn, display=False)

        response = tc.execute_out_file(execute)
        tc.execute_prepare_results(response)

        result_list = dict_get(
            tc.execute_as_dict(with_key=False, compiled=True),
            f"{ExecuteConfigNode.RESULT}",
        )
        result_local_val = app.get_local(ctx.filepath_hash, ExecuteConfigNode.LOCAL)

        assert len(result_list) == len(result_local_val)
        assert set(result_list) == set(result_local_val.keys())

        del app.compiled_doc[ctx.filepath_hash]

    def test_execute_prepare_results_pass_with_underscore(self):
        file = RES_DIR + "pass_cases/testcases/03_UserCreateSpec_ResultListIgnore.chk"
        ctx = FileContext.from_file(file, {"result": True})

        document = ChkFileLoader.to_dict(ctx.filepath)
        app.set_compiled_doc(ctx.filepath_hash, document)

        tc = HavingExecute(ctx)
        execute = functools.partial(execute_fn, display=False)

        response = tc.execute_out_file(execute)
        tc.execute_prepare_results(response)

        result_list = dict_get(
            tc.execute_as_dict(with_key=False, compiled=True),
            f"{ExecuteConfigNode.RESULT}",
        )
        result_list = [itm for itm in result_list if itm != "_"]

        result_local_val = app.get_local(ctx.filepath_hash, ExecuteConfigNode.LOCAL)

        assert len(result_list) == len(result_local_val)
        assert set(result_list) == set(result_local_val.keys())

        del app.compiled_doc[ctx.filepath_hash]

    def test_execute_prepare_results_pass_no_result(self):
        file = RES_DIR + "pass_cases/testcases/04_UserCreateSpec_NoResult.chk"
        ctx = FileContext.from_file(file, {"result": True})

        document = ChkFileLoader.to_dict(ctx.filepath)
        app.set_compiled_doc(ctx.filepath_hash, document)

        tc = HavingExecute(ctx)
        execute = functools.partial(execute_fn, display=False)

        response = tc.execute_out_file(execute)
        tc.execute_prepare_results(response)

        result_list = dict_get(
            tc.execute_as_dict(with_key=False, compiled=True),
            f"{ExecuteConfigNode.RESULT}",
        )

        assert result_list is None

        result_local_val = app.get_local(ctx.filepath_hash, ExecuteConfigNode.LOCAL)

        assert "$_response" in result_local_val
        assert len(result_local_val["$_response"]) == 2

        del app.compiled_doc[ctx.filepath_hash]
