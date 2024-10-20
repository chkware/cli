"""
Logging Module Test
"""

from chk.infrastructure.logging import LoggingManager, create_session_id


class TestGetLogFile:
    """TestGetLogFile"""

    @staticmethod
    def create_cache_dir():
        """test_get_log_file"""

        p = LoggingManager.create_cache_dir()

        assert p.exists() and p.is_dir()

    @staticmethod
    def create_create_log_dir():
        """test_get_log_file"""

        p = LoggingManager.create_cache_dir()
        q = LoggingManager.create_log_dir(p)

        assert q.exists() and q.is_dir()


def test_create_session_id():
    new_session = create_session_id()

    assert isinstance(new_session, str)
