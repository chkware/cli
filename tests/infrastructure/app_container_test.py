# type: ignore

"""
test global chk functions
"""
from types import MappingProxyType

import pytest
import tests
import sys
from io import TextIOWrapper, BytesIO

from chk.infrastructure.containers import App, CompiledOptions
from chk.infrastructure.file_loader import FileContext, ChkFileLoader
from chk.infrastructure.helper import data_set, data_get


class TestChk:
    """Test chk functions"""

    @staticmethod
    def test_app_variables_set():
        app = App()
        data_set(app.original_doc, "some.key", "Some name: {name}")
        assert app.original_doc["some"]["key"] == "Some name: {name}"

    @staticmethod
    def test_app_variables_get():
        app = App()
        assert data_get(app.original_doc, "some.key") == "Some name: {name}"


class TestApp:
    """Test App container functionality"""

    @staticmethod
    def test_app_set_original_doc_pass():
        app = App()
        app.set_original_doc("ab12", {"a": 1})
        assert app.original_doc["ab12"] == {"a": 1}

    @staticmethod
    def test_app_set_original_doc_fail():
        app = App()
        with pytest.raises(RuntimeError):
            app.set_original_doc("ab12", ["a", 1])
            assert app.original_doc["ab12"] == ["a", 1]

    @staticmethod
    def test_app_get_original_doc_pass():
        app = App()
        ret_doc = app.get_original_doc("ab12")
        assert ret_doc == {"a": 1}

    @staticmethod
    def test_app_set_compiled_doc_fail_key_len():
        app = App()
        with pytest.raises(RuntimeError):
            app.set_compiled_doc("ab22", {"a": 1})

    @staticmethod
    def test_app_set_compiled_doc_fail_allowed_key():
        app = App()
        with pytest.raises(RuntimeError):
            app.set_compiled_doc(
                "ab22",
                {
                    "a": 1,
                    "b": 2,
                    "c": 3,
                },
            )

    @staticmethod
    def test_app_set_compiled_doc_pass():
        app = App()
        app.set_compiled_doc(
            "ab22", {"request": 1, "version": 2, "variables": 3, "expose": None}
        )

    @staticmethod
    def test_app_set_compiled_doc_part_fail():
        app = App()
        with pytest.raises(RuntimeError):
            app.set_compiled_doc(
                "ab22",
                part="re",
                value={
                    "a": 1,
                    "b": 2,
                    "c": 3,
                },
            )

    @staticmethod
    def test_app_set_compiled_doc_part_pass():
        app = App()
        val = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        app.set_compiled_doc("ab22", part="request", value=val)
        assert app.get_compiled_doc("ab22", "request") == val

    @staticmethod
    def test_app_set_compiled_doc_local_part_pass():
        app = App()
        val = {
            "a": 1,
            "b": 2,
            "c": 3,
        }

        app.set_compiled_doc("ab22", part="__local", value=val)
        assert app.get_compiled_doc("ab22", "__local") == val

    @staticmethod
    def test_app_set_compiled_doc_local_multiple_part_pass():
        app = App()
        val = {
            "a": 1,
            "b": 2,
            "c": 3,
        }

        app.set_compiled_doc("ab22", part="__local.some", value=val)
        assert app.get_compiled_doc("ab22", "__local.some") == val

    @staticmethod
    def test_app_get_compiled_doc_part_fail():
        app = App()
        with pytest.raises(RuntimeError):
            app.get_compiled_doc("ab22", part="re")

    @staticmethod
    def test_app_get_compiled_doc_part_pass():
        app = App()
        assert app.get_compiled_doc("ab22", part="request") == {
            "a": 1,
            "b": 2,
            "c": 3,
        }

    @staticmethod
    def test_app_get_compiled_doc_dot_part_pass():
        app = App()
        data_set(app.compiled_doc, "ab22.request.body", {"var": "val"})
        assert app.get_compiled_doc("ab22", part="request.body") == {"var": "val"}
        assert app.get_compiled_doc("ab22", part="request.body.var") == "val"

        del app.compiled_doc["ab22"]

    @staticmethod
    def test_app_load_original_doc_from_file_context_pass():
        app = App()
        file = tests.RES_DIR + "UserOk.chk"
        fpath_mangled, fpath_hash = ChkFileLoader.get_mangled_name(file)

        ctx = FileContext(
            filepath=file,
            filepath_mangled=fpath_mangled,
            filepath_hash=fpath_hash,
        )

        app.load_original_doc_from_file_context(ctx)
        assert app.original_doc[ctx.filepath_hash] == ChkFileLoader.to_dict(
            ctx.filepath
        )

    @staticmethod
    def test_app_load_original_doc_from_file_with_arguments():
        app = App()
        file = tests.RES_DIR + "UserOk.chk"
        fpath_mangled, fpath_hash = ChkFileLoader.get_mangled_name(file)

        ctx = FileContext(
            filepath=file,
            filepath_mangled=fpath_mangled,
            filepath_hash=fpath_hash,
            arguments=MappingProxyType(
                {
                    "variables": {
                        "Method": "GET",
                    }
                }
            ),
        )

        app.load_original_doc_from_file_context(ctx)

        assert app.original_doc[ctx.filepath_hash] == ChkFileLoader.to_dict(
            ctx.filepath
        ) | {
            "__outer": {
                "variables": {
                    "Method": "GET",
                }
            }
        }

    @staticmethod
    def test_app_load_original_doc_from_file_with_options():
        app = App()
        file = tests.RES_DIR + "UserOk.chk"
        fpath_mangled, fpath_hash = ChkFileLoader.get_mangled_name(file)

        ctx = FileContext(
            filepath=file,
            filepath_mangled=fpath_mangled,
            filepath_hash=fpath_hash,
            options=MappingProxyType(
                {
                    "result": False,
                    "dump": False,
                }
            ),
        )

        app.load_original_doc_from_file_context(ctx)

        assert app.config("result") is False
        assert app.config("dump") is False

    @staticmethod
    def test_config_pass():
        app = App()
        app.config("buffer_access_off", True)

        assert app.config("buffer_access_off") is True
        assert app.config("buffer_access_off", {"d": 1}) == {"d": 1}
        assert app.config("buffer_access_off") == {"d": 1}

    @staticmethod
    def test_app_set_local_pass():
        app = App()
        app.set_local("ab22", part="re", val=12)

        assert app.compiled_doc["ab22"]["__local"]["re"] == 12
        del app.compiled_doc["ab22"]

    @staticmethod
    def test_app_get_local_pass():
        app = App()
        app.set_local("ab22", part="re", val=12)

        assert app.compiled_doc["ab22"]["__local"]["re"] == app.get_local("ab22", "re")
        assert app.get_local("ab22", "re") == 12

    @staticmethod
    def test_app_set_outer_pass():
        app = App()
        app.set_outer("ab22", part="re", val=12)

        assert app.original_doc["ab22"]["__outer"]["re"] == 12
        del app.original_doc["ab22"]

    @staticmethod
    def test_app_get_outer_pass():
        app = App()
        app.set_outer("ab22", part="re", val=12)

        assert app.original_doc["ab22"]["__outer"]["re"] == app.get_outer("ab22", "re")
        assert app.get_outer("ab22", "re") == 12

    @staticmethod
    def test_app_print_fmt_pass_get_string():
        app = App()

        assert app.print_fmt("Some", ret_s=True) == "Some"

    @staticmethod
    def test_app_print_fmt_pass_get_string_with_cb():
        def cb(val):
            return f"1:{val}"

        app = App()

        assert app.print_fmt("Some", cb, True) == "1:Some"

    @staticmethod
    def test_app_print_fmt_pass_print():
        # setup the environment
        old_stdout = sys.stdout
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

        app = App()
        app.print_fmt("Some")

        # get output
        sys.stdout.seek(0)  # jump to the start
        out = sys.stdout.read()  # read output

        # restore stdout
        sys.stdout.close()
        sys.stdout = old_stdout

        # assert
        assert out == "Some\n"

    @staticmethod
    def test_app_print_fmt_pass_print_with_cb():
        def fmt(val):
            return f"1:{val}"

        # setup the environment
        old_stdout = sys.stdout
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

        app = App()
        app.print_fmt("Some", fmt)

        # get output
        sys.stdout.seek(0)  # jump to the start
        out = sys.stdout.read()  # read output

        # restore stdout
        sys.stdout.close()
        sys.stdout = old_stdout

        # assert
        assert out == "1:Some\n"

    @staticmethod
    def test_app_print_fmt_pass_print_with_cb_dict():
        def fmt(val):
            return f"Hello, I am {val['name']}. I am {val['age']} years old."

        # setup the environment
        old_stdout = sys.stdout
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

        app = App()
        app.print_fmt({"name": "Some One", "age": 43}, fmt)

        # get output
        sys.stdout.seek(0)  # jump to the start
        out = sys.stdout.read()  # read output

        # restore stdout
        sys.stdout.close()
        sys.stdout = old_stdout

        # assert
        assert out == "Hello, I am Some One. I am 43 years old.\n"


class TestCompiledOptions:
    @staticmethod
    def test_from_file_context():
        ctx = FileContext(
            options=MappingProxyType(
                {
                    "result": False,
                    "dump": False,
                }
            )
        )

        obj = CompiledOptions.from_file_context(ctx).dict()

        assert "result" in obj
        assert "dump" in obj
        assert obj["dump"] is False
