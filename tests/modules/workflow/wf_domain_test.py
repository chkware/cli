# type: ignore
"""
Domain test code
"""
from pydantic import BaseModel, Field

from chk.infrastructure.symbol_table import Variables
from chk.modules.workflow import WorkflowDocument, WorkflowDocumentSupport
from chk.modules.workflow.entities import ChkwareTask, WorkflowUses
from tests import SPEC_DIR, load_chk_file, load_file_ctx_for_file


class TestWorkflowDocument:
    @staticmethod
    def test_from_file_context_pass(load_chk_file, load_file_ctx_for_file):

        class TaskDict(BaseModel):
            file: str = Field(default=str)
            name: str = Field(default=str)
            uses: WorkflowUses

        filepath = f"{SPEC_DIR}workflow/simple-btc-wf.chk"
        file_ctx = load_file_ctx_for_file(filepath)

        wfdoc = WorkflowDocument.from_file_context(file_ctx)
        assert wfdoc.id == "simple-btc-workflow-1"

        assert isinstance(wfdoc.tasks, list)
        assert all(TaskDict(**i) for i in wfdoc.tasks)

    @staticmethod
    def test_from_file_context_pass_noid(load_chk_file, load_file_ctx_for_file):

        class TaskDict(BaseModel):
            file: str = Field(default=str)
            name: str = Field(default=str)
            uses: WorkflowUses

        filepath = f"{SPEC_DIR}workflow/simple-btc-wf.chk"
        file_ctx = load_file_ctx_for_file(filepath)

        del file_ctx.document["id"]  # remove document id
        wfdoc = WorkflowDocument.from_file_context(file_ctx)

        # check if document id defaults to file name
        assert wfdoc.id == "simple-btc-workflow"

        assert isinstance(wfdoc.tasks, list)
        assert all(TaskDict(**i) for i in wfdoc.tasks)


class TestWorkflowDocumentSupport:
    @staticmethod
    def test_process_task_template_pass(load_chk_file, load_file_ctx_for_file):
        # filepath = f"{SPEC_DIR}workflow/simple-btc-wf.chk"
        filepath = f"{SPEC_DIR}workflow_cases/simple/coinstats-usd-workflow.chk"
        file_ctx = load_file_ctx_for_file(filepath)

        wfdoc = WorkflowDocument.from_file_context(file_ctx)

        rpt = WorkflowDocumentSupport.process_task_template(wfdoc, Variables({"_steps": []}))
        assert isinstance(rpt, list)
