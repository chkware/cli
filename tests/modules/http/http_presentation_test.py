from chk.modules.http.presentation import Presentation


class TestHttpPresentation:
    """Test methods of http.Presentation class."""

    def test_displayable_exec_summary_valid(self):
        """Test test_displayable_exec_summary with valid parameter."""
        filepath = '/home/some_path/GET-WithHeaders.chk'
        expected_summary = 'File: {}\r\n\nExecuting request\r\n\n- Making request [Success]\r\n===='.format(filepath)
        summary = Presentation.displayable_execution_summary(filepath)
        assert expected_summary == summary
