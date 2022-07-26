from chk.modules.http.presentation import Presentation


class TestHttpPresentation:
    """Test methods of http.Presentation class."""

    def test_displayable_summary_success(self):
        """Test test_displayable_summary with success parameter."""
        filepath = '/home/some_path/GET-WithHeaders.chk'
        expected_summary = 'File: {}\r\n\nExecuting request\r\n\n- Making request [Success]\r\n===='.format(filepath)
        summary = Presentation.displayable_summary(filepath, status='Success')
        assert expected_summary == summary

    def test_displayable_summary_failed(self):
        """Test test_displayable_summary with failed parameter."""
        filepath = '/home/some_path/GET-WithHeaders.chk'
        expected_summary = 'File: {}\r\n\nExecuting request\r\n\n- Making request [Failed]\r\n===='.format(filepath)
        summary = Presentation.displayable_summary(filepath, status='Failed')
        assert expected_summary == summary
