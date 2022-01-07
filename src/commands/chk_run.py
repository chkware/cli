import click
from yaml import safe_load
from requests import request
from dotmap import DotMap


@click.command()
@click.argument('file')
def execute(file):
    """execute command"""
    doc = read_chk(file)
    response = make_request(doc.request)

    # process data
    print(response.text)


def read_chk(file_name: str) -> DotMap:
    """read yml data"""
    with open(file_name, 'r') as yf:
        return DotMap(safe_load(yf))


def make_request(request_data: DotMap):
    """Make external api call"""
    response = request(
        request_data.method,
        request_data.path,
    )

    return response
