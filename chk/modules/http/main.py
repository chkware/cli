"""
Main driver
"""
from typing import Any
from json import dumps

import click

from chk.infrastructure.contexts import app
from chk.infrastructure.document import CallingContextData
from chk.infrastructure.version import DocumentVersionMaker
from chk.infrastructure.work import handle_worker
from chk.infrastructure.file_loader import FileContext
from chk.modules.http.document import HttpDocument

from chk.modules.http.entities import HttpSpec
from chk.modules.http.presentation import present_result
from chk.modules.http.validation import HttpDocumentValidation


def execute(ctx: CallingContextData) -> Any:
    """Execute command functionality"""

    # validate document
    # @TODO update validation with json schema validation
    HttpDocumentValidation.validate_or_fail(ctx.document)

    # create version from document
    doc_ver = DocumentVersionMaker.from_dict(ctx.document)

    # exit()

    # create expose from document
    # create variables from document
    # set to parent constructor
    HttpDocument(request=)

    # create request
    # create response

    # http_spec = HttpSpec(file_ctx)
    # try:
    #     response = handle_worker(http_spec)
    #     if app.config(file_ctx.filepath_hash, "dump"):
    #         output_formatter = (
    #             present_result
    #             if app.config(file_ctx.filepath_hash, "format")
    #             else dumps
    #         )
    #         app.print_fmt(response, output_formatter)  # type: ignore
    #
    #     return response
    # except RuntimeError as err:
    #     return (
    #         click.echo(f"\r\n---\r\n{str(err)}")
    #         if app.config(file_ctx.filepath_hash, "dump")
    #         else err
    #     )
