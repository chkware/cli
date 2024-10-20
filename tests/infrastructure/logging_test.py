"""
Logging Module Test
"""

from chk.infrastructure.logging import LoggingManager


class TestGetLogFile:
    """TestGetLogFile"""

    @staticmethod
    def test_get_log_file():
        """test_get_log_file"""

        LoggingManager.get_log_file()
