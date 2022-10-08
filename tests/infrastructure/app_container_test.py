"""
test global chk functions
"""
import pytest
import tests

from chk.infrastructure.containers import App, EventLog
from chk.infrastructure.file_loader import FileContext, ChkFileLoader
from chk.infrastructure.helper import data_set, data_get

app = App()


class TestChk:
    """Test chk functions"""

    @staticmethod
    def test_app_variables_set():
        data_set(app.original_doc, "some.key", "Some name: {name}")
        assert app.original_doc["some"]["key"] == "Some name: {name}"

    @staticmethod
    def test_app_variables_get():
        assert data_get(app.original_doc, "some.key") == "Some name: {name}"


class TestApp:
    """Test App container functionality"""

    @staticmethod
    def test_app_set_original_doc_pass():
        app.set_original_doc("ab12", {'a': 1})
        assert app.original_doc["ab12"] == {'a': 1}

    @staticmethod
    def test_app_set_original_doc_fail():
        with pytest.raises(SystemExit):
            app.set_original_doc("ab12", ['a', 1])
            assert app.original_doc["ab12"] == ['a', 1]

    @staticmethod
    def test_app_get_original_doc_pass():
        ret_doc = app.get_original_doc("ab12")
        assert ret_doc == {'a': 1}

    @staticmethod
    def test_app_set_compiled_doc_fail_key_len():
        with pytest.raises(SystemExit):
            app.set_compiled_doc("ab22", {'a': 1})

    @staticmethod
    def test_app_set_compiled_doc_fail_allowed_key():
        with pytest.raises(SystemExit):
            app.set_compiled_doc("ab22", {'a': 1, 'b': 2, 'c': 3, })

    @staticmethod
    def test_app_set_compiled_doc_pass():
        app.set_compiled_doc("ab22", {'request': 1, 'version': 2, 'variables': 3, })

    @staticmethod
    def test_app_set_compiled_doc_part_fail():
        with pytest.raises(SystemExit):
            app.set_compiled_doc("ab22", part="re", value={'a': 1, 'b': 2, 'c': 3, })

    @staticmethod
    def test_app_set_compiled_doc_part_pass():
        app.set_compiled_doc("ab22", part="request", value={'a': 1, 'b': 2, 'c': 3, })

    @staticmethod
    def test_app_set_compiled_doc_local_part_pass():
        app.set_compiled_doc("ab22", part="__local", value={'a': 1, 'b': 2, 'c': 3, })

    @staticmethod
    def test_app_get_compiled_doc_local_part_pass():
        assert app.get_compiled_doc("ab22", part="__local") == {'a': 1, 'b': 2, 'c': 3, }

    @staticmethod
    def test_app_get_compiled_doc_part_fail():
        with pytest.raises(SystemExit):
            app.get_compiled_doc("ab22", part="re")

    @staticmethod
    def test_app_get_compiled_doc_part_pass():
        assert app.get_compiled_doc("ab22", part="request") == {'a': 1, 'b': 2, 'c': 3, }

    @staticmethod
    def test_app_load_original_doc_from_file_context_pass():
        file = tests.RES_DIR + "UserOk.chk"
        fpath_mangled, fpath_hash = ChkFileLoader.get_mangled_name(file)

        ctx = FileContext(
            filepath=file,
            filepath_mangled=fpath_mangled,
            filepath_hash=fpath_hash,
        )

        app.load_original_doc_from_file_context(ctx)
        assert app.original_doc[ctx.filepath_hash] == ChkFileLoader.to_dict(ctx.filepath)

    @staticmethod
    def test_set_event_log_pass():
        app.set_event_log("ab12", EventLog("some_event_1", "some event 1", "INFO", "DEBUG"))

    @staticmethod
    def test_get_event_log_pass():
        e_lst = app.get_event_log("ab12")

        assert isinstance(e_lst, list)
        assert isinstance(e_lst[0], EventLog)
