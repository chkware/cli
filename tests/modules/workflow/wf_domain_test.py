# type: ignore
"""
Domain test code
"""
from icecream import ic

from chk.modules.workflow import WorkflowDocument, WorkflowDocumentSupport
from chk.modules.workflow.entities import ChkwareTask

from tests import load_chk_file, load_file_ctx_for_file, SPEC_DIR


class TestWorkflowDocument:
    @staticmethod
    def test_from_file_context_pass(load_chk_file, load_file_ctx_for_file):
        filepath = f"{SPEC_DIR}workflow/simple-btc-wf.chk"
        file_ctx = load_file_ctx_for_file(filepath)

        wfdoc = WorkflowDocument.from_file_context(file_ctx)
        assert wfdoc.id == "simpleBtcWf"

        assert isinstance(wfdoc.tasks, list)
        assert all(isinstance(i, ChkwareTask) for i in wfdoc.tasks)

    @staticmethod
    def test_from_file_context_pass_noid(load_chk_file, load_file_ctx_for_file):
        filepath = f"{SPEC_DIR}workflow/simple-btc-wf.chk"
        file_ctx = load_file_ctx_for_file(filepath)

        del file_ctx.document["id"]  # remove document id

        wfdoc = WorkflowDocument.from_file_context(file_ctx)
        assert wfdoc.id == "simple-btc-wf"  # check if document id defaults to file name

        assert isinstance(wfdoc.tasks, list)
        assert all(isinstance(i, ChkwareTask) for i in wfdoc.tasks)


class TestWorkflowDocumentSupport:
    @staticmethod
    def test_process_task_template_pass(load_chk_file, load_file_ctx_for_file):
        filepath = f"{SPEC_DIR}workflow/simple-btc-wf.chk"
        file_ctx = load_file_ctx_for_file(filepath)

        wfdoc = WorkflowDocument.from_file_context(file_ctx)

        WorkflowDocumentSupport.process_task_template(wfdoc, ...)
