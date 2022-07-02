"""
test global chk functions
"""
from chk.console.app_container import App, app


class TestChk:
    """Test chk functions"""
    @staticmethod
    def test_app_context():
        assert isinstance(app, App)

    @staticmethod
    def test_config_set():
        app.messages['exception']['key'] = 'Some name: {name}'
        assert app.messages['exception']['key'] == 'Some name: {name}'

    @staticmethod
    def test_config_get():
        assert app.messages['exception']['key'] == 'Some name: {name}'
