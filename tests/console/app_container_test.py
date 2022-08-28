"""
test global chk functions
"""
from chk.console.app_container import App
from chk.console.helper import data_set, data_get

app = App()


class TestChk:
    """Test chk functions"""

    @staticmethod
    def test_app_variables_set():
        data_set(app.variables, "some.key", "Some name: {name}")
        assert app.variables["some"]["key"] == "Some name: {name}"

    @staticmethod
    def test_app_variables_get():
        assert data_get(app.variables, "some.key") == "Some name: {name}"
