# type: ignore
"""
Workflow module test
"""

from chk.modules.workflow import execute

from tests import load_chk_file, load_file_ctx_for_file, get_exec_ctx, SPEC_DIR


class TestWorkflowExecute:
    @staticmethod
    def test_execute(load_chk_file, load_file_ctx_for_file, get_exec_ctx):
        filepath = f"{SPEC_DIR}workflow/simple-btc-wf.chk"
        file_ctx = load_file_ctx_for_file(filepath)
        execution_ctx = get_exec_ctx(False)

        execute(file_ctx, execution_ctx)
