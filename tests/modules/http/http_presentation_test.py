from types import MappingProxyType

from chk.infrastructure.contexts import app
from chk.modules.http.presentation import Presentation


class TestHttpPresentation:
    """Test methods of http.Presentation class."""

    def test_buffer_msg_success(self):
        Presentation.display_buffer = []
        app.config("buffer_access_off", False)

        Presentation.buffer_msg("Some message 1")
        Presentation.buffer_msg("Some message 2")
        assert len(Presentation.display_buffer) == 2

    def test_displayable_summary_success(self):
        """Test test_displayable_summary with success parameter."""
        Presentation.display_buffer = []
        app.config("buffer_access_off", False)

        expected_summary = 'Some test case\r\n\r\n===='
        Presentation.buffer_msg('Some test case')

        assert expected_summary == Presentation.displayable_summary()

    def test_present_result_suppress_summary(self, capsys):
        """Tests suppressing result summary with --result=True."""

        response = {'have_all': False}
        Presentation.present_result(response)
        captured = capsys.readouterr()
        assert 'Executing request' not in captured.out
