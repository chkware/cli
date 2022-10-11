from types import MappingProxyType

from chk.infrastructure.contexts import app
from chk.infrastructure.file_loader import FileContext
from chk.modules.http.presentation import Presentation, buffer_msg


class TestHttpPresentation:
    """Test methods of http.Presentation class."""

    def test_displayable_summary_success(self):
        """Test test_displayable_summary with success parameter."""
        app.config("buffer_access_off", False)

        expected_summary = 'Some test case\r\n\r\n===='
        buffer_msg('Some test case')

        assert expected_summary == Presentation.displayable_summary()

    def test_displayable_summary_failed(self):
        """Test test_displayable_summary with failed parameter."""
        filepath = '/home/some_path/GET-WithHeaders.chk'
        expected_summary = f'File: {filepath}\r\n\nExecuting request\r\n\n- Making request [Failed]\r\n===='
        summary = Presentation.displayable_summary(filepath, status='Failed')
        assert expected_summary == summary

    def test_present_result_suppress_summary(self, capsys):
        """Tests suppressing result summary with --result=True."""
        options = MappingProxyType(
            dict(
                result=True,
            ),
        )
        file_ctx = FileContext(options)
        response = {'have_all': False}
        Presentation.present_result(file_ctx, response)
        captured = capsys.readouterr()
        assert 'Executing request' not in captured.out

    def test_present_result_show_summary(self, capsys):
        """Tests suppressing result summary with --result=False."""
        options = MappingProxyType(
            dict(
                result=False,
            ),
        )
        file_ctx = FileContext(options)
        response = {'have_all': False}
        Presentation.present_result(file_ctx, response)
        captured = capsys.readouterr()
        assert 'Executing request' in captured.out
