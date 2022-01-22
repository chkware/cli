"""
run command
"""
import click
from yaml import safe_load
from chk.support.http_requestor import make_request
from chk.support.output_cli import ResponseToStringFormatter
from dotmap import DotMap


@click.command()
@click.argument('file')
def execute(file):
    """execute command"""
    doc = read_chk(file)
    response = make_request(doc.request)
    fmt_str = ResponseToStringFormatter(response).get()

    # print data
    print(fmt_str)


def read_chk(file_name: str) -> DotMap:
    """read yml data"""
    with open(file_name, 'r') as yf:
        try:
            chk_yaml = safe_load(yf)
        except:
            raise SystemExit(f'`{file_name}` is not a valid YAML.')

        return DotMap(chk_yaml)
