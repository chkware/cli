import click
from yaml import safe_load
from support.http_requestor import make_request
from dotmap import DotMap


@click.command()
@click.argument('file')
def execute(file):
    """execute command"""
    doc = read_chk(file)
    response = make_request(doc.request)

    # process data
    print(response.url)
    print(response.headers.get('content-type'))
    print(response.json())


def read_chk(file_name: str) -> DotMap:
    """read yml data"""
    with open(file_name, 'r') as yf:
        return DotMap(safe_load(yf))
