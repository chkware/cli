"""
test global chk functions
"""
import pytest

from chk.infrastructure.exception import messages
from chk.infrastructure.helper import dict_get
from chk.infrastructure.translation import l10n


class TestTranslation:
    """Test chk functions"""
    def test_l10n_should_pass(self) -> None:
        message = str(dict_get(messages, 'fatal.V0003', {}))

        assert l10n(message, {'file_name': 'test.chk'}) == \
               'Document exception: `test.chk` is not a valid YAML'

    def test_l10n_should_fail_on_empty_message(self) -> None:
        with pytest.raises(ValueError):
            l10n('', {'name': 'Hasan'})
