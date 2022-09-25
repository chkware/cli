"""
test global chk functions
"""
import pytest

from chk.infrastructure.contexts import app
from chk.infrastructure.translation import l10n


class TestTranslation:
    """Test chk functions"""
    def test_l10n_should_pass(self):
        retstr = l10n(app.messages['exception']['key'], {'name': 'Hasan'})

        assert retstr == 'Some name: Hasan'

    def test_l10n_should_fail_on_empty_message(self):
        with pytest.raises(ValueError):
            l10n(None, {'name': 'Hasan'})


