"""
test global chk functions
"""
import pytest

from chk.infrastructure.containers import App
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
