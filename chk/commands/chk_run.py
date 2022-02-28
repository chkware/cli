"""
run command
"""
import click
import dotmap
from chk.support.http_requestor import make_request
from chk.support.output_cli import ResponseToStringFormatter
from chk.support.loader import ChkFileLoader
from chk.archetypes.defaults.http_config import HttpV072


@click.command()
@click.argument('file')
def execute(file):
    """execute command"""
    if ChkFileLoader.is_file_ok(file):
        # load as dict
        doc = ChkFileLoader.to_dict(file)

        doc_ver = HttpV072()
        doc_ver.validate_config(doc)
        del doc_ver

        doc = dotmap.DotMap(doc)

        response = make_request(doc.request)
        fmt_str = ResponseToStringFormatter(response).get()

        print(fmt_str)  # print data
    else:
        from chk.globals import current_app
        raise SystemExit(current_app().config.error.fatal.V0002)
