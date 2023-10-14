"""
Workflow module
"""

from collections import abc

from icecream import ic

from chk.infrastructure.file_loader import FileContext, ExecuteContext
from chk.infrastructure.symbol_table import Variables, VariableTableManager
from chk.modules.workflow.domain import WorkflowDocument, WorkflowDocumentSupport

VERSION_SCOPE = ["workflow"]


def execute(
    ctx: FileContext, exec_ctx: ExecuteContext, cb: abc.Callable = lambda *args: ...
) -> None:
    """Run a workflow document

    Args:
        ctx: FileContext object to handle
        exec_ctx: ExecuteContext
        cb: Callable
    """

    wflow_doc = WorkflowDocument.from_file_context(ctx)
    ic(wflow_doc)

    variable_doc = Variables()
    VariableTableManager.handle(variable_doc, wflow_doc, exec_ctx)

    service = WorkflowDocumentSupport()
    service.process_task_template(wflow_doc, variable_doc)

    # DocumentVersionMaker.verify_if_allowed(
    #     DocumentVersionMaker.from_dict(wflow_doc.as_dict), VERSION_SCOPE
    # )

    # VersionedDocumentSupport.validate_with_schema(
    #     HttpDocumentSupport.build_schema(), http_doc
    # )
