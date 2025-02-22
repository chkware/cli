# type: ignore
"""
Workflow module test
"""

from chk.infrastructure.symbol_table import ExecResponse
from chk.modules.workflow import call, execute
from tests import SPEC_DIR


class TestWorkflowExecute:
    @staticmethod
    def test_execute_pass_vars(
        load_chk_file, load_file_ctx_for_file, get_exec_ctx, capsys
    ):
        """test_execute"""

        filepath = f"{SPEC_DIR}workflow_cases/get-req-vars/coinstats-usd-workflow.chk"
        file_ctx = load_file_ctx_for_file(filepath)
        execution_ctx = get_exec_ctx(True)

        execute(file_ctx, execution_ctx)

        captured = capsys.readouterr()
        assert "------" in captured.out

    @staticmethod
    def test_execute_pass_args(
        load_chk_file, load_file_ctx_for_file, get_exec_ctx, capsys
    ):
        """test_execute"""

        filepath = f"{SPEC_DIR}workflow_cases/pass_data/coinstats-usd-workflow.chk"
        file_ctx = load_file_ctx_for_file(filepath)
        execution_ctx = get_exec_ctx(True)

        execute(file_ctx, execution_ctx)

        captured = capsys.readouterr()
        assert "======" in captured.out

class TestWorkflowCall:
    """TestWorkflowCall"""

    @staticmethod
    def test_pass(load_chk_file, load_file_ctx_for_file, get_exec_ctx):
        """test_call"""

        filepath = f"{SPEC_DIR}workflow_cases/get-req-vars/coinstats-usd-workflow.chk"
        file_ctx = load_file_ctx_for_file(filepath)
        execution_ctx = get_exec_ctx(True)

        er = call(file_ctx, execution_ctx)
        assert isinstance(er, ExecResponse)
