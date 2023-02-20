# type: ignore
"""
Test for variables_environment/support.py
"""
from chk.modules.variables_environment.support import get_os_env_vars
from var_dump import var_dump


class TestSupport:
    def test_get_os_env_vars_pass(self):
        assert isinstance(get_os_env_vars(), dict)
