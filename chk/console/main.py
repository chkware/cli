"""Commands"""
import click
import dotmap
from chk.infrastructure.file_loader import ChkFileLoader
from chk.modules.http.entities import HttpV072
from chk.modules.http.presentation import ResponseToStringFormatter
from chk.support.http_requestor import make_request
from chk.console.app_container import app


# run command
@click.command()
@click.argument('file')
def run(file):
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
        raise SystemExit(app.messages.exception.fatal.V0002)


# root command
@click.group()
def chk(): pass


chk.add_command(run)
