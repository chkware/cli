from types import MappingProxyType

from chk.infrastructure.file_loader import FileContext
from chk.modules.http.presentation import Presentation


class TestHttpPresentation:
    """Test methods of http.Presentation class."""

    def test_displayable_summary_success(self):
        """Test test_displayable_summary with success parameter."""
        filepath = '/home/some_path/GET-WithHeaders.chk'
        expected_summary = f'File: {filepath}\r\n\nExecuting request\r\n\n- Making request [Success]\r\n===='
        summary = Presentation.displayable_summary(filepath, status='Success')
        assert expected_summary == summary

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
