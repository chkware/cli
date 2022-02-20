"""
test global chk functions
"""
from chk.globals import App, current_app, l10n


class TestChk:
    """Test chk functions"""

    def test_current_app(self):
        app = current_app()
        assert isinstance(app, App)

    def test_config_set(self):
        app = current_app()
        app.config.error.key = 'Some name: {name}'

        assert app.config.error.key == 'Some name: {name}'

    def test_config_get(self):
        app = current_app()
        str = l10n(app.config.error.key, {'name': 'Hasan'})

        assert str == 'Some name: Hasan'
